# 项目：标准函数库
# 模块：音乐文件转换
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-03-07 10:45

from orange import R, Path

Pattern = R/'".*?"|\S+'


class CueTime(object):
    __slots__ = 'value'

    def __init__(self, value: str):
        if isinstance(value, str):
            m, s, f = map(int, value.split(':'))
            self.value = m * 60*75+s*75+f
        else:
            self.value = value

    def __sub__(self, other):
        return CueTime(self.value-other.value)

    def __str__(self):
        s, f = divmod(self.value, 75)
        m, s = divmod(s, 60)
        return '%02d:%02d:%02d' % (m, s, f)

    @property
    def time(self):
        return '%.2f' % (self.value/75)


class CueSheet(object):
    def __init__(self, filename):
        self.album = {}
        self.tracks = {}
        for cmd, tags in filter(None, map(Pattern.findall, Path(filename).lines)):
            print(cmd, tags)


if __name__ == '__main__':
    a = Path('~/a.cue')
