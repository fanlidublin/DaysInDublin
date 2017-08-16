#coding=UTF8
from numpy import *
import operator
from os import listdir

def classify0(inX, dataset, labels, k):
    dataSetSize = dataset.shape[0]    
    diffMat = tile(inX, (dataSetSize, 1)) - dataset
    sqDiffMat = diffMat ** 2   
    sqDistance = sqDiffMat.sum(axis=1)
    distance = sqDistance ** 0.5
    sortedDistIndicies = distance.argsort()

    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
    
def file2matrix(filename):
    """
    从文件中读入训练数据，并存储为矩阵
    """
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #获取 numberOfLines=样本的行数
    returnMat = zeros((numberOfLines,3))        #创建一个矩阵用于存放训练样本数据，一共有numberOfLines行，每一行存放3个数据
    classLabelVector = []                       #创建一个1维数组用于存放训练样本标签。  
    index = 0
    for line in fr.readlines():
        # 把回车符号给去掉
        line = line.strip()    
        # 把每一行数据用\t分割(将整行数据分割成一个元素列表)
        listFromLine = line.split('\t')
        # 把分割好的数据放至数据集，其中index是该样本数据的下标，就是放到第几行
        returnMat[index,:] = listFromLine[0:3]
        # 把该样本对应的标签放至标签集，顺序与样本集对应。
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector
    
def autoNorm(dataSet):
    """
    训练数据归一化
    """
    # 获取数据集中每一列的最小数值
    # 以createDataSet()中的数据为例，group.min(0)=[0,0]
    minVals = dataSet.min(0) 
    # 获取数据集中每一列的最大数值
    # group.max(0)=[1, 1.1]
    maxVals = dataSet.max(0) 
    # 最大值与最小的差值
    ranges = maxVals - minVals
    # 创建一个与dataSet同shape的全0矩阵，用于存放归一化后的数据
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    # 把最小值扩充为与dataSet同shape，然后作差
    normDataSet = dataSet - tile(minVals, (m,1))
    # 把最大最小差值扩充为dataSet同shape，然后作商。 ！！！注意：是指对应元素进行除法运算，而不是矩阵除法。
    # 矩阵除法在numpy中要用linalg.solve(A,B)
    normDataSet = normDataSet/tile(ranges, (m,1))
    return normDataSet, ranges, minVals
   
def datingClassTest():
    # 将数据集中10%的数据留作测试用，其余的90%用于训练
    hoRatio = 0.10
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d, result is :%s" % (classifierResult, datingLabels[i],classifierResult==datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount

if __name__=="__main__"
    datingClassTest()