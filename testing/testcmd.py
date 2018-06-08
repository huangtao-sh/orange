import unittest
from orange.version import *
from orange import *


class TestVer(unittest.TestCase):
    def test_ver(self):
        for ver, seg, new_ver in (('1.0', 'o', '1.0.1a1'),
                                  ('1.0.1', 'n', '1.1a1'),
                                  ('1.0.1a1', '#', '1.0.1a2'),
                                  ('1.0.1a2', 'd', '1.0.1b1'),
                                  ('1.2.1a3', 'd', '1.2.1b1'),
                                  ('1.2.1b3', 'dev', '1.2.1'),
                                  ('1.3.4', 0, '2.0a1'),
                                  ):
            self.assertEqual(upgrade_ver(ver, seg), new_ver)

    def test_debug(self):
        '''
        from orange.debug import trace
        @trace
        def abc(a,b):
            return a+b            

        abc(1,20)
        '''

    def test_datetime(self):
        d = datetime.today()
        self.assertEqual(d % '%Y-%m-%d', d.strftime('%Y-%m-%d'))

    def test_py(self):
        self.assertEqual('ht', PY/'黄涛')
        self.assertEqual('huang tao', PY | '黄涛')

    def test_regex(self):
        self.assertEqual('test_case', convert_cls_name('TestCase'))

    '''
    def test_crawler(this):
        from orange.hclient import Crawler,wait,BS4
        class TestCrawler(Crawler):
            root='http://localhost'
            async def run(self):
                soup=await self.get_soup('blog')
                this.assertTrue(soup.title.text.startswith('Well'))
                await self.json()
            async def json(self):
                j=await self.get_json('vacation/2017')
                this.assertTrue('anpai' in j)
                
        TestCrawler.start()
    '''

    def test_args(self):
        @command(description='command show')
        def show():
            pass

        @command(description='command work')
        @arg('-a', '--appear')
        def work():
            pass

        @command(show, work, description='main command')
        @arg('-p', '--pear')
        def main():
            pass
