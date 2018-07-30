# 项目：基本库函数
# 模块：sqlite 数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-7-18

import sqlite3
from werkzeug.local import LocalStack, LocalProxy
from orange import Path, is_dev, info


__all__ = 'db_config', 'connect', 'execute', 'executemany',\
    'executescript', 'find', 'findone', 'find_', 'findone_'

ROOT = Path('~/OneDrive')
ROOT = ROOT / ('testdb' if is_dev() else 'db')
_db_config = None
_conn_stack = LocalStack()


def _get_conn():
    conn = _conn_stack.top
    info(f'get conn:{id(conn)}')
    if not conn:
        raise Exception('Connection is not exists!')
    return conn


conn = LocalProxy(_get_conn)


def db_config(database: str, **kw):
    global _db_config
    kw['database'] = database
    _db_config = kw


class connect():
    def __init__(self, database: str=None, **kw):
        if not database:
            kw = _db_config.copy()
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
        connection = sqlite3.connect(self._db, **self._kw)
        _conn_stack.push(connection)
        return connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        conn = _conn_stack.pop()
        if exc_type:
            conn.rollback()
        else:
            conn.commit()
        conn.close()

    async def __aenter__(self):
        import aiosqlite3
        connection = await aiosqlite3.connect(self._db, **self._kw)
        _conn_stack.push(connection)
        return connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        conn = _conn_stack.pop()
        if exc_type:
            await conn.rollback()
        else:
            await conn.commit()
        await conn.close()


def execute(sql, params=None):
    params = params or []
    return conn.execute(sql, params)


def executescript(sql, params=None):
    return conn.executescript(sql)


def executemany(sql, params=None):
    params = params or []
    return conn.executemany(sql, params)


def find(sql, params=None, multi=True):
    con_ = _conn_stack.top
    if not isinstance(con_, sqlite3.Connection):
        con_ = con_._conn
    params = params or []
    cursor = con_.execute(sql, params)
    if multi:
        return cursor.fetchall()
    else:
        return cursor.fetchone()


def findone(sql, params=None):
    return find(sql, params, multi=False)


async def findone_(sql, params=None):
    cursor = await execute(sql, params)
    return await cursor.fetchone()


async def find_(sql, params=None):
    cursor = await execute(sql, params)
    return await cursor.fetchall()

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
            d = find('select * from abc')
            for row in d:
                print(*row)
            b = await findone_('select * from abc')
            print(*b)
    print('*'*20)
    run(_())
