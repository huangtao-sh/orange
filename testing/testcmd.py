import unittest
from orange import main
class TestCmd(unittest.TestCase):
    def test_cmdline(self):
        cmds=['setup -d abc def',
              'setup',
              'setup stdlib grace orange']
        for cmd in cmds:
            main(cmd.split())
            
    def test_b(self):
        self.assertEqual('a','a')
        
        
