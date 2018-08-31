# 项目：基本库函数
# 模块：sqlite 数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-7-18

import sqlite3
from werkzeug.local import LocalStack
from orange import Path, is_dev, info, decode
from contextlib import closing
from functools import partial


__all__ = 'db_config', 'connect', 'execute', 'executemany',\
    'executescript', 'find', 'findone', 'executefile', 'insert'

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
        if not str(database).startswith(':'):
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

    @classmethod
    def droptable(cls, *tables):
        script = ";".join('drop table if exists %s\n' % (table)
                          for table in tables)
        info('executescript')
        info(script)
        return cls.executescript(script)

    @classmethod
    def createtable(cls, name, *fields, pk=None):
        if pk:
            fields = list(fields)
            if not isinstance(pk, str):
                pk = ",".join(pk)
            fields.append(f"primary key({pk})")

        sql = f'create table if not exists {name} ({",".join(fields)})'
        return cls.execute(sql)

    @classmethod
    def executefile(cls, pkg, filename):
        from pkgutil import get_data
        data = get_data(pkg, filename)
        sql = decode(data)
        return executescript(sql)

    @classmethod
    def insert(cls, table, data, fields=None, oper='insert'):
        data = tuple(data)
        if fields:
            fields = '(%s)' % (','.join(fields))
            values = ','.join(['?']*len(fields))
        else:
            fields = ''
            values = ','.join(['?']*len(data[0]))
        sql = f'{oper} into {table}{fields} values({values})'
        return cls.executemany(sql, data)


db_config = Connection.config
connect = Connection
execute = Connection.execute
executemany = Connection.executemany
executescript = Connection.executescript
executefile = Connection.executefile
find = Connection.find
findone = Connection.findone
droptable = Connection.droptable
createtable = Connection.createtable
insert = Connection.insert
