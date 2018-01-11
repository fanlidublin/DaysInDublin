# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '07/10/2017 13:14'

from nltk.corpus import stopwords
import numpy as np
from scipy.stats import entropy


def entropy1(labels, base=None):
    value, counts = np.unique(labels, return_counts=True)
    return entropy(counts, base=base)


text = open('/Users/fan/Desktop/spam.txt')
rawtext = text.read()
stop = stopwords.words('english')
corpus = [i for i in rawtext.split() if i not in stop]
entropy_num = entropy1(corpus)
print(entropy_num)
