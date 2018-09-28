# 项目：库函数
# 模块：系统模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-27 19:21

import os
from collections import ChainMap
from subprocess import run

POSIX = os.name == 'posix'

DEFAULT = {
    'capture_output': True,
    'encoding': 'UTF8' if POSIX else 'GBK',
}


class Shell(type):
    def __call__(self, *args, **kw):
        '''
        调用方式： sh > 'dir'
        系统直接打印输出执行命令的输出
        返回值 ：操作系统的返回值
        '''
        shell = len(args) == 1
        return run(args, **ChainMap(kw, shell=shell, DEFAULT))

    def __gt__(self, args):
        '''
        调用方式： r = sh('dir')
        返回值： r.returncode 系统返回值
                r.stdout     命令输出内容
                r.stderr     错误输出内容
        '''
        if not isinstance(args, tuple):
            args = (args,)
        result = self(*args, capture_output=False)
        return result.returncode


class sh(metaclass=Shell):
    pass
