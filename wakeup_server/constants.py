from dotenv import load_dotenv
import os

load_dotenv()

current_dir = os.path.dirname(os.path.realpath(__file__))

HOSTNAME = os.getenv("HOSTNAME")
PORT = os.getenv("PORT")
ZERO_MQ_SERVER_URL = os.getenv("ZERO_MQ_SERVER_URL")
DEV_MODE = os.getenv("DEV_MODE").lower() == "true" if os.getenv("DEV_MODE") != None else False
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

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