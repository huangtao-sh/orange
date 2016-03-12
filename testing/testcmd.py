import unittest
from orange.version import *
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
        from orange.debug import trace
        @trace
        def abc(a,b):
            return a+b            

        abc(1,20)
