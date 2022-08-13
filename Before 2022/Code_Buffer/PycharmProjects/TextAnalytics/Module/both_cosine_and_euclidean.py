# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '13/10/2017 18:22'

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances

corpus = [
    'text analytics is a important branch of computer science in discover meaningful information.',
    'machine learning is also a branch of computer science.',
    'text analytics and machine learning are branches of data science.'
]

vectorizer = CountVectorizer()
tfidf_vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(corpus).todense()
tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

eucDis12 = euclidean_distances(features[0], features[1])
eucDis13 = euclidean_distances(features[0], features[2])
eucDis23 = euclidean_distances(features[1], features[2])
print(eucDis12, eucDis13, eucDis23)
cosSim12 = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
cosSim13 = cosine_similarity(tfidf_matrix[0], tfidf_matrix[2])
cosSim23 = cosine_similarity(tfidf_matrix[1], tfidf_matrix[2])
print(cosSim12, cosSim13, cosSim23)
