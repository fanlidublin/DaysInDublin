# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '23/01/2018 19:19'

import numpy as np
from sklearn.datasets.samples_generator import make_regression
from scipy import stats


def gradient_descent(alpha, x, y, ep=0.0001, max_iter=10000):
    converged = False
    iteration = 0
    m = x.shape[0]  # number of samples

    beta0 = np.random.random(x.shape[1])
    beta1 = np.random.random(x.shape[1])

    J = sum([(beta0 + beta1 * x[i] - y[i]) ** 2 for i in range(m)])

    while not converged:
        grad0 = 1.0 / m * sum([(beta0 + beta1 * x[i] - y[i]) for i in range(m)])
        grad1 = 1.0 / m * sum([(beta0 + beta1 * x[i] - y[i]) * x[i] for i in range(m)])

        beta0 = beta0 - alpha * grad0
        beta1 = beta1 - alpha * grad1

        mean_square_err = sum([(beta0 + beta1 * x[i] - y[i]) ** 2 for i in range(m)])

        # 若上一次的error与这次的error之间的距离相差在预定值范围内，则是一个满足的停止条件
        if abs(J - mean_square_err) <= ep:
            print("Converged iterations {}".format(iteration))
            converged = True

        J = mean_square_err
        iteration += 1

        if iteration == max_iter:
            print("Max iteration.")
            converged = True

    return beta0, beta1


if __name__ == '__main__':
    x, y = make_regression(n_samples=100, n_features=1, n_informative=1, random_state=0, noise=35)
    print("x.shape={}, y.shape={}".format(x.shape, y.shape))

    beta0, beta1 = gradient_descent(0.01, x, y, 0.01, max_iter=1000)
    print('beta0 = {}, beta1 = {}'.format(beta0, beta1))

    # check the answer from our algorithm with scipy stat package
    slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x[:, 0], y)
    print('intercept = {}, slope = {}'.format(intercept, slope))
