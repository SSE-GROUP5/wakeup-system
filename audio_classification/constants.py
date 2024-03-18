import os
import sys
from dotenv import load_dotenv

CONNECTION_CHECK_INTERVAL = 10

current_dir = os.path.dirname(os.path.realpath(__file__))
def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

custom_modules_path = "./" if is_exe_file() else current_dir + "/../"  
sys.path.append(custom_modules_path)

python_executable_dir = os.path.dirname(sys.executable)
config_path = os.path.join(python_executable_dir, '../audio_classification/') if is_exe_file() else current_dir
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
}