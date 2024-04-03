#!/bin/bash
set -e
DIRECTORY=$(dirname $0)


# check if windows 
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi




pyinstaller \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --add-data "$DIRECTORY/../beepy:beepy" \
  --add-data "$DIRECTORY/static:static" \
  --hidden-import=zmq \
    $ADD_DATA \
  --onefile "$DIRECTORY/run.py"

mv dist/run $DIRECTORY/wakeup_server