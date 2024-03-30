#!/bin/bash
set -e
DIRECTORY=$(dirname $0)


# Check if it is python3.10 
if [[ $(python3 --version) != *"3.10"* ]]; then
  echo "Please create a virtual environment first with python3.10"
  echo "Eg. python3.10 -m venv venv"
  echo "Then activate the virtual environment"
  exit 1
fi

pip3 install zmq requests python-dotenv ultralytics simpleaudio

# check if windows 
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi

ADD_DATA=""
if [ "$IS_WINDOWS" = true ]; then
  ADD_DATA="--add-data $DIRECTORY/venv/Lib/site-packages/ultralytics:ultralytics"
else
  ADD_DATA="--add-data $DIRECTORY/venv/lib/python3.10/site-packages/ultralytics:ultralytics"
fi


pyinstaller \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --add-data "$DIRECTORY/../beepy:beepy" \
    $ADD_DATA \
  --hidden-import=ultralytics \
  --hidden-import=simpleaudio \
  --hidden-import=zmq \
  --onefile "$DIRECTORY/fall_upper_detection.py"

mkdir -p vision_upper_body_fall
cp dist/fall_upper_detection vision_upper_body_fall

# check if the yolo model is already downloaded
# if not
if [ ! -f yolov8m-pose.pt ]; then
  wget https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8m-pose.pt 
fi 

mv yolov8m-pose.pt vision_upper_body_fall
