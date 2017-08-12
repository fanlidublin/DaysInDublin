'''
Created on Aug 10, 2017
Decision Tree Source Code for Machine Learning in Action Ch. 3
@author: Peter Harrington
'''
#coding=utf-8
from math import log
import operator

def createDataSet():
    dataSet =[[1,1,'yes'],
              [1,1,'yes'],
              [1,0,'no'],
              [0,1,'no'],
              [0,1,'no']]  #创建数据集
    labels = ['no surfacing','flippers'] #分类属性
    return dataSet,labels
'''
测试结果
[[1, 'no'], [1, 'no']]
>>> dataSet
[[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'], [0, 1, 'no']]
>>> labels
['no surfacing', 'flippers']
'''


def calcShannonEnt(dataSet):   #计算给定数据集的香农熵
    numEntries = len(dataSet)  #求长度
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1] #获得标签
        if currentLabel not in labelCounts.keys():  #如果标签不在新定义的字典里创建该标签值
            labelCounts[currentLabel]=0
        labelCounts[currentLabel]+=1 #该类标签下含有数据的个数
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries  #同类标签出现的概率
        shannonEnt -=prob*log(prob,2)   #以2为底求对数
    return shannonEnt
'''
测试结果
>>> trees.calcShannonEnt(dataSet)
0.9709505944546686
'''


def splitDataSet(dataSet,axis,value):  #划分数据集,三个参数为带划分的数据集，划分数据集的特征，特征的返回值
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] ==value:
            #将相同数据集特征的抽取出来
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet #返回一个列表
'''
测试结果
>>> trees.splitDataSet(dataSet,0,1)
[[1, 'yes'], [1, 'yes'], [0, 'no']] 
>>> trees.splitDataSet(dataSet,0,0)
[[1, 'no'], [1, 'no']]
'''   


def chooseBestFeatureToSplit(dataSet):  #选择最好的数据集划分方式
    numFeature = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    beatFeature = -1
    for i in range(numFeature):
        featureList = [example[i] for example in dataSet] #获取第i个特征所有的可能取值
        uniqueVals = set(featureList)  #从列表中创建集合，得到不重复的所有可能取值
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)  #以i为数据集特征，value为返回值，划分数据集
            prob = len(subDataSet)/float(len(dataSet))   #数据集特征为i的所占的比例
            newEntropy +=prob * calcShannonEnt(subDataSet)   #计算每种数据集的信息熵
        infoGain = baseEntropy- newEntropy
        #计算最好的信息增益，增益越大说明所占决策权越大
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature
'''
测试结果
>>> trees.chooseBestFeatureToSplit(dataSet)
0
说明：第0个特征是最好的用于划分数据集的特征
'''


def majorityCnt(classList):      
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote]=0
        classCount[vote]+=1
    sortedClassCount = sorted(classCount.iteritems(),key =operator.itemgetter(1),reverse=True)#排序，True升序
    return sortedClassCount[0][0] #返回出现次数最多的


def createTree(dataSet,labels):     #创建树的函数代码
    classList = [example[-1]  for example in dataSet]
    if classList.count(classList[0])==len(classList): #类别完全相同则停止划分
        return classList[0]
    if len(dataSet[0]) ==1:            #遍历完所有特征值时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)   #选择最好的数据集划分方式
    bestFeatLabel = labels[bestFeat]   #得到对应的标签值
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])      #清空labels[bestFeat],在下一次使用时清零
    featValues = [example[bestFeat] for example in dataSet] 
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels =labels[:]
        #递归调用创建决策树函数
        myTree[bestFeatLabel][value]=createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree  
'''
测试结果
>>> reload(trees)
<module 'trees' from 'trees.py'>
>>> dataSet,labels = trees.createDataSet()
>>> myTree = trees.createTree(dataSet,labels)
>>> myTree
{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
'''