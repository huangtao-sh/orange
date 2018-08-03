import unittest
from orange.sqlite import connect, execute, executemany, executescript, \
    droptable, find, findone, db_config
from orange import Path
from orange.coroutine import run

db_config(':memory:')


class TestSqlite(unittest.TestCase):

    def tearDown(self):
        # if Path('test.db'):
        #    Path('test.db').unlink()
        pass

    def test_sqlite(self):
        with connect():
            rows = ('make', 'you', 'good')
            execute('create table if not exists test(a,b,c)')
            execute('insert into test values(?,?,?)', rows)
            result = findone('select * from test')
            self.assertListEqual(list(rows), list(result))

    def test_query(self):
        rows = [('a', 'b', i) for i in range(10)]

        async def _():
            async with connect():
                await execute('create table if not exists test(a,b,c)')
                await executemany('insert into test values(?,?,?)', rows)
                await executescript('insert into test values("a","b",2)')
                ab = await find('select * from test')
                self.assertEqual(len(ab), 11)
                d = await findone('select * from test limit 1')
                self.assertEqual(d[0], 'a')
                await droptable('abc', 'test')

        run(_())
