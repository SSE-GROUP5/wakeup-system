#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

pip3 install zmq requests python-dotenv  

# check if windows 
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi

ADD_DATA=""
if [ "$IS_WINDOWS" = true ]; then
  ADD_DATA="--add-data $DIRECTORY/../venv/Lib/site-packages/whisper:whisper"
else
  ADD_DATA="--add-data $DIRECTORY/../venv/lib/python3.10/site-packages/whisper:whisper"
fi

pyinstaller \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
    $ADD_DATA \
  --hidden-import=zmq \
  --onefile "$DIRECTORY/whisper_transcribe.py"
