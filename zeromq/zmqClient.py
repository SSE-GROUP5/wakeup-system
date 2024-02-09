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
  client.send_data("andy_vision", {"MIN_BLINKING_TIME": 3})
