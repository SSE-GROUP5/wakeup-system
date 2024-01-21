# soundtriggerbox_vosk.py

from vosk import Model, KaldiRecognizer
import pyaudio
import soundtrigger
import json
import time
import numpy as np
import noisereduce as nr


global running


def reset_recognizer(model):
    return KaldiRecognizer(model, 16000)


# This code is adapted from https://pypi.org/project/noisereduce/
def record_background_noise(stream, frame_length, seconds=1):
    background_noise = b''
    for _ in range(0, int(16000 / frame_length * seconds)):
        background_noise += stream.read(frame_length)
    return np.frombuffer(background_noise, dtype=np.int16)


# The function `run_soundtriggerbox_vosk` initializes a Vosk model and
# Opens a PyAudio stream for real-time speech recognition.
# This code has been adapted from https://www.youtube.com/watch?v=3Mga7_8bYpw.
def run_soundtriggerbox_vosk():
    global running
    running = True
    model = Model(r"./vosk-model-small-en-us-0.15")
    recognizer = reset_recognizer(model)

    mic = pyaudio.PyAudio()

    frame_length = 960  # Update this value
    stream = mic.open(rate=16000, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=frame_length)
    stream.start_stream()

    # Record background noise
    background_noise = record_background_noise(stream, frame_length, seconds=1)

    debounce_time = 10.0  # Time in seconds to wait before processing the trigger
    last_trigger_time = None

    reset_interval = 60.0  # Time in seconds to reset the recognizer if no trigger detected
    last_reset_time = time.time()

    while running:
        data = stream.read(frame_length, exception_on_overflow=False)  # Update this value
        if len(data) == 0:
            break

        audio_data = np.frombuffer(data, dtype=np.int16)

        # Apply noise reduction using noisereduce
        # This code is adapted from https://pypi.org/project/noisereduce/
        audio_data_denoised = nr.reduce_noise(y=audio_data, y_noise=background_noise, sr=16000)

        # Transcribe audio data to text
        # This code is adapted from https://github.com/alphacep/vosk-api/blob/master/python/example/test_gradio.py
        recognizer.AcceptWaveform(audio_data_denoised.tobytes())
        text = recognizer.PartialResult()
        result_json = json.loads(text)
        text = result_json.get("partial", "")
        print(result_json)
        print(text)

        signal = soundtrigger.SoundDetection(text)

        current_time = time.time()
        if signal != 0:
            # stop the program
            if signal == 2:
                stop_sound_trigger()
                return

            if last_trigger_time is None or current_time - last_trigger_time >= debounce_time:
                last_trigger_time = current_time

                soundtrigger.SoundTriggering(signal)
                recognizer = reset_recognizer(model)  # Reset the recognizer after triggering
                last_reset_time = current_time
        elif current_time - last_reset_time >= reset_interval:
            recognizer = reset_recognizer(model)  # Reset the recognizer after the reset_interval
            last_reset_time = current_time


def stop_sound_trigger():
    global running
    print("Program stopped")
    running = False
