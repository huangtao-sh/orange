# 项目：   数据处理模块
# 模块：
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2020-02-05 20:14


def itemgetter(columns):
    def _(row):
        return [row[i]for i in columns]
    return _


def excluder(columns):
    def _(row):
        return [item for i, item in enumerate(row) if i not in set(columns)]
    return _


def converter(conv):
    def _(row):
        for i, c in conv.items():
            row[i] = c(row[i])
        return row
    return conv if callable(conv) else _


def filterer(func):
    def _(row):
        return row if func(row)else None

    return _


class Data(object):
    def __init__(self, data, pipelines=None, **kw):
        pipelines = list(pipelines)if pipelines else []
        pipelines.extend(kw.items())
        self.data = data
        self.pipelines = pipelines

    def get_proc(self):
        pipelines = [
            {
                'filter': filterer,
                'include': itemgetter,
                'columns': itemgetter,
                'converter': converter,
                'exclude': excluder
            }.get(k)(v) for k, v in self.pipelines
        ]

        def _(row):
            for f in pipelines:
                row = f(row)
                if not row:
                    break
            return row
        return _

    def __iter__(self):
        yield from filter(None, map(self.get_proc(), self.data))

    async def __aiter__(self):
        proc = self.get_proc()
        async for row in self.data:
            row = proc(row)
            if row:
                yield row
