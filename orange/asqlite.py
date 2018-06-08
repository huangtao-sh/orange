# 项目：工具库函数
# 模块：aiosqlite 的简单封装
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-06-08 15:34

import aiosqlite
import asyncio
from .sqlite import connect as _connect

__all__ = 'Connection', 'connect'


class Connection(aiosqlite.Connection):

    async def findone(self, sql: str, params=None)->tuple:
        async with self.execute(sql, params)as cursor:
            return await cursor.fetchone()

    async def findall(self, sql: str, params=None):
        async with self.execute(sql, params)as cursor:
            return await cursor.fetchall()

    def trans(self):
        return Trans(self)


Connection.find = Connection.execute


class Trans():
    __slots__ = ('_db',)

    def __init__(self, db: Connection):
        self._db = db

    async def __aenter__(self):
        return self._db

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self._db.rollback()
        else:
            await self._db.commit()


def connect(db, **kw):
    def connector():
        return _connect(db, **kw)
    return Connection(connector, asyncio.get_event_loop())
