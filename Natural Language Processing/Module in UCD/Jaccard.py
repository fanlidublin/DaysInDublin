# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '12/10/2017 19:29'


def JaccardIndex(str1, str2):
    set1 = set(str1.split())
    set2 = set(str2.split())
    ans = 1 - float(len(set1 & set2)) / len(set1 | set2)
    return round(ans, 2)


def DiceDis(str1, str2):
    list1 = list(str1.split())
    list2 = list(str2.split())
    print(set2)
    # ans = 1 - float(2 * len(set1 & set2)) / (len(set1) + len(set2))
    return set2


entity1 = "text analystics is a module in data science"
entity2 = "machine learning is a module in data science"
# entity3 = "iphone X is a new discovery in science areas"
# entity4 = "advance mathematics is a module in math areas"
entity5 = "machine learning is helpful in many daily areas"
# entity6 = "text discover is a module in data science"

# pair12 = DiceDis(entity1, entity2)
# pair13 = DiceDis(entity1, entity3)
# pair14 = DiceDis(entity1, entity4)
pair15 = DiceDis(entity1, entity5)
# pair16 = DiceDis(entity1, entity6)
# pair23 = DiceDis(entity2, entity3)
# pair24 = DiceDis(entity2, entity4)
# pair25 = DiceDis(entity2, entity5)
# pair26 = DiceDis(entity2, entity6)
# pair34 = DiceDis(entity3, entity4)
# pair35 = DiceDis(entity3, entity5)
# pair36 = DiceDis(entity3, entity6)
# pair45 = DiceDis(entity4, entity5)
# pair46 = DiceDis(entity4, entity6)
# pair56 = DiceDis(entity4, entity6)

# result = {"pair12": pair12, "pair13": pair13, "pair14": pair14,
#           "pair15": pair15, "pair16": pair16, "pair23": pair23,
#           "pair24": pair24, "pair25": pair25, "pair26": pair26,
#           "pair34": pair34, "pair35": pair35, "pair36": pair36,
#           "pair45": pair45, "pair46": pair46, "pair56": pair56}
print(pair15)
