# 项目：标准库函数
# 模块：网络爬虫
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-12-21 19:54

from requests import *
from bs4 import BeautifulSoup
from os.path import join

class Crawler(Session):
    def sget(self,url,params=None,features='lxml',proc=None,**kw):
        reponse=self.get(url,params=params)
        if reponse:
            soup=BeautifulSoup(reponse.text,features,**kw)
        if callable(proc):
            proc(soup)
        return soup

    def __init__(self,root=None):
        if root:
            if not ':' in root:
                root='http://%s'%(root)
            if root.endswith('/'):
                root=root[:-1]
        self._root=root or ''
        super().__init__()

    def request(self,method,url,**kw):
        if not ':' in url:
            if url.startswith('/'):
                url=url[1:]
            url='/'.join([self._root,url])
        return super().request(method,url,**kw)
                    
