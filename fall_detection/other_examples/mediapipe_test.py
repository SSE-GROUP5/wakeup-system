# https://medium.com/@oetalmage16/a-tutorial-on-finger-counting-in-real-time-video-in-python-with-opencv-and-mediapipe-114a988df46a

from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import cv2
import mediapipe as mp
import time
import math

NOSE = 0
LEFT_EYE = 2
RIGHT_EYE = 5
LEFT_EAR = 7
RIGHT_EAR = 8
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_MOUTH = 9
RIGHT_MOUTH = 10

TEXT_COLOR = (0, 0, 0)

def get_angle_between_points(p1, p2):
    if p1 is None or p2 is None:
        return None
    if p1[0] == p2[0] and p1[1] == p2[1]:
        return 0
    if p1[0] == p2[0]:
        return 90
    if p1[1] == p2[1]:
        return 0
      
    x1, y1, _ = p1
    x2, y2, _ = p2
    return 180 - abs(math.atan2(y2-y1, x2-x1) * 180 / math.pi)
  


def draw_landmarks_on_image(rgb_image, detection_result: mp.tasks.vision.PoseLandmarkerResult):
    try:
      if detection_result.pose_landmarks == []:
          return rgb_image, []
        
      pose_landmarks_list = detection_result.pose_landmarks
      annotated_image = np.copy(rgb_image)
      xyz = []
      for idx in range(len(pose_landmarks_list)):
          pose_landmarks = pose_landmarks_list[idx]
          # Draw the pose landmarks.
          pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
          pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
          ])
          solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())
          xyz = [[landmark.x, landmark.y, landmark.z] for landmark in pose_landmarks]
      
      return annotated_image, xyz
      
    except:
      return rgb_image, []
  

model_path = "pose_landmarker_heavy.task"
BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


class landmarker_and_result():
   def __init__(self):
      self.result =  mp.tasks.vision.PoseLandmarkerResult
      self.landmarker =  mp.tasks.vision.PoseLandmarker
      self.createLandmarker()
   
   def createLandmarker(self):
      def update_result(result: mp.tasks.vision.PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
         self.result = result

      options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=update_result
      )
      
      self.landmarker = self.landmarker.create_from_options(options)
   
   def detect_async(self, frame):
      mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
      self.landmarker.detect_async(image = mp_image, timestamp_ms = int(time.time() * 1000))

   def close(self):
      # close landmarker
      self.landmarker.close()
      
      
      
# Open the video file
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()


pose_landmarker = landmarker_and_result()

while cap.isOpened():
    success, frame = cap.read()

    if success:
        pose_landmarker.detect_async(frame)
        frame, xyz = draw_landmarks_on_image(frame, pose_landmarker.result)
        if len(xyz) > 0:
          
          eyes_angle = get_angle_between_points(xyz[LEFT_EYE], xyz[RIGHT_EYE])
          ears_angle = get_angle_between_points(xyz[LEFT_EAR], xyz[RIGHT_EAR])
          shoulders_angle = get_angle_between_points(xyz[LEFT_SHOULDER], xyz[RIGHT_SHOULDER])
          mouth_angle = get_angle_between_points(xyz[LEFT_MOUTH], xyz[RIGHT_MOUTH])
          print('left_eye: ', xyz[LEFT_EYE])
          cv2.putText(frame, "eyes_angle: " + str(eyes_angle), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2, cv2.LINE_AA)
          cv2.putText(frame, "ears_angle: " + str(ears_angle), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2, cv2.LINE_AA)
          cv2.putText(frame, "shoulders_angle: " + str(shoulders_angle), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2, cv2.LINE_AA)
          cv2.putText(frame, "mouth_angle: " + str(mouth_angle), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, TEXT_COLOR, 2, cv2.LINE_AA)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
pose_landmarker.close()
cv2.destroyAllWindows()