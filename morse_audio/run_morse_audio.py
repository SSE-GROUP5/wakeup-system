import pyaudio
import time
import audioop
from morse_functions import decode_morse_letter
from dotenv import load_dotenv
import os
import sys
import requests

current_dir = os.path.dirname(os.path.realpath(__file__))
def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)

custom_modules_path = "./" if is_exe_file() else current_dir + "/../"  
sys.path.append(custom_modules_path)
from zeromq.zmqServer import ZeroMQServer

def check_connection(config):
    try:
        response = client.get(config["WAKEUP_SERVER_URL"], timeout=1)
        if response.status_code == 200:
            return b'OK' in response.content
    except requests.ConnectionError:
        return False
    return False


def update_env_vars(config, msg):
    for key in config.keys():
        if key in msg:
            config[key] = msg[key]
            print(f'Updated {key} to {msg[key]}')
    with open('env_trigger.txt', 'w') as f:
        for key in config.keys():
            f.write(f'{key}={config[key]}\n')
    return config
  
def confirm_to_server(config):
    try:
        request = client.post(config["WAKEUP_SERVER_URL"]+"/triggers/confirm", json={'id': config["ID"]})
        if request.status_code == 200:
            print('SUCCESS: Confirmed to wakeup server')
        elif request.status_code == 404:
            print('Device id not registered in wakeup server')
        elif request.status_code != 200:
            print('Error confirming to wakeup server')
    except Exception as e:
        print(e)
        

python_executable_dir = os.path.dirname(sys.executable)
config_path = os.path.join(python_executable_dir, '../sound_morse/') if is_exe_file() else current_dir
config_path = os.path.normpath(config_path)
config_path = os.path.join(config_path, 'env_trigger.txt')

if not os.path.exists(config_path):
    print(f'Please create env_trigger.txt file in {config_path} with the following content:')
    print("In the file, please set WAKEUP_SERVER_URL, ID, ZMQ_SERVER")
    exit(1)


load_dotenv(dotenv_path=config_path)
# variables for wakeup server that must be set in env_trigger.txt
WAKEUP_SERVER_URL= os.getenv('WAKEUP_SERVER_URL')
__ID= os.getenv('ID') 
__ZMQ_SERVER= os.getenv('ZMQ_SERVER')


if __ID is None or __ZMQ_SERVER is None or WAKEUP_SERVER_URL is None:
    print('Please set ID, WAKEUP_SERVER_URL and ZMQ_SERVER in env_trigger.txt file')
    exit(1)

client = requests.session()
CHANNELS = 1
RATE = 44100
CHUNK = 1024
FORMAT = pyaudio.paInt16




def start_listening(config, zmqServer):
  RECORD_SECONDS = config["RECORD_SECONDS"]
  THRESHOLD = config["THRESHOLD"]

  p = pyaudio.PyAudio()

  stream = p.open(format=FORMAT,
          channels=CHANNELS,
          rate=RATE,
          input=True,
          frames_per_buffer=CHUNK)

  RECORD_SECONDS = config["RECORD_SECONDS"]
  THRESHOLD = config["THRESHOLD"]
  END_WORD_TIME = config["END_WORD_TIME"]
  START_LISTEN_TIME = config["START_LISTEN_TIME"]

  total_letter = ''
  letter_timer = 0
  is_waiting = False
  is_listen = False
  counter = 0
  
  last_health_check = time.time()

  while True:
    
    message = zmqServer.receive()
    if message != None:
        topic, msg = message
        if topic == config["ID"]:
            config = update_env_vars(config, msg)
  

    RECORD_SECONDS = int(config["RECORD_SECONDS"])
    THRESHOLD = int(config["THRESHOLD"])
    END_WORD_TIME = int(config["END_WORD_TIME"])
    START_LISTEN_TIME = int(config["START_LISTEN_TIME"])
    
    
    if time.time() - last_health_check > 5:
      last_health_check = time.time()
      is_connected = check_connection(config)
      print(f'WakeUp server is_connected: {is_connected}')
      
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)    # here's where you calculate the volume
    if counter < START_LISTEN_TIME:
      if rms > THRESHOLD:
        counter += 1
        print(counter)
      else:
        counter = counter - 1 if counter > 0 else 0
        
    if counter >= START_LISTEN_TIME:
      print('Start listen')
      is_listen = True
    

    if is_listen and counter != 0:
      is_listen = False
      counter = 0
      stream.stop_stream()
      stream = p.open(format=FORMAT,
          channels=CHANNELS,
          rate=RATE,
          input=True,
          frames_per_buffer=CHUNK)
      for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)    # here's where you calculate the volume

        # Convert RMS value to Morse code
        encoded_char = ''
        if rms > THRESHOLD:  # Set your desired threshold value
          encoded_char = '-'
          
        else:
          if len(total_letter) > 0 and total_letter[-1] == '-':
            encoded_char = ' '
            is_waiting = False

          if not is_waiting and len(total_letter) > 0 and total_letter[-1] == ' ':
            letter_timer = time.time()
            is_waiting = True

          if is_waiting and time.time() - letter_timer > END_WORD_TIME:
            encoded_char = '/'
            is_waiting = False

        total_letter += encoded_char
        print(total_letter)
      
     
      morse_letter = get_morse_letter(total_letter, config)
      print(morse_letter)
      letter = decode_morse_letter(morse_letter)
      print(letter)
      try:
        request = client.post(config["WAKEUP_SERVER_URL"]+"/signals", json={'name': config["ID"], 'action': 'sound_morse', 'num_actions': letter})
        if request.status_code == 200:
            print('SUCCESS: Sent signal to wakeup server')
      except Exception as e:
        print(e)
      total_letter = ''

  stream.stop_stream()
  stream.close()
  p.terminate()




def dashes_to_morse(morse_code, config):
  MAX_DASHES_FOR_DOT = int(config["MAX_DASHES_FOR_DOT"])
  MIN_DASHES_FOR_DASH = int(config["MIN_DASHES_FOR_DASH"])
  decode_word = ''
  dashes = morse_code.split(' ')
  for dash in dashes:
    print(dash)
    if dash == '':
      decode_word += ' '
    elif len(dash) < MAX_DASHES_FOR_DOT and len(dash) > MIN_DASHES_FOR_DASH:
      decode_word += '.'
    elif len(dash) >= MAX_DASHES_FOR_DOT:
      decode_word += '-'

  return decode_word


def get_morse_letter(morse_code, config):
  morse_letter = ''
  words = morse_code.split(' /')
  for word in words:
    morse_letter += dashes_to_morse(word, config)
  return morse_letter





def main():
  config = {
    "WAKEUP_SERVER_URL": WAKEUP_SERVER_URL,
    "ID": __ID,
    "ZMQ_SERVER": __ZMQ_SERVER,
    "RECORD_SECONDS": os.getenv('RECORD_SECONDS') or 10,
    "THRESHOLD": os.getenv('THRESHOLD') or 1400,
    "END_WORD_TIME": os.getenv('END_WORD_TIME') or 1,
    "START_LISTEN_TIME": os.getenv('START_LISTEN_TIME') or 50,
    "MAX_DASHES_FOR_DOT": os.getenv('MAX_DASHES_FOR_DOT') or 20,
    "MIN_DASHES_FOR_DASH": os.getenv('MIN_DASHES_FOR_DASH') or 5,
  }
  zmqServer = ZeroMQServer(config["ZMQ_SERVER"])
  is_connected = check_connection(config)
  print(f'WakeUp server is_connected: {is_connected}')
  confirm_to_server(config)
  
  start_listening(config, zmqServer)

if __name__ == "__main__":
  main()
  