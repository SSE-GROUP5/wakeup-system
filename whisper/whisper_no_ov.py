import whisper
import time
import os
import psutil

# For windows users only
ffmpeg_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
os.environ['PATH'] += os.pathsep + ffmpeg_path

model = whisper.load_model("base")
print("Transcription started")
start_time = time.time()  # Start time for inference
cpu_before = psutil.cpu_percent(interval=None)
result = model.transcribe("audio.mov")
print(result["text"])
# End measuring the inference time and compute the resources used
inference_time = time.time() - start_time
cpu_after = psutil.cpu_percent(interval=None)
# Printing the performance metrics
print(f"Inference Time: {inference_time:.2f} seconds")
print(f"CPU Usage Increase: {cpu_after - cpu_before:.2f}%")
