import whisper
import time
import os

# For windows users only
#ffmpeg_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
#os.environ['PATH'] += os.pathsep + ffmpeg_path

start_time = time.time()

model = whisper.load_model("base")
result = model.transcribe("audio.mov")
print(result["text"])
print("Regular Execution Time: {:.2f} seconds".format(time.time() - start_time))
