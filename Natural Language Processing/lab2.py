# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/9/21 下午3:52'

import nltk

txt = open("/Users/fan/Desktop/lab2.txt")
rawText = txt.read()
tokens = nltk.word_tokenize(rawText)
tags = nltk.pos_tag(tokens)

wn = nltk.WordNetLemmatizer()

#
# def convert_tags(tag):
#     if tag == 'vbd' or tag == 'vbg' or tag == 'vbz':
#         return 'v'
#     else:
#         return 'n'
#
#
# for tagged_item in tags:
#     word = tagged_item[0]
#     word_pos = convert_tags(tagged_item[1].lower())
#     lemma = wn.lemmatize(word, word_pos)
#     print(lemma)
