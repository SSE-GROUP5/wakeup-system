# soundtrigger.py
from config import *


def SoundDetection(text):
    config = load_json('config.json')
    trigger_words_values = config['user_made_sounds']['trigger_words'].values()
    sound_pattern_values = config['user_made_sounds']['sound_pattern'].values()
    if any(value in text for value in trigger_words_values) or any(value in text for value in sound_pattern_values):
        return 1
    elif "stop" in text:
        return 2
    else:
        return 0

def SoundTriggering(signal):
    if signal == 1:
        print("Trigger sent to the message queue")
    else:
        return
    return
