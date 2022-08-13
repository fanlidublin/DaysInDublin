# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '25/10/2017 14:32'

# Taken from https://datasciencelab.wordpress.com/2013/12/12/clustering-with-k-means-in-python/
# Just added plotting for 3-k cases

import numpy as np
import random
import matplotlib.pyplot as plt


def init_board(N):
    X = np.array([(random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(N)])
    return X


def cluster_points(X, mu):
    clusters = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm(x - mu[i[0]]))
                         for i in enumerate(mu)], key=lambda t: t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters


def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis=0))
    return newmu


def has_converged(mu, oldmu):
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))


def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(X, K)
    mu = random.sample(X, K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        cls = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, cls)
    return (mu, cls)


def change_coords(array):
    return list(map(list, zip(*array)))


def parse_output(data):
    clusters = data[1]
    points1 = change_coords(clusters[0])
    plt.plot(points1[0], points1[1], 'ro')
    points2 = change_coords(clusters[1])
    plt.plot(points2[0], points2[1], 'g^')
    points3 = change_coords(clusters[2])
    plt.plot(points3[0], points3[1], 'ys')
    centroids = change_coords(data[0])
    plt.plot(centroids[0], centroids[1], 'kx')
    plt.axis([-1.0, 1, -1.0, 1])
    plt.show()


# data = init_board(15)
data = np.array([[-0.5, 0.5],
                 [-0.3, 0.23],
                 [-0.45, 0.25],
                 [-0.39, 0.52],
                 [-0.43, 0.47],
                 [-0.71, 0.42],
                 [-0.75, -0.12],
                 [-0.5, -0.5],
                 [-0.75, -0.5],
                 [0.46, -0.81],
                 [0.72, -0.76],
                 [0.24, -0.62],
                 [0.42, -0.32],
                 [0.47, -0.64],
                 [-0.65, -0.26]])
print(data)
print(type(data))
out = find_centers(list(data), 3)
parse_output(out)
