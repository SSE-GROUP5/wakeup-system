import time

start_time = time.process_time()

import cv2
import time
from ultralytics import YOLO
import requests
from configuration import MODEL_VERBOSE, LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_EAR, RIGHT_EAR, LEFT_EYE, RIGHT_EYE, CONNECTION_CHECK_INTERVAL
from configuration import config
from utils import send_signal, get_angle_between_points, check_connection, update_env_vars, confirm_to_server
import os 
import sys
import torch
from benchmark_body import Benchmark_body




current_dir = os.path.dirname(os.path.realpath(__file__))
def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

custom_modules_path = "./" if is_exe_file() else current_dir + "/../"  
sys.path.append(custom_modules_path)
from zeromq.zmqServer import ZeroMQServer

zmqServer = ZeroMQServer(config["ZMQ_SERVER"])
# Load the YOLOv8 model and send it to the CPU
device = torch.device('cpu')
model = YOLO('yolov8m-pose.pt', verbose=MODEL_VERBOSE).to(device)
benchmark_data_dict = Benchmark_body()

# Export the model
model.export(format='openvino')  # creates 'yolov8n_openvino_model/'

# Load the exported OpenVINO model
model = YOLO('yolov8m-pose_openvino_model/')


# Open the video file
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()



client = requests.session()
is_connected = False
last_connection_time = 0
confirm_to_server(client, config)
    
start_time = time.process_time()


boot_time = time.process_time() - start_time
print(f"Boot time: {boot_time}")

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
        benchmark_data_dict.append_time(results[0].speed['preprocess'], results[0].speed['inference'], results[0].speed['postprocess'])
        
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
                continue                
            left_should = points[LEFT_SHOULDER]
            right_shoulder = points[RIGHT_SHOULDER]
            left_ear = points[LEFT_EAR]
            right_ear = points[RIGHT_EAR]
            left_eye = points[LEFT_EYE]
            right_eye = points[RIGHT_EYE]
            angle_between_eyes = get_angle_between_points(left_eye, right_eye)
            angles_between_ears = get_angle_between_points(left_ear, right_ear)
            angles_between_shoulders = get_angle_between_points(left_should, right_shoulder)
            
            # add angle text to frame
            cv2.putText(annotated_frame, str(angle_between_eyes), left_eye, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(annotated_frame, str(angles_between_ears), left_ear, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(annotated_frame, str(angles_between_shoulders), left_should, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            is_falling_eyes = int(config["MAX_ANGLE_BETWEEN_EYES"]) < angle_between_eyes
            is_falling_ears = int(config["MAX_ANGLE_BETWEEN_EARS"]) < angles_between_ears
            is_falling_shoulders = int(config["MAX_ANGLE_BETWEEN_SHOULDERS"]) < angles_between_shoulders
            falling_counter = is_falling_eyes + is_falling_ears + is_falling_shoulders
            
            if falling_counter >= 2:
                print('fall detected')
                send_signal(client, config, frame)
                
        # Display the annotated frame
        cv2.imshow("Upper body fall Detection Trigger", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q") or time.process_time() - start_time > 180:
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()


print(f"Average time for preprocessed data: {benchmark_data_dict.get_average_time()[0]} with standard deviation: {benchmark_data_dict.get_std_deviation()[0]}")
print(f"Average time for inference data: {benchmark_data_dict.get_average_time()[1]} with standard deviation: {benchmark_data_dict.get_std_deviation()[1]}")
print(f"Average time for postprocessed data: {benchmark_data_dict.get_average_time()[2]} with standard deviation: {benchmark_data_dict.get_std_deviation()[2]}")
