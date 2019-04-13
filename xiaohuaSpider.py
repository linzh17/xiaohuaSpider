import requests 
from pyquery import PyQuery as pq 

import json 

baseurl = 'http://xiaohua.zol.com.cn'

headers = {
    'Host':'xiaohua.zol.com.cn',
    'ReFerer':'http://xiaohua.zol.com.cn/new/',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Cookie':'z_pro_city=s_provice%3Dguangdong%26s_city%3Dguangzhou; userProvinceId=30; userCityId=347; userCountyId=0; userLocationId=9; lv=1555148545; vn=1; ip_ck=58KC4vzxj7QuMDUzNTY2LjE1NTUxNDg1NDU%3D; Hm_lvt_ae5edc2bc4fc71370807f6187f0a2dd0=1555148546; _ga=GA1.3.665815662.1555148546; _gid=GA1.3.317574655.1555148546; bdshare_firstime=1555148546616; questionnaire_pv=1555113607; Hm_lpvt_ae5edc2bc4fc71370807f6187f0a2dd0=1555150377; _gat=1; 7f79fd1f7ae9e6490eca2c63c04d181f=bv26fv1u2g39n3ch256u%7B%7BZ%7D%7D2%7B%7BZ%7D%7Dnull; 93f3d4f8e19ffac58e54d318a37efe74=bv26fv1u2g39n3ch256u%7B%7BZ%7D%7D2%7B%7BZ%7D%7Dnull; MyZClick_7f79fd1f7ae9e6490eca2c63c04d181f=/html/body/div%5B6%5D/div/div%5B2%5D/div/a/; MyZClick_93f3d4f8e19ffac58e54d318a37efe74=/html/body/div%5B6%5D/div/div%5B2%5D/div/a/',

}
def getPage(index):
    print('开始爬取')
    url = baseurl+'/new/{}.html'.format(str(index))
    response = requests.get(url = url,headers = headers)
    if response.status_code == 200:
        #print(response.text)
        text = response.text
        return  text
    else:
        return None


def parsePage(text):
    print('解析页面')
    doc = pq(text)
    xiaohuaList = doc('.article-list li').items()
    print(xiaohuaList)
    for item in xiaohuaList:
        print(item.children('.article-title a'))
        href = item.children('.article-title a').attr.href
        print(href)
        if href == None:
            continue
        url = baseurl+href
        
        content = getXiaohua(url)
        yield{
            'content':content
        }


        
def getXiaohua(url):
    response = requests.get(url = url ,headers=headers)
    if response.status_code == 200:
        text = response.text
        doc = pq(text)
        content = doc('.article-text').text()
        return content

def writeItem(item):
    with open('xiaohua.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False)+'\n')

def startSpider():
    index = 2
    while True:
        print('爬取'+str(index)+'页')
        result = getPage(index)
        if result != None:
            for item in parsePage(result):
                writeItem(item)
            index = index+1
        else:
            print('结束')
            break

startSpider()