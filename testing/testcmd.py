import unittest
from orange import main
class TestCmd(unittest.TestCase):
    def test_cmdline(self):
        #main()
        main('init -p 登月计划 -a 黄涛  -e huangtao@czbank.com'.split())
        
