import sounddevice as sd
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import scipy.signal
import csv

# Load the YAMNet model
model = hub.load('https://tfhub.dev/google/yamnet/1')

def class_names_from_csv(class_map_csv_text):
    """Returns list of class names corresponding to score vector."""
    class_names = []
    with tf.io.gfile.GFile(class_map_csv_text) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            class_names.append(row['display_name'])
    return class_names

class_map_path = model.class_map_path().numpy()
class_names = class_names_from_csv(class_map_path)

def ensure_sample_rate(original_sample_rate, waveform, desired_sample_rate=16000):
    """Resample waveform if required."""
    if original_sample_rate != desired_sample_rate:
        desired_length = int(round(float(len(waveform)) / original_sample_rate * desired_sample_rate))
        waveform = scipy.signal.resample(waveform, desired_length)
    return desired_sample_rate, waveform

# Function to handle incoming audio frames and make predictions
def process_audio_frame(frame, sample_rate):
    frame = frame / np.iinfo(np.int16).max  # Normalize waveform
    frame = frame.astype(np.float32)
    # Ensure the sample rate is correct
    _, frame = ensure_sample_rate(sample_rate, frame)
    scores, embeddings, spectrogram = model(frame)
    class_scores = np.mean(scores, axis=0)
    top_class = np.argmax(class_scores)
    print(f"Detected sound: {class_names[top_class]}")

# Audio stream callback
def callback(indata, frames, time, status):
    if status:
        print(status)
    process_audio_frame(indata[:, 0], sample_rate=16000)

# Start streaming from microphone
with sd.InputStream(callback=callback, channels=1, samplerate=16000):
    print("Listening...")
    sd.sleep(10000)  # Keep listening for 10 seconds, change as needed
