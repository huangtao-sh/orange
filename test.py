from orange.hclient import *
from orange.coroutine import *
from orange import *

async def main():
    async with Crawler('http://www.jianshu.com/') as sess:
        '''
        async def _(soup):
            print(soup.title.text)
        '''
        async def _(json):
            print(json)
        await wait([sess.get_json('http://localhost/vacation/2016',proc=_),
                       sess.get_json('http://localhost/vacation/2017',proc=_)])
                    
start(main())
