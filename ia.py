import numpy as np

def sigmoid(value):
    return 1 / (1 + np.exp(-value))

class IA:
    def __init__(self, internal_id):
        self.id = internal_id
        self.weights = np.random.uniform(low=-1.0, high=1.0, size=2)
        self.bias = 0.0

    def should_flap(self, bird_y, pipe_distance):
        pre_sig = self.bias + (bird_y * self.weights[0]) + (pipe_distance * self.weights[1])
        sig = sigmoid(pre_sig)
       # print(f"id: {self.id}, weights: {self.weights}, preSigmoid: {pre_sig}, sigmoid: {sig}")
        return sig > 0.5
