import os
from dotenv import load_dotenv

env_file = '.env.wakeup'
file_dir = os.path.dirname(os.path.abspath(__file__))
print(file_dir)
if not os.path.exists(file_dir + "/" + env_file):
    raise Exception("No env file, please use GUI to generate one")


load_dotenv(env_file)

DEVICE_ID = os.getenv('DEVICE_ID')
TYPE = os.getenv('TYPE')
TIMEOUT = os.getenv('TIMEOUT')

print(DEVICE_ID)
print(TYPE)
print(TIMEOUT)
