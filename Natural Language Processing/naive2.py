# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '18/10/2017 21:50'

import nltk

names = nltk.corpus.names
names.fileids()
male_names = names.words('male.txt')
female_names = names.words('female.txt')
[w for w in male_names if w in female_names]

cfd = nltk.ConditionalFreqDist((file, name[0])
                               for file in names.fileids()
                               for name in names.words(file))
cfd.plot()
