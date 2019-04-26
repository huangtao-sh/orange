# 项目：公共函数库
# 模块：数据处理模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-04-25 11:09

from functools import partial
from .htutil import split, tprint


def _convert(converter):
    '''数据转换'''
    def _(row):
        for idx, conv in converter.items():
            row[idx] = conv(row[idx])
        return row
    return _


def itemgetter(columns: 'iterable') -> 'func':
    '获取提定对象的指定列'
    'columns 为 tuple 或者 list'
    def _(row):
        return [row[col]for col in columns]
    return _


class Data():
    __slots__ = '_data', "_rows"

    def __init__(self, data, header=None, rows=0, **kw):
        self._data = iter(data)
        if header:
            self.header(header)
        for k, v in kw.items():
            getattr(self, k)(v)
        self._rows = rows

    def header(self, header):
        for row in self._data:
            if all(x in row for x in header):
                self.columns([row.index(title)for title in header])
                if isinstance(header, dict):
                    self.converter(
                        {idx: conv for idx, conv in enumerate(header.values())if conv})
                break

    def filter(self, filter_):
        self._data = filter(filter_, self._data)

    def converter(self, converter):
        if converter:
            if callable(converter):
                self._data = map(converter, self._data)
            else:
                self._data = map(_convert(converter), self._data)

    def columns(self, columns):
        self._data = map(itemgetter(columns), self._data)

    def __iter__(self):
        if self._rows:
            self._data = split(self._data, self._rows)
        return self._data

    def split(self, count=10000):
        self._rows = count

    def print(self, format_spec, sep=' '):
        tprint(self._data, format_spec=format_spec, sep=sep)
