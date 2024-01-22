# main.py
# The following python file is based on the techniques found at:
# https://realpython.com/python-gui-tkinter/
# https://realpython.com/inner-functions-what-are-they-good-for/
# https://realpython.com/intro-to-python-threading/
# https://www.youtube.com/watch?v=YXPyB4XeYLA

# import psutil
import os
import threading
import soundtriggerbox_vosk
from trigger_word_training import *


class Controller:
    def __init__(self):
        self.sound_trigger_instance = soundtriggerbox_vosk
        self.trained_sounds_counter = 0
        self.update_button_state()
        self.running_thread = None  # keep track of running thread

    # Start SoundsTriggerBox Service
    def run_soundtriggerbox_vosk(self):
        print("Starting SoundTriggerBox")
        self.running_thread = threading.Thread(target=self.sound_trigger_instance.run_soundtriggerbox_vosk)
        self.running_thread.start()
        print("SoundTriggerBox Started")

    def update_button_state(self):
        # Initialize flag
        config_exists = False

        # Check if 'config.json' exists and has the necessary keys
        if os.path.exists('config.json'):
            with open('config.json', 'r') as file:
                data = json.load(file)
                if data.get('user_made_sounds') and data['user_made_sounds'].get('trigger_words') and data[
                     'user_made_sounds'].get('sound_pattern'):
                    config_exists = True

        # If both files are present and valid
        if config_exists:
            print("Config file found")
            self.run_soundtriggerbox_vosk()
        else:
            print("Config file was not found")

if __name__ == "__main__":

    # Connect the program with the last E cores on a 12 gen intel cpu
    # Make sure you have "psutil" library pip installed.
    # Code provided by James Bown:
    #
    # Core_counter = psutil.cpu_count()
    #
    # processID = psutil.Process().pid
    # print("Current PID: ", processID)
    # p = psutil.Process(processID).cpu_affinity([Core_counter - 1])
    app = Controller()
