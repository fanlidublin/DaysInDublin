# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '16/10/2017 19:23'

from sklearn import datasets
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt

model = linear_model.LinearRegression()  # select the models
# Loading and segmenting target data sets
boston = datasets.load_boston()
y = boston.target
# cross validation
predicted = cross_val_predict(model, boston.data, y, cv=10)

fig, ax = plt.subplots()
ax.scatter(y, predicted, edgecolors='black')
ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()
