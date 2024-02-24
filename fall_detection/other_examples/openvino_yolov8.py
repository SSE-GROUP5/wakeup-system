# https://github.com/openvinotoolkit/openvino_notebooks/blob/main/notebooks/230-yolov8-optimization/230-yolov8-keypoint-detection.ipynb

import cv2
from ultralytics import YOLO
import math
import os
import openvino as ov
import numpy as np
from typing import Tuple
from ultralytics.utils import ops
import torch

# Load the YOLOv8 model
POSE_MODEL_NAME='yolov8m-pose'
models_dir = 'models'
os.makedirs(models_dir, exist_ok=True)
pose_model_path = f"{models_dir}/{POSE_MODEL_NAME}.pt"
pose_model = YOLO(pose_model_path)

# https://docs.ultralytics.com/integrations/openvino/
# model.export(format='openvino')

core = ov.Core()
device = 'CPU'
pose_model_path = f"{models_dir}/{POSE_MODEL_NAME}_openvino_model/{POSE_MODEL_NAME}.xml"
if not os.path.exists(pose_model_path):
    pose_model.export(format="openvino", dynamic=True, half=False)
    
pose_ov_model = core.read_model(pose_model_path)
pose_compiled_model = core.compile_model(pose_ov_model, device)

NOSE = 0
LEFT_EYE = 1
RIGHT_EYE = 2
LEFT_EAR = 3
RIGHT_EAR = 4
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6

def postprocess(
    pred_boxes:np.ndarray, 
    input_hw:Tuple[int, int], 
    orig_img:np.ndarray, 
    min_conf_threshold:float = 0.25, 
    nms_iou_threshold:float = 0.45, 
    agnosting_nms:bool = False, 
    max_detections:int = 80,
):
    """
    YOLOv8 model postprocessing function. Applied non maximum supression algorithm to detections and rescale boxes to original image size
    Parameters:
        pred_boxes (np.ndarray): model output prediction boxes
        input_hw (np.ndarray): preprocessed image
        orig_image (np.ndarray): image before preprocessing
        min_conf_threshold (float, *optional*, 0.25): minimal accepted confidence for object filtering
        nms_iou_threshold (float, *optional*, 0.45): minimal overlap score for removing objects duplicates in NMS
        agnostic_nms (bool, *optiona*, False): apply class agnostinc NMS approach or not
        max_detections (int, *optional*, 300):  maximum detections after NMS
    Returns:
       pred (List[Dict[str, np.ndarray]]): list of dictionary with det - detected boxes in format [x1, y1, x2, y2, score, label] and 
                                           kpt - 17 keypoints in format [x1, y1, score1]
    """
    nms_kwargs = {"agnostic": agnosting_nms, "max_det":max_detections}
    preds = ops.non_max_suppression(
        torch.from_numpy(pred_boxes),
        min_conf_threshold,
        nms_iou_threshold,
        nc=1,
        **nms_kwargs
    )

    results = []

    kpt_shape = [17, 3]
    for i, pred in enumerate(preds):
        shape = orig_img[i].shape if isinstance(orig_img, list) else orig_img.shape
        pred[:, :4] = ops.scale_boxes(input_hw, pred[:, :4], shape).round()
        pred_kpts = pred[:, 6:].view(len(pred), *kpt_shape) if len(pred) else pred[:, 6:]
        pred_kpts = ops.scale_coords(input_hw, pred_kpts, shape)
        results.append({"box": pred[:, :6].numpy(), 'kpt': pred_kpts.numpy()})
    
    return results

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

def image_to_tensor(image:np.ndarray):
    """
    Preprocess image according to YOLOv8 input requirements. 
    Takes image in np.array format, resizes it to specific size using letterbox resize and changes data layout from HWC to CHW.
    
    Parameters:
      img (np.ndarray): image for preprocessing
    Returns:
      input_tensor (np.ndarray): input tensor in NCHW format with float32 values in [0, 1] range 
    """
    input_tensor = image.astype(np.float32)  # uint8 to fp32
    input_tensor /= 255.0  # 0 - 255 to 0.0 - 1.0
    
    # add batch dimension
    if input_tensor.ndim == 3:
        input_tensor = np.expand_dims(input_tensor, 0)
    return input_tensor

def preprocess_image(img0: np.ndarray):
    """
    Preprocess image according to YOLOv8 input requirements. 
    Takes image in np.array format, resizes it to specific size using letterbox resize and changes data layout from HWC to CHW.
    
    Parameters:
      img0 (np.ndarray): image for preprocessing
    Returns:
      img (np.ndarray): image after preprocessing
    """
    # resize
    img = cv2.resize(img0, (640, 640), interpolation=cv2.INTER_LINEAR)
    
    # Convert HWC to CHW
    img = img.transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    return img
     
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        frame_numpy = preprocess_image(frame)
        frame_tensor = image_to_tensor(frame_numpy)
        results = pose_compiled_model(frame_tensor)
        boxes = results[pose_compiled_model.output(0)]
        input_hw = frame_tensor.shape[2:]
        detections = postprocess(pred_boxes=boxes, input_hw=input_hw, orig_img=frame)
        detections = detections[0]

        # Visualize the results on the frame
        annotated_frame = frame.copy()

        keypoints_persons = detections['kpt']      
        shape = frame.shape[:2]  
        points = []
        for i, keypoint_person in enumerate(keypoints_persons):
            for i, k in enumerate(keypoint_person):
                if i > RIGHT_SHOULDER:
                    break
                x_coord, y_coord, score = int(k[0]), int(k[1]), k[2]
                if x_coord % shape[1] != 0 and y_coord % shape[0] != 0:
                    if score < 0.5:
                        points.append([None, None])
                    points.append([x_coord, y_coord])
                    cv2.circle(annotated_frame, (x_coord, y_coord), 5, (0, 255, 0), -1)
  
        if len(points) >= RIGHT_SHOULDER:
            left_ear = points[LEFT_EAR]
            right_ear = points[RIGHT_EAR]
            left_eye = points[LEFT_EYE]
            right_eye = points[RIGHT_EYE]
            left_shoulder = points[LEFT_SHOULDER]
            right_shoulder = points[RIGHT_SHOULDER]
            
            if left_ear[0] is not None and right_ear[0] is not None:
                angles_between_ears = get_angle_between_points(left_ear, right_ear) 
                cv2.putText(annotated_frame, str(angles_between_ears), left_ear, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
            # # add angle text to frame
            if left_eye[0] is not None and right_eye[0] is not None:
              angle_between_eyes = get_angle_between_points(left_eye, right_eye)
              cv2.putText(annotated_frame, str(angle_between_eyes), left_eye, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
          
            if left_shoulder[0] is not None and right_shoulder[0] is not None:
                angles_between_shoulders = get_angle_between_points(left_shoulder, right_shoulder)
                cv2.putText(annotated_frame, str(angles_between_shoulders), left_shoulder, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
        # # Display the annotated frame
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