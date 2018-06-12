# 项目：标准库函数
# 模块：sqlite封装
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-06-12 19:51

from orange import Path, convert_cls_name
from contextlib import contextmanager
import sqlite3


class Cursor(sqlite3.Cursor):
    def execute(self, sql, params=None):
        params = params or []
        return super().execute(sql, params)

    def findall(self, sql, params=None):
        self.execute(sql, params)
        return self.fetchall()

    def findone(self, sql, params=None):
        self.execute(sql, params)
        return self.fetchone()


class Model(dict):
    __slots__ = tuple()
    _db = None
    __db = None
    _fields = None

    @classmethod
    def execute(cls, sql, params=None, db=None):
        print(sql, params)
        # return
        if db:
            db.execute(sql, params)
        else:
            with cls.connect()as db:
                db.execute(sql, params)

    @classmethod
    def drop_table(cls, db=None):
        sql = 'drop table if exists %s' % (convert_cls_name(cls.__name__))
        cls.execute(sql, db=db)

    @classmethod
    def create_table(cls, db=None):
        sql = 'create table if not exists %s(%s)' % (
            convert_cls_name(cls.__name__),
            ",".join("%s %s" % (k, v)for k, v in cls._fields.items()))
        cls.execute(sql, db=db)

    @classmethod
    def _get_dbname(cls):
        if not cls.__db:
            if not cls._db:
                raise Exception('数据库文件未定义')
            path = Path(cls._db)
            if not path.root:
                path = Path('~/OneDrive/db') / path
            path = path.with_suffix('.db')
            cls.__db = str(path)
        return cls.__db

    @classmethod
    def aconnect(cls):
        import aiosqlite
        return aiosqlite.connect(cls._get_dbname())

    @classmethod
    @contextmanager
    def connect(cls):
        con = sqlite3.connect(cls._get_dbname())
        try:
            cursor = con.cursor(Cursor)
            try:
                with con:
                    yield cursor
            finally:
                cursor.close()
        finally:
            con.close()

    @classmethod
    def findall(cls, sql, params=None):
        with cls.connect() as db:
            return db.findall(sql, params)

    @classmethod
    def findone(self, sql, params=None):
        with self.connect() as db:
            return db.findone(sql, params)


if __name__ == '__main__':
    class Test(Model):
        _db = 'test'
        _fields = {'a': 'int primary key',
                   'b': 'int'}

    async def _():
        with Test.connect() as db:
            Test.drop_table(db=db)
            Test.create_table(db=db)
            # Test.drop_table(db=db)
            # Test.create_table(db=db)
            db.execute('insert into test values(?,?)', [128, 81])

        with Test.connect()as db:
            for row in db.findall('select * from test'):
                print(*row)

            print('-'*30)
            for k in db.findall('select * from sqlite_master'):
                print(*k)

    from orange.coroutine import run
    run(_())
