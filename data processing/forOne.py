from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


datafile = 'D:/experience/临时实验/s1-100(纯特征整合版+早近合一).xls' #参数初始化
data = pd.read_excel(datafile) #读取数据

df1 = data['作者h指数'].values.reshape(-1, 1)
df2 = data['文献时间'].values.reshape(-1, 1)
df3 = data['rp'].values.reshape(-1, 1)
df4 = data['sjr'].values.reshape(-1, 1)
df5 = data['snip'].values.reshape(-1, 1)
df6 = data['施引文献'].values.reshape(-1, 1)
df7 = data['标题相似性'].values.reshape(-1, 1)
df8 = data['摘要相似性'].values.reshape(-1, 1)
df9 = data['主题相似性'].values.reshape(-1, 1)
df10 = data['作者相似度（利用jaccard）'].values.reshape(-1, 1)
df11 = data['早期引用状况'].values.reshape(-1, 1)
df12 = data['近期引用状况'].values.reshape(-1, 1)
# df11 = data['早期被引频次（发表后两年的）'].values.reshape(-1, 1)
# df12 = data['早期被不同期刊引用次数'].values.reshape(-1, 1)
# df13 = data['早期被不同国家引用次数'].values.reshape(-1, 1)
# df14 = data['早期被不同机构引用次数'].values.reshape(-1, 1)
# df15 = data['早期被不同学科引用次数'].values.reshape(-1, 1)
# df16 = data['近两年被引次数'].values.reshape(-1, 1)
# df17 = data['近两年被不同期刊引用次数'].values.reshape(-1, 1)
# df18 = data['近两年被不同国家引用次数'].values.reshape(-1, 1)
# df19 = data['近两年被不同机构引用次数'].values.reshape(-1, 1)
# df20 = data['近两年被不同学科引用次数'].values.reshape(-1, 1)

min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0.01, 0.99))
x_minmax1 = min_max_scaler.fit_transform(df1)
x_minmax2 = min_max_scaler.fit_transform(df2)
x_minmax3 = min_max_scaler.fit_transform(df3)
x_minmax4 = min_max_scaler.fit_transform(df4)
x_minmax5 = min_max_scaler.fit_transform(df5)
x_minmax6 = min_max_scaler.fit_transform(df6)
x_minmax7 = min_max_scaler.fit_transform(df7)
x_minmax8 = min_max_scaler.fit_transform(df8)
x_minmax9 = min_max_scaler.fit_transform(df9)
x_minmax10 = min_max_scaler.fit_transform(df10)
x_minmax11 = min_max_scaler.fit_transform(df11)
x_minmax12 = min_max_scaler.fit_transform(df12)
# x_minmax13 = min_max_scaler.fit_transform(df13)
# x_minmax14 = min_max_scaler.fit_transform(df14)
# x_minmax15 = min_max_scaler.fit_transform(df15)
# x_minmax16 = min_max_scaler.fit_transform(df16)
# x_minmax17 = min_max_scaler.fit_transform(df17)
# x_minmax18 = min_max_scaler.fit_transform(df18)
# x_minmax19 = min_max_scaler.fit_transform(df19)
# x_minmax20 = min_max_scaler.fit_transform(df20)
np.set_printoptions(threshold=np.inf)
print(x_minmax1)
data['作者h指数'] = x_minmax1
data['文献时间'] = x_minmax2
data['rp'] = x_minmax3
data['sjr'] = x_minmax4
data['snip'] = x_minmax5
data['施引文献'] = x_minmax6
data['标题相似性'] = x_minmax7
data['摘要相似性'] = x_minmax8
data['主题相似性'] = x_minmax9
data['作者相似度（利用jaccard）'] = x_minmax10
data['早期引用状况'] = x_minmax11
data['近期引用状况'] = x_minmax12
# data['早期被不同国家引用次数'] = x_minmax13
# data['早期被不同机构引用次数'] = x_minmax14
# data['早期被不同学科引用次数'] = x_minmax15
# data['近两年被引次数'] = x_minmax16
# data['近两年被不同期刊引用次数'] = x_minmax17
# data['近两年被不同国家引用次数'] = x_minmax18
# data['近两年被不同机构引用次数'] = x_minmax19
# data['近两年被不同学科引用次数'] = x_minmax20
data.to_excel('D:/experience/临时实验/s1-100(纯特征整合版+早近合一)(forone).xls')


