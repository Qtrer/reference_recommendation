import xlrd
import math
import numpy as np
import pandas as pd

#读数据并求熵
path=u"D:/experience/临时实验/s1-100(纯特征整合版)(forone).xls"
hn,nc=1,21
#hn为表头行数,nc为表头列数
sheetname=u'Sheet1'
datafile = 'D:/experience/临时实验/s1-100(纯特征整合版)(forone).xls' #参数初始化
data = pd.read_excel(datafile)
cols = [
    '近两年被引次数',
    '近两年被不同期刊引用次数',
    '近两年被不同国家引用次数',
    '近两年被不同机构引用次数',
    '近两年被不同学科引用次数',
    '早期被引频次（发表后两年的）',
    '早期被不同期刊引用次数',
    '早期被不同国家引用次数',
    '早期被不同机构引用次数',
    '早期被不同学科引用次数',
]
x = data[cols]
rnum = x.index.size
cnum = x.columns.size
k = 1.0/math.log(rnum)
inf = [[None] * cnum for i in range(rnum)]
x = np.array(x)
inf = np.array(inf)
for i in range(rnum):
    for j in range(cnum):
        p = x[i][j]/x.sum(axis=0)[j]
        infij = math.log(p)*p*(-k)
        inf[i][j]=infij
inf = pd.DataFrame(inf)
d = 1-inf.sum(axis=0)
w = [[None] * 1 for i in range(cnum)]
for i in range(cnum):
    wi = d[i]/sum(d)
    w[i]=wi
w=pd.DataFrame(w)
w.index = cols
w.columns = ['weight']
print(w)

# def readexcel(hn,nc):
#     data = xlrd.open_workbook(path)
#     table = data.sheet_by_name(sheetname)
#     nrows = table.nrows
#     data=[]
#     for i in range(hn,nrows):
#         data.append(table.row_values(i)[nc:])
#     return np.array(data)
#
# def entropy(data0):
#     #返回每个样本的指数
#     #样本数，指标个数
#     n,m=np.shape(data0)
#     #一行一个样本，一列一个指标
#     #下面是归一化
#     maxium=np.max(data0,axis=0)
#     minium=np.min(data0,axis=0)
#     data= (data0-minium)*1.0/(maxium-minium)
#     ##计算第j项指标，第i个样本占该指标的比重
#     sumzb=np.sum(data,axis=0)
#     data=data/sumzb
#     #对ln0处理
#     a=data*1.0
#     a[np.where(data==0)]=0.0001
#     #计算每个指标的熵
#     e=(-1.0/np.log(n))*np.sum(data*np.log(a),axis=0)
#     print(e)
#     #计算权重
#     w=(1-e)/np.sum(1-e)
#     recodes=np.sum(data0*w,axis=1)
#     return recodes
#
# data=readexcel(hn,nc)
# grades=entropy(data)
# print(grades)