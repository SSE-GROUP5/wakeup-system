# Setup the trigger

## The Project

The system receives video as input, scans each frame of the video, and then creates 17 key-points for each individual, each of which corresponds to a position of that person's body parts in that frame. This is done using the [YOLOv7-POSE](https://github.com/WongKinYiu/yolov7/tree/pose "YOLOv7-POSE") model.


## How To Use

- Clone this repository into your drive
- Download the [YOLOv7-POSE](https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7-w6-pose.pt "YOLOv7-POSE") model into `Human-Fall-Detection` directory.
- Install all the requirements with `pip install -r requirements.txt`
- Run main.py file

## Command-Line Arguments

1. `--mode`: Specifies the mode of operation, which can be either 'live' or 'file'.
   - Usage: `--mode [live/file]`
   - Default: If not specified, defaults to 'live'.

2. `--video`: Specifies the path to the video file.
   - Usage: `--video [path_to_video_file]`
   - Required in file mode (`--mode file`).

Example command usages:

- To run the main.py in live mode:
  ```
  python main.py --mode live
  ```

- To run the script in file mode and provide the path to the video file:
  ```
  python main.py --mode file --video /path/to/video/file.mp4
  ```

- If you omit the `--video` argument in file mode, an error will be raised:
  ```
  python main.py --mode file
  ```

