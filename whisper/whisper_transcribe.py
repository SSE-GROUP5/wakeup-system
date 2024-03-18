import argparse
import sys
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
import re
import psutil
import time

from utils_wakeup_server import confirm_to_server, check_connection, send_signal, is_exe_file, update_env_vars
current_dir = os.path.dirname(os.path.realpath(__file__))
custom_modules_path = "./" if is_exe_file() else current_dir + "/../"
sys.path.append(custom_modules_path)
from zeromq.zmqServer import ZeroMQServer

# Function to check for repetitive sounds
def check_repetitive_sounds(text, config):
    ah_pattern = re.compile(r'(ah[\s,\.]*){3,}', re.IGNORECASE)  # Pattern to match "ah" repeated at least 3 times
    oh_pattern = re.compile(r'(oh[\s,\.]*){3,}', re.IGNORECASE)  # Pattern to match "oh" repeated at least 3 times
    uh_pattern = re.compile(r'(uh[\s,\.]*){3,}', re.IGNORECASE)  # Pattern to match "uh" repeated at least 3 times
    if ah_pattern.search(text) or uh_pattern.search(text):
        print("Detected repetitive 'ah' sound")
        send_signal("ah", config)
    if oh_pattern.search(text):
        print("Detected repetitive 'oh' sound")
        send_signal("oh", config)

def main():
	parser = argparse.ArgumentParser()
	from constants import config
	parser.add_argument("--model", default="base", help="Model to use",
						choices=["tiny", "base", "small", "medium", "large"])
	parser.add_argument("--non_english", action='store_true',
						help="Don't use the English model.")
	parser.add_argument("--energy_threshold", default=1000,
						help="Energy level for mic to detect.", type=int)
	parser.add_argument("--record_timeout", default=3,
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
			for index, name in enumerate(sr.Microphone.list_microphone_names()):
				if mic_name in name:
					source = sr.Microphone(sample_rate=16000, device_index=index)
					break
	else:
		source = sr.Microphone(sample_rate=16000, device_index=5)

	model = args.model
	if args.model != "large" and not args.non_english:
		model = model + ".en"
	audio_model = whisper.load_model(model)

	transcription = ['']
	total_inference_time = 0

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
	  
	print("Starting the transcriber...")
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

				result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
				text = result['text'].strip()

				# Performance metrics
				inference_time = time.time() - start_time
				total_inference_time += inference_time 
				# cpu_after = psutil.cpu_percent(interval=None)
				# memory_after = psutil.virtual_memory().percent

				# print(f"CPU Usage Increase: {cpu_after - cpu_before:.2f}%")
				# print(f"Memory Usage Increase: {memory_after - memory_before:.2f}%")

				# Check for repetitive sounds after each transcription
				check_repetitive_sounds(text, config)

				if text:  # If there's any transcription result
					if phrase_complete:
						transcription.append(text)
					else:
						transcription[-1] = text

					print(text)
				else:
					print("No transcription detected for the latest audio segment.")

				sleep(0.25)
				print(f"\nTotal Inference Time: {total_inference_time:.2f} seconds")
		except KeyboardInterrupt:
			print(f"\nTotal Inference Time: {total_inference_time:.2f} seconds")
			break


	print("\n\nTranscription:")
	for line in transcription:
		print(line)


if __name__ == "__main__":
	main()
