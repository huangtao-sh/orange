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

    def test_xlsx(self):
        return
        from orange.xlsx import Book
        with Book('a.xlsx') as book:
            book.worksheet='test'
            book.A1_D1='Title','mh2'
            book.A2='hunter','h2'
            book.B2=1344.33,'currency'
            book.A3=['adfs',23.4]
            book.row=4
            book[0]=['hunter',34.6]
            book[4,0]=['zhangsan',77.6]
            book[5,0,5,6]='merge','mh2'
            book[6,0]=[10,20,30]
            book.row=7
            book.D7="=sum(A{0}:C{0})",'currency'

