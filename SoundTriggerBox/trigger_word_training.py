# trigger_word_training.py
# This python file is implemented based on vowel_recognition.py as described in
# Emily Pulford's Sound Recognition Project.
# For more information, check https://github.com/pulfdev/Sound_Recognition/blob/main/vowel_recognition.py

import pyaudio
from statistics import mode, StatisticsError
from vosk import Model, KaldiRecognizer
from config import *

# Clear the user_made_sounds dictionary
# clear_user_made_sounds()

# Load the current configuration
config = load_json('config.json')
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)


def recognise_words():
    text = ''
    cap = pyaudio.PyAudio()
    stream = cap.open(
        format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192
    )
    stream.start_stream()

    streaming = True

    while streaming:
        data = stream.read(4096)

        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            text = text[14:-3]
            print(text)
            streaming = False
    stream.stop_stream()
    return text


def train_sounds(sound_name, number, sys_mode):
    words = []

    while number != 0:
        # print("say " + sound_name)
        word = recognise_words()
        words.append(word)
        number = number - 1

    try:
        most_frequent_word = mode(words)
    except StatisticsError:
        # print("No unique mode found. Using the first word as the most frequent word.")
        most_frequent_word = words[0]

    if sys_mode == 1:
        # "ah" will become "ah ah ah"
        repeated_element = " ".join([most_frequent_word] * 3)
        update_user_made_sounds("sound_pattern", sound_name, repeated_element)  # TO DO: create user_made_sounds_dict
    elif sys_mode == 2:
        update_user_made_sounds("trigger_words", sound_name, most_frequent_word)  # TO DO: create user_made_sounds_dict
    else:
        print("Invalid system mode. Please try again.")
