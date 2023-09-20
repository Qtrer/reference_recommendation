import requests
import io
import xlrd
import time
import re
import sys
import xlwt

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': '__cfduid=d17128132556b29731cbfef8de9be7b731603349641; SCSessionID=11F7A3F71379DD03F1F60B335998A735.i-0c4c3d3d024279f01; scopusSessionUUID=d0310f56-e809-4cb9-8; scopus.machineID=11F7A3F71379DD03F1F60B335998A735.i-0c4c3d3d024279f01; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1D72C995BEC855D78A7BC15617CA44A2FBEE90A4EB31143EE3AF1171BFCBADA40BAFDF2ADE925350150D7900CAD0CA8A6BE26E9A523E25F8FDF161F36517F33E1; at_check=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=359503849%7CMCIDTS%7C18558%7CMCMID%7C37341042514334149960217821896021463503%7CMCAAMLH-1603954480%7C11%7CMCAAMB-1603954480%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1603356880s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-18565%7CMCCIDH%7C1246701492%7CvVersion%7C5.0.1; mbox=session#2c2148f5bf69439cbb0e37cba6bc0fbc#1603351527|PC#2c2148f5bf69439cbb0e37cba6bc0fbc.38_0#1666594526; s_pers=%20v8%3D1603349727992%7C1697957727992%3B%20v8_s%3DFirst%2520Visit%7C1603351527992%3B%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1603351528019%3B%20v68%3D1603349724890%7C1603351528051%3B; s_sess=%20s_cpc%3D0%3B%20s_cc%3Dtrue%3B%20e41%3D1%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C39%252C39%252C396%252C1920%252C396%252C1280%252C720%252C1%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Adocument%252520searchform%252C39%252C39%252C396%252C1560%252C314%252C1280%252C720%252C1%252CP%3B',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}
headerDetail = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'scopus.machineID=565E426BB5379DC87C63C542901909C3.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1587562861883r0.38711136738597673; optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22referral%22%7D; optimizelyBuckets=%7B%7D; xmlHttpRequest=true; __cfduid=d954c5c2b9549289b92a76b614def85111601106950; SCSessionID=7BCE83825C0E7BB09D8709B3F855D307.i-09332002b2788427d; scopusSessionUUID=78acca6a-31ef-4212-9; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB11CCFA00974352D50DA1FCC2256F108F763A4097648817510BC913BD12D46BFFF8278FC278415EC1A7924B82E83258A309EB9C4B6D8DEE046F1987799469E9766; javaScript=true; at_check=true; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=359503849%7CMCIDTS%7C18550%7CMCMID%7C09635205066540933810671114848219444600%7CMCAAMLH-1603281891%7C11%7CMCAAMB-1603281891%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1602684291s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C5.0.1%7CMCCIDH%7C1246701492; screenInfo="900:1440"; __cfruid=32f33f3fbff08a43614b7f58ab3f5db440a9bf1b-1602677109; mbox=PC#7f4649f1b841468a940386570b585808.38_0#1665921923|session#36f85b85286c4faea060e50392457eb0#1602678950; s_pers=%20c19%3Dsc%253Arecord%253Adocument%2520record%7C1602678927673%3B%20v68%3D1602677120020%7C1602678927714%3B%20v8%3D1602677127753%7C1697285127753%3B%20v8_s%3DLess%2520than%25207%2520days%7C1602678927753%3B; s_sess=%20s_cpc%3D0%3B%20c21%3Dtitle-abs-key%2528science%2529%3B%20e13%3Dtitle-abs-key%2528science%2529%253A1%3B%20c13%3Ddate%2520%2528newest%2529%3B%20e78%3Dtitle-abs-key%2528science%2529%3B%20s_sq%3D%3B%20e41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C36%252C36%252C368%252C1440%252C368%252C1440%252C900%252C1%252CP%3B%20s_ppv%3Dsc%25253Arecord%25253Adocument%252520record%252C2%252C2%252C454%252C1440%252C454%252C1440%252C900%252C1%252CP%3B',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
}

url1 = 'https://www.scopus.com/results/results.uri?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1='
url2 = '&field1=DOI&dateType=Publication_Date_Type&yearFrom=Before+1960&yearTo=Present&loadDate=7&documenttype=All&accessTypes=All&resetFormLink=&st1='
url3 = '&st2=&sot=b&sdt=b&sl=22&s=DOI%28'
url4 = '%29&sid=04d9016932b494f613c131f956db3e87&searchId=04d9016932b494f613c131f956db3e87&txGid=cd4965c8585c87e1b28188380fa2685e&sort=plf-f&originationType=b&rr='

citationturl1 = 'https://www.scopus.com/search/submit/citedby.uri?eid='
citationturl2 = '&src=s&origin=recordpage'

snipurl = 'https://www.scopus.com/api/rest/sources/'

detail1 = 'https://www.scopus.com/record/display.uri?eid='
# 2-s2.0-84944149175
detail2 = '&origin=resultslist&sort=plf-f&src=s&st1='
# 10.1007
detail3 = '%2f'
# s11192-014-1269-8
detail4 = '&st2=&sid=bf43c8536b4c20bfb146383e8ae724aa&sot=b&sdt=b&sl=30&s=DOI%2810.'
# 1007
detail5 = '%2f'
# s11192-014-1269-8
detail6 = '%29&relpos=0&citeCnt=46&searchTerm='

snip1 = 'https://www.scopus.com/results/results.uri?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1='
# 10.1016%2Fj.joi.2009.11.002
snip2 = '&field1=DOI&dateType=Publication_Date_Type&yearFrom=Before+1960&yearTo=Present&loadDate=7&documenttype=All&accessTypes=All&resetFormLink=&st1='
# 10.1016%2Fj.joi.2009.11.002
snip3 = '&st2=&sot=b&sdt=b&sl=30&s=DOI%28'
# 10.1016%2Fj.joi.2009.11.002
snip4 = '%29&sid=f90ade8a461ec3d0e4486e0fb8eb8e48&searchId=f90ade8a461ec3d0e4486e0fb8eb8e48&txGid=7d30969d45fa0773883a37d730690f93&sort=plf-f&originationType=b&rr='
# snip web
snip5 = 'https://www.scopus.com/api/rest/sources/'

def Cheak_main_words(mainWords,mainWordsChe):
    if mainWords ==mainWordsChe:
        return 1
    else:
        return 0

def get_main_words(page_source):
    mainWords0 = re.findall(r'<div class="sciTopicsVal displayNone"(.*?)</div>', page_source.text, re.S)
    mainWords = re.findall(r'"name":"(.*?)","id', str(mainWords0), re.S)
    return mainWords

def Cheak_H(HChe0,HChe1,HChe2):
    H = ['X']
    if HChe0 == HChe1 or HChe0 ==HChe2:
        H = HChe0
    if HChe1 ==HChe2:
        H = HChe1
    return H

# 旧：拉取整个网页，获取h
def get_HUrl(page_source):
    H = []
    hIndexUrls0 = re.findall(r'<section id="authorlist(.*?)</section>', page_source.text, re.S)
    hIndexUrls = re.findall(r'type="hidden"><a href="(.*?)" title="', str(hIndexUrls0), re.S)
    for hIndexUrl in hIndexUrls:
        hIndexUrl_source = requests.get(url=hIndexUrl, headers=headerDetail, allow_redirects=False)
        print(hIndexUrl_source.text)
        hIndex0 = re.findall(r'h</span>-index:(.*?)<button type=', hIndexUrl_source.text, re.S)
        hIndex = re.findall(r'<span class="fontLarge">(.*?)</span>', str(hIndex0), re.S)
        if hIndex:
            H.append(hIndex[0])
    return H

# 新：仅拉取h所在的特定请求
def get_H(page_source):
    H = []
    authorId0 = re.findall(r'<section id="authorlist(.*?)</section>', page_source.text, re.S)
    authorIds = re.findall(r'authorId=(.*?)&amp;amp;', str(authorId0), re.S)
    for authorId in authorIds:
        hIndexUrl = 'https://www.scopus.com/api/authors/' + authorId + '?&_=1602679106234'
        hIndexUrl_source = requests.get(url=hIndexUrl, headers=headerDetail, allow_redirects=False)
        hIndex0 = re.findall(r'"hindex":(.*?),"coAuthorsCount', hIndexUrl_source.text, re.S)
        if hIndex0:
            H.append(int(hIndex0[0]))
    return H

def Cheak_SnipSjrRpNew(snipSjrRp,snipSjrRpChe):
    if snipSjrRp ==snipSjrRpChe:
        return 1
    else:
        return 0

def get_SnipSjrRpNew(url):
    dataSnipSjrRp = []
    page_source = requests.get(url=url, headers=headers, allow_redirects=False)
    data0 = re.findall(r'<td data-type="source">\n<a href="(.*?)class="ddmDocSource"', page_source.text, re.S)
    if data0:
        data1 = data0[0]
        data2 = data1[10:21]
        snipUrl = snip5 + data2
        s1 = requests.Session()
        page_source1 = s1.get(snipUrl, headers=headers, allow_redirects = False)
        datasnip = re.findall(r'<name>SNIP</name><value>(.*?)</value>', page_source1.text, re.S)
        if datasnip:
            dataSnipSjrRp.append(datasnip[0])
        else:
            dataSnipSjrRp.append('')

        datasjr = re.findall(r'<name>SJR</name><value>(.*?)</value>', page_source1.text, re.S)
        if datasjr:
            dataSnipSjrRp.append(datasjr[0])
        else:
            dataSnipSjrRp.append('')

        datarp = re.findall(r'<name>RP</name><value>(.*?)</value>', page_source1.text, re.S)
        if datarp:
            dataSnipSjrRp.append(datarp[0])
        else:
            dataSnipSjrRp.append('')

        return dataSnipSjrRp

    else:
        return []

def get_SnipSjrRp(url):
    dataSnipSjrRp = []
    page_source = requests.get(url=url, headers=headers, allow_redirects=False)
    data0 = re.findall(r'<td data-type="source">\n<a href="(.*?)class="ddmDocSource"', page_source.text, re.S)
    print(data0)
    if data0:
        data1 = data0[0]
        data2 = data1[10:20]
        snipUrl = snip5 + data2
        s1 = requests.Session()
        page_source1 = s1.get(snipUrl, headers=headers, allow_redirects = False)
        print(page_source1.text)
        print(snipUrl)
        datasnip0 = re.findall(r'name>SNIP&lt;/name>(.*?)/value>', page_source1.text, re.S)
        datasnip = re.findall(r'&lt;value>(.*?)&lt;', str(datasnip0), re.S)
        if datasnip:
            dataSnipSjrRp.append(datasnip[0])
            print(dataSnipSjrRp)
        else:
            dataSnipSjrRp.append('')

        datasjr0 = re.findall(r'name>SJR&lt;/name>(.*?)/value>', page_source1.text, re.S)
        datasjr = re.findall(r'&lt;value>(.*?)&lt;', str(datasjr0), re.S)
        if datasjr:
            dataSnipSjrRp.append(datasjr[0])
        else:
            dataSnipSjrRp.append('')

        datarp0 = re.findall(r'name>RP&lt;/name>(.*?)/value>', page_source1.text, re.S)
        datarp = re.findall(r'&lt;value>(.*?)&lt;', str(datarp0), re.S)
        if datarp:
            dataSnipSjrRp.append(datarp[0])
        else:
            dataSnipSjrRp.append('')

        return dataSnipSjrRp

    else:
        return []

def get_subjectArea(page_source):
    subData0 = re.findall(r'<label class="checkbox-label" for=\'cat_SUBJAREA(.*?)\n</label>', page_source, re.S)
    subData = re.findall(r'class="btnText">\\n(.*?)\\n</span>', str(subData0), re.S)
    return subData

def get_country(page_source):
    counData0 = re.findall(r'<label class="checkbox-label" for=\'cat_COUNTRY(.*?)\n</label>', page_source, re.S)
    counData = re.findall(r'class="btnText">\\n(.*?)\\n</span>', str(counData0), re.S)
    return counData

def get_excel(indexStart,indexEnd):
    file = "D:/我的桌面/临时实验/sno1-30.xls"
    data = xlrd.open_workbook(file, formatting_info=True)
    table = data.sheet_by_name('Sheet2')
    papers = []
    for i in range(indexStart,indexEnd):
        paper = {}
        content = table.row_values(i)
        paper['种子序号'] = content[0]
        paper['被引序号'] = content[1]
        paper['标题'] = content[4]
        paper['年份'] = content[5]
        paper['来源出版物名称'] = content[6]
        paper['DOI'] = content[14]
        paper['EID'] = content[44]
        print(i+1)
        print(paper['标题'])

        papers.append(paper)
    return papers

def get_data_excel_head(dataSheet):
    dataSheet.write(0, 0, '种子序号+被引序号')
    dataSheet.write(0, 1, '标题')
    dataSheet.write(0, 2, '作者h指数')
    dataSheet.write(0, 3, '主题词')
    dataSheet.write(0, 4, '国家')
    dataSheet.write(0, 5, '机构')
    dataSheet.write(0, 6, '学科')
    dataSheet.write(0, 7, 'rp')
    dataSheet.write(0, 8, 'sjr')
    dataSheet.write(0, 9, 'snip')

if __name__ == '__main__':
    # 设置收集起始序号
    indexStart = 11
    indexEnd = 21

    # 获取代收数据
    papers = get_excel(indexStart,indexEnd)

    # 创建收取数据文件
    fileName = 'D:/我的桌面/临时实验/' + str(indexStart) + '-' + str(indexEnd - 1) + '基本特征h收取结果.xls'
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
        doi = paper['DOI']
        dataSheet.write(index, 0, str(paper['种子序号'])+ ' + ' + str(paper['被引序号']))
        dataSheet.write(index, 1, paper['标题'])
        writebook.save(fileName)

        # ====================================1=====================================
        if doi != '':
            url = url1 + doi + url2 + doi + url3 + doi + url4
            page_source = requests.get(url=url, headers=headers, allow_redirects=False)

            # # -----------------学科-------------------
            # subjectArea = get_subjectArea(page_source.text)
            # print("Subject area:")
            # print(subjectArea)
            # print("\n")
            # dataSheet.write(index, 6, subjectArea)
            #
            # # -----------------国家-------------------
            # print("Country:")
            # country = get_country(page_source.text)
            # print(country)
            # print("\n")
            # dataSheet.write(index, 4, country)
            # time.sleep(1)

            detailUrl1 = re.findall(r'<td data-type="docTitle">(.*?)</td>', page_source.text, re.S)
            detailUrl2 = re.findall(r'href="(.*?)"class="ddmDocTitle"', str(detailUrl1), re.S)
            if detailUrl2:
                detailUrl = detailUrl2[0].replace('amp;', '')
                page_source = requests.get(url=detailUrl, headers=headerDetail, allow_redirects=False)

                # -----------------H指数-------------------
                print("H Index:")
                # HChe0 = get_H(page_source)
                # time.sleep(1)
                # HChe1 = get_H(page_source)
                # time.sleep(1)
                # HChe2 = get_H(page_source)
                # H = Cheak_H(HChe0,HChe1,HChe2)
                H = get_H(page_source)
                print(H)
                if H != ['X']:
                    if H:
                        maxH = max(H)
                        dataSheet.write(index, 2, maxH)
                        print(maxH)
                        print("\n")
                    else:
                        dataSheet.write(index, 2, "NONE")
                else:
                    dataSheet.write(index, 2, "ERROR")

                # -----------------主题词-------------------
                # print("Main Words:")
                # mainWords = get_main_words(page_source)
                # mainWordsCHe = get_main_words(page_source)
                # flag = Cheak_main_words(mainWords,mainWordsCHe)
                # if(flag ==1):
                #     dataSheet.write(index, 3, mainWords)
                #     print(mainWords)
                #     print("\n")
                # else:
                #     dataSheet.write(index, 3, "ERROR")
            else:
                dataSheet.write(index, 2, "NONE")
                # dataSheet.write(index, 3, "NONE")
            time.sleep(1)
        else:
            dataSheet.write(index, 2, "NONE")
            # dataSheet.write(index, 3, "NONE")
            # dataSheet.write(index, 4, "NONE")
            # dataSheet.write(index, 6, "NONE")
        # ====================================2=====================================
        # if doi != '':
        #     # -----------------机构--------------------
        #     s = 'DOI(' + doi + ')'
        #     st1 = doi
        #     data = {
        #         'clusterDisplayCount': '10',
        #         'sot': 'b',
        #         'navigatorName': 'AFFIL',
        #         'clusterCategory': 'selectedAffiliationClusterCategories',
        #         'cite': '',
        #         'refeid': '',
        #         'refeidnss': '',
        #         's': s,
        #         'st1': st1,
        #         'st2': '',
        #         'sid': 'e635e35a50254e190a9379ccc39a7b30',
        #         'sdt': 'b',
        #         'sort': 'plf-f',
        #         'citingId': '',
        #         'citedAuthorId': '',
        #         'listId': '',
        #         'origin': 'resultslist',
        #         'src': 's',
        #         'affilCity': '',
        #         'affilName': '',
        #         'affilCntry': '',
        #         'affiliationId': '',
        #         'cluster': '',
        #         'offset': '1',
        #         'scla': '',
        #         'scls': '',
        #         'sclk': '',
        #         'scll': '',
        #         'sclsb': '',
        #         'sclc': '',
        #         'scfs': '',
        #         'ref': '',
        #         'isRebrandLayout': 'true',
        #     }
        #     rep = requests.post(
        #         url='https://www.scopus.com/standard/retrieveClusterAttributes.uri', data=data,
        #         headers=headers)
        #     affiliation = re.findall(r'class="btnText">(.*?)</span>', rep.text, re.S)
        #     print("\nAffiliation:")
        #     print(affiliation)
        #     dataSheet.write(index, 5, affiliation)
        #     time.sleep(1)
        # else:
        #     dataSheet.write(index, 5, "NONE")
        # ====================================3=====================================
        # if doi != '':
        #     # --------------SNIP SJR RP----------------
        #     doiSnip = doi.replace('/', '%2F')
        #     urlSnip0 = snip1 + doiSnip + snip2 + doiSnip + snip3 + doiSnip + snip4
        #     snipSjrRp = get_SnipSjrRpNew(urlSnip0)
        #     time.sleep(1)
        #     snipSjrRpChe = get_SnipSjrRpNew(urlSnip0)
        #     flag = Cheak_SnipSjrRpNew(snipSjrRp, snipSjrRpChe)
        #     if flag == 1:
        #         if snipSjrRp:
        #             snip = snipSjrRp[0]
        #             sjr = snipSjrRp[1]
        #             rp = snipSjrRp[2]
        #             dataSheet.write(index, 9, snip)
        #             dataSheet.write(index, 8, sjr)
        #             dataSheet.write(index, 7, rp)
        #             print("SNIP:" + snip + "  SJR:" + sjr + "  RJ:" + rp)
        #             print("\n")
        #         else:
        #             dataSheet.write(index, 9, "NONE")
        #             dataSheet.write(index, 8, "NONE")
        #             dataSheet.write(index, 7, "NONE")
        #     else:
        #         dataSheet.write(index, 9, "ERROR")
        #         dataSheet.write(index, 8, "ERROR")
        #         dataSheet.write(index, 7, "ERROR")
        #     time.sleep(1)
        #
        # else:
        #     dataSheet.write(index, 9, "NONE")
        #     dataSheet.write(index, 8, "NONE")
        #     dataSheet.write(index, 7, "NONE")
        index = index + 1
        writebook.save(fileName)
        print("=======================================================================")


