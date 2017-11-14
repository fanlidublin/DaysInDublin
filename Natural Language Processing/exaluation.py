# _*_ encoding:utf-8 _*_
__author__ = 'lifan'
__date__ = '05/11/2017 23:07'

import matplotlib.pyplot as plt

#      threshold, TP, FN, FP, TN
dataset = [[1, 20, 80, 2, 98],
           [5, 50, 50, 5, 95],
           [10, 60, 40, 10, 90],
           [15, 80, 20, 20, 80],
           [20, 88, 12, 30, 70],
           [25, 90, 10, 40, 60],
           [30, 95, 5, 50, 50],
           [35, 96, 4, 60, 40],
           [40, 97, 3, 70, 30],
           [50, 98, 2, 80, 20]]

precision = list(map(lambda x: x[1] / (x[1] + x[3]), dataset))
recall = list(map(lambda x: x[1] / (x[1] + x[2]), dataset))
f1_measure = {dataset[i][0]: (2 * precision[i] * recall[i] / (precision[i] + recall[i])) for i in range(len(dataset))}
fallout = list(map(lambda x: x[3] / (x[3] + x[4]), dataset))
miss_rate = list(map(lambda x: x[2] / (x[1] + x[2]), dataset))

print(f1_measure)
print('When the threshold is %d, the f1 measure score is the highest.' % max(f1_measure, key=f1_measure.get))

# ROC
# x axes => false positive rate (fallout) => FP/(FP+TN)
# y axes => true positive rate (recall) => TP/(TP+FN)
# plt.plot(fallout, recall)
# plt.title('ROC Curve')
# plt.xlabel('false positive rate')
# plt.ylabel('true positive rate')
# plt.show()
#
# # DET
# # x axes => false positive rate (fallout) => FP/(FP+TN)
# # y axes => false negative rate (miss rate) => FN/(TP+FN)
plt.plot(fallout, miss_rate)
plt.title('DET Curve')
plt.xlabel('false positive rate')
plt.ylabel('false negative rate')
plt.show()
