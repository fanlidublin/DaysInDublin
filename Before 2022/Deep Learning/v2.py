# Linear Regression with Gradient Descent from Scratch
# Fan Li, June 1st
from numpy import *


def run():
    data = genfromtxt('v2_data.csv', delimiter=',')
    # hyper-parameters: while it is too low, the model is slow to converage whereas if it's too high, the model will never converage
    learning_rate = 0.0001
    initial_b = 0
    initial_w = 0
    num_iterations = 1000
    [b, w] = gd_runner(data, initial_b, initial_w, learning_rate, num_iterations)
    print(b)
    print(w)


def gd_runner(data, starting_b, starting_w, learning_rate, num_iterations):
    b = starting_b
    w = starting_w

    for i in range(num_iterations):
        b, w = step_gradient(b, w, array(data), learning_rate)
    return [b, w]


def step_gradient(b_current, w_current, data, learning_rate):
    b_gradient = 0
    w_gradient = 0
    N = float(len(data))
    for i in range(0, len(data)):
        x = data[i, 0]
        y = data[i, 1]
        b_gradient += -(2 / N) * (y - (w_current * x) + b_current)
        w_gradient += -(2 / N) * x * (y - (w_current * x) + b_current)
    new_b = b_current - learning_rate * b_gradient
    new_w = w_current - learning_rate * w_gradient
    return [new_b, new_w]


def compute_error(b, w, data):
    total_error = 0
    for i in range(0, len(data)):
        x = data[i, 0]
        y = data[i, 1]
        total_error += (y - (w * x + b)) ** 2
    return total_error / float(len(data))


if __name__ == '__main__':
    run()
