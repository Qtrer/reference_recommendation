import pandas as pd
import os

data = pd.read_csv(u'D:/experience/临时实验/61-100/61-1.csv')
df = pd.DataFrame(columns=data.columns)
for i in range(61, 101):
    j = 1
    file = u'D:/experience/临时实验/61-100/' + str(i) + '-' + str(j) + '.csv'
    while(os.path.exists(file)):
        try:
            df1 = pd.read_csv(file)
        except:
            df1 = pd.read_csv(file, encoding='unicode_escape')
        df1['种子序号'] = str(i)
        df1['被引序号'] = str(j)
        df = pd.concat([df, df1])
        j = j + 1
        file = u'D:/experience/临时实验/61-100/' + str(i) + '-' + str(j) + '.csv'
    print('i=' + str(i))
    print('j=' + str(j))
df.to_csv(u'D:/experience/临时实验/61-100/61-100.csv')