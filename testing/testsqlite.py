import unittest
from orange.sqlite import connect
from orange import Path


class TestSqlite(unittest.TestCase):

    def tearDown(self):
        #if Path('test.db'):
        #    Path('test.db').unlink()
        pass
    def test_sqlite(self):
        with connect('test.db')as db:
            rows = ('make', 'you', 'good')
            with db.trans():
                db.execute('create table if not exists test(a,b,c)')
                db.execute('insert into test values(?,?,?)', rows)
            result = db.findone('select * from test')
            self.assertListEqual(list(rows), list(result))

    def test_query(self):
        rows=[('a','b',i) for i in range(10)]
        with connect('test.db')as db:
            with db.trans():
                db.execute('delete from test')
                db.executemany('insert into test values(?,?,?)',rows)
            ab=db.find('select * from test')
            self.assertEqual(len(ab),10)