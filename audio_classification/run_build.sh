#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

pyinstaller \
  --add-data "$DIRECTORY/yamnet.tflite:." \
  --onefile "$DIRECTORY/classify.py"   