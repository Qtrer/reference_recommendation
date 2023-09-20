from sklearn.svm import SVC
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split,ShuffleSplit
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression


# 导入数据集中的数据（每项有18个特征数据值，1个目标类别值）
datafile = 'D:/experience/临时实验/s1-100(纯特征整合版+早近合一)(forone).xls' #参数初始化
data = pd.read_excel(datafile) #读取数据
col = data.columns.values.tolist()
#print(col)
datas=np.array(data)

# X为特征数据 y是类别值
cols = [
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
        # '早期引用状况',
    ]
#print(cols)
X = np.array(data[cols])
print(X)
y = data['是否被引']


# #递归特征消除法
svc = SVC(kernel="linear", C=1)
rfe = RFE(estimator=svc, n_features_to_select=1, step=1)
# # score = []
# # for i in range(X.shape[1]):
# #         score = train_test_split(rfe, X[:,i:i+1],y,scoring='r2',cv=ShuffleSplit(len(X),3,.3))
# #         score.append((round(np.mean(score),3),cols[i]))
# # print((sorted(score, reverse=True)))
rfe.fit(X, y)
print(rfe.score(X,y))
ranking = rfe.ranking_
print('递归特征消除法')
for r in ranking:
        print(r)

# 逻辑回归
rfe2 = RFE(estimator=LogisticRegression(), n_features_to_select=1).fit(X, y)
# score = []
# for i in range(X.shape[1]):
#         score = train_test_split(rfe2, X[:,i:i+1],y,scoring='r2',cv=ShuffleSplit(len(X),3,.3))
#         score.append((round(np.mean(score),3),cols[i]))
# print((sorted(score, reverse=True)))
print('逻辑回归')
print(rfe2.score(X,y))
for c in rfe2.ranking_:
    print(c)
