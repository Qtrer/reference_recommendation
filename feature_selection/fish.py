from feature_selection import fisher_score
import numpy as np
import pandas as pd

# X = np.loadtxt('LN110.txt')
# X = np.array(X)
# print('已加载评论文本特征向量赋给X')
# y=np.loadtxt('LN-110.txt')
# y=np.array(y)
# print('已加载y')
# #kwargs={'高':1,'中':2,'低':3}
# #dict = {}
# #dict["Alice"] = 18
# print('已加载')


datafile = 'D:/experience/临时实验/s1-100(纯特征整合版+早近合一)(forone).xls' #参数初始化
data = pd.read_excel(datafile) #读取数据
# ['施引文献', '作者h指数', 'snip', '两篇文章是否同一领域', '文献时间',
        # '是否为作者之前的论文', '是否作者合著者的论文', '文章作者是否作者之前引用过的作者', '是否作者之前引用过的文章',
        # '标题相似性', '摘要相似性', '主题相似性', '是否来源于美国', '是否来源于欧洲', '作者相似度（利用jaccard）', '是否有资金赞助', 'rp', 'sjr']
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

X = np.array(data[cols])
y = data['是否被引']

score=fisher_score.fisher_score(X, y)
Fid=fisher_score.feature_ranking(score)
for f in Fid:
        print(f)
