# exec > output.txt 2>&1

# Path: fall_detection/benchmark/benchmark.sh

# create venv
echo 'create venv'
python3 -m venv benchmark
source benchmark/bin/activate

# install requirements
# TODO add requirements.txt
echo 'install dependencies'
pip install -r requirement.txt

rm -rf output.txt
touch output.txt

# download the model and export OV model
python setupEnv.py --model yolov8n-pose 

# live benchmark
echo 'start live benchmark, please start dancing in front of the camera!'

echo 'start live benchmark for YOLO'
python live_benchmark.py --model yolo --model_name yolov8n-pose
echo '   '
echo '   '

echo 'start live benchmark for OV'
python live_benchmark.py --model ov --model_name yolov8n-pose
echo '   '
echo '   '


# offline benchmark
echo 'start offline benchmark'

# Check if the file "val_2017.zip" exists, download it if it doesn't exist
if [ ! -f "val2017.zip" ]; then
    echo "Downloading val_2017.zip..."
    wget "http://images.cocodataset.org/zips/val2017.zip"
fi


# Check if the folder "2017_val" exists, unzip the file "val_2017.zip" if it doesn't exist
if [ ! -d "val2017" ]; then
    echo "Folder 'val2017' does not exist. Unzipping val_2017.zip..."
    unzip val2017.zip
fi

# Run the offline benchmark
echo 'start offline benchmark'
python offline_benchmark.py --dataset_path './val2017' --model yolov8n-pose
echo '   '

echo 'End of benchmark. Results are saved in output.txt.'






