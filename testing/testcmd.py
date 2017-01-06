import unittest
from orange.version import *
from orange import *


class TestVer(unittest.TestCase):
    def test_ver(self):
        for ver,seg,new_ver in (('1.0','o','1.0.1a1'),
                                ('1.0.1','n','1.1a1'),
                                ('1.0.1a1','#','1.0.1a2'),
                                ('1.0.1a2','d','1.0.1b1'),
                                ('1.2.1a3','d','1.2.1b1'),
                                ('1.2.1b3','dev','1.2.1'),
                                ('1.3.4',0,'2.0a1'),
                                ):
            self.assertEqual(upgrade_ver(ver,seg),new_ver)
    def test_debug(self):
        '''
        from orange.debug import trace
        @trace
        def abc(a,b):
            return a+b            

        abc(1,20)
        '''
    def test_datetime(self):
        import datetime as dt

    def test_py(self):
        self.assertEqual('ht',PY/'黄涛')
        self.assertEqual('huang tao',PY|'黄涛')

    def test_crawler(self):
        from orange.hclient import Crawler,start
        url='http://localhost/exchange/download'
        async def download():
            async with Crawler() as sess:
                await sess.download(url)
                print('下载文件成功')

        start(download())
