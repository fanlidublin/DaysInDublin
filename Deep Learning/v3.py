# Simple neural network
# Fan Li, June 2nd
from numpy import *


class NeuralNetwork:
    def __init__(self):
        random.seed(1)
        self.weights = 2 * random.random((3, 1)) - 1

    def sigmoid(self, z):
        return 1 / (1 + exp(-z))

    def sigmoid_prime(self, z):
        return z * (1 - z)

    def train(self, inputs, outputs, iterations):
        for i in range(iterations):
            output = self.predict(inputs)
            error = outputs - output
            adjustment = dot(inputs.T, error * self.sigmoid_prime(output))
            self.weights += adjustment

    def predict(self, inputs):
        return self.sigmoid(dot(inputs, self.weights))


if __name__ == '__main__':
    neural_network = NeuralNetwork()

    print('Random starting weights:')
    print(neural_network.weights)

    training_set_i = array([[0, 0, 1], [1, 1, 1], [1, 0, 1], [0, 1, 1]])
    training_set_o = array([[0, 1, 1, 0]]).T

    neural_network.train(training_set_i, training_set_o, 10000)

    print('New weights after training:')
    print(neural_network.weights)

    print('Considering situation [1,0,0] -> :')
    print(neural_network.predict(array([1, 0, 0])))
