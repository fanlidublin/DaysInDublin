# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '06/10/2017 22:47'
import nltk
from nltk.corpus import brown
from math import log
from nltk.corpus import stopwords
from nltk.collocations import *
from nltk.collocations import BigramAssocMeasures

stop = stopwords.words('english')
text = open('/Users/fan/Desktop/pra4.txt')
rawtext = text.read()
a = [i for i in rawtext.split() if i not in stop]
b = " ".join(a)

finder = BigramCollocationFinder.from_words(b.split(), window_size=2)
finder1 = BigramCollocationFinder.from_words(b.split(), window_size=2)

bigram_measures = BigramAssocMeasures()
finder.score_ngrams(bigram_measures.pmi)
finder1.score_ngrams(bigram_measures.pmi)


_Fdist = nltk.FreqDist([x for x in brown.words(categories='news')])

_Sents = [[j for j in i] for i in brown.sents(categories='news')]

def p(x):
    return _Fdist[x] / float(len(_Fdist))

def pxy(x, y):
    return (len(list(filter(lambda s: x in s and y in s, _Sents))) + 1) / float(len(_Sents))

def pmi(x, y):
    return log(pxy(x, y) / (p(x) * p(y)), 2)

# N = len(a)
# log_n = log(N,2)
# print(log_n)


# b = " ".join(a)
# print(b)
