# 项目：标准库函数
# 模块：Python 升级程序
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-14 20:35

import sys

from orange.path import Path


class PythonUpgrade(object):
    @classmethod
    def main(cls):
        platform = sys.platform
        getattr(cls, platform)()

    @classmethod
    def win32(cls):
        from .regkey import add_path
        destpath = Path('%ProgramFiles%/Python')
        srcpath = Path('%localappdata%/Programs/Python')
        curpath = max(srcpath.glob('Python*'))
        if curpath:
            print(f'Python 的安装路径为  {curpath}')
            destpath >> curpath  # 连接安装目录
            print(f'连接安装目录： {destpath} -> {curpath}')
            scripts = destpath / 'Scripts'
            path = ';'.join([str(destpath), str(scripts)])
            add_path(path, replace='Python')
            print('设置 Path 成功！')
