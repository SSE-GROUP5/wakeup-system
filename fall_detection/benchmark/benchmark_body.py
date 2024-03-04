import numpy as np


class Benchmark_body:
    def __init__(self):
        self.prepoceesed_data = []
        self.inference_data = []
        self.postprocessed_data = []

    def append_time(self, preprocessed, inference, postprocessed):
        self.prepoceesed_data.append(preprocessed)
        self.inference_data.append(inference)
        self.postprocessed_data.append(postprocessed)

    def get_average_time(self):
        return np.mean(self.prepoceesed_data), np.mean(self.inference_data), np.mean(self.postprocessed_data)
    
    def get_std_deviation(self):
        return np.std(self.prepoceesed_data), np.std(self.inference_data), np.std(self.postprocessed_data)