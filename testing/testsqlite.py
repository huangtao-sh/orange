import unittest
from orange.utils.sqlite import execute, executemany, executescript, \
    find, findone, db_config, findvalue, trans
from orange import Path

db_config(':memory:')


class TestSqlite(unittest.TestCase):

    def tearDown(self):
        # if Path('test.db'):
        #    Path('test.db').unlink()
        pass

    def test_sqlite(self):
        rows = [1, 2, 3]
        execute('create table if not exists test(a,b,c)')
        execute('insert into test values(?,?,?)', rows)
        result = findone('select * from test')
        self.assertListEqual(list(rows), list(result))

    def test_query(self):
        rows = [('a', 'b', i) for i in range(10)]
        execute('create table if not exists test(a,b,c)')
        with trans():
            executemany('insert into test values (?,?,?)', rows)
        self.assertEqual(10,findvalue('select count(a) from test'))
        with trans():
            execute('delete from test')
