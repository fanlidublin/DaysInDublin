# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/9/21 下午8:36'

import nltk

txt = open("/Users/fan/Desktop/lab2_text_q1.txt")
rawText = txt.read()
tokens = nltk.word_tokenize(rawText)
words = [w.lower() for w in tokens]
words_tags = nltk.pos_tag(words)
print(words_tags)