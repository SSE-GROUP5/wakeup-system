# Audio Classification

This project uses the MediaPipe framework to continuously classify audio data acquired from a device's microphone in real-time. Currently it is used to identify *Finger Snapping*, but can be adjusted for other sounds (see [yamnet model](https://storage.googleapis.com/mediapipe-tasks/audio_classifier/yamnet_label_list.txt) list.)


# Setup the trigger

## Create the environment variables files if they don't exist

```bash
echo "WAKEUP_SERVER_URL=http://localhost:5001
ID=tmp_id
ZMQ_SERVER=tcp://*:5556 > env_trigger.txt
```


## Create the pyton 3.10 virtual environment

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Build the executable file

```bash
pip3 install pyinstaller
./run_build.sh
cp env_trigger.txt sound_classification
```

# Run the trigger

## Locally

```bash
source venv/bin/activate (MacOS)
source venv/Scripts/activate (Windows)
python audio_classification.py
```

## From the executable file

- Make sure the `env_trigger.txt` file is in the same directory as the executable file.

the folder `sound_classification` should contain the following files:

```
├── env_trigger.txt
└── audio_classification
```

Run the executable file:
```bash
cd sound_classification
./audio_classification
```


# Add it to the wake up server

1. Make sure the wake up server is running
```bash
curl http://localhost:5001/health
```

2. Add the trigger to the wake up server with postman or curl
```bash
curl -X POST http://localhost:5001/triggers -H "Content-Type: application/json" -d '{"type": "sound_classification", "name": "my_device_5"}'
```

Copy the `id` from the response and replace the `ID` in the `env_trigger.txt` file.


3. Run the trigger
```bash
python audio_classification.py
```
or 
```bash
cd sound_classification
./audio_classification
```

You should see the following message:
```
SUCCESS: Confirmed to wakeup server
```
