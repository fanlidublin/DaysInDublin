# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '07/10/2017 00:21'


from nltk.corpus import stopwords
from collections import Counter
from math import log

stop = stopwords.words('english')
text = open('/Users/fan/Desktop/pra4.txt')
rawtext = text.read()
# get the 10-doc corpus (stopwords removed)
corpus = [i for i in rawtext.split() if i not in stop]
# the number of words in the whole corpus
N = len(corpus)
# get the adjacent pairs
pairs = [[corpus[i], corpus[i + 1]] for i in range(N - 1)]

for [w1, w2] in pairs:
    num_w1_w2 = pairs.count([w1, w2])
    num_w1 = Counter(corpus)[w1]
    num_w2 = Counter(corpus)[w2]
    # to do a frequency cut-off
    if num_w1 > 1:
        # to calculate the pmi
        pmi = log(num_w1_w2, 2) + log(N, 2) - log(num_w1, 2) - log(num_w2, 2)
        print([w1, w2], pmi)
