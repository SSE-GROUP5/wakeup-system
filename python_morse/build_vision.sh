#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

pyinstaller \
  --add-data "$DIRECTORY/.env.morse_vision:.env.morse_vision" \
  --hidden-import=simpleaudio \
  --hidden-import=zmq \
  --add-data "$DIRECTORY/../zeromq:zeromq" \
  --add-data "$DIRECTORY/../beepy:beepy" \
  --add-data "$DIRECTORY/../venv/lib/python3.10/site-packages/mediapipe:mediapipe" \
  --onefile "$DIRECTORY/morse_vision.py"        