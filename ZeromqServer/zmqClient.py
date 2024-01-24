import zmq
import time
import json

def zmq_client():
    # Prepare our context and sockets
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5556")
    data = {
        "CLOSED_EYES_FRAME": 3,
        "BLINKING_RATIO": 4.5,
        "TIMEOUT_SEC": 1,
        "WAKEUP_SERVER_URL": "http://localhost:5001",
        "ID": "sound_device_1"
    }

    topic = "Camera"
    json_data = json.dumps(data)
    # Send a request
    socket.send_multipart([topic.encode('utf-8'), json_data.encode('utf-8')])

    # socket.send_string("Hello")

    # Wait for the reply
    # message = socket.recv_string()
    # print(f"Received reply: {message}")

if __name__ == "__main__":
    zmq_client()
