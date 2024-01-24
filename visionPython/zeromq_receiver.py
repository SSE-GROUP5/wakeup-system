import zmq

class ZeroMQReceiver:
  def __init__(self, address):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.SUB)
    self.socket.connect(address)
    self.socket.setsockopt_string(zmq.SUBSCRIBE, '')
    self.message_buffer = []

  def receive(self):
    message = self.socket.recv_string()
    return message
  
  def receive_non_blocking(self):
    try:
      message = self.socket.recv_string(flags=zmq.NOBLOCK)
      return message
    except zmq.Again:
      return None
    
  def receive_all(self):
    while True:
      message = self.receive_non_blocking()
      if message is None:
        break
      self.message_buffer.append(message)
    return self.message_buffer
  
  def has_message(self):
    return self.receive_non_blocking() is not None
