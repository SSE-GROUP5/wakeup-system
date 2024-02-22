import json
import os
from dotenv import load_dotenv


class Constants:
    def __init__(self, envFilename):
        self.file_name = envFilename
        file_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.path.exists(file_dir + "/" + self.file_name ):
            raise Exception("No env file, please use GUI to generate one")
        
        self.updateConfig()

        if self.CLOSED_EYES_FRAME is None:
            raise Exception("CLOSED_EYES_FRAME not found in .env")
        if self.BLINKING_RATIO is None:
            raise Exception("BLINKING_RATIO not found in .env")
        if self.TIMEOUT_SEC is None:
            raise Exception("TIMEOUT_SEC not found in .env")
        if self.WAKEUP_SERVER_URL is None:
            raise Exception("WAKEUP_SERVER_URL not found in .env")
        if self.DEVICE_ID is None:
            raise Exception("DEVICE_ID not found in .env")

    def updateConfig(self):
        load_dotenv(self.file_name)

        self.CLOSED_EYES_FRAME = int(os.getenv('CLOSED_EYES_FRAME'))
        self.BLINKING_RATIO = float(os.getenv('BLINKING_RATIO'))
        self.TIMEOUT_SEC = int(os.getenv('TIMEOUT_SEC'))
        self.WAKEUP_SERVER_URL = os.getenv('WAKEUP_SERVER_URL')
        self.DEVICE_ID = os.getenv('DEVICE_ID')

    def updateEnvFile(self, jsonStr):
        jsonData = json.load(jsonStr)
        with open(self.filename, "w") as file:
            file.write(f"DEVICE_ID={self.DEVICE_ID}")
            file.write(f"WAKEUP_SERVER_URL={self.WAKEUP_SERVER_URL}")
            for key in jsonData:
                file.write(f"{key}={jsonData[key]}")

        # Load the new env file
        self.updateConfig()



if __name__ == "__main__":
    const = Constants()

    print(const.CLOSED_EYES_FRAME)
    print(const.BLINKING_RATIO)
    print(const.TIMEOUT_SEC)