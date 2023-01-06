from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
from lxml import etree
import os
import re
name = input("illust号:")

# 低级方法
if re.match(r'\d{1,}', name):
    print("匹配成功.")
    url = "https://www.vilipix.com/illust/"+str(name)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    imglist = soup.find_all('img')
    lenth = len(imglist)  #计算集合的个数
    for i in range(lenth-1):
        data = str(imglist[i-1])
        list1 = data.split(" ")
        strlist = list1[1:3]
        strlist = ','.join(strlist)
        string = strlist.replace("'",'')
        s = 'alt="a",src="b"/>'
        result = re.findall(r'src="(.*?)"', string)[0]
        result = re.split(r'\?.{1,}',result)[0]
        print(result)


    #for one in data:
    #    img_url = soup.find_all("img")
    #    print(img_url)
else:
    print("illust账号不符合标准.")
    os._exit(0)