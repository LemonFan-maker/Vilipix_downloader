from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
from lxml import etree
import os
import re
import sys
import argparse

# 判断illust账号是否符合标准
def determine(param):
    if re.match(r'\d{1,}', param):
        return 0
    else:
        print(param)
        print("illust不符合标准,退出.")
        os._exit(0)

# 检查illust存在
def webpages(illust):
    url = "https://www.vilipix.com/illust/"+str(illust)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
    }
    response = requests.get(url, headers=headers).status_code
    if response in range(200,300):
        return 0
    else:
        print("报错", response, "请检查illust是否存在.")
        os._exit(0)

# 下载图片
def downpic(illust):
    url = "https://www.vilipix.com/illust/"+str(illust)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('ul',attrs={'class':'illust-pages'})
    for one in data:
        img_url = re.findall("https://img9.vilipix.com/picture/pages/regular/(.*?)_p0_master1200.jpg?",str(one))
        img_date = re.sub('[\[\]\'\"]', '', str(img_url))
        real_url = "https://img9.vilipix.com/picture/pages/regular/"+str(img_date)+"_p0_master1200.jpg"
        pattern = "<img alt.{1,}/>"
        element = re.search(pattern, str(data)).group()
        tree = etree.HTML(element)
        alt = tree.xpath('//img/@alt')[0]
        print(alt)
        print(real_url)

if len(sys.argv)>1:
    param = str(sys.argv[1])
    determine(param)
    webpages(param)
    downpic(param)
else:
    print("没有输入")
    os._exit(0)