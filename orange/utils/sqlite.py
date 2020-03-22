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

__all__ = 'db_config', 'connect', 'execute', 'executemany', 'executescript', 'executefile',\
    'find', 'findone', 'findvalue', 'trans', 'fetch', 'fetchone', 'fetchvalue', 'transaction',\
    'loadcheck', 'Values'


def Values(count):
    '''提供 sql 语句的占符  用法： f"insert into test(a,b,c) Values(3)" '''
    return f'VALUES({",".join("?"*count)})'


def fix_db_name(database: str) -> str:
    '''修复数据库文件名'''
    if not str(database).startswith(':'):
        db = Path(database)
        if not db.root:
            db = ROOT / db
        database = str(db.with_suffix('.db'))
    return database


class Connection(sqlite3.Connection):
    default_config = {}

    @classmethod
    def config(cls, database: str, **kw):
        kw['database'] = str(fix_db_name(database))
        cls.default_config = kw.copy()

    def __init__(self, database: str = None, **kw) -> 'Connection':
        if database:
            kw['database'] = str(fix_db_name(database))
        else:
            kw = self.default_config
        super().__init__(**kw)

    def executefile(self, pkg: str, filename: str):
        '''
        执行程序中附带的资源文件
        pkg         : 所在包的名称
        filename    : 相关于包的文件名，包括路径
        '''
        from pkgutil import get_data
        data = get_data(pkg, filename)
        return self.executescript(data.decode())

    def fetch(self, sql: str, params: list = [], multi=True):
        '执行一条 sql 语句，并取出所以查询结果'
        cur = self.execute(sql, params)
        with closing(cur):
            return cur.fetchall() if multi else cur.fetchone()

    def fetchone(self, sql: str, params: list = []):
        '执行一条 sql 语句， 并取出第一条记录'
        return self.fetch(sql, params, multi=False)

    def fetchvalue(self, sql: str, params: list = []):
        '执行一条 sql 语句，并取出第一行第一列的值'
        row = self.fetchone(sql, params)
        return row and row[0]

    def attach(self, filename: Path, name: str):
        '''附加数据库'''
        filename = fix_db_name(filename)
        return self.execute(f'attach database "{filename}" as {name}')

    def detach(self, name: str):
        ''' 分离数据库 '''
        return self.execute(f'detach database {name}')

    def fprint(self, sql: str, params: list = []):
        for row in self.fetch(sql, params):
            print(*row)

    def fprintf(self, fmt: str, sql: str, params: list = []):
        for row in self.fetch(sql, params):
            print(fmt.format(row))

    def insert(self,
               table: str,
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
        sql = f'{method} into {table}{fields} values({values})'
        return self.executemany(sql, data) if multi else self.execute(
            sql, data)

    def insertone(self,
                  table: str,
                  data: 'iterable',
                  fields: list = None,
                  fieldcount: int = 0,
                  method: str = 'insert') -> "Cursor":
        '插入一行数据'
        return self.insert(table,
                           data,
                           fields,
                           fieldcount,
                           method,
                           multi=False)

    def tran(self, func):
        '''装饰器，将一下函数里所有的操作封装成一个事务。使用方法如下：
        @db.tran
        def abc():
            execute(sql1)
            execute(sql2)
        '''

        @wraps(func)
        def _(*args, **kw):
            with self:
                func(*args, **kw)

        return _

    def loadcheck(self, func: 'function'):
        '装饰器，对应的函数防目重复导入的功能。该函数的第一个参数必须为 filename '
        self.executescript('create table if not exists LoadFile( -- 文件重复检查表 \n'
                           'filename text primary key,       -- 文件名\n'
                           'mtime int                        -- 修改时间\n'
                           ');')

        @self.tran
        def _(filename, *args, **kw):
            file = Path(filename)
            name = file.name
            a = self.fetchvalue('select mtime from LoadFile where filename=?',
                                [name])  # 查询是否已导入
            is_imported = a and a >= file.mtime  # 判断是否已经导入
            if not is_imported:
                func(filename, *args, **kw)
                self.execute(
                    'insert or replace into LoadFile values(?,?)',  # 保存记录
                    [name, file.mtime])
            else:
                print(f'{name} 已导入，忽略')

        return _

    def loadfile(self,
                 path: Path,
                 data: 'iterable',
                 table: str,
                 fields: list = None,
                 drop: bool = True,
                 success: callable = None,
                 method: str = 'insert'):
        '将文导入数据库中'

        @self.loadcheck
        def _(path: Path):
            if drop:
                self.execute(f'delete from {table}')
            self.insert(table, fields=fields, data=data, method=method)
            if callable(success):
                success()
            print(f'{path.name} 导入成功')

        return _(path)


db_config = Connection.config

_conn = None


def connect(database: str = None, **kw) -> Connection:
    '打开指定的数据库，如未指定根据事先配置好的文件连接数据库'
    if database:
        return Connection(database, **kw)
    else:
        global _conn
        if not _conn:
            _conn = Connection()
            atexit.register(_conn.close)
        return _conn


@contextmanager
def db(database, **kw) -> Connection:
    '打开数据库，用完自动关闭'
    db = Connection(database, **kw)
    with closing(db):
        yield db


def wrapper(name: str) -> 'function':
    def _(*args, **kw):
        return getattr(connect(), name)(*args, **kw)

    return _


execute = wrapper('execute')
executemany = wrapper('executemany')
executescript = wrapper('executescript')
executefile = wrapper('executefile')
insert = wrapper('insert')
insertone = wrapper('insertone')
fetch = find = wrapper('fetch')
fetchone = findone = wrapper('fetchone')
fetchvalue = findvalue = wrapper('fetchvalue')
fprint = wrapper('fprint')
fprintf = wrapper('fprintf')


def trans(): return connect()


tran = transaction = wrapper('tran')
loadcheck = wrapper('loadcheck')
loadfile = wrapper('loadfile')
attach = wrapper('attach')
detach = wrapper('detach')


@arg('-d', '--db', dest='_db', default=':memory:', nargs='?', help='连接的数据库')
@arg('sql', nargs='*', help='执行的 sql 语句')
def execsql(_db, sql):
    sql = ' '.join(sql)
    if sql:
        with db(_db) as __db:
            for row in __db.fetch(sql):
                print(*row)
