from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report

# 导入数据集中的数据（每项有18个特征数据值，1个目标类别值）
datafile = 'D:/experience/临时实验/s1-100(纯特征整合版+早近合一)(forone).xls' #参数初始化
data = pd.read_excel(datafile) #读取数据
score = []
recall = []
f1 = []
# error = ['文章作者是否作者之前引用过的作者',
#     '是否为作者之前的论文',
#     '标题相似性',
#     '是否作者之前引用过的文章',
#     '主题相似性',
#     '近期引用状况',]
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
dftotal=pd.DataFrame()
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
    gnb = GaussianNB()
    # bnb = BernoulliNB()
    # mnb = MultinomialNB()
    gnb.fit(train_X, train_Y)
    # bnb.fit(train_X, train_Y)
    # mnb.fit(train_X, train_Y)
    # gnb.score(test_X, test_Y)
    # bnb.score(test_X, test_Y)
    # mnb.score(test_X, test_Y)
    y_predicted = gnb.predict(test_X)
    # print(y_predicted)
    # df = pd.DataFrame(columns=['种子序号','是否被引','预测结果'])
    # df.loc['种子序号']=i
    # df.loc['是否被引']=test_Y
    # df['预测结果']=y_predicted
    # dftotal=pd.concat([dftotal,df])
    # y_predicted_b = bnb.predict(test_X)
    # y_predicted_m = mnb.predict(test_X)

    # 显示预测结果
    # print("\n预测结果:\n", y_predicted)
    # print("\n预测结果:\n", y_predicted_b)
    # print("\n预测结果:\n", y_predicted_m)
    # # 显示预测错误率

    # print("\n总数据%d条 预测失误%d条" % (test_X.data.shape[0], (test_Y!= y_predicted).sum()))
    # print("\n总数据%d条 预测失误%d条" % (test_X.data.shape[0], (test_Y!= y_predicted_b).sum()))
    # print("\n总数据%d条 预测失误%d条" % (test_X.data.shape[0], (test_Y!= y_predicted_m).sum()))
    # #获取结果
    # print ('The Accuracy of GaussianNB Classifier is:', gnb.score(test_X, test_Y))
    # print (classification_report(test_Y, y_predicted, target_names = ['0', '1']))
    # print ('The Accuracy of BernoulliNB Classifier is:', bnb.score(test_X, test_Y))
    # print (classification_report(test_Y, y_predicted_b, target_names = ['0', '1']))
    # print ('The Accuracy of MultinomialNB Classifier is:', mnb.score(test_X, test_Y))
    # print (classification_report(test_Y, y_predicted_m, target_names = ['0', '1']))

    # error_num = (test_Y != y_predicted).sum()
    # error_percent = error_num/len(test_Y)
    # error.append(error_percent)
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    test_Y=test_Y.tolist()
    y_predicted=y_predicted.tolist()
    for i in range(len(y_predicted)):
        if test_Y[i] == 1 and y_predicted[i] == 1:
            tp+=1
        elif test_Y[i] == 0 and y_predicted[i] == 1:
            fp+=1
        elif test_Y[i] == 1 and y_predicted[i] == 0:
            fn+=1
        elif test_Y[i] == 0 and y_predicted[i] == 0:
            tn+=1
    p=(tp+tn)/(tp+fp+fn+tn)
    r=(tp)/(tp+fn)
    f=(2*p*r)/(p+r)
    score.append(p)
    recall.append(r)
    f1.append(f)
    # score.append(gnb.score(test_X, test_Y))
    # graph = classification_report(test_Y, y_predicted, target_names = ['0', '1'])
    # recall.append(float(graph[302:306]))
    # f1.append(float(graph[312:316]))


# print(score)
# print(recall)
# print(f1)
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
# dftotal.to_excel('D:/experience/临时实验/cited_test.xls')
