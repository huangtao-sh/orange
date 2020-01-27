from orange import Path
import unittest


class TestData(unittest.TestCase):
    def test_offsets(self):
        text = (
            '012345678123\n'
            'hunterabc'
        )
        with Path.tempfile(data=text, suffix='.csv')as f:
            data = tuple(f.read_data(skip_header=False, offsets=(0, 6)))
            self.assertListEqual(['hunter', 'abc'], data[1])
            data = tuple(f.read_data(skip_header=True, offsets=(0, 6)))
            self.assertListEqual(['hunter', 'abc'], data[0])

    def test_sep(self):
        text = (
            '0123456,78123\n'
            'hunter   ,   abc'
        )
        with Path.tempfile(data=text, suffix='.csv')as f:
            data = tuple(f.read_data(skip_header=False, sep=','))
            self.assertListEqual(['hunter', 'abc'], data[1])
            data = tuple(f.read_data(skip_header=True, sep=b','))
            self.assertListEqual(['hunter', 'abc'], data[0])

    def test_quote(self):
        text = (
            '0123456,78123\n'
            '"hunter",   abc'
        )
        with Path.tempfile(data=text, suffix='.csv')as f:
            data = tuple(f.read_data(skip_header=False, quote='"', sep=','))
            self.assertListEqual(['hunter', 'abc'], data[1])
            data = tuple(f.read_data(skip_header=True, quote='"', sep=b','))
            self.assertListEqual(['hunter', 'abc'], data[0])
