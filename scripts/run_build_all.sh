#!/bin/bash

set -e

# Remove all builds
rm -rf dist
rm -rf fall_detection/dist
rm -rf morse_vision/dist
rm -rf morse_audio/dist
rm -rf audio_classification/dist
rm -rf whisper/dist
rm -rf python_blinking/dist


# Build all the images
mkdir -p dist

## Build fall detection upper body
cd fall_detection && \
python3.10 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt && \
./run_build.sh && \
deactivate 


cd ..
cp fall_detection/dist/fall_upper_detection dist/

## Build morse vision

cd morse_vision && \
python3.10 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt && \
./run_build.sh && \
deactivate

cd ..
cp morse_vision/dist/morse_vision dist/morse_vision


## Build morse sound

cd morse_audio && \
python3.10 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt && \
./run_build.sh && \
deactivate

cd ..
cp morse_audio/dist/run_morse_audio dist/run_morse_audio

## Build sound classification
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi
cd audio_classification && \

if [ "$IS_WINDOWS" = true ]; then
  python -m venv venv && \
  source venv/Scripts/activate && \
else
  python3.10 -m venv venv && \
  source venv/bin/activate && \
fi

pip install --upgrade pip && \
pip install -r requirements.txt && \
./run_build.sh && \
deactivate

cd ..
cp audio_classification/dist/audio_classification dist/audio_classification

## Build whisper
IS_WINDOWS=false
if [[ "$OSTYPE" == "msys" ]]; then
  IS_WINDOWS=true
fi
cd whisper && \

if [ "$IS_WINDOWS" = true ]; then
  python -m venv venv && \
  source venv/Scripts/activate && \
else
  python3.10 -m venv venv && \
  source venv/bin/activate && \
fi

pip install --upgrade pip && \
pip install -r requirements.txt && \
./run_build.sh && \
deactivate

cd ..
cp whisper/dist/whisper_transcribe dist/whisper_transcribe


## Build blinking detection

cd python_blinking && \
python3.10 -m venv venv && \
source venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt && \
./run_build.sh && \
deactivate

cd ..
cp python_blinking/dist/blink_detect dist/blink_detect





