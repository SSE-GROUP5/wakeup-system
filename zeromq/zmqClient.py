import zmq
import json

class ZMQClient:
  def __init__(self, address):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.REQ)
    self.socket.connect(address)

  def send_data(self, topic, data):
    json_data = { "topic": topic, "data": data }
    self.socket.send(json.dumps(json_data).encode())

  def receive_reply(self):
    message = self.socket.recv_string()
    return message


if __name__ == "__main__":
  client = ZMQClient("tcp://localhost:5556")
  client.send_data("andy_vision", 
  { 
    "WAKEUP_SERVER_URL": "http://localhost:5001",
    "CHANNEL":0,
    "CLOSED_EYES_FRAME":3.0,
    "BLINKING_RATIO":4.5,
    "MIN_BLINKING_TIME":0.1,
    "MAX_SHORT_BLINKING_TIME":0.6,
    "TIMEOUT_MORSE_READER":1.5,
  })
  print("Received: ", client.receive_reply())
