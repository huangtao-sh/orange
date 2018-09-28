# 项目：库函数
# 模块：系统模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-27 19:21

import os
from subprocess import getstatusoutput

POSIX = os.name == 'posix'


class Shell(type):
    def __call__(self, cmd: str, *args: list, prefix: str = '-',
                 **options)->'code,output':
        '''
        调用方式： code,output = sh('dir')
        返回值：   code 系统返回值
                  output     命令输出内容
        '''
        if prefix == None:
            prefix = '-' if POSIX else '/'
        params = [cmd]
        for arg in args:
            if not isinstance(arg, str):
                arg = str(arg)
            if any(space in arg for space in (' ', '\t'))and not arg.startswith('"'):
                arg = f'"{arg}"'
            params.append(arg)
        for option, arg in options.items():
            if prefix == '-' and len(option) > 1:
                p = '--'
            else:
                p = prefix
            if isinstance(arg, bool):
                if arg:
                    params.append(f'{p}{option}')
            else:
                arg = str(arg)
                params.append(f'{p}{option}:{arg}')
        cmd = " ".join(params)
        return getstatusoutput(cmd)

    def __gt__(self, cmd: str)->int:
        '''
        调用方式： sh > 'dir'
        系统直接打印输出执行命令的输出
        返回值 ：操作系统的返回值
        '''
        return os.system(cmd)


class sh(metaclass=Shell):
    pass
