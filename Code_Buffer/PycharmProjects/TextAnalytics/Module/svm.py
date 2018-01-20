# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '18/10/2017 22:07'

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

classifier = svm.SVC(gamma=100, C=100)

print(len(digits.data))

x, y = digits.data[:-1], digits.target[:-1]

classifier.fit(x, y)

print('Prediction:', classifier.predict(digits.data[9]))

plt.imshow(digits.images[9], cmap=plt.cm.gray_r, interpolation='nearest')
# plt.show()
