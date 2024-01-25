import zmq
import time
import json

class ZeroMQServer:
  def __init__(self, address):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.REP)
    self.socket.bind(address)
    # Create a poller
    self.poller = zmq.Poller()
    self.poller.register(self.socket, zmq.POLLIN) # Register the socket for polling

    self.message_buffer = []

  def receive(self):
    socks = dict(self.poller.poll(timeout=0))  # Timeout in milliseconds

    if self.socket in socks and socks[self.socket] == zmq.POLLIN:
        # Receive the message
        data = self.socket.recv()
        json_data = json.loads(data)
        topic = json_data.get('topic')
        msg = json_data.get('data')
        print(f"Received on topic '{topic}' message: {msg}")
        # The needs to send a reply back to the client
        self.socket.send(b"Message received")
        return topic, msg

    else:
        # No message received, server can do other tasks here
        # keep same line
        print("No message received. Server is free for other tasks.", end="\r")
        
        return None
    

  def receive_all(self):
    while True:
      message = self.receive()
      if message is None:
        break
      self.message_buffer.append(message)
    return self.message_buffer

  

if __name__ == "__main__":
    server = ZeroMQServer("tcp://*:5556")
    time.sleep(5)
    server.receive()
    while True:
        server.receive()
        time.sleep(1)