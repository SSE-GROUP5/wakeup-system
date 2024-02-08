import matplotlib.pyplot as plt
import torch
import cv2
import math
from torchvision import transforms
import numpy as np
import os
import sys
from datetime import datetime
import argparse

from tqdm import tqdm

from utils.datasets import letterbox
from utils.general import non_max_suppression_kpt
from utils.plots import output_to_keypoint, plot_skeleton_kpts

output_folder = "output_videos"


def fall_detection(poses):
    for pose in poses:
        xmin, ymin = (pose[2] - pose[4] / 2), (pose[3] - pose[5] / 2)
        xmax, ymax = (pose[2] + pose[4] / 2), (pose[3] + pose[5] / 2)
        left_shoulder_y = pose[23]
        left_shoulder_x = pose[22]
        right_shoulder_y = pose[26]
        left_body_y = pose[41]
        left_body_x = pose[40]
        right_body_y = pose[44]
        len_factor = math.sqrt(((left_shoulder_y - left_body_y) ** 2 + (left_shoulder_x - left_body_x) ** 2))
        left_foot_y = pose[53]
        right_foot_y = pose[56]
        dx = int(xmax) - int(xmin)
        dy = int(ymax) - int(ymin)
        difference = dy - dx
        if left_shoulder_y > left_foot_y - len_factor and left_body_y > left_foot_y - (
                len_factor / 2) and left_shoulder_y > left_body_y - (len_factor / 2) or (
                right_shoulder_y > right_foot_y - len_factor and right_body_y > right_foot_y - (
                len_factor / 2) and right_shoulder_y > right_body_y - (len_factor / 2)) \
                or difference < 0:
            return True, (xmin, ymin, xmax, ymax)
    return False, None


def falling_alarm(image, bbox):
    x_min, y_min, x_max, y_max = bbox
    cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), color=(0, 0, 255),
                  thickness=5, lineType=cv2.LINE_AA)
    cv2.putText(image, 'Person Fell down', (11, 100), 0, 1, [0, 0, 2550], thickness=3, lineType=cv2.LINE_AA)


def get_pose_model():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("device: ", device)
    weigths = torch.load('yolov7-w6-pose.pt', map_location=device)
    model = weigths['model']
    _ = model.float().eval()
    if torch.cuda.is_available():
        model = model.half().to(device)
    return model, device


def get_pose(image, model, device):
    image = letterbox(image, 960, stride=64, auto=True)[0]
    image = transforms.ToTensor()(image)
    image = torch.tensor(np.array([image.numpy()]))
    if torch.cuda.is_available():
        image = image.half().to(device)
    with torch.no_grad():
        output, _ = model(image)
    output = non_max_suppression_kpt(output, 0.25, 0.65, nc=model.yaml['nc'], nkpt=model.yaml['nkpt'],
                                     kpt_label=True)
    with torch.no_grad():
        output = output_to_keypoint(output)
    return image, output


def prepare_image(image):
    _image = image[0].permute(1, 2, 0) * 255
    _image = _image.cpu().numpy().astype(np.uint8)
    _image = cv2.cvtColor(_image, cv2.COLOR_RGB2BGR)
    return _image


def prepare_vid_out(video_path, vid_cap):
    vid_write_image = letterbox(vid_cap.read()[1], 960, stride=64, auto=True)[0]
    resize_height, resize_width = vid_write_image.shape[:2]
    # out_video_name = f"{video_path.split('/')[-1].split('.')[0]}_keypoint.mp4"
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    output_video_path = os.path.join(output_folder, f"output_video_file{current_time}.mp4")
    
    # Define the video writer
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (resize_width, resize_height))

    # out = cv2.VideoWriter(out_video_name, cv2.VideoWriter_fourcc(*'mp4v'), 30, (resize_width, resize_height))
    return out

def process_frame(frame, model, device, vid_writer):
    image, output = get_pose(frame, model, device)
    _image = prepare_image(image)
    is_fall, bbox = fall_detection(output)
    if is_fall:
        falling_alarm(_image, bbox)
        
    # Write the processed frame to the video writer
    vid_writer.write(_image)
        
    return _image

def process_live_video():
    model, device = get_pose_model()

    # Open webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Couldn't open webcam.")
        return

    # Get the width and height of the webcam feed
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define the current date and time
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Define the output video path with a unique identifier
    output_video_path = os.path.join(output_folder, f"output_video_live{current_time}.mp4")
    
    # Define the video writer
    vid_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't capture frame.")
            break
        
        # Process frame for pose estimation and fall detection
        processed_frame = process_frame(frame, model, device, vid_writer)
        
        # Display the processed frame
        cv2.imshow('Processed Frame', processed_frame)

        # Check for key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video writer, webcam, and close OpenCV windows
    vid_writer.release()
    cap.release()
    cv2.destroyAllWindows()

def process_video_file(video_path):
    vid_cap = cv2.VideoCapture(video_path)

    if not vid_cap.isOpened():
        print('Error while trying to read video. Please check path again')
        return

    model, device = get_pose_model()
    vid_out = prepare_vid_out(video_path, vid_cap)

    success, frame = vid_cap.read()
    _frames = []
    while success:
        _frames.append(frame)
        success, frame = vid_cap.read()

    for image in tqdm(_frames):
        image, output = get_pose(image, model, device)
        _image = prepare_image(image)
        is_fall, bbox = fall_detection(output)
        if is_fall:
            falling_alarm(_image, bbox)
        vid_out.write(_image)



    vid_out.release()
    vid_cap.release()

if __name__ == "__main__":
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Process live video or video file for fall detection.')
    parser.add_argument('--mode', choices=['live', 'file'], default='live', help='Mode of operation: live or file')
    parser.add_argument('--video', default=None, help='Path to the video file (required in file mode)')
    args = parser.parse_args()

    # Check mode and execute the corresponding function
    if args.mode == 'live':
        process_live_video()
    elif args.mode == 'file':
        if args.video is None:
            parser.error("Video file path is required in file mode.")
        process_video_file(args.video)