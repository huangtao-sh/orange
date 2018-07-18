# 项目：基本库函数
# 模块：sqlite 数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-7-18

import sqlite3
from contextlib import contextmanager, closing
from orange import Path, is_dev

__all__ = 'db_config', 'begin_tran', 'begin_query'

_db_config = None
ROOT = Path('~/OneDrive')
ROOT = ROOT / ('testdb' if is_dev() else 'db')


def db_config(database: str, **kw):
    global _db_config
    kw['database'] = database
    _db_config = kw


@contextmanager
def _connect(database: str=None, **kw):
    if not database:
        kw = _db_config.copy()
        database = kw.pop('database')
        if not Path(database).root:
            database = str((ROOT/database).with_suffix('.db'))
    connection = sqlite3.connect(database, **kw)
    with closing(connection):
        yield connection


@contextmanager
def begin_tran(database: str=None, **kw):
    with _connect(database, **kw) as connection:
        cursor = connection.cursor()
        with connection, closing(cursor):
            yield cursor


@contextmanager
def begin_query(database: str=None, **kw):
    with _connect(database, **kw) as connection:
        cursor = connection.cursor()
        with closing(cursor):
            yield cursor


if __name__ == '__main__':
    db_config('hello')
    with begin_tran()as db:
        sql = '''
        drop table if exists abc;
        create table  if not exists abc(a,b);
        insert into abc values(1,2);
        update abc set b=b+1 where a=1;
        update or replace abc set b=b+1 where a=2;
        '''
        db.executescript(sql)

    with begin_query() as cursor:
        cursor.execute('select * from abc')
        for i in cursor:
            print(*i)
