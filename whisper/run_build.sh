#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

pip3 install zmq requests python-dotenv  

# check if windows 
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi


pyinstaller \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --hidden-import=zmq \
  --onefile "$DIRECTORY/whisper_transcribe.py"

mkdir -p sound_whisper
cp dist/whisper_transcribe sound_whisper
