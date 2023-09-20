from sklearn.svm import SVC
from sklearn import datasets
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import LeaveOneOut
from sklearn.model_selection import LeavePOut
from sklearn.model_selection import ShuffleSplit

datafile = 'D:/experience/临时实验/s1-100(纯特征整合版+早近合一)(forone).xls' #参数初始化
data = pd.read_excel(datafile) #读取数据
score = []
recall = []
f1 = []
# error = []
cols = [
'文章作者是否作者之前引用过的作者',
    '近期引用状况',
    '主题相似性',
    '标题相似性',
    '是否为作者之前的论文',
    '是否作者之前引用过的文章',
    '作者相似度',

]
all_cols = [
        '标题相似性',
        '摘要相似性',
        '主题相似性',
        '作者相似度（利用jaccard）',
        '是否为作者之前的论文',
        '是否作者合著者的论文',
        '文章作者是否作者之前引用过的作者',
        '是否作者之前引用过的文章',
        '施引文献',
        '作者h指数',
        '两篇文章是否同一领域',
        '文献时间',
        '是否来源于美国',
        '是否来源于欧洲',
        '是否有资金赞助',
        'rp',
        'sjr',
        'snip',
        '近期引用状况',
        '早期引用状况',
]
for i in range(1,101):
    data0 = data.loc[data['种子文献编号'] != i]
    data1 = data.loc[data['种子文献编号'] == i]
    # print(data0, data1)
    print(i)
    train_X = np.array(data0[cols])
    test_X = np.array(data1[cols])
    train_Y = data0['是否被引']
    test_Y = data1['是否被引']
    # print(train_X, train_Y, test_X, test_Y)

    model = SVC(kernel='linear', probability=True)
    model.fit(train_X,train_Y)
    y_predicted = model.predict(test_X)
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    test_Y = test_Y.tolist()
    y_predicted = y_predicted.tolist()
    for i in range(len(y_predicted)):
        if test_Y[i] == 1 and y_predicted[i] == 1:
            tp += 1
        elif test_Y[i] == 0 and y_predicted[i] == 1:
            fp += 1
        elif test_Y[i] == 1 and y_predicted[i] == 0:
            fn += 1
        elif test_Y[i] == 0 and y_predicted[i] == 0:
            tn += 1
    p = (tp + tn) / (tp + fp + fn + tn)
    r = (tp) / (tp + fn)
    f = (2 * p * r) / (p + r)
    score.append(p)
    recall.append(r)
    f1.append(f)
    # score.append(model.score(test_X, test_Y))
    # graph = classification_report(test_Y, y_predicted, target_names=['0', '1'])
    # recall.append(float(graph[302:306]))
    # f1.append(float(graph[312:316]))

print(score)
print(recall)
print(f1)
scoreSum = 0
recallSum = 0
f1Sum = 0
for i in range(len(score)):
    scoreSum += score[i]
    recallSum += recall[i]
    f1Sum += f1[i]
scoreAvg = scoreSum/len(score)
recallAvg = recallSum/len(recall)
f1Avg = f1Sum/len(f1)
print('scoreAvg')
print('recallAvg')
print('f1Avg')
print(scoreAvg)
print(recallAvg)
print(f1Avg)
print(' ')
print(str(scoreAvg) + '\t' + str(recallAvg) + '\t' + str(f1Avg))

