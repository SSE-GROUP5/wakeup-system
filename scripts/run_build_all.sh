#!/bin/bash

set -e

# Remove all builds
rm -rf dist
rm -rf fall_detection/dist
rm -rf morse_vision/dist
rm -rf morse_audio/dist


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



