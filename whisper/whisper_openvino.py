# To convert mov to wav:
# ffmpeg -i audio.mov -ab 160k -ac 2 -ar 44100 -vn audio.wav

from pathlib import Path
from utils import preprocess_audio
from transformers import AutoProcessor,  AutoModelForSpeechSeq2Seq
from optimum.intel.openvino import OVModelForSpeechSeq2Seq
from transformers import pipeline
import time

# For windows users only
#ffmpeg_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
#os.environ['PATH'] += os.pathsep + ffmpeg_path


model_id = "openai/whisper-base"
model_path = Path(model_id.replace('/', '_'))

ov_config = {"CACHE_DIR": ""}
if not model_path.exists():
    ov_model = OVModelForSpeechSeq2Seq.from_pretrained(
        model_id, ov_config=ov_config, export=True, compile=False, load_in_8bit=False
    )
    ov_model.half()
    ov_model.save_pretrained(model_path)
else:
    ov_model = OVModelForSpeechSeq2Seq.from_pretrained(
        model_path, ov_config=ov_config, compile=False
    )

device = "AUTO"
ov_model.to(device)
ov_model.compile()

processor = AutoProcessor.from_pretrained(model_id)

pt_model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id)
pt_model.eval()

ov_model.generation_config = pt_model.generation_config

pipe = pipeline(
    "automatic-speech-recognition",
    model=ov_model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=15,
    batch_size=16,
)

input_audio_path = Path("audio.wav")
input_audio = preprocess_audio(input_audio_path)

start_time = time.time()
result = pipe(input_audio.copy(), return_timestamps=True)
end_time = time.time()
print(result['text'])
print("OpenVINO Execution Time: {:.2f} seconds, Device: {}".format(end_time - start_time, device))

