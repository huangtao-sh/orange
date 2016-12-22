# 项目：标准库函数
# 模块：网络爬虫
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-12-21 19:54

from requests import *
from bs4 import BeautifulSoup as BS4
from os.path import join

class Crawler(Session):
    '''网络爬虫'''
    def sget(self,url,params=None,features='lxml',proc=None,**kw):
        reponse=self.get(url,params=params)
        '''向网络获取内容，并直接转换成BeautifulSoup实例'''
        if reponse:
            soup=BS4(reponse.text,features,**kw)
        if callable(proc):
            proc(soup)
        return soup

    def __init__(self,root=None):
        '''初始化，可以指定根目录'''
        if root:
            if not ':' in root:
                root='http://%s'%(root)
            if root.endswith('/'):
                root=root[:-1]
        self._root=root or ''
        super().__init__()

    def request(self,method,url,**kw):
        '''网络请求'''
        if not ':' in url:
            if url.startswith('/'):
                url=url[1:]
            url='/'.join([self._root,url])
        return super().request(method,url,**kw)

    def get(self,url,params=None,**kw):
        return super().get(url,params=params,**kw)
    
    def download(self,url,params=None,filename,**kw):
        '''下载文件'''
        reponse=self.get(url,params=params,**kw)
        if reponse:
            Path(filename).write(data=reponse.content)
            
