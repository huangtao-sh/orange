# 项目：常用库函数
# 模块：SQLite封装
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-06-08 14:45

import sqlite3
from contextlib import contextmanager

__all__ = 'Connection', 'connect'


class Connection(sqlite3.Connection):

    def findone(self, *args, **kw):
        '''查找一条数据
        sql: sql 语句
        params: 查询参数
        '''
        with self.find(*args, **kw)as cursor:
            return cursor.fetchone()

    def findall(self, *args, **kw):
        with self.find(*args, **kw)as cursor:
            return cursor.fetchall()

    @contextmanager
    def find(self, *args, **kw):
        cursor = self.execute(*args, **kw)
        try:
            yield cursor
        finally:
            cursor.close()

    @contextmanager
    def trans(self):
        try:
            yield self
            self.commit()
        except Exception as e:
            self.rollback()
            raise e


def connect(*args, **kw):
    return Connection(*args, **kw)
