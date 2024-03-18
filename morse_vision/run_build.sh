#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

# check if windows 
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi

ADD_DATA=""
if [ "$IS_WINDOWS" = true ]; then
  ADD_DATA="--add-data $DIRECTORY/venv/Lib/site-packages/mediapipe:mediapipe"
else
  ADD_DATA="--add-data $DIRECTORY/venv/lib/python3.10/site-packages/mediapipe:mediapipe"
fi

pip3 install zmq requests python-dotenv ultralytics simpleaudio


pyinstaller \
  --hidden-import=simpleaudio \
  --hidden-import=zmq \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --add-data "$DIRECTORY/../beepy:beepy" \
  $ADD_DATA \
  --onefile "$DIRECTORY/morse_vision.py"        


mkdir -p vision_morse
cp dist/morse_vision vision_morse
