from ultralytics import YOLO

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, help='name of the benchmark model')
args = parser.parse_args()

model_name = args.model

# Download the model
model = YOLO(f'{model_name}.pt')  

# Export the OV model
model.export(format='openvino')  # creates 'yolov8n_openvino_model/'

