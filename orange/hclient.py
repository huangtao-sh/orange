# 项目：标准库函数
# 模块：网络爬虫
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-12-26 17:08

from aiohttp import *
from orange.coroutine import *
from orange import *

class Crawler(ClientSession):
    def __init__(self,root=None,*args,**kw):
        root=root or ''
        if root.endswith('/'):
            root=root[:-1]
        self.root=root
        super().__init__(*args,**kw)

    def get_url(self,url):
        if ':' not in url:
            if url.startswith('/'):
                url=url[1:]
            url='/'.join([self.root,url])
        return url

    def post(self,url,data=None,*args,**kw):
        return super().post(self.get_url(url),*args,data=data,**kw)

    def get(self,url,params=None,*args,**kw):
        return super().get(self.get_url(url),*args,params=params,**kw)

    async def get_text(self,url,params=None,*args,**kw):
        async with self.get(url,*args,params=params,**kw)as resp:
            return resp.text()

    def get_soup(self,url,params=None,*args,**kw):
        from bs4 import BeautifulSoup as BS4
        return BS4(self.get_text(url,params=params,*args,**kw),'lxml')

    async def download(self,url,params=None,path='.',*args,**kw):
        async with self.get(url,params=params,*args,**kw)as resp:
            path=Path(path)
            if path.is_dir():
                from urllib.parse import unquote
                filename=resp.headers['Content-Disposition'] # 获取文件名字段
                filename=filename.split(';')[-1]  # 获取最后一个
                tp,filename=filename.split('=')
                if tp.strip()=='filename*':
                    filename=(filename.split("'"))[-1]
                if filename.startswith('"'):
                    filename=filename[1:-1]
                filename=unquote(filename)
                path=path / Path(filename).name
            path.write(data=await resp.read())
                    
    async def get_json(self,url,params=None,proc=None,*args,**kw):
        async with self.get(url,params=params,*args,**kw)as resp:
            return resp.json()

    '''
        
    async def get(self,url,params=None,proc=None,*args,**kw):
        url=self.get_url(url)
        async with await super().get(url,params=params,*args,**kw) as resp:
            if resp.status==200:
                if proc:
                    r=proc(resp)
                    if iscoroutine(r):
                        await r
                        
    async def get_text(self,url,params=None,proc=None,*args,**kw):
        async def _(resp):
            text=await resp.text()
            r=proc(text)
            if iscoroutine(r):
                await r
        await self.get(url,params,_ if proc else None,*args,**kw)
                    
    async def get_soup(self,url,params=None,proc=None,*args,**kw):
        from bs4 import BeautifulSoup as BS4
        async def _(text):
            r=proc(BS4(text,'lxml'))
            if iscoroutine(r):
                await r
        await self.get_text(url,params,_ if proc else None,*args,**kw)
        
    async def download(self,url,params=None,path='.',*args,**kw):
        from urllib.parse import unquote
        path=Path(path)
        async def _(resp):
            nonlocal path
            if path.is_dir():
                filename=resp.headers['Content-Disposition']
                filename=(R/r'filename="(.*?)"'%filename).group(1)
                filename=unquote(filename)
                path=path / Path(filename).name
            path.write(data=await resp.read())
        await self.get(url,params,proc=_,*args,**kw)
        
    async def get_json(self,url,params=None,proc=None,*args,**kw):
        async def _(resp):
            json=await resp.json()
            r=proc(json)
            if iscoroutine(r):
                await r
        await self.get(url,params,_ if proc else None,*args,**kw)
'''
