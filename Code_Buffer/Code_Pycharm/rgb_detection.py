# _*_ encoding:utf-8 _*_

__author__ = 'lifan'
__date__ = '15/10/2017 17:35'

import numpy as np
from skimage import data
from scipy import misc
import matplotlib.pyplot as plt

photo_data = misc.imread('./fan.JPG')
print(type(photo_data))
plt.figure(figsize=(15, 15))
plt.imshow(photo_data)

print(photo_data)
