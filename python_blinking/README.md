# Setup the trigger

## Create the environment variables files if they don't exist

```bash
echo "WAKEUP_SERVER_URL=http://localhost:5001
ID=tmp_id
ZMQ_SERVER=tcp://localhost:5556
CLOSED_EYES_FRAME=2
BLINKING_RATIO=3.5
TIMEOUT_SEC=3
CHANNEL=0" > env_trigger.txt
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
cp env_trigger.txt blink_detect
```

# Run the trigger

## Locally

```bash
source venv/bin/activate
python blink_detect.py
```
## From the executable file

- Make sure the `env_trigger.txt` file is in the same directory as the executable file.

the folder `blink_detect` should contain the following files:

```
├── env_trigger.txt
└── blink_detect
```

Run the executable file:
```bash
cd blink_detect
./blink_detect
```

# Add it to the wake up server

1. Make sure the wake up server is running
```bash
curl http://localhost:5001/health
```

2. Add the trigger to the wake up server with postman or curl
```bash
curl -X POST http://localhost:5001/triggers -H "Content-Type: application/json" -d '{"type": "blink_detect", "name": "my_device_6"}'
```

Copy the `id` from the response and replace the `ID` in the `env_trigger.txt` file.


3. Run the trigger
```bash
python blink_detect.py
```
or 
```bash
cd blink_detect
./blink_detect
```

You should see the following message:
```
SUCCESS: Confirmed to wakeup server
```

