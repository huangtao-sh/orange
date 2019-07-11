import unittest
from orange.utils.sqlite import execute, executemany, executescript, \
    find, findone, db_config, findvalue, trans,insert,fetchvalue,\
        insertone
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
        self.assertEqual(10, findvalue('select count(a) from test'))
        with trans():
            execute('delete from test')

    def test_insert(self):
        def producer():
            for i in range(100):
                yield i, i, i

        execute('create table if not exists test(a,b,c)')
        insert('test', fields=('a', 'b', 'c'), data=producer())
        self.assertEqual(100, fetchvalue('select count(*) from test'))
        execute('drop table test')

    def test_insert2(self):
        def producer():
            for i in range(100):
                yield i, i, i

        execute('create table if not exists test(a,b,c)')
        insert('test', fieldcount=3, data=producer())
        self.assertEqual(100, fetchvalue('select count(*) from test'))
        execute('drop table test')

    def test_insert3(self):
        def producer():
            for i in range(100):
                yield i, i, i

        execute('create table if not exists test(a,b,c)')
        insert('test', data=producer())
        self.assertEqual(100, fetchvalue('select count(*) from test'))
        execute('drop table test')

    def test_insert4(self):
        data = [(1, 2, 3), (4, 5, 6)]

        execute('create table if not exists test(a,b,c)')
        insert('test', data=data)
        self.assertEqual(2, fetchvalue('select count(*) from test'))
        execute('drop table test')

    def test_insertone(self):
        execute('create table if not exists test(a,b,c)')
        insertone('test', data=[1, 2, 4])
        self.assertEqual(1, fetchvalue('select count(*) from test'))
        execute('drop table test')
