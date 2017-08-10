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

    
def img2vector(filename):
    """
    将图片数据转换为01矩阵。
    每张图片是32*32像素，也就是一共1024个字节。
    因此转换的时候，每行表示一个样本，每个样本含1024个字节。
    """
    # 每个样本数据是1024=32*32个字节
    returnVect = zeros((1,1024))
    fr = open(filename)
    # 循环读取32行，32列。
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels = []
    # 加载训练数据
    trainingFileList = listdir('trainingDigits')           
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        # 从文件名中解析出当前图像的标签，也就是数字是几
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    # 加载测试数据
    testFileList = listdir('testDigits')        #iterate through the test set
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]     #take off .txt
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d, the real answer is: %d, The predict result is: %s" % (classifierResult, classNumStr, classifierResult==classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d / %d" %(errorCount, mTest)
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))

if __name__== "__main__":
    handwritingClassTest()    