import numpy as np

def sigmoid(value):
    return 1 / (1 + np.exp(-value))

base_variance = 0.1
max_generation = 10

class IA:
    def __init__(self, internal_id, weights = [], generation = 0):
        self.id = internal_id
        if len(weights) == 0:
            self.weights = np.random.uniform(low=-1.0, high=1.0, size=4)
        else:
            self.weights = weights
        self.bias = 0.0
        self.generation = min(generation, max_generation)

    @classmethod
    def from_ia(cls, other):
        variance = base_variance * (0.95 ** min((other.generation + 1), max_generation))
        weight_offset = np.random.uniform(low=-variance, high=variance, size=4)
        weights = other.weights.copy()
        for (i, weight) in enumerate(weights):
            weights[i] = weight + weight_offset[i]
        return cls(other.id, weights, other.generation + 1)

    def should_flap(self, bird_y, pipe_x, pike_top_y, pike_bottom_y):
        pre_sig = self.bias + (bird_y * self.weights[0]) + (pipe_x * self.weights[1]) + (pike_top_y * self.weights[2]) + (pike_bottom_y * self.weights[3])
        sig = sigmoid(pre_sig)
        # print(f"id: {self.id}, weights: {self.weights}, preSigmoid: {pre_sig}, sigmoid: {sig}")
        return sig > 0.5
