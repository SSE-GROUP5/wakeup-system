import sys
import os
from constants import ZERO_MQ_SERVER_URL
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir + "/..")


from zeromq.zmqClient import ZMQClient
zmq_client = ZMQClient(ZERO_MQ_SERVER_URL)


