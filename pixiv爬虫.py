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
        os.makedirs('./image/', exist_ok=True)
        urlretrieve(real_url, './image/'+str(alt)+"."+str(name)+'.png')
        print("保存成功.")
else:
    print("illust账号不符合标准.")
    os._exit(0)