import numpy as np

def sigmoid(value):
    return 1 / (1 + np.exp(-value))

class IA:
    def __init__(self, internal_id):
        self.id = internal_id
        self.weights = np.random.uniform(low=-1.0, high=1.0, size=2)
        self.bias = 0.0

    @classmethod
    def from_ia(cls, other):
        weight_offset = np.random.uniform(low=-0.1, high=0.1, size=2)
        weights = other.weights.copy()
        for (i, weight) in enumerate(weights):
            weights[i] = weight + weight_offset[i]
        return cls(other.id, weights)

    def should_flap(self, bird_y, pipe_distance):
        pre_sig = self.bias + (bird_y * self.weights[0]) + (pipe_distance * self.weights[1])
        sig = sigmoid(pre_sig)
        # print(f"id: {self.id}, weights: {self.weights}, preSigmoid: {pre_sig}, sigmoid: {sig}")
        return sig > 0.5
