import os
from benchmark_body import Benchmark_body
from tqdm import tqdm
from ultralytics import YOLO
import matplotlib.pyplot as plt


def offline_benchmark(dataset_path: str, model_name: str, if_openvino: bool):
    # Load a model
    model = YOLO(f"{model_name}.pt")  # pretrained YOLOv8n model
    benchmark_data_dict = Benchmark_body()

    if (if_openvino):
        # Export the model
        model.export(format='openvino')  # creates 'yolov8n_openvino_model/'

        # Load the exported OpenVINO model
        model = YOLO(f'{model_name}_openvino_model/')
        
    for root, dirs, files in os.walk(dataset_path):
        for file in tqdm(files):
            file_path = os.path.join(root, file)
            # print(file_path)

            results = model(file_path, verbose = False,device = 'cpu')  # return a list of Results objects
            benchmark_data_dict.append_time(results[0].speed['preprocess'], results[0].speed['inference'], results[0].speed['postprocess'])

    print(f"Average time for preprocessed data: {benchmark_data_dict.get_average_time()[0]} with standard deviation: {benchmark_data_dict.get_std_deviation()[0]}")
    print(f"Average time for inference data: {benchmark_data_dict.get_average_time()[1]} with standard deviation: {benchmark_data_dict.get_std_deviation()[1]}")
    print(f"Average time for postprocessed data: {benchmark_data_dict.get_average_time()[2]} with standard deviation: {benchmark_data_dict.get_std_deviation()[2]}")

    return benchmark_data_dict.get_average_time(), benchmark_data_dict.get_std_deviation()


def plot_average_time_with_std(labels, average_time, std_deviation, file_name='average_time_with_std', stage = 'inference'):
    x = range(len(labels))
    plt.bar(x, average_time, yerr=std_deviation, align='center', alpha=0.5, capsize=5)
    plt.xticks(x, labels)
    plt.xlabel('Model')
    plt.ylabel('Time (ms)')
    plt.title(f'Average {stage} Time with Standard Deviation')
    plt.savefig(f'{file_name}_{stage}.png')
    plt.show()
    plt.clf()


if __name__ == '__main__':

    dataset_path = '/home/diantu/Documents/wakeup-system/fall_detection/other_examples/val2017'
    model_name = 'yolov8n-pose'
    yolo_avg_time, yolo_std_time = offline_benchmark(dataset_path, model_name, False)
    ov_avg_time, ov_std_time = offline_benchmark(dataset_path, model_name, True)

    

    # Call the function with the desired data
    labels = ['YOLO', 'OpenVINO']
    inference_average_time = [yolo_avg_time[1], ov_avg_time[1]]
    inference_std_deviation = [yolo_std_time[1], ov_std_time[1]]
    plot_average_time_with_std(labels, inference_average_time, inference_std_deviation, stage='inference')

    preprocessing_average_time = [yolo_avg_time[0], ov_avg_time[0]]
    preprocessing_std_deviation = [yolo_std_time[0], ov_std_time[0]]
    plot_average_time_with_std(labels, preprocessing_average_time, preprocessing_std_deviation, stage='preprocessing')

    postprocessing_average_time = [yolo_avg_time[2], ov_avg_time[2]]
    postprocessing_std_deviation = [yolo_std_time[2], ov_std_time[2]]
    plot_average_time_with_std(labels, postprocessing_average_time, postprocessing_std_deviation, stage='postprocessing')