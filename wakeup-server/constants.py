from dotenv import load_dotenv
import os

load_dotenv()

HOSTNAME = os.getenv("HOSTNAME")
PORT = os.getenv("PORT")

if not HOSTNAME:
    raise ValueError("No HOSTNAME set for Flask applicaton")
if not PORT:
    raise ValueError("No PORT set for Flask applicaton")


# HOMEASSISTANT CONFIG
HOMEASSISTANT_URL = os.getenv("HOMEASSISTANT_URL")
HOMEASSISTANT_TOKEN = os.getenv("SUPERVISOR_TOKEN") or os.getenv("HOMEASSISTANT_TOKEN")

if HOMEASSISTANT_URL == None:
    print("HOMEASSISTANT_URL not set in .env file")
    exit(1)
if HOMEASSISTANT_TOKEN == None:
    print("HOMEASSISTANT_TOKEN not set in .env file")
    exit(1)

print("HOMEASSISTANT_URL: " + HOMEASSISTANT_URL)
