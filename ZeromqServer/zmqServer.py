import zmq
import time


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
        topic, msg = self.socket.recv_multipart()
        print(f"Received on topic '{topic.decode('utf-8')}': {msg.decode('utf-8')}")

        msg = msg.decode('utf-8')
        topic = topic.decode('utf-8')
        return topic, msg

    else:
        # No message received, server can do other tasks here
        print("No message received. Server is free for other tasks.")
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