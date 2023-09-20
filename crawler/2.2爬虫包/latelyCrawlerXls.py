import requests
import io
import xlrd
import time
import re
import sys

import xlwt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')

YEAR = 2018

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'scopus.machineID=565E426BB5379DC87C63C542901909C3.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1587562861883r0.38711136738597673; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22referral%22%7D; optimizelyBuckets=%7B%7D; xmlHttpRequest=true; __cfduid=d954c5c2b9549289b92a76b614def85111601106950; SCSessionID=F487184E3381B0766E92A9222F236F9B.i-0e67e3b3089173990; scopusSessionUUID=aa0d981c-0199-44d1-9; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB18CDB063B58CC42E0DB2D5375A980599FBAFC9ED2DBE86A696ED76959032F54EEA31AAC5A6BDE3E4B4DACF34F3854CEEBA855375B6C8861506D27AB7E080049E0; javaScript=true; at_check=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; screenInfo="900:1440"; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=359503849%7CMCIDTS%7C18538%7CMCMID%7C09635205066540933810671114848219444600%7CMCAAMLH-1602241769%7C11%7CMCAAMB-1602241769%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1601644169s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18382%7CvVersion%7C5.0.1%7CMCCIDH%7C1246701492; __cfruid=e68a72d397aed1f18236931ed466a6a43812a8d5-1601637087; mbox=PC#7f4649f1b841468a940386570b585808.38_0#1664886085|session#a0b93885db334badb65efd559bd48b8d#1601642818; s_pers=%20v8%3D1601641285051%7C1696249285051%3B%20v8_s%3DLess%2520than%25201%2520day%7C1601643085051%3B%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1601643085062%3B%20v68%3D1601641283515%7C1601643085069%3B; s_sess=%20s_cpc%3D0%3B%20e78%3Ddoi%252810.1007%252Fs11192-015-1702-7%2529%3B%20s_sq%3D%3B%20c21%3Ddoi%252810.1007%252Fs11192-015-1621-7%2529%3B%20e13%3Ddoi%252810.1007%252Fs11192-015-1621-7%2529%253A1%3B%20c13%3Ddate%2520%2528oldest%2529%3B%20s_cc%3Dtrue%3B%20e41%3D1%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C50%252C50%252C740%252C1440%252C740%252C1440%252C900%252C1%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Adocument%252520searchform%252C50%252C50%252C740%252C1440%252C150%252C1440%252C900%252C1%252CP%3B',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}

data = {
    'clusterDisplayCount': '160',
    'sot': 'cite',
    'navigatorName': '',
    'clusterCategory': '',
    'cite': 'eid',
    'refeid': '',
    'refeidnss': '',
    's': '',
    'st1': '',
    'st2': '',
    'sid': 'a9592be3f087a90dfeddc534be959fc5',
    'sdt': 'cl',
    'sort': 'plf-f',
    'citingId': '',
    'citedAuthorId': '',
    'listId': '',
    'origin': 'resultslist',
    'src': 's',
    'affilCity': '',
    'affilName': '',
    'affilCntry': '',
    'affiliationId': '',
    'cluster': 'scopubyr,\"2017\",t,\"2016\",t',
    'offset': '1',
    'scla': '',
    'scls': '',
    'sclk': '',
    'scll': '',
    'sclsb': '',
    'sclc': '',
    'scfs': '',
    'ref': '',
    'isRebrandLayout': 'true',
}

clusterCategorySub = 'selectedSubjectClusterCategories'
navigatorNameSub = 'SUBJAREA'

clusterCategorySource = 'selectedSourceClusterCategories'
navigatorNameSource = 'EXACTSRCTITLE'

clusterCategoryAffi = 'selectedAffiliationClusterCategories'
navigatorNameAffi = 'AFFIL'

clusterCategoryCoun = 'selectedCountryClusterCategories'
navigatorNameCoun = 'COUNTRY_NAME'

cluster1 = 'scopubyr,\"'
# 2017
cluster2 = '\",t,\"'
# 2016
cluster3 = '\",t'

cluster_sole1 = 'scopubyr,\"'
cluster_sole2 = '\",t'

u1 = 'https://www.scopus.com/results/citedbyresults.uri?sort=plf-f&cite='
# 2-s2.0-34249309179
u2 = '&src=s&nlo=&nlr=&nls=&imp=t&sid=6e6e378fd1ca34b491c59fa079886305&sot=cite&sdt=cl&cluster=scopubyr%2C%22'
# 2008
u3 = '%22%2Ct%2C%22'
# 2007
u4 = '%22%2Ct&sl=0&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid='


u1_sole = 'https://www.scopus.com/results/citedbyresults.uri?sort=plf-f&cite='
# 2-s2.0-34249309179
u2_sole = '&src=s&nlo=&nlr=&nls=&imp=t&sid=b5cb8e30a8dc7e290b6e70f99e76daec&sot=cite&sdt=cl&cluster=scopubyr%2C%22'
# 2017
u3_sole = '%22%2Ct&sl=0&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid='

def get_excel(indexStart,indexEnd):
    file = "../sourceData/2015待推荐文献.xls"
    data = xlrd.open_workbook(file, formatting_info=True)
    table = data.sheet_by_name('1')
    papers = []
    for i in range(indexStart,indexEnd):
        paper = {}
        content = table.row_values(i)
        paper['序号'] = content[0]
        paper['标题'] = content[3]
        paper['年份'] = content[4]
        paper['来源出版物名称'] = content[5]
        paper['DOI'] = content[13]
        paper['EID'] = content[43]
        print(i+1)
        print(paper['标题'])
        papers.append(paper)

    return papers

def get_data_excel_head(dataSheet):
    dataSheet.write(0, 0, '序号')
    dataSheet.write(0, 1, '标题')
    dataSheet.write(0, 2, '近两年被引次数')
    dataSheet.write(0, 3, '近两年被引学科数')
    dataSheet.write(0, 4, '近两年来源出版物数')
    dataSheet.write(0, 5, '近两年被引机构数')
    dataSheet.write(0, 6, '近两年被引国家数')

if __name__ == '__main__':
    # 设置收集起始序号
    indexStart = 211
    indexEnd = 328

    # 获取代收数据
    papers = get_excel(indexStart,indexEnd)

    # 创建收取数据文件
    fileName = '../data/' + str(indexStart) + '-' + str(indexEnd) + '近两年特征收取结果.xls'
    print(fileName)
    writebook = xlwt.Workbook()  # 打开excel
    dataSheet = writebook.add_sheet('data')  # 添加一个名字叫data的sheet
    # 写入表头，方便查阅
    get_data_excel_head(dataSheet)
    writebook.save(fileName)

    # 初始化数据
    index = 1
    data['cluster'] = cluster1 + str(YEAR - 2)[0:4] + cluster2 + str(YEAR - 1)[0:4] + cluster3

    for paper in papers:
        eid = paper['EID']
        year = paper['年份']
        dataSheet.write(index, 0, paper['序号'])
        dataSheet.write(index, 1, paper['标题'])
        writebook.save(fileName)
        if eid != '':
             # -----------------学科-------------------
                dataSub = data
                dataSub['navigatorName'] = navigatorNameSub
                dataSub['clusterCategory'] = clusterCategorySub
                dataSub['cite'] = eid
                if year >= YEAR-1:
                    dataSub['cluster'] = cluster_sole1 + str(YEAR-1)[0:4] + cluster_sole2

                rep = requests.post(
                    url='https://www.scopus.com/standard/viewMore.uri', data=dataSub,
                    headers=headers)
                latelySub0 = re.findall(r'btnText\\">(.*?)<', rep.text, re.S)
                print("\nlatelySub:")
                latelySub = len(latelySub0) / 2
                print(latelySub)
                dataSheet.write(index, 3, latelySub)
                time.sleep(1)
                # -----------------来源-------------------

                dataSource = data
                dataSource['navigatorName'] = navigatorNameSource
                dataSource['clusterCategory'] = clusterCategorySource
                dataSource['cite'] = eid
                if year >= YEAR-1:
                    dataSource['cluster'] = cluster_sole1 + str(YEAR-1)[0:4] + cluster_sole2

                rep = requests.post(
                    url='https://www.scopus.com/standard/viewMore.uri', data=dataSource,
                    headers=headers)
                latelySource0 = re.findall(r'btnText\\">(.*?)<', rep.text, re.S)
                print("\nlatelySource:")
                latelySource = len(latelySource0) / 2
                print(latelySource)
                dataSheet.write(index, 4, latelySource)
                time.sleep(1)

                # -----------------机构-------------------
                dataAffi = data
                dataAffi['navigatorName'] = navigatorNameAffi
                dataAffi['clusterCategory'] = clusterCategoryAffi
                dataAffi['cite'] = eid
                if year >= YEAR-1:
                    dataAffi['cluster'] = cluster_sole1 + str(YEAR-1)[0:4] + cluster_sole2

                rep = requests.post(
                    url='https://www.scopus.com/standard/viewMore.uri', data=dataAffi,
                    headers=headers)
                latelyAffi0 = re.findall(r'btnText\\">(.*?)<', rep.text, re.S)
                print("\nlatelyAffi:")
                latelyAffi = len(latelyAffi0) / 2
                print(latelyAffi)
                dataSheet.write(index, 5, latelyAffi)
                time.sleep(1)
                # -----------------国家-------------------
                dataCoun = data
                dataCoun['navigatorName'] = navigatorNameCoun
                dataCoun['clusterCategory'] = clusterCategoryCoun
                dataCoun['cite'] = eid
                if year >= YEAR-1:
                    dataCoun['cluster'] = cluster_sole1 + str(YEAR-1)[0:4] + cluster_sole2

                rep = requests.post(
                    url='https://www.scopus.com/standard/viewMore.uri', data=dataCoun,
                    headers=headers)
                latelyCoun0 = re.findall(r'btnText\\">(.*?)<', rep.text, re.S)
                print("\nlatelyCoun:")
                latelyCoun = len(latelyCoun0) / 2
                print(latelyCoun)
                dataSheet.write(index, 6, latelyCoun)
                time.sleep(1)

                # -----------------引用-------------------
                if year >= YEAR-1:
                    url = u1_sole + eid + u2_sole + str(YEAR-1)[0:4] + u3_sole
                else:
                    url = u1 + eid + u2 + str(YEAR-2)[0:4] + u3 + str(YEAR-1)[0:4] + u4
                print(url)
                page_source = requests.get(url=url, headers=headers, allow_redirects=False)
                count = re.findall(r'<span class="resultsCount">\n(.*?)\n</span>', page_source.text, re.S)
                print("latelyCites:")
                if count:
                    print(count[0])
                    dataSheet.write(index, 2, count[0])
                else:
                    dataSheet.write(index, 2, 0)
                print("\n")
        else:
            dataSheet.write(index, 2, 0)
            dataSheet.write(index, 3, 0)
            dataSheet.write(index, 4, 0)
            dataSheet.write(index, 5, 0)
            dataSheet.write(index, 6, 0)

        index = index + 1
        writebook.save(fileName)
        print("=======================================================================")







