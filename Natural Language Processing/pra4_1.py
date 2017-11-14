# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '04/10/2017 21:15'


import nltk
from nltk.corpus import stopwords

stop = stopwords.words('english')
text = open('/Users/fan/Desktop/pra4.txt')
rawtext = text.read()
a = [i for i in rawtext.split() if i not in stop]
b = " ".join(a)
print(b)


