# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/9/21 下午7:06'

from nltk.stem import PorterStemmer

txt = open("/Users/fan/Desktop/lab2.txt")
rawText = txt.read()
splitRawText = rawText.split(" ")
stemmer = PorterStemmer()
print([stemmer.stem(x) for x in splitRawText])
