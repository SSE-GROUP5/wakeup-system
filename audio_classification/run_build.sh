#!/bin/bash
set -e
DIRECTORY=$(dirname $0)

pyinstaller \
  --add-data "$DIRECTORY/yamnet.tflite:." \
  --hidden-import=tkinter \
  --hidden-import=requests \
  --add-data "$DIRECTORY/../triggers_gui_config:triggers_gui_config" \
  --onefile "$DIRECTORY/classify.py"   