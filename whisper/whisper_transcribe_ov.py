import argparse
import os
import sys
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
import re

import whisper
from pathlib import Path
import openvino as ov
from typing import Optional, Tuple
from functools import partial
from utils import patch_whisper_for_ov_inference, OpenVINOAudioEncoder, OpenVINOTextDecoder
import psutil
import time

from constants import config
from utils_wakeup_server import confirm_to_server, check_connection, send_signal, is_exe_file, update_env_vars
current_dir = os.path.dirname(os.path.realpath(__file__))
custom_modules_path = "./" if is_exe_file() else current_dir + "/../"
sys.path.append(custom_modules_path)
from zeromq.zmqServer import ZeroMQServer


# Function to check for repetitive sounds
def check_repetitive_sounds(text):
    ah_pattern = re.compile(r'(ah[\s,\.]*){3,}', re.IGNORECASE)  # Pattern to match "ah" repeated at least 3 times
    oh_pattern = re.compile(r'(oh[\s,\.]*){3,}', re.IGNORECASE)  # Pattern to match "oh" repeated at least 3 times
    
    if ah_pattern.search(text):
        print("Detected repetitive 'ah' sound")
        send_signal(config, "ah")
    if oh_pattern.search(text):
        print("Detected repetitive 'oh' sound")
        send_signal(config, "oh")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="base", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the English model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=2,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()

    phrase_time = None
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    recorder.dynamic_energy_threshold = False

    if 'linux' in platform:
        mic_name = args.default_microphone
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return
        else:
            source = None
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    source = sr.Microphone(sample_rate=16000, device_index=index)
                    break
            if source is None:
                print(f"Microphone {mic_name} not found.")
                return
    else:
        source = sr.Microphone(sample_rate=16000)


    # For windows users only
    ffmpeg_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
    os.environ['PATH'] += os.pathsep + ffmpeg_path
    WHISPER_ENCODER_OV = Path(f"whisper_base_encoder.xml")
    WHISPER_DECODER_OV = Path(f"whisper_base_decoder.xml")

    model_id = args.model
    if args.model != "large" and not args.non_english:
        model_id = model_id + ".en"
    model = whisper.load_model(model_id)
    model.to("cpu")
    model.eval()

    mel = torch.zeros((1, 80 if 'v3' not in "base" else 128, 3000))
    audio_features = model.encoder(mel)
    if not WHISPER_ENCODER_OV.exists():
        encoder_model = ov.convert_model(model.encoder, example_input=mel)
        ov.save_model(encoder_model, WHISPER_ENCODER_OV)

    def attention_forward(
        attention_module,
        x: torch.Tensor,
        xa: Optional[torch.Tensor] = None,
        mask: Optional[torch.Tensor] = None,
        kv_cache: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
    ):
        """
        Override for forward method of decoder attention module with storing cache values explicitly.
        Parameters:
        attention_module: current attention module
        x: input token ids.
        xa: input audio features (Optional).
        mask: mask for applying attention (Optional).
        kv_cache: dictionary with cached key values for attention modules.
        idx: idx for search in kv_cache.
        Returns:
        attention module output tensor
        updated kv_cache
        """
        q = attention_module.query(x)

        if xa is None:
            # hooks, if installed (i.e. kv_cache is not None), will prepend the cached kv tensors;
            # otherwise, perform key/value projections for self- or cross-attention as usual.
            k = attention_module.key(x)
            v = attention_module.value(x)
            if kv_cache is not None:
                k = torch.cat((kv_cache[0], k), dim=1)
                v = torch.cat((kv_cache[1], v), dim=1)
            kv_cache_new = (k, v)
        else:
            # for cross-attention, calculate keys and values once and reuse in subsequent calls.
            k = attention_module.key(xa)
            v = attention_module.value(xa)
            kv_cache_new = (None, None)

        wv, qk = attention_module.qkv_attention(q, k, v, mask)
        return attention_module.out(wv), kv_cache_new


    def block_forward(
        residual_block,
        x: torch.Tensor,
        xa: Optional[torch.Tensor] = None,
        mask: Optional[torch.Tensor] = None,
        kv_cache: Optional[Tuple[torch.Tensor, torch.Tensor]] = None,
    ):
        """
        Override for residual block forward method for providing kv_cache to attention module.
        Parameters:
            residual_block: current residual block.
            x: input token_ids.
            xa: input audio features (Optional).
            mask: attention mask (Optional).
            kv_cache: cache for storing attention key values.
        Returns:
            x: residual block output
            kv_cache: updated kv_cache

        """
        x0, kv_cache = residual_block.attn(residual_block.attn_ln(
            x), mask=mask, kv_cache=kv_cache)
        x = x + x0
        if residual_block.cross_attn:
            x1, _ = residual_block.cross_attn(
                residual_block.cross_attn_ln(x), xa)
            x = x + x1
        x = x + residual_block.mlp(residual_block.mlp_ln(x))
        return x, kv_cache



    # update forward functions
    for idx, block in enumerate(model.decoder.blocks):
        block.forward = partial(block_forward, block)
        block.attn.forward = partial(attention_forward, block.attn)
        if block.cross_attn:
            block.cross_attn.forward = partial(attention_forward, block.cross_attn)


    def decoder_forward(decoder, x: torch.Tensor, xa: torch.Tensor, kv_cache: Optional[Tuple[Tuple[torch.Tensor, torch.Tensor]]] = None):
        """
        Override for decoder forward method.
        Parameters:
        x: torch.LongTensor, shape = (batch_size, <= n_ctx) the text tokens
        xa: torch.Tensor, shape = (batch_size, n_mels, n_audio_ctx)
            the encoded audio features to be attended on
        kv_cache: Dict[str, torch.Tensor], attention modules hidden states cache from previous steps 
        """
        if kv_cache is not None:
            offset = kv_cache[0][0].shape[1]
        else:
            offset = 0
            kv_cache = [None for _ in range(len(decoder.blocks))]
        x = decoder.token_embedding(
            x) + decoder.positional_embedding[offset: offset + x.shape[-1]]
        x = x.to(xa.dtype)
        kv_cache_upd = []

        for block, kv_block_cache in zip(decoder.blocks, kv_cache):
            x, kv_block_cache_upd = block(x, xa, mask=decoder.mask, kv_cache=kv_block_cache)
            kv_cache_upd.append(tuple(kv_block_cache_upd))

        x = decoder.ln(x)
        logits = (
            x @ torch.transpose(decoder.token_embedding.weight.to(x.dtype), 1, 0)).float()

        return logits, tuple(kv_cache_upd)

    # override decoder forward
    model.decoder.forward = partial(decoder_forward, model.decoder)

    tokens = torch.ones((5, 3), dtype=torch.int64)
    logits, kv_cache = model.decoder(tokens, audio_features, kv_cache=None)

    tokens = torch.ones((5, 1), dtype=torch.int64)

    if not WHISPER_DECODER_OV.exists():
        decoder_model = ov.convert_model(model.decoder, example_input=(tokens, audio_features, kv_cache))
        ov.save_model(decoder_model, WHISPER_DECODER_OV)

    core = ov.Core()

    patch_whisper_for_ov_inference(model)

    model.encoder = OpenVINOAudioEncoder(core, WHISPER_ENCODER_OV, device='CPU')
    model.decoder = OpenVINOTextDecoder(core, WHISPER_DECODER_OV, device='CPU')


    transcription = ['']

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        start_time = time.time()  # Start time for inference
        cpu_before = psutil.cpu_percent(interval=None)
        memory_before = psutil.virtual_memory().percent

        data = audio.get_raw_data()
        data_queue.put((data, start_time, cpu_before, memory_before))


    recorder.listen_in_background(source, record_callback, phrase_time_limit=args.record_timeout)

    print("Model loaded.\n")

    # Check wakeup server
    is_wakeup_server_connected = check_connection(config)
    if is_wakeup_server_connected:
        confirm_to_server(config)

    zmqServer = ZeroMQServer("tcp://*:5556")
    while True:
      
        message = zmqServer.receive()
        if message != None:
            topic, msg = message
            if topic == config["ID"]:
                config = update_env_vars(config, msg)
      
      
        try:
            now = datetime.utcnow()
            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=args.phrase_timeout):
                    phrase_complete = True
                phrase_time = now
                
                audio_data, start_time, cpu_before, memory_before = data_queue.get()  # Adjusted to unpack performance metrics
                
                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                # Start measuring the inference time
                result = model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                # End measuring the inference time and compute the resources used
                inference_time = time.time() - start_time
                cpu_after = psutil.cpu_percent(interval=None)
                memory_after = psutil.virtual_memory().percent

                # Printing the performance metrics
                # print(f"Inference Time: {inference_time:.2f} seconds")
                # print(f"CPU Usage Increase: {cpu_after - cpu_before:.2f}%")
                # print(f"Memory Usage Increase: {memory_after - memory_before:.2f}%")

                # Check for repetitive sounds after each transcription
                check_repetitive_sounds(text)

                if text:  # If there's any transcription result
                    if phrase_complete:
                        transcription.append(text)
                    else:
                        transcription[-1] = text

                    print(text)
                else:
                    print("No transcription detected for the latest audio segment.")

                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcription:
        print(line)


if __name__ == "__main__":
    main()
