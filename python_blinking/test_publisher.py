import zmq
import json
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)

# Example data
data = {
        "CLOSED_EYES_FRAME": 3,
        "BLINKING_RATIO": 7,
        "TIMEOUT_SEC": 1,
        "WAKEUP_SERVER_URL": "http://localhost:5001",
        "ID": "XXXXXXXXXXXX",
        "ZMQ_SERVER": "tcp://localhost:5556",
    }

socket.bind(data["ZMQ_SERVER"])
topic = "Camera"
json_data = json.dumps(data)
time.sleep(1)

socket.send_multipart([topic.encode('utf-8'), json_data.encode('utf-8')])

socket.close()
context.term()