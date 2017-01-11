# 项目：标准库函数
# 模块：网络爬虫
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-12-26 17:08

from aiohttp import *
from orange.coroutine import *
from orange import *
from bs4 import BeautifulSoup as BS4

__all__='Crawler','wait','BS4'

class Crawler(ClientSession):
    root=''
    def __init__(self,root=None,*args,**kw):
        if root:
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
            return await resp.text()

    async def get_soup(self,url,params=None,*args,**kw):
        text=await self.get_text(url,params=params,*args,**kw)
        return BS4(text,'lxml')

    async def download(self,url,params=None,path='.',*args,**kw):
        async with self.get(url,params=params,*args,**kw)as resp:
            path=Path(path)
            if path.is_dir():
                from urllib.parse import unquote
                # 获取文件名字段
                filename=resp.headers['Content-Disposition'] 
                filename=filename.split(';')[-1]  # 获取最后一个参数
                tp,filename=filename.split('=')
                if tp.strip()=='filename*':
                    filename=(filename.split("'"))[-1]
                if filename.startswith('"'):
                    filename=filename[1:-1]
                filename=unquote(filename)
                path=path / Path(filename).name
            path.write(data=await resp.read())
                    
    async def get_json(self,url,params=None,*args,encoding=None,
                           **kw):
        async with self.get(url,params=params,*args,**kw)as resp:
            return await resp.json(encoding=encoding)

    async def run(self):
        raise Exception('This function doesn''t exist!')

    @classmethod
    def start(cls,*args,**kw):
        async def _main():
            async with cls(*args,**kw)as sess:
                await sess.run()
        start(_main())
 
