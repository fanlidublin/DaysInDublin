# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '13/10/2017 22:29'

import nltk.metrics
import distance

normal1 = "The @HoustonRockets hit 11 3P's in the first half against the Knicks!"
normal2 = "Today @ 12(CST)-my official announcement press conference as @HoustonRockets owner. Livestream on http://Rockets.com  #RunAsOne"

distance1 = distance.levenshtein(normal1, normal2)
print(distance1)