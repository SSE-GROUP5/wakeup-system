@echo off
REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install requirements
REM TODO: Add requirements.txt
echo Installing dependencies...
pip install -r requirement_windows.txt

REM Clean up previous output
if exist output.txt del /f output.txt
echo. > output.txt

@REM REM Download the model and export OV model
@REM python setupEnv.py --model yolov8n-pose 

REM Live benchmark
echo Start live benchmark, please start dancing in front of the camera!
echo Live benchmark for yolov8n
python live_benchmark.py --model yolo --model_name yolov8n-pose
echo.
echo.
echo start live benchmark for OV
python live_benchmark.py --model ov --model_name yolov8n-pose
echo.
echo.

REM Offline benchmark
echo Start offline benchmark

REM Check if the file "val2017.zip" exists, download it if it doesn't exist
if not exist "val2017.zip" (
    echo Downloading val2017.zip...
    powershell -Command "Invoke-WebRequest http://images.cocodataset.org/zips/val2017.zip -OutFile val2017.zip"
)

REM Check if the folder "val2017" exists, unzip the file "val2017.zip" if it doesn't exist
if not exist "val2017\" (
    echo Folder 'val2017' does not exist. Unzipping val2017.zip...
    powershell -Command "Expand-Archive -Path val2017.zip -DestinationPath ."
)

REM Run the offline benchmark
echo Starting offline benchmark
python offline_benchmark.py --dataset_path ./val2017 --model yolov8n-pose
echo.

echo End of benchmark. Results are saved in output.txt.
