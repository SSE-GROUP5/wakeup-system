# Audio Classification

This project uses the MediaPipe framework to continuously classify audio data acquired from a device's microphone in real-time. Currently it is used to identify *Finger Snapping*, but can be adjusted for other sounds (see [yamnet model](https://storage.googleapis.com/mediapipe-tasks/audio_classifier/yamnet_label_list.txt) list.)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before running the script, ensure you have Python 3.10 installed on your system.

### Set up

1. Navigate into the project directory

```
cd audio_classification
```

2. Install the required Python packages:

```
pip install -r requirements.txt
```

## Usage
To run the script, use the following command in the terminal:
```
python audio_classification.py [options]
```

Available options include:

- *model*: Name of the TensorFlow Lite audio classification model (default amd reccomended: yamnet.tflite).
- *maxResults*: Maximum number of classification results to display (default: 5).
- *overlappingFactor*: Overlapping factor between adjacent inferences, value must be between 0 and 1 (default: 0.5).
- *scoreThreshold*: The score threshold of classification results (default: 0.0).

## Generating .exe file
If you plan to use the project as an executable on Windows, run the following command to set up the environment and create the .exe file. Ensure you have the necessary permissions to execute the script:

```
./run_script.sh
```
