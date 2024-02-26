#!/bin/bash
set -e
DIRECTORY=$(dirname $0)


# Check if the venv exists
if [ ! -d "$DIRECTORY/../venv/lib/python3.10" ]; then
  echo "Please create a virtual environment with folder name venv and with python3.10"
  echo "Eg. python3.10 -m venv ../venv"
  exit 1
fi

pip3 install zmq
pip3 install ultralytics
pip3 install simpleaudio

pyinstaller \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --add-data "$DIRECTORY/../beepy:beepy" \
  --hidden-import=simpleaudio \
  --add-data "$DIRECTORY/../venv/lib/python3.10/site-packages/zmq:zmq" \
  --add-data "$DIRECTORY/../venv/lib/python3.10/site-packages/ultralytics:ultralytics" \
  --onefile "$DIRECTORY/yolov8_fall_upper_detection.py"
