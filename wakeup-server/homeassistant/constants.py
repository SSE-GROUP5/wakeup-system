from dotenv import load_dotenv
import os
file_path = os.path.dirname(os.path.realpath(__file__))

load_dotenv(dotenv_path=f"{file_path}/../.env")
import os

if not os.path.isfile(f"{file_path}/../.env"):
    print(".env file not found")
    exit(1)

# HOMEASSISTANT CONFIG
HOMEASSISTANT_URL = os.getenv("HOMEASSISTANT_URL")
HOMEASSISTANT_TOKEN = os.getenv("HOMEASSISTANT_TOKEN")

if HOMEASSISTANT_URL == None:
    print("HOMEASSISTANT_URL not set in .env file")
    exit(1)

if HOMEASSISTANT_TOKEN == None:
    print("HOMEASSISTANT_TOKEN not set in .env file")
    exit(1)
