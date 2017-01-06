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
        from orange.hclient import Crawler,wait
        class CrawlerTest(Crawler):
            async def run(self):
                url='https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=2017-01-10&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=HZH&purpose_codes=ADULT'
                x=await self.get_json(url)
                print(x)
        CrawlerTest.start()
