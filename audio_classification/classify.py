# Copyright 2023 The MediaPipe Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Main scripts to run audio classification."""

import argparse
import time
import os
import sys
from dotenv import load_dotenv
from mediapipe.tasks import python
from mediapipe.tasks.python.audio.core import audio_record
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
def get_model_path():
	# Determine if we are running in a bundled environment and set the base path
	if getattr(sys, 'frozen', False):
		application_path = sys._MEIPASS
	else:
		application_path = os.path.dirname(os.path.abspath(__file__))

	# Join the base path with the model filename
	model_path = os.path.join(application_path, 'yamnet.tflite')
	return model_path

def get_current_path():
  if getattr(sys, 'frozen', False):
    return os.path.dirname(sys.executable)
  elif __file__:
    return os.path.dirname(__file__)

current_path = get_current_path()
env_path = os.path.join(current_path, '.env.wakeup')
load_dotenv(dotenv_path=env_path)

def run(model: str, max_results: int, score_threshold: float,
		overlapping_factor: float, gui_active: bool) -> None:
	"""Continuously run inference on audio data acquired from the device.

	Args:
		model: Name of the TFLite audio classification model.
		max_results: Maximum number of classification results to display.
		score_threshold: The score threshold of classification results.
		overlapping_factor: Target overlapping between adjacent inferences.
	"""    

	# Validate overlapping factor and score threshold values
	if (overlapping_factor <= 0) or (overlapping_factor >= 1.0):
		raise ValueError('Overlapping factor must be between 0 and 1.')

	if (score_threshold < 0) or (score_threshold > 1.0):
		raise ValueError('Score threshold must be between (inclusive) 0 and 1.')

	# List to store classification results
	classification_result_list = []
	# Initialize a plotter instance to display the classification results.

	# Callback function to save classification results
	def save_result(result: audio.AudioClassifierResult, timestamp_ms: int):
		result.timestamp_ms = timestamp_ms
		classification_result_list.append(result)

	# Initialize the audio classification model.
	model_file_path = get_model_path()  # Dynamically get the model file path
	base_options = python.BaseOptions(model_asset_path=model_file_path)
	options = audio.AudioClassifierOptions(
		base_options=base_options, running_mode=audio.RunningMode.AUDIO_STREAM,
		max_results=max_results, score_threshold=score_threshold,
		result_callback=save_result)
	classifier = audio.AudioClassifier.create_from_options(options)

	# Initialize the audio recorder and a tensor to store the audio input.
	# The sample rate may need to be changed to match your input device.
	# For example, an AT2020 requires sample_rate 44100.
	buffer_size, sample_rate, num_channels = 15600, 16000, 1
	audio_format = containers.AudioDataFormat(num_channels, sample_rate)
	record = audio_record.AudioRecord(num_channels, sample_rate, buffer_size)
	audio_data = containers.AudioData(buffer_size, audio_format)

	# We'll try to run inference every interval_between_inference seconds.
	# This is usually half of the model's input length to create an overlapping
	# between incoming audio segments to improve classification accuracy.
	input_length_in_second = float(len(audio_data.buffer)) / audio_data.audio_format.sample_rate
	interval_between_inference = input_length_in_second * (1 - overlapping_factor)
	pause_time = interval_between_inference * 0.1
	last_inference_time = time.time()

	# Initialize variables for debouncing mechanism
	last_detection_time = 0
	detection_interval = 1  # 1 second

	# Start the audio recording
	record.start_recording()

	# Main loop for continuous audio processing
	while True:
		now = time.time()
		diff = now - last_inference_time
		if diff < interval_between_inference:
			time.sleep(pause_time)
			continue
		last_inference_time = now

		# Load audio data and run classification
		data = record.read(buffer_size)
		audio_data.load_from_array(data)
		classifier.classify_async(audio_data, round(last_inference_time * 1000))

		# Process classification results
		if classification_result_list:
			# print(f'Classification results: {classification_result_list}')
			current_time = time.time()
			for result in classification_result_list:
				for classification in result.classifications:
					for category in classification.categories:
						# Check for specific events and apply debouncing
						if category.category_name == 'Finger snapping':
							if (current_time - last_detection_time) > detection_interval:
								print("Finger snapping detected.")
								last_detection_time = current_time
						# elif category.category_name == 'Clapping':
						# 	if (current_time - last_detection_time) > detection_interval:
						# 		print("Clapping detected.")
						# 		last_detection_time = current_time

					
			# Clear the results list for next iteration
			classification_result_list.clear()

def main():
	# Parse command-line arguments
	parser = argparse.ArgumentParser(
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument(
		'--model',
		help='Name of the audio classification model.',
		required=False,
		default='yamnet.tflite')
	parser.add_argument(
		'--maxResults',
		help='Maximum number of results to show.',
		required=False,
		default=5)
	parser.add_argument(
		'--overlappingFactor',
		help='Target overlapping between adjacent inferences. Value must be in (0, 1)',
		required=False,
		default=0.5)
	parser.add_argument(
		'--gui',
		help='Activate the GUI for displaying results.',
		action='store_true') 
	args = parser.parse_args()

	SCORE_THRESHOLD = 0  # Score threshold for classification results

	# Run the main function with the parsed arguments
	run(args.model, int(args.maxResults), float(SCORE_THRESHOLD), float(args.overlappingFactor), args.gui)

if __name__ == '__main__':	

  main()
