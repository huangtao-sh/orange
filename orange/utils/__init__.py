# 项目：工具库
# 模块：
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-27 19:27

from .click import arg, command
from .datetime_ import UTC, LOCAL, now, datetime, FixedOffset, ONEDAY,\
    ONESECOND, date_add, LTZ
from .regex import R, convert_cls_name, extract
from .pinyin import get_py, PY
from .htutil import first, last, _any, _all, desensitize, limit, groupby, timeit
from .hz import Ordinal
from .data import Data, mapper, filterer, itemgetter, converter
from .log import set_debug, set_verbose, debug, error, info, warning, fatal


@arg('module', nargs='?', help='指定模块')
@arg('tokens', nargs='?', help='该函数所需的参数')
def py(module, tokens):
    result = exec(f'import {module};{tokens}')
    result and print(result)
