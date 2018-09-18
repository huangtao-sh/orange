# 项目：标准库函数
# 模块：Python 升级程序
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-14 20:35

import sys

from .path import Path


class PythonUpgrade(object):
    @classmethod
    def main(cls):
        platform = sys.platform
        getattr(cls, platform)()

    @classmethod
    def darwin(cls):
        from .pyver import get_cur_ver
        curpath = get_cur_ver(Path('/usr/local/Cellar/Python').glob('*/bin'))
        binpath = Path('/usr/local/bin')
        print(f'当前安装路径为 {curpath}')
        for cmd in ('python3', 'pip3'):
            (binpath/cmd) >> (curpath/cmd)
            print(f'连接 {cmd} 成功')

    @classmethod
    def win32(cls):
        from .regkey import add_path, HKLM, REG_SZ
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

        with HKLM/'SYSTEM/CurrentControlSet/Control/Session Manager/Environment' as key:
            pythonpath = ";".join([str(destpath/'DLLs'),
                                   str(destpath/'Lib'),
                                   str(destpath/'Lib/site-packages')])
            key['PYTHONPATH'] = pythonpath, REG_SZ
            print('设置 PYTHONPATH 环境变量成功！')
