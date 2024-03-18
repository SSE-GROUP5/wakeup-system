#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

pip3 install zmq requests python-dotenv mediapipe

# check if windows 
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi

ADD_DATA_MEDIAPIPE=""
if [ "$IS_WINDOWS" = true ]; then
  ADD_DATA_MEDIAPIPE="--add-data $DIRECTORY/../venv/Lib/site-packages/mediapipe:mediapipe"
else
  ADD_DATA_MEDIAPIPE="--add-data $DIRECTORY/../venv/lib/python3.10/site-packages/mediapipe:mediapipe \
  --add-data $DIRECTORY/../venv/lib/python3.10/site-packages/mediapipe/modules/face_landmark:mediapipe/modules/face_landmark"
fi

pyinstaller \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --hidden-import=zmq \
   $ADD_DATA_MEDIAPIPE \
  --onefile "$DIRECTORY/blink_detect.py"          