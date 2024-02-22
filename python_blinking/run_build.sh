#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

pyinstaller \
  --add-data "$DIRECTORY/config.json:." \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --add-data "$DIRECTORY/../venv/lib/python3.9/site-packages/zmq:zmq" \
  --add-data "$DIRECTORY/../venv/lib/python3.9/site-packages/mediapipe:mediapipe" \
  --onefile "$DIRECTORY/blink_detect.py"          