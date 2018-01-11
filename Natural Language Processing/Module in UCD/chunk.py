# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '2017/9/21 下午5:28'

import nltk
from nltk.corpus import wordnet as wn

def penn2morphy(penntag, returnNone=False):
    morphy_tag = {'NN':wn.NOUN, 'JJ':wn.ADJ,
                  'VB':wn.VERB, 'RB':wn.ADV}
    try:
        return morphy_tag[penntag]
    except:
        return None if returnNone else ''


txt = open("/Users/fan/Desktop/lab2.txt")
rawText = txt.read()
tokens = nltk.word_tokenize(rawText)
tags = nltk.pos_tag(tokens)

ne_chunks = nltk.ne_chunk(tags, binary=True)
# print(ne_chunks)
a = list(ne_chunks)
# print(a)

wnl = nltk.WordNetLemmatizer()

for tagged_item in a:
    word = tagged_item[0]
    word_pos = tagged_item[1]
    word_convert_pos = penn2morphy(word_pos)
    lemma = wnl.lemmatize(word, pos=word_convert_pos)
    print(lemma)
