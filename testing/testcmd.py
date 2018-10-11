import unittest
from orange import datetime, convert_cls_name, command, arg, PY
from orange.pykit import Ver
from orange import tempfile, tempdir


class TestVer(unittest.TestCase):
    def test_ver(self):
        self.assertEqual(Ver('1.2a1').upgrade('#'), Ver('1.2a2'))
        self.assertEqual(Ver('1.2a1').upgrade(3), Ver('1.2b1'))
        self.assertEqual(Ver('1.2').upgrade(1), Ver('1.3a1'))

    def test_datetime(self):
        d = datetime.today()
        self.assertEqual(d % '%Y-%m-%d', d.strftime('%Y-%m-%d'))

    def test_py(self):
        self.assertEqual('ht', PY/'黄涛')
        self.assertEqual('huang tao', PY | '黄涛')

    def test_regex(self):
        self.assertEqual('test_case', convert_cls_name('TestCase'))

    def test_wlen(self):
        from orange.utils.htutil import wlen
        self.assertEqual(wlen('我们like'), 8)

    def test_path(self):
        s = ['abc', 'def']
        with tempfile(data="\n".join(s), suffix='.csv')as f:
            a = list(x[0] for x in f.iter_csv())
            self.assertEqual(f.suffix,'.csv')
            self.assertTrue(f)
        self.assertFalse(f)
        self.assertListEqual(s, a)
        self.assertEqual(s[0],a[0])

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
