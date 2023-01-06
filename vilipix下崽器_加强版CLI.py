from bs4 import BeautifulSoup
import requests
from urllib.request import urlretrieve
from lxml import etree
import os
import re
import sys
import logging
import argparse

parser = argparse.ArgumentParser(description='下载vilipix的图片', add_help=False)

action_group = parser.add_argument_group("程序")
action_group.add_argument('illust', type=str, nargs="+", help='vilipix的illust号')

help_group = parser.add_argument_group("帮助")
help_group.add_argument('-h', "--help", action="help", help="查看帮助信息")

log_group = parser.add_argument_group("日志")
log_group.add_argument('-l', "--log", action="store_true", help="日志保存")

def callback(param):
    return param

def webpages(illust):
    url = "https://www.vilipix.com/illust/"+str(illust)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
    }
    response = requests.get(url, headers=headers).status_code
    if response in range(200,300):
        return 0
    else:
        print("报错",response,"请检查illust是否存在.")
        os._exit(0)

def downpic(illust):
    url = "https://www.vilipix.com/illust/"+str(illust)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('ul',attrs={'class':'illust-pages'})
    imglist = soup.find_all('img')
    lenth = len(imglist)  #计算集合的个数
    for i in range(lenth-1):
        dt = str(imglist[i-1])
        list1 = dt.split(" ")
        strlist = list1[1:3]
        strlist = ','.join(strlist)
        string = strlist.replace("'",'')
        result = re.findall(r'src="(.*?)"', string)[0]
        result = re.split(r'\?.{1,}',result)[0]
        print(result)

    for one in data:
        img_url = re.findall("https://img9.vilipix.com/picture/pages/regular/(.*?)_p0_master1200.jpg?",str(one))
        img_date = re.sub('[\[\]\'\"]', '', str(img_url))
        real_url = "https://img9.vilipix.com/picture/pages/regular/"+str(img_date)+"_p0_master1200.jpg"
        pattern = "<img alt.{1,}/>"
        element = re.search(pattern, str(data)).group()
        tree = etree.HTML(element)
        alt = tree.xpath('//img/@alt')[0]
        #print("准备下载",alt)
        return real_url, alt

def save(url,alt,illust):
    abs = sys.path[0]
    downdir = abs+"\\images\\"
    if os.path.exists(downdir):
        print('目录存在,忽略')
    else:    
        print("目录不存在,创建.")
        os.makedirs("images")
    os.chdir(downdir)
    urlretrieve(url, str(alt)+"."+str(illust)+'.png')
            
args = parser.parse_args()
param = parser.parse_args().illust
data = param[0]
illust = callback(data)
webpages(data)
real_url, alt = downpic(data)
save(real_url,alt,illust)