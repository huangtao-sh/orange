# 项目：工具库
# 模块：拼音模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-27 21:29

def get_py(s, style=4, sep=''):
    '''
    获取拼音字母。
    '''
    from pypinyin.core import phrase_pinyin
    return sep.join([x[0] for x in phrase_pinyin(s, style, None)])


class _PY(type):

    def __truediv__(self, s):
        return get_py(s)

    def __or__(self, s):
        return get_py(s, style=0, sep=' ')


class PY(metaclass=_PY):
    '''以一种高逼格的方式获取拼音
    获取拼音首字母：  PY/'我们'   ===>   'wm'
    获取拼音：       PY|'我们'   ===>    'wo men'
    '''
    pass