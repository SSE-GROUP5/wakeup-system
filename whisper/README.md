# Speech Recognition and Transcription 

This project is designed to perform real-time speech recognition and transcription using the Whisper and OpenVINO models for efficient audio processing. It also includes functionality to detect repetitive sounds in the transcribed text. The project also allows to use Whisper OpenVINO for audio file transcription.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before running the script, ensure you have Python 3.10 installed on your system.

### Set up

1. Navigate into the project directory

```
cd whisper
```

2. Install the required Python packages:

```
pip install -r requirements.txt
```

## Usage
To run the script, use the following command in the terminal:
```
python whipser_transcribe_ov.py [options]
```

Available options include:

- *model*: Choose the model size (default is "base"). Options are "tiny", "base", "small", "medium", "large".
- *non_english*: Use this flag if you do not want to use the English model.
- *energy_threshold*: Set the energy level for the microphone to detect sound (default is 1000).
- *record_timeout*: Set how real-time the recording is, in seconds (default is 2).
- *phrase_timeout*: Set how much empty space between recordings before considering it a new line in the transcription (default is 2).
- *default_microphone*: (Linux only) Set the default microphone name for SpeechRecognition.

## Generating .exe file
If you plan to use the project as an executable on Windows, run the following command to set up the environment and create the .exe file. Ensure you have the necessary permissions to execute the script:

```
./run_script.sh
```
