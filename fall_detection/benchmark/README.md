### Andy's Vision Benchmark: Upper Body Fall Detection with Yolo and Openvino

Andy's Vision Benchmark is designed to assess the performance of upper body fall detection triggers using Yolo, enhanced with the performance boost provided by Openvino. This benchmark evaluates both live and offline performance, with a focus on runtime efficiency.

## Benchmark Process Overview
# Live Benchmark

- Requirement: Presence in front of the camera is necessary during the live benchmark process.
- Duration: Depending on your CPU's performance, the process could take between 10 to 30 minutes in total.

# Offline Benchmark
- Dataset: Utilises the COCO 2017 dataset for validation.
- Procedure: The script automatically downloads and unzips the dataset for you.
- Duration: Total time may vary from 10 to 30 minutes, depending on CPU performance.


All statistics gathered from the benchmark will be saved to `output.txt`.

## Setup Instructions
# Prerequisites

Ensure Python is installed on your system. The required Python version differs by operating system:
- Linux: Python 3.12
- Windows: Python 3.8

## Running the Benchmark
# Linux 

Execute the benchmark script by running:

```
bash benchmark.sh
```

# Windows
Execute the benchmark script by running:

```
benchmark.bat
```