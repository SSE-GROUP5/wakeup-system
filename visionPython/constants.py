import json
import os


class Constants:
    def __init__(self):
        self.file_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(self.file_dir + "/config.json"):
            emtpy_config = {
                "CLOSED_EYES_FRAME": 3,
                "BLINKING_RATIO": 4.5,
                "TIMEOUT_SEC": 1,
                "WAKEUP_SERVER_URL": "http://localhost:5001",
                "ID": "sound_device_1"
            }
            # Writing to config file
            with open(self.file_dir + "/config.json", "w") as outfile:
                json.dump(emtpy_config, outfile)
            raise Exception("config.json not found. Please fill in the config.json file and restart the program. A template has been created for you.")

        # Reading the config file
        file = open(self.file_dir + "/config.json", "r")
        config = json.load(file)

        self.CLOSED_EYES_FRAME = config['CLOSED_EYES_FRAME']
        self.BLINKING_RATIO = config['BLINKING_RATIO']
        self.TIMEOUT_SEC = config['TIMEOUT_SEC']
        self.WAKEUP_SERVER_URL = config['WAKEUP_SERVER_URL']
        self.ID = config['ID']

        if self.CLOSED_EYES_FRAME is None:
            raise Exception("CLOSED_EYES_FRAME not found in config.json")
        if self.BLINKING_RATIO is None:
            raise Exception("BLINKING_RATIO not found in config.json")
        if self.TIMEOUT_SEC is None:
            raise Exception("TIMEOUT_SEC not found in config.json")
        if self.WAKEUP_SERVER_URL is None:
            raise Exception("WAKEUP_SERVER_URL not found in config.json")
        if self.ID is None:
            raise Exception("ID not found in config.json")



    def updateConfig(self, json_str):
        config = json.loads(json_str)

        # Update the config file
        with open(self.file_dir + "/config.json", "w") as outfile:
            json.dump(config, outfile)

        # Update Parameters

        self.CLOSED_EYES_FRAME = config['CLOSED_EYES_FRAME']
        self.BLINKING_RATIO = config['BLINKING_RATIO']
        self.TIMEOUT_SEC = config['TIMEOUT_SEC']
        self.WAKEUP_SERVER_URL = config['WAKEUP_SERVER_URL']
        self.ID = config['ID']



