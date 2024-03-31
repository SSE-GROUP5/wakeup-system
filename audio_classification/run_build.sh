#!/bin/bash
set -e
DIRECTORY=$(dirname $0)


# Check if it is python3.10 
if [[ $(python3 --version) != *"3.10"* ]]; then
  echo "Please create a virtual environment first with python3.10"
  echo "Eg. python3.10 -m venv ../sound_venv"
  echo "Then activate the virtual environment"
  exit 1
fi

pip3 install zmq requests python-dotenv  

# check if windows 
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi


pyinstaller \
  --add-data "$DIRECTORY/yamnet.tflite:." \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --hidden-import=zmq \
  --onefile "$DIRECTORY/audio_classification.py"   

mkdir -p sound_classification
cp dist/audio_classification sound_classification