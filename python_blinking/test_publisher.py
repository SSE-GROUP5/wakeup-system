import zmq
import json
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")
data = {
        "CLOSED_EYES_FRAME": 3,
        "BLINKING_RATIO": 4.5,
        "TIMEOUT_SEC": 1,
        "WAKEUP_SERVER_URL": "http://localhost:5001",
        "ID": "sound_device_1"
    }

topic = "Camera"
json_data = json.dumps(data)
time.sleep(1)

socket.send_multipart([topic.encode('utf-8'), json_data.encode('utf-8')])

socket.close()
context.term()