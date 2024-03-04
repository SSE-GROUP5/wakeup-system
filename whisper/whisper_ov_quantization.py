import whisper
from pathlib import Path
import torch
import openvino as ov
from typing import Optional, Tuple
from functools import partial
from utils import patch_whisper_for_ov_inference, OpenVINOAudioEncoder, OpenVINOTextDecoder, get_audio
import time
import os
import ipywidgets as widgets
import psutil
from contextlib import contextmanager
from datasets import load_dataset
from tqdm.notebook import tqdm
import nncf
from openvino.runtime import serialize
from openvino import Core


# For windows users only
ffmpeg_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
os.environ['PATH'] += os.pathsep + ffmpeg_path
def get_model_id(model_path):
    return model_path.name.replace("whisper_", "").replace("encoder.xml", "").replace("_", "")

model_list = [get_model_id(model_path) for model_path in Path('.').glob("whisper_*encoder.xml")]
model_list = [model_name for model_name in model_list if model_name]

core = Core()

task = "transcribe"
model_id = "base"
device = "CPU"

WHISPER_ENCODER_OV = Path(f"whisper_{model_id}_encoder.xml")
WHISPER_DECODER_OV = Path(f"whisper_{model_id}_decoder.xml")

WHISPER_ENCODER_OV_INT8 = Path(f"whisper_{model_id}_encoder_int8.xml")
WHISPER_DECODER_OV_INT8 = Path(f"whisper_{model_id}_decoder_int8.xml")

# model_fp32 = whisper.load_model(model_id, "cpu").eval()
# patch_whisper_for_ov_inference(model_fp32)

# model_fp32.encoder = OpenVINOAudioEncoder(core, WHISPER_ENCODER_OV, device=device)
# model_fp32.decoder = OpenVINOTextDecoder(core, WHISPER_DECODER_OV, device=device)

# COLLECT_CALIBRATION_DATA = False
# encoder_calibration_data = []
# decoder_calibration_data = []

# @contextmanager
# def calibration_data_collection():
#     global COLLECT_CALIBRATION_DATA
#     try:
#         COLLECT_CALIBRATION_DATA = True
#         yield
#     finally:
#         COLLECT_CALIBRATION_DATA = False


# def encoder_forward(self, mel: torch.Tensor):
#     if COLLECT_CALIBRATION_DATA:
#         encoder_calibration_data.append(mel)
#     return torch.from_numpy(self.compiled_model(mel)[self.output_blob])

# def decoder_forward(self, x: torch.Tensor, xa: torch.Tensor, kv_cache: Optional[dict] = None):
#     feed_dict = {'x': ov.Tensor(x.numpy()), 'xa': ov.Tensor(xa.numpy())}
#     feed_dict = (self.preprocess_kv_cache_inputs(feed_dict, kv_cache))
#     if COLLECT_CALIBRATION_DATA:
#         decoder_calibration_data.append(feed_dict)
#     res = self.compiled_model(feed_dict)
#     return self.postprocess_outputs(res)

# model_fp32.encoder.forward = partial(encoder_forward, model_fp32.encoder)
# model_fp32.decoder.forward = partial(decoder_forward, model_fp32.decoder)

# CALIBRATION_DATASET_SIZE = 30

# calibration_dataset = load_dataset("librispeech_asr", "clean", split="validation", streaming=True).take(CALIBRATION_DATASET_SIZE)

# with calibration_data_collection():
#     for data_item in tqdm(calibration_dataset, desc="Collecting calibration data", total=CALIBRATION_DATASET_SIZE):
#         model_fp32.transcribe(data_item["audio"]["array"].astype("float32"), task=task)

# print("Quantizing encoder...")
# quantized_encoder = nncf.quantize(
#     model=model_fp32.encoder.model,
#     calibration_dataset=nncf.Dataset(encoder_calibration_data),
#     subset_size=len(encoder_calibration_data),
#     model_type=nncf.ModelType.TRANSFORMER,
#     advanced_parameters=nncf.AdvancedQuantizationParameters(
#         smooth_quant_alpha=0.5      # Smooth Quant algorithm reduces activation quantization error; optimal alpha value was obtained through grid search
#     )
# )
# serialize(quantized_encoder, WHISPER_ENCODER_OV_INT8)
# print(f"Saved quantized encoder at ./{WHISPER_ENCODER_OV_INT8}")

# print("Quantizing decoder...")
# quantized_decoder = nncf.quantize(
#     model=model_fp32.decoder.model,
#     calibration_dataset=nncf.Dataset(decoder_calibration_data),
#     subset_size=len(decoder_calibration_data),
#     model_type=nncf.ModelType.TRANSFORMER,
#     advanced_parameters=nncf.AdvancedQuantizationParameters(
#         smooth_quant_alpha=0.95     # Smooth Quant algorithm reduces activation quantization error; optimal alpha value was obtained through grid search
#     )
# )
# serialize(quantized_decoder, WHISPER_DECODER_OV_INT8)
# print(f"Saved quantized decoder at ./{WHISPER_DECODER_OV_INT8}")

model_int8 = whisper.load_model(model_id, device="cpu").eval()
patch_whisper_for_ov_inference(model_int8)

model_int8.encoder = OpenVINOAudioEncoder(core, WHISPER_ENCODER_OV_INT8, device=device)
model_int8.decoder = OpenVINOTextDecoder(core, WHISPER_DECODER_OV_INT8, device=device)

print("Transcription started")
start_time = time.time()  # Start time for inference
cpu_before = psutil.cpu_percent(interval=None)
print(f"CPU Usage Before: {cpu_before:.2f}%")
result = model_int8.transcribe("audio.mov", task=task)
print(result["text"])
# End measuring the inference time and compute the resources used
inference_time = time.time() - start_time
cpu_after = psutil.cpu_percent(interval=None)
print(f"CPU Usage After: {cpu_after:.2f}%")
# Printing the performance metrics
print(f"Inference Time: {inference_time:.2f} seconds")
print(f"CPU Usage Increase: {cpu_after - cpu_before:.2f}%")
