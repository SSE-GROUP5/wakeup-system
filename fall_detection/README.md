# Setup the trigger

## Create the environment variables files if they don't exist

```bash
echo "WAKEUP_SERVER_URL=http://localhost:5001
ID=tmp_id
ZMQ_SERVER=tcp://*:5556
MAX_ANGLE_BETWEEN_EYES=50
MAX_ANGLE_BETWEEN_EARS=50
MAX_ANGLE_BETWEEN_SHOULDERS=50" > env_trigger.txt
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
cp env_trigger.txt vision_upper_body_fall
```

# Run the trigger

## Locally

```bash
source venv/bin/activate
python fall_upper_detection.py
```

## From the executable file

- Make sure the `env_trigger.txt` file is in the same directory as the executable file.
- If you don't have the model file, it will be downloaded directly from the script with an internet connection.

the folder `vision_upper_body_fall` should contain the following files:

```
├── env_trigger.txt
├── fall_upper_detection
└── yolov8m-pose.pt
```

Run the executable file:
```bash
cd vision_upper_body_fall
./fall_upper_detection
```


# Add it to the wake up server

1. Make sure the wake up server is running
```bash
curl http://localhost:5001/health
```

2. Add the trigger to the wake up server with postman or curl
```bash
curl -X POST http://<hostname>:5001/triggers -H "Content-Type: application/json" -d '{"type": "vision_upper_body_fall", "name": "my_device"}'
```

Copy the `id` from the response and replace the `ID` in the `env_trigger.txt` file.


3. Run the trigger
```bash
python fall_upper_detection.py
```
or 
```bash
cd vision_upper_body_fall
./fall_upper_detection
```

You should see the following message:
```
SUCCESS: Confirmed to wakeup server
```


