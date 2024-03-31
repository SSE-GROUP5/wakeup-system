# Speech Recognition and Transcription 

This project is designed to perform real-time speech recognition and transcription using the Whisper and OpenVINO models for efficient audio processing. It also includes functionality to detect repetitive sounds in the transcribed text.
## Benchmarking
In order to evalate the efficiency of the OpenVINO the benchmark was constructed for 2 use cases:
1. Whisper with/without OpenVINO for audio file transcription.
2. Whisper with/without OpenVINO for live audio transcription.

The `benchmark` folder is only created for benchmarking purposes, it has the following files:
- `whisper_no_ov.py` - a base Whisper for audio file transcription.
- `whisper_openvino.py` - Whisper with OpenVINO for audio file transcription.
- `whisper_transcribe.py` - a base Whisper for audio file transcription.
- `whisper_transcribe_ov.py` - Whisper with OpenVINO for live audio transcription.

## Setup the trigger

### Create the environment variables files if they don't exist

```bash
echo "WAKEUP_SERVER_URL=http://localhost:5001
ID=tmp_id
ZMQ_SERVER=tcp://*:5556 > env_trigger.txt
```


### Create the pyton 3.10 virtual environment

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Build the executable file

```bash
pip3 install pyinstaller
./run_build.sh
cp env_trigger.txt sound_whisper
```

## Run the trigger

### Locally

```bash
source venv/bin/activate (MacOS)
source venv/Scripts/activate (Windows)
python whisper_transcribe.py
```

### From the executable file
*Note*: Executable file for live audio transcription can only be created for base Whisper without OpenVINO, because OpenVINO does not support pyinstaller. This will be resolved in future work.

- Make sure the `env_trigger.txt` file is in the same directory as the executable file.

the folder `sound_whisper` should contain the following files:

```
├── env_trigger.txt
└── whisper_transcribe
```

Run the executable file:
```bash
cd sound_whisper
./whisper_transcribe
```


## Add it to the wake up server

1. Make sure the wake up server is running
```bash
curl http://localhost:5001/health
```

2. Add the trigger to the wake up server with postman or curl
```bash
curl -X POST http://localhost:5001/triggers -H "Content-Type: application/json" -d '{"type": "sound_whisper", "name": "my_device_4"}'
```

Copy the `id` from the response and replace the `ID` in the `env_trigger.txt` file.


3. Run the trigger
```bash
python whisper_transcribe.py
```
or 
```bash
cd sound_whisper
./whisper_transcribe
```

You should see the following message:
```
SUCCESS: Confirmed to wakeup server
```