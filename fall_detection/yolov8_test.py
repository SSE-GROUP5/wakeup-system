import cv2
from ultralytics import YOLO
import math
import torch

device = torch.device('cpu')

# Load the YOLOv8 model
model = YOLO('yolov8m-pose.pt').to(device)
NOSE = 0
LEFT_EYE = 1
RIGHT_EYE = 2
LEFT_EAR = 3
RIGHT_EAR = 4
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6



def get_angle_between_points(p1, p2):
    if p1 is None or p2 is None:
        return None
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return 0
    if p1[0] == p2[0]:
        return 90
    if p1[1] == p2[1]:
        return 0
      
    x1, y1 = p1
    x2, y2 = p2
    return 180 - abs(math.atan2(y2-y1, x2-x1) * 180 / math.pi)
  

# Open the video file
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)

        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        keypoints = results[0].keypoints.cpu().numpy()            
        for keypoint in keypoints:                               
            points = keypoint.xy[0].astype(int)                      
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
            
        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()