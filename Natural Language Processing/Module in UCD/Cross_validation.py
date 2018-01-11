# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '19/10/2017 16:28'

import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
import matplotlib.pyplot as plt

names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']
data = pd.read_csv('./iris.csv', header=None, names=names)

X = np.array(data.ix[:, 0:4])
y = np.array(data['class'])

k_range = range(1, 21)
cv_scores = []

for k in k_range:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X, y, cv=5, scoring='accuracy')
    cv_scores.append(scores.mean())

plt.plot(k_range, cv_scores)
plt.xlabel('Number of Neighbors K')
plt.ylabel('accuracy')
plt.show()
