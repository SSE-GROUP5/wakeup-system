import os
from dotenv import load_dotenv

env_file = '.env.wakeup'


load_dotenv(env_file)

DEVICE_ID = os.getenv('DEVICE_ID')
TYPE = os.getenv('TYPE')
TIMEOUT = os.getenv('TIMEOUT')

print(DEVICE_ID)
print(TYPE)
print(TIMEOUT)
