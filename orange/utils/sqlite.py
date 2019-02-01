# 项目：   标准库函数
# 模块：   数据库
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-18 19:30

import atexit
import sqlite3
from contextlib import contextmanager, closing
from orange import is_dev, decode, Path
from functools import wraps

ROOT = Path('~/OneDrive') / ('testdb' if is_dev() else 'db')
_conn = None
_config = {}

__all__ = 'db_config', 'connect', 'execute', 'executemany', 'executescript', 'executefile',\
    'find', 'findone', 'findvalue', 'trans', 'fetch', 'fetchone', 'fetchvalue', 'transaction'


def fix_db_name(database: str)->str:
    if not str(database).startswith(':'):
        db = Path(database)
        if not db.root:
            db = ROOT/db
        database = str(db.with_suffix('.db'))
    return database


def db_config(database: str, **kw):
    global _config
    kw['database'] = str(fix_db_name(database))
    _config = kw


def connect():
    global _conn
    if not _conn:
        _conn = sqlite3.connect(**_config)
        atexit.register(_conn.close)
    return _conn


@contextmanager
def trans():
    try:
        conn = connect()
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def transaction(func):
    @wraps(func)
    def _(*args, **kw):
        try:
            conn = connect()
            func(*args, **kw)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
    return _


def execute(sql: str, params: list = []):
    return connect().execute(sql, params)


def executemany(sql: str, params: list = []):
    return connect().executemany(sql, params)


def executescript(sql: str):
    return connect().executescript(sql)


def executefile(pkg: str, filename: str):
    '''
    执行程序中附带的资源文件
    pkg         : 所在包的名称
    filename    : 相关于包的文件名，包括路径
    '''
    from pkgutil import get_data
    data = get_data(pkg, filename)
    return executescript(data.decode())


def insert(table: str, data: list, fields: list = None, method: str = 'insert'):
    data = tuple(data)
    if fields:
        fields = '(%s)' % (','.join(fields))
        values = ','.join(['?']*len(fields))
    else:
        fields = ''
        values = ','.join(['?']*len(data[0]))
    sql = f'{method} into {table}{fields} values({values})'
    return executemany(sql, data)


def attach(filename: Path, name: str):
    '''附加数据库'''
    filename = fix_db_name(filename)
    return execute(f'attach database {filename} as {name}')


def detach(name: str):
    ''' 分离数据库 '''
    return execute(f'detach database {name}')


def find(sql: str, params: list = [], multi=True):
    cur = execute(sql, params)
    with closing(cur):
        return cur.fetchall()if multi else cur.fetchone()


def findone(sql: str, params: list = []):
    return find(sql, params, multi=False)


def findvalue(sql: str, params: list = []):
    row = findone(sql, params)
    return row and row[0]


fetch = find
fetchone = findone
fetchvalue = findvalue
