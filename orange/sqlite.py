# 项目：基本库函数
# 模块：sqlite 数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-7-18

import sqlite3
from werkzeug.local import LocalStack
from orange import Path, is_dev, info
from contextlib import closing
from functools import partial


__all__ = 'db_config', 'connect', 'execute', 'executemany',\
    'executescript', 'find', 'findone'

ROOT = Path('~/OneDrive') / ('testdb' if is_dev() else 'db')


class Connection():
    _config = {}
    stack = LocalStack()

    @classmethod
    def get_conn(cls):
        conn = cls.stack.top
        info(f'get conn:{id(conn)}')
        if not conn:
            raise Exception('Connection is not exists!')
        return conn

    @classmethod
    def config(cls, database: str, **kw):
        kw['database'] = database
        cls._config = kw

    def __init__(self, database: str=None, **kw):
        if not database:
            kw = self._config.copy()
            database = kw.pop('database')
        if not database.startswith(':'):
            db = Path(database)
            if not db.root:
                db = ROOT/db
            db = db.with_suffix('.db')
            database = str(db)
        self._db = database
        self._kw = kw

    def __enter__(self):
        conn = sqlite3.connect(self._db, **self._kw)
        self.stack.push(conn)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        conn = self.stack.pop()
        if exc_type:
            conn.rollback()
        else:
            conn.commit()
        conn.close()

    async def __aenter__(self):
        import aiosqlite3
        conn = await aiosqlite3.connect(self._db, **self._kw)
        self.stack.push(conn)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        conn = self.stack.pop()
        if exc_type:
            await conn.rollback()
        else:
            await conn.commit()
        await conn.close()

    @classmethod
    def execute(cls, sql: str, params=None):
        params = params or []
        return cls.get_conn().execute(sql, params)

    @classmethod
    def executemany(cls, sql: str, params=None):
        return cls.get_conn().executemany(sql, params)

    @classmethod
    def executescript(cls, sql: str):
        return cls.get_conn().executescript(sql)

    @classmethod
    def find(cls, sql: str, params=None, multi=True):
        fetch = 'fetchall' if multi else 'fetchone'
        if isinstance(cls.stack.top, sqlite3.Connection):
            cursor = cls.execute(sql, params)
            with closing(cursor):
                return getattr(cursor, fetch)()
        else:
            async def _():
                async with cls.execute(sql, params) as cursor:
                    return await getattr(cursor, fetch)()
            return _()

    @classmethod
    def findone(cls, sql: str, params=None):
        return cls.find(sql, params, multi=False)


db_config = Connection.config
connect = Connection
execute = Connection.execute
executemany = Connection.executemany
executescript = Connection.executescript
find = Connection.find
findone = Connection.findone


if __name__ == '__main__':
    from orange.coroutine import run
    db_config('hello')
    from orange import config_log
    config_log()
    with connect():
        sql = '''
        drop table if exists abc;
        create table  if not exists abc(a,b);
        insert into abc values(1,2);
        update abc set b=b+1 where a=1;
        update or replace abc set b=b+1 where a=2;
        '''
        # db.executescript(sql)
        executescript(sql)
        execute('insert into abc values(2,3)')
        execute('insert into abc values(4,5)')

    with connect():
        '''
        cursor.execute('select * from abc')
        for i in cursor:
            print(*i)
        '''
        for i in find('select * from abc'):
            print(*i)

        print('-'*10)
        with connect():
            a = findone('select * from abc limit 1')
            print(*a)
        print('-'*20)
        for b in find('select * from abc limit 2'):
            print(*b)

    async def _():
        async with connect():
            await execute('insert into abc values(7,8)')
            data = [(x, x+20)for x in range(20)]
            await executemany('insert into abc values(?,?)', data)
            d = await find('select * from abc')
            for row in d:
                print(*row)
            b = await findone('select * from abc')
            print(*b)
    print('*'*20)
    run(_())
