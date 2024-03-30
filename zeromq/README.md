# ZeroMQ package


This package provides a high-level API for the ZeroMQ messaging library. It is based on the `zmq` package and provides a simple interface to send and receive messages using ZeroMQ sockets.

## Installation

To install the package, run the following command:

```bash
pip install .
```

## Usage

The package provides a client and a server class that can be used to send and receive messages. The client and server classes are based on the `zmq.Context` and `zmq.Socket` classes from the `pyzmq` package.

### Server example

```python
if __name__ == "__main__":
    server = ZeroMQServer("tcp://*:5556")
    time.sleep(5)
    server.receive()
    while True:
        server.receive()
        time.sleep(1)
```

### Client example

```python
if __name__ == "__main__":
  client = ZMQClient("tcp://localhost:5556")
  client.send_data("<id_of_the_trigger>", 
  { 
    "WAKEUP_SERVER_URL": "http://localhost:5001",
    "MAX_ANGLE_BETWEEN_EARS": 100,
  })
  print("Received: ", client.receive_reply())
```

# Use in the project

Search for the `zeromq` in the project


## License

This package is licensed under the MIT license.
