import urllib.request

import xlwt
from bs4 import BeautifulSoup
import requests
import xlrd
import time
import re

YEAR = 2018

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'scopus.machineID=565E426BB5379DC87C63C542901909C3.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1587562861883r0.38711136738597673; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22referral%22%7D; optimizelyBuckets=%7B%7D; xmlHttpRequest=true; __cfduid=d954c5c2b9549289b92a76b614def85111601106950; SCSessionID=7936DF1A18E9AF9EA137B3B62CA7AC76.i-04ff8b9e76c8bf1fe; scopusSessionUUID=06ca8f33-6b2c-4ac7-a; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB13375EED7A6E356D054B2696F16B25CCFDA56F468A6258FAD8C4CE9D504F131B4A31AAC5A6BDE3E4B4DACF34F3854CEEB0E3252CD978C6598BCBD3CE542C873F5; at_check=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; javaScript=true; mbox=PC#7f4649f1b841468a940386570b585808.38_0#1665026106|session#45ea7dac4d004f07966f7924b9d870a6#1601783040; s_pers=%20v8%3D1601781305213%7C1696389305213%3B%20v8_s%3DLess%2520than%25207%2520days%7C1601783105213%3B%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1601783105227%3B%20v68%3D1601781302422%7C1601783105241%3B; s_sess=%20e41%3D1%3B%20s_cpc%3D1%3B%20s_cc%3Dtrue%3B; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=359503849%7CMCIDTS%7C18540%7CMCMID%7C09635205066540933810671114848219444600%7CMCAAMLH-1602386105%7C11%7CMCAAMB-1602386105%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1601788505s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18382%7CvVersion%7C5.0.1%7CMCCIDH%7C1249006796; screenInfo="900:1440"',
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

cluster_sole1 = 'scopubyr,\"'
cluster_sole2 = '\",t'

cluster1 = 'scopubyr,\"'
# 2017
cluster2 = '\",t,\"'
# 2016
cluster3 = '\",t'

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


def serch(url,headers):
    req = urllib.request.Request(url=url, headers=headers)
    rsp = urllib.request.urlopen(req,timeout=20000)
    html = rsp.read().decode()
    s = BeautifulSoup(html, 'html.parser')
    return s

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
    dataSheet.write(0, 2, '早两年被引次数')
    dataSheet.write(0, 3, '早两年被引学科数')
    dataSheet.write(0, 4, '早两年来源出版物数')
    dataSheet.write(0, 5, '早两年被引机构数')
    dataSheet.write(0, 6, '早两年被引国家数')

def get_subjectArea(page_source):
    subData0 = re.findall(r'<label class="checkbox-label" for=\'cat_SUBJAREA(.*?)\n</label>', page_source, re.S)
    subData = re.findall(r'class="btnText">\\n(.*?)\\n</span>', str(subData0), re.S)
    return subData

def get_country(page_source):
    counData0 = re.findall(r'<label class="checkbox-label" for=\'cat_COUNTRY(.*?)\n</label>', page_source, re.S)
    counData = re.findall(r'class="btnText">\\n(.*?)\\n</span>', str(counData0), re.S)
    return counData

def get_source(page_source):
    subData0 = re.findall(r'<label class="checkbox-label" for=\'cat_EXACTSRCTITLE(.*?)\n</label>', page_source, re.S)
    subData = re.findall(r'class="btnText">\\n(.*?)\\n</span>', str(subData0), re.S)
    return subData

if __name__ == '__main__':

    # 设置收集起始序号
    indexStart = 211
    indexEnd = 328

    # 获取代收数据
    papers = get_excel(indexStart, indexEnd)

    # 创建收取数据文件
    fileName = '../data/' + str(indexStart) + '-' + str(indexEnd) + '早两年特征收取结果.xls'
    print(fileName)
    writebook = xlwt.Workbook()  # 打开excel
    dataSheet = writebook.add_sheet('data')  # 添加一个名字叫data的sheet
    # 写入表头，方便查阅
    get_data_excel_head(dataSheet)
    writebook.save(fileName)

    # 初始化数据
    index = 1

    for paper in papers:
        eid = paper['EID']
        year = paper['年份']
        dataSheet.write(index, 0, paper['序号'])
        dataSheet.write(index, 1, paper['标题'])
        writebook.save(fileName)

        # ====================================1=====================================

        if eid != '':
            if year >= YEAR-1:
                url = u1_sole + eid + u2_sole + str(YEAR-1)[0:4] + u3_sole
            else:
                url = u1 + eid + u2 + str(year+2)[0:4] + u3 + str(year+1)[0:4] + u4
            print(url)
            page_source = requests.get(url=url, headers=headers, allow_redirects=False)
            # -----------------引用-------------------
            count = re.findall(r'<span class="resultsCount">\n(.*?)\n</span>', page_source.text, re.S)
            print("earlyCites:")
            if count:
                print(count[0])
                dataSheet.write(index, 2, count[0])
            else:
                dataSheet.write(index, 2, 0)
            print("\n")
            # -----------------学科-------------------

            subjectArea = get_subjectArea(page_source.text)
            earlySub = len(subjectArea)
            if earlySub >= 10:
                dataSub = data
                dataSub['navigatorName'] = navigatorNameSub
                dataSub['clusterCategory'] = clusterCategorySub
                dataSub['cite'] = eid
                dataSub['cluster'] = cluster1 + str(year+2)[0:4] + cluster2 + str(year+1)[0:4] + cluster3
                if year >= YEAR-1:
                    dataSub['cluster'] = cluster_sole1 + str(YEAR-1)[0:4] + cluster_sole2

                rep = requests.post(
                    url='https://www.scopus.com/standard/viewMore.uri', data=dataSub,
                    headers=headers)
                earlySub0 = re.findall(r'btnText\\">(.*?)<', rep.text, re.S)
                subjectArea = earlySub0
                earlySub = len(earlySub0) / 2
            print("Subject area:")
            print(subjectArea)
            print(earlySub)
            print("\n")
            dataSheet.write(index, 3, earlySub)
            time.sleep(1)

            # -----------------来源-------------------


            source = get_source(page_source.text)
            earlySource = len(source)

            if earlySource >= 10:
                dataSource = data
                dataSource['navigatorName'] = navigatorNameSource
                dataSource['clusterCategory'] = clusterCategorySource
                dataSource['cite'] = eid
                dataSource['cluster'] = cluster1 + str(year+2)[0:4] + cluster2 + str(year+1)[0:4] + cluster3
                if year >= YEAR-1:
                    dataSource['cluster'] = cluster_sole1 + str(YEAR-1)[0:4] + cluster_sole2

                rep = requests.post(
                    url='https://www.scopus.com/standard/viewMore.uri', data=dataSource,
                    headers=headers)
                earlySource0 = re.findall(r'btnText\\">(.*?)<', rep.text, re.S)
                source = earlySource0
                earlySource = len(earlySource0) / 2
            print("Source:")
            print(source)
            print(earlySource)
            print("\n")
            dataSheet.write(index, 4, earlySource)
            time.sleep(1)

            # -----------------机构-------------------
            dataAffi = data
            dataAffi['navigatorName'] = navigatorNameAffi
            dataAffi['clusterCategory'] = clusterCategoryAffi
            dataAffi['cite'] = eid
            dataAffi['cluster'] = cluster1 + str(year + 2)[0:4] + cluster2 + str(year + 1)[0:4] + cluster3
            if year >= YEAR-1:
                dataAffi['cluster'] = cluster_sole1 + str(YEAR-1)[0:4] + cluster_sole2

            rep = requests.post(
                url='https://www.scopus.com/standard/viewMore.uri', data=dataAffi,
                headers=headers)
            earlyAffi0 = re.findall(r'btnText\\">(.*?)<', rep.text, re.S)
            affilication = earlyAffi0
            earlyAffi = len(earlyAffi0) / 2
            print("Affilication:")
            print(affilication)
            print(earlyAffi)
            print("\n")
            dataSheet.write(index, 5, earlyAffi)
            time.sleep(1)

            # -----------------国家-------------------

            country = get_country(page_source.text)
            earlyCoun = len(country)

            if earlyCoun == 10:
                dataCoun = data
                dataCoun['navigatorName'] = navigatorNameCoun
                dataCoun['clusterCategory'] = clusterCategoryCoun
                dataCoun['cite'] = eid
                dataCoun['cluster'] = cluster1 + str(year + 2)[0:4] + cluster2 + str(year + 1)[0:4] + cluster3
                if year >= YEAR-1:
                    dataCoun['cluster'] = cluster_sole1 + str(YEAR-1)[0:4] + cluster_sole2

                rep = requests.post(
                    url='https://www.scopus.com/standard/viewMore.uri', data=dataCoun,
                    headers=headers)
                earlyCoun0 = re.findall(r'btnText\\">(.*?)<', rep.text, re.S)
                country = earlyCoun0
                earlyCoun = len(earlyCoun0) / 2

            print("Country:")
            print(country)
            print(earlyCoun)
            print("\n")
            dataSheet.write(index, 6, earlyCoun)
            time.sleep(1)

        else:
            dataSheet.write(index, 2, 0)
            dataSheet.write(index, 3, 0)
            dataSheet.write(index, 4, 0)
            dataSheet.write(index, 5, 0)
            dataSheet.write(index, 6, 0)

        index = index + 1
        writebook.save(fileName)
        print("=======================================================================")



