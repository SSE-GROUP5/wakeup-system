#!/bin/bash
set -e
DIRECTORY=$(dirname $0)


# Check if it is python3.10 
if [[ $(python3 --version) != *"3.10"* ]]; then
  echo "Please create a virtual environment first with python3.10"
  echo "Eg. python3.10 -m venv ../venv"
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
  ADD_DATA="--add-data $DIRECTORY/../venv/Lib/site-packages/ultralytics:ultralytics"
else
  ADD_DATA="--add-data $DIRECTORY/../venv/lib/python3.10/site-packages/ultralytics:ultralytics"
fi

pyinstaller \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --add-data "$DIRECTORY/../beepy:beepy" \
    $ADD_DATA \
  --hidden-import=simpleaudio \
  --hidden-import=zmq \
  --onefile "$DIRECTORY/yolov8_fall_upper_detection.py"
