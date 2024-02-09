import whisper
from pathlib import Path
import torch
import openvino as ov
from typing import Optional, Tuple
from functools import partial
from utils import patch_whisper_for_ov_inference, OpenVINOAudioEncoder, OpenVINOTextDecoder
import time
import os
import ipywidgets as widgets

ffmpeg_path = r"C:\Program Files\ffmpeg-master-latest-win64-gpl\bin"
os.environ['PATH'] += os.pathsep + ffmpeg_path
WHISPER_ENCODER_OV = Path(f"whisper_base_encoder.xml")
WHISPER_DECODER_OV = Path(f"whisper_base_decoder.xml")

start_time = time.time()

model_id = "base"
model = whisper.load_model("base")
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

device = widgets.Dropdown(
    options=core.available_devices + ["AUTO"],
    value='AUTO',
    description='Device:',
    disabled=False,
)

patch_whisper_for_ov_inference(model)

model.encoder = OpenVINOAudioEncoder(core, WHISPER_ENCODER_OV, device=device.value)
model.decoder = OpenVINOTextDecoder(core, WHISPER_DECODER_OV, device=device.value)
print("Transcription started")
result = model.transcribe("audio.mp3")
print(result["text"])
print("OpenVINO Execution Time: {:.2f} seconds".format(time.time() - start_time))
