import zmq
import json

class ZMQClient:
  def __init__(self, address):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.REQ)
    self.socket.connect(address)
    self.socket.RCVTIMEO = 1000

  def send_data(self, topic, data):
    json_data = { "topic": topic, "data": data }
    try:
      self.socket.send(json.dumps(json_data).encode(), zmq.NOBLOCK)
    except Exception as e:
      print(e)
      print("Warning: ZMQ Server needs to be started to proceed.")

  def receive_reply(self):
    message = self.socket.recv_string()
    return message


if __name__ == "__main__":
  client = ZMQClient("tcp://localhost:5556")
  client.send_data("4fdcc4ae-bf7a-434a-9ad4-aff78ef52e8d", 
  { 
    "WAKEUP_SERVER_URL": "http://localhost:5001",
    "MAX_ANGLE_BETWEEN_EARS": 100,
  })
  print("Received: ", client.receive_reply())
