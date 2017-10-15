# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '15/10/2017 20:03'

import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from sklearn.cluster import KMeans

style.use('ggplot')

X = np.array([[1, 2],
              [1.5, 1.8],
              [5, 8],
              [8, 8],
              [1, 0.6],
              [9, 11]])

# plt.scatter(X[:, 0], X[:, 1], s=150, linewidths=5, zorder=10)
# plt.show()

clf = KMeans(n_clusters=3)
clf.fit(X)

centroids = clf.cluster_centers_
labels = clf.labels_

colors = 10*['g.', 'r.', 'c.', 'b.', 'k.']

for i in range(len(X)):
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=25)
plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=150, linewidths=5)
plt.show()
