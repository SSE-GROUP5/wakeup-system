import os
import sys
from dotenv import load_dotenv

MODEL_VERBOSE = False
NOSE = 0
LEFT_EYE = 1
RIGHT_EYE = 2
LEFT_EAR = 3
RIGHT_EAR = 4
LEFT_SHOULDER = 5
RIGHT_SHOULDER = 6

CONNECTION_CHECK_INTERVAL = 10

current_dir = os.path.dirname(os.path.realpath(__file__))
def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

custom_modules_path = "./" if is_exe_file() else current_dir + "/../"  
sys.path.append(custom_modules_path)
from zeromq.zmqServer import ZeroMQServer
import beepy

python_executable_dir = os.path.dirname(sys.executable)
config_path = os.path.join(python_executable_dir, '../vision_upper_body_fall/') if is_exe_file() else current_dir
config_path = os.path.normpath(config_path)
config_path = os.path.join(config_path, 'env_trigger.txt')

if not os.path.exists(config_path):
    print(f'Please create env_trigger.txt file in {config_path} with the following content:')
    print("In the file, please set WAKEUP_SERVER_URL, ID, ZMQ_SERVER")
    exit(1)

load_dotenv(config_path)

# variables for wakeup server that must be set in env_trigger.txt
__WAKEUP_SERVER_URL= os.getenv('WAKEUP_SERVER_URL')
__ID= os.getenv('ID') 
__ZMQ_SERVER= os.getenv('ZMQ_SERVER')

if __ID is None or __ZMQ_SERVER is None or __WAKEUP_SERVER_URL is None:
    print('Please set WAKEUP_SERVER_URL, ID and ZMQ_SERVER in env_trigger.txt file')
    exit(1)

config = {
    "WAKEUP_SERVER_URL": __WAKEUP_SERVER_URL,
    "ID": __ID,
    "ZMQ_SERVER": __ZMQ_SERVER,
    "RESET_TIME": 5,
    "MAX_ANGLE_BETWEEN_EYES": int(os.getenv('MAX_ANGLE_BETWEEN_EYES')) or 50,
    "MAX_ANGLE_BETWEEN_EARS": int(os.getenv('MAX_ANGLE_BETWEEN_EARS')) or 50,
    "MAX_ANGLE_BETWEEN_SHOULDERS": int(os.getenv('MAX_ANGLE_BETWEEN_SHOULDERS')) or 50,
    "NUMBER_OF_PERSONS_TO_DETECT": 1,
}