# Setup the trigger

## Create the environment variables files if they don't exist

```bash
echo "WAKEUP_SERVER_URL=http://localhost:5001
ID=tmp_id
ZMQ_SERVER=tcp://*:5556
RECORD_SECONDS=10
THRESHOLD=1400
END_WORD_TIME=1
START_LISTEN_TIME=50
MAX_DASHES_FOR_DOT=20
MIN_DASHES_FOR_DASH=5" > env_trigger.txt
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
cp env_trigger.txt sound_morse
```

# Run the trigger

## Locally

```bash
source venv/bin/activate
python run_morse_audio.py
```

## From the executable file

- Make sure the `env_trigger.txt` file is in the same directory as the executable file.

the folder `sound_morse` should contain the following files:

```
├── env_trigger.txt
└── run_morse_audio
```

Run the executable file:
```bash
cd sound_morse
./run_morse_audio
```


# Add it to the wake up server

1. Make sure the wake up server is running
```bash
curl http://localhost:5001/health
```

2. Add the trigger to the wake up server with postman or curl
```bash
curl -X POST http://localhost:5001/triggers -H "Content-Type: application/json" -d '{"type": "sound_morse", "name": "my_device_sound"}'
```

Copy the `id` from the response and replace the `ID` in the `env_trigger.txt` file.


3. Run the trigger
```bash
python morse_vision.py
```
or 
```bash
cd sound_morse
./morse_vision
```

You should see the following message:
```
SUCCESS: Confirmed to wakeup server
```


