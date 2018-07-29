# 项目：基本库函数
# 模块：sqlite 数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-7-18

import sqlite3
from werkzeug.local import LocalStack, LocalProxy
from contextlib import contextmanager, closing
from orange import Path, is_dev, info


__all__ = 'db_config', 'begin_tran', 'begin_query', 'execute', 'executemany',\
    'executescript', 'find', 'findone', 'cursor'

ROOT = Path('~/OneDrive')
ROOT = ROOT / ('testdb' if is_dev() else 'db')
_db_config = None
_cursor_stack = LocalStack()


def _get_cursor():
    cursor = _cursor_stack.top
    info(f'get cursor:{id(cursor)}')
    if not cursor:
        raise Exception('Cursor is not exists!')
    return cursor


cursor = LocalProxy(_get_cursor)


def db_config(database: str, **kw):
    global _db_config
    kw['database'] = database
    _db_config = kw


@contextmanager
def _connect(database: str=None, **kw):
    if not database:
        kw = _db_config.copy()
        database = kw.pop('database')
    if not database.startswith(':'):
        db = Path(database)
        if not db.root:
            db = ROOT/db
        db = db.with_suffix('.db')
        database = str(db)
    connection = sqlite3.connect(database, **kw)
    with closing(connection):
        yield connection


@contextmanager
def begin_tran(database: str=None, is_tran=True, **kw):
    with _connect(database, **kw) as connection:
        cursor = connection.cursor()
        with connection, closing(cursor):
            _cursor_stack.push(cursor)
            yield cursor
            _cursor_stack.pop()


@contextmanager
def begin_query(database: str=None, **kw):
    with _connect(database, **kw) as connection:
        cursor = connection.cursor()
        with closing(cursor):
            _cursor_stack.push(cursor)
            yield cursor
            _cursor_stack.pop()


def execute(sql, params=None):
    params = params or []
    return cursor.execute(sql, params)


def executescript(sql, params=None):
    cursor.executescript(sql)


def executemany(sql, params=None):
    params = params or []
    cursor.executemany(sql, params)


def findone(sql, params=None):
    return execute(sql, params).fetchone()


def find(sql, params=None):
    return execute(sql, params).fetchall()


if __name__ == '__main__':
    db_config('hello')
    from orange import config_log
    config_log()
    with begin_tran()as db:
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

    with begin_query():
        '''
        cursor.execute('select * from abc')
        for i in cursor:
            print(*i)
        '''
        for i in find('select * from abc'):
            print(*i)

        print('-'*10)
        with begin_query():
            a = findone('select * from abc limit 1')
            print(*a)
        print('-'*20)
        for b in find('select * from abc limit 2'):
            print(*b)
