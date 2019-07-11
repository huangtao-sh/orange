# 项目：   标准库函数
# 模块：   数据库
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-18 19:30
# 修订：2019-03-16 21:21 增加 insertone 函数

import atexit
import sqlite3
from contextlib import contextmanager, closing
from orange import is_dev, decode, Path, arg
from functools import wraps
from itertools import chain

ROOT = Path('~/OneDrive') / ('testdb' if is_dev() else 'db')
_conn = None
_config = {}

__all__ = 'db_config', 'connect', 'execute', 'executemany', 'executescript', 'executefile',\
    'find', 'findone', 'findvalue', 'trans', 'fetch', 'fetchone', 'fetchvalue', 'transaction',\
    'loadcheck'


def fix_db_name(database: str) -> str:
    '''修复数据库文件名'''
    if not str(database).startswith(':'):
        db = Path(database)
        if not db.root:
            db = ROOT / db
        database = str(db.with_suffix('.db'))
    return database


def db_config(database: str, **kw):
    '配置数据库参数'
    global _config
    kw['database'] = str(fix_db_name(database))
    _config = kw


def connect():
    '根据事先配置好的文件连接数据库'
    global _conn
    if not _conn:
        _conn = sqlite3.connect(**_config)
        atexit.register(_conn.close)
    return _conn


@contextmanager
def trans():
    '''进入数据库sql 语句执行环境，使用方法：
    with trans():
        execute(sql)
    '''
    try:
        conn = connect()
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e


def transaction(func):
    '''装饰器，将一下函数里所有的操作封装成一个事务。使用方法如下：
    @transaction
    def abc():
        execute(sql1)
        execute(sql2)
    '''

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
    '执行一条 sql 语句'
    return connect().execute(sql, params)


def executemany(sql: str, params: list = []):
    '执行多条 sql 语句'
    return connect().executemany(sql, params)


def executescript(sql: str):
    '执行多条脚本'
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


def insert(table: str,
           data: 'iterable',
           fields: list = None,
           fieldcount: int = 0,
           method: str = 'insert',
           multi: bool = True) -> "Cursor":
    '''执行插入命令
    table:  插入的表名
    data:   插入的数据，
    fields: 插入的字段列表
    method: 插入的方法，默认为 insert 可以为： insert or replace ,insert or ignore 等
    multi:  是否插入多行数据
    '''
    #data = tuple(data)
    if fields:  # 参数中有字段列表
        values = ','.join(['?'] * len(fields))
        fields = '(%s)' % (','.join(fields))
    else:  # 参数中无字段列表
        fields = ''
        if not fieldcount:  # 参数中如有字段数量
            if not multi:
                fieldcount = len(data)
            elif hasattr(data, '__getitem__'):  # 数据为 tuple 或 list
                fieldcount = len(data[0])
            else:
                data = iter(data)  # 将数据转换成 iter
                firstobj = next(data)  # 取第一条数据
                fieldcount = len(firstobj)  # 取得字段长度
                data = chain([firstobj], data)  # 恢复原数据
        values = ','.join(['?'] * fieldcount)
        #    values = ','.join(['?'] * len(data[0] if multi else data))
    # else:
    #    fields = ''
    #    values = ','.join(['?'] * len(data[0] if multi else data))
    sql = f'{method} into {table}{fields} values({values})'
    return executemany(sql, data) if multi else execute(sql, data)


def insertone(table: str,
              data: 'iterable',
              fields: list = None,
              fieldcount: int = 0,
              method: str = 'insert') -> "Cursor":
    '插入一行数据'
    return insert(table, data, fields, fieldcount, method, multi=False)


def attach(filename: Path, name: str):
    '''附加数据库'''
    filename = fix_db_name(filename)
    return execute(f'attach database "{filename}" as {name}')


def detach(name: str):
    ''' 分离数据库 '''
    return execute(f'detach database {name}')


def find(sql: str, params: list = [], multi=True):
    '执行一条 sql 语句，并取出所以查询结果'
    cur = execute(sql, params)
    with closing(cur):
        return cur.fetchall() if multi else cur.fetchone()


def findone(sql: str, params: list = []):
    '执行一条 sql 语句， 并取出第一条记录'
    return find(sql, params, multi=False)


def findvalue(sql: str, params: list = []):
    '执行一条 sql 语句，并取出第一行第一列的值'
    row = findone(sql, params)
    return row and row[0]


need_create = True


def __createtable():
    global need_create
    executescript('''
    create table if not exists LoadFile( -- 文件重复检查表
        filename text primary key,       -- 文件名
        mtime int                        -- 修改时间
    );
    ''')
    need_create = False


def loadcheck(func):
    '装饰器，对应的函数防目重复导入的功能。该函数的第一个参数必须为 filename '
    need_create and __createtable()  # 第一次执行本函数时建表

    @transaction
    def _(filename, *args, **kw):
        file = Path(filename)
        name = file.name
        a = fetchvalue('select mtime from LoadFile where filename=?',
                       [name])  # 查询是否已导入
        is_imported = a and a >= file.mtime  # 判断是否已经导入
        if not is_imported:
            func(filename, *args, **kw)
            execute(
                'insert or replace into LoadFile values(?,?)',  # 保存记录
                [name, file.mtime])
        else:
            print(f'{name} 已导入，忽略')

    return _


fetch = find
fetchone = findone
fetchvalue = findvalue


@arg('-d', '--db', default=':memory:', nargs='?', help='连接的数据库')
@arg('sql', nargs='*', help='执行的 sql 语句')
def execsql(db, sql):
    sql = ' '.join(sql)
    if sql:
        with sqlite3.connect(fix_db_name(db)) as db:
            for row in db.execute(sql):
                print(*row)
