from dotenv import load_dotenv
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
def is_exe_file():
	# Determine if we are running in a bundled environment and set the base path
	return getattr(sys, 'frozen', False)


python_executable_dir = os.path.dirname(sys.executable)
config_path = os.path.join(python_executable_dir, '../wakeup_server/') if is_exe_file() else current_dir
config_path = os.path.normpath(config_path)
config_path = os.path.join(config_path, '.env')

if not os.path.exists(config_path):
    print(f'Please create .env file in {config_path} with the following content:')
    print("In the file, please set HOSTNAME, PORT, ZERO_MQ_SERVER_URL, HOMEASSISTANT_URL, HOMEASSISTANT_TOKEN")
    print("You should use the env.example file as a template or the setup_local_env.sh script to create the .env file") 
    exit(1)
    
load_dotenv(config_path)


HOSTNAME = os.getenv("HOSTNAME")
PORT = os.getenv("PORT")
ZERO_MQ_SERVER_URL = os.getenv("ZERO_MQ_SERVER_URL")
DEV_MODE = os.getenv("DEV_MODE").lower() == "true" if os.getenv("DEV_MODE") != None else False
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WAKE_ON_LAN_PORT = 9

if not HOSTNAME:
    raise ValueError("No HOSTNAME set for Flask applicaton")
if not PORT:
    raise ValueError("No PORT set for Flask applicaton")
if not ZERO_MQ_SERVER_URL:
    raise ValueError("No ZERO_MQ_SERVER_URL set for Flask applicaton")


# HOMEASSISTANT CONFIG
HOMEASSISTANT_URL = os.getenv("HOMEASSISTANT_URL")
HOMEASSISTANT_TOKEN = os.getenv("SUPERVISOR_TOKEN") or os.getenv("HOMEASSISTANT_TOKEN")
HOMEASSISTANT_OFFLINE_MODE = os.getenv("HOMEASSISTANT_OFFLINE_MODE").lower() == "true" if os.getenv("HOMEASSISTANT_OFFLINE_MODE") != None else False

if HOMEASSISTANT_URL == None:
    print("HOMEASSISTANT_URL not set in .env file")
    exit(1)
if HOMEASSISTANT_TOKEN == None:
    print("HOMEASSISTANT_TOKEN not set in .env file")
    exit(1)

is_telegram_bot_token_set = "set" if TELEGRAM_BOT_TOKEN else "not set"
print(f"TELEGRAM_BOT_TOKEN is {is_telegram_bot_token_set}")

print("HOMEASSISTANT_URL: " + HOMEASSISTANT_URL)
print(f"DEV_MODE: {DEV_MODE}")
print(f"HOMEASSISTANT_OFFLINE_MODE is {HOMEASSISTANT_OFFLINE_MODE}")

DATA_FOLDER_PATH = os.path.join(current_dir, "data")
os.makedirs(DATA_FOLDER_PATH, exist_ok=True)

TRIGGERS_TYPES = {
  "sound_classification": {
    "verify" : lambda trigger_num_actions: isinstance(trigger_num_actions, int) and trigger_num_actions > 1,
    "fail_message" : "Trigger action sound_classification must have a value greater than 1"
  },
  "sound_whisper": {
    "verify" : lambda trigger_num_actions: trigger_num_actions in ["ah", "oh"],
    "fail_message" : "Trigger action sound_whisper must have a value of 'ah' or 'oh'"
  },
  "sound_morse": {
    "verify" : lambda trigger_num_actions: trigger_num_actions.isalpha() and len(trigger_num_actions) == 1,
    "fail_message" : "Trigger action sound_morse must have a single letter"
  },
  "vision_morse": {
    "verify" : lambda trigger_num_actions: trigger_num_actions.isalpha() and len(trigger_num_actions) == 1,
    "fail_message" : "Trigger action vision_morse must have a single letter"
  },
  "vision_blink": {
    "verify" : lambda trigger_num_actions: isinstance(trigger_num_actions, int) and trigger_num_actions > 1,
    "fail_message" : "Trigger action vision_blink must have a value greater than 1"
  },
  "vision_upper_body_fall": {
    "verify" : lambda trigger_num_actions: trigger_num_actions in ["left", "right", "alert"],
    "fail_message" : "Trigger action vision_upper_body_fall must have a value of 'left', 'right' or 'alert'"
  },
}



TARGETS_TYPES = ["telegram", "wake_on_lan", "homeassistant"]