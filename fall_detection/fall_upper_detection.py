import cv2
import time
from ultralytics import YOLO
import requests
from configuration import MODEL_VERBOSE, LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_EAR, RIGHT_EAR, LEFT_EYE, RIGHT_EYE, CONNECTION_CHECK_INTERVAL
from configuration import config
from utils import send_signal, get_falling_side, get_angle_between_points, check_connection, update_env_vars, confirm_to_server
import os 
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

custom_modules_path = "./" if is_exe_file() else current_dir + "/../"  
sys.path.append(custom_modules_path)
from zeromq.zmqServer import ZeroMQServer

zmqServer = ZeroMQServer(config["ZMQ_SERVER"])
# Load the YOLOv8 model
model = YOLO('yolov8m-pose.pt', verbose=MODEL_VERBOSE)


# Open the video file
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    

client = requests.session()
is_connected = False
last_connection_time = 0
confirm_to_server(client, config)
has_alerted = False
reset_start_time = None
body_detected = False

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
    
    message = zmqServer.receive()
    if message != None:
        topic, msg = message
        if topic == config["ID"]:
            config = update_env_vars(config, msg)

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame, verbose=MODEL_VERBOSE)
        
        if last_connection_time + CONNECTION_CHECK_INTERVAL < time.time():
            is_connected = check_connection(client, config)
            last_connection_time = time.time()
        
        connection_color = (0, 255, 0) if is_connected else (0, 0, 255)
        cv2.putText(frame, f"WAKEUP SERVER is {'connected' if is_connected else 'disconnected'}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, connection_color, 2, cv2.LINE_AA)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        keypoints = results[0].keypoints.cpu().numpy()
        number_of_persons_to_detect = config["NUMBER_OF_PERSONS_TO_DETECT"] if config["NUMBER_OF_PERSONS_TO_DETECT"] < len(keypoints) else len(keypoints)         
        number_of_persons_to_detect = 1 if number_of_persons_to_detect < 1 else number_of_persons_to_detect
        for keypoint in keypoints[:number_of_persons_to_detect]:                               
            points = keypoint.xy[0].astype(int)    
            if len(points) < 7:
                body_detected = False
                if not has_alerted:
                  send_signal(client, config, frame)
                  has_alerted = True
                  reset_start_time = time.time()
                  
                continue   
            body_detected = True             
            left_should = points[LEFT_SHOULDER]
            right_shoulder = points[RIGHT_SHOULDER]
            left_ear = points[LEFT_EAR]
            right_ear = points[RIGHT_EAR]
            left_eye = points[LEFT_EYE]
            right_eye = points[RIGHT_EYE]
            angle_between_eyes = get_angle_between_points(left_eye, right_eye)
            angles_between_ears = get_angle_between_points(left_ear, right_ear)
            angles_between_shoulders = get_angle_between_points(left_should, right_shoulder)
            falling_side = get_falling_side(left_should, right_shoulder)
            
            # add angle text to frame
            cv2.putText(annotated_frame, str(angle_between_eyes), left_eye, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(annotated_frame, str(angles_between_ears), left_ear, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(annotated_frame, str(angles_between_shoulders), left_should, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            is_falling_eyes = int(config["MAX_ANGLE_BETWEEN_EYES"]) < angle_between_eyes
            is_falling_ears = int(config["MAX_ANGLE_BETWEEN_EARS"]) < angles_between_ears
            is_falling_shoulders = int(config["MAX_ANGLE_BETWEEN_SHOULDERS"]) < angles_between_shoulders
            falling_counter = is_falling_eyes + is_falling_ears + is_falling_shoulders
            
            
            if has_alerted and reset_start_time + config["RESET_TIME"] < time.time():
                has_alerted = False
                reset_start_time = None
                falling_counter = 0
                print('Ready to detect fall again')
            
            
            
            if falling_counter >= 2 and not has_alerted:
                print(f'Falling detected on the {falling_side} side')
                send_signal(client, config, frame)
                has_alerted = True
                reset_start_time = time.time()
                
        # Display the annotated frame
        cv2.imshow("Upper body fall Detection Trigger", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()