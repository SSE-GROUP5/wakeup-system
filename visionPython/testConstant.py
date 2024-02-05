import json
import os
from dotenv import load_dotenv


class Constants:
    def __init__(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(file_dir + "/.env.wakeup" ):
            raise Exception("No env file, please use GUI to generate one")
        
        load_dotenv('.env.wakeup')

        self.CLOSED_EYES_FRAME = os.getenv('CLOSED_EYES_FRAME')
        self.BLINKING_RATIO = os.getenv('BLINKING_RATIO')
        self.TIMEOUT_SEC = os.getenv('TIMEOUT_SEC')
        self.WAKEUP_SERVER_URL = os.getenv('WAKEUP_SERVER_URL')
        self.ID = os.getenv('ID')

        if self.CLOSED_EYES_FRAME is None:
            raise Exception("CLOSED_EYES_FRAME not found in .venv")
        if self.BLINKING_RATIO is None:
            raise Exception("BLINKING_RATIO not found in .venv")
        if self.TIMEOUT_SEC is None:
            raise Exception("TIMEOUT_SEC not found in .venv")
        if self.WAKEUP_SERVER_URL is None:
            raise Exception("WAKEUP_SERVER_URL not found in .venv")
        if self.ID is None:
            raise Exception("ID not found in .venv")

    def updateConfig(self, json_data):
        # TODO WILL THERE STILL BE RUNTIME CONFIG CHANGE? 
        return

