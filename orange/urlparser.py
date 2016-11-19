# 项目：标准库函数
# 模块：网而数据分析
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-11-19 16:56


from urllib import parse,request
from bs4 import BeautifulSoup as BeautifulSoup
from orange.path import *

def url_open(url,data=None,features='lxml',**kw):
    if data:
        url='%s?%s'%(url,parse.urlencode(data))
    with request.urlopen(url) as fn:
        data=fn.read()
        markup=decode(data)
    return BeautifulSoup(markup,features,**kw)
