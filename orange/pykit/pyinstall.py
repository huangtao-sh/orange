# 项目：Pytohon工具包
# 模块：安装模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-09-03 16:02
# 修改：2016-03-08 16:47
# 修改：2016-04-13 21:07
# 修改：2016-9-7 将通过shell调用pip命令调整为直接引入pip模块
# 修改：2018-7-12 调整参数处理方法

import os
import sys
import re
from orange import R, Path, info, command, arg, shell
from orange.deploy import Ver, run_pip, run_setup, pyclean
from collections import defaultdict


RootPath = '~/OneDrive/pylib'
Pattern = R / r'\d+(\.\d+)*([ab]\d+)?'


def find_ver(path):
    v = Pattern.search(path.name)
    if v:
        return Ver(v.group())


def get_pkgs(root=Path(RootPath)):
    pkgs = defaultdict(lambda: (None, Ver('0.0')))
    for path in root.glob('*.*'):
        info = path.verinfo
        if info:
            name, ver = info[:2]
            if ver > pkgs[name][1]:
                pkgs[name] = path, ver
    return pkgs


@command(allow_empty=True)
@arg('packages', help='python package', nargs='*', metavar='package')
@arg('-p', '--path', default=RootPath, help='指定的目录')
@arg('-d', '--download', help='默认的包目录', action='store_true')
@arg('-u', '--upgrade', help='升级系统中已安装的软件包', action='store_true')
def py_setup(packages=None, path=None, download=None, upgrade=False):
    root = Path(path)
    if download:
        run_pip('download', '-d', str(root), *packages)
        # exec_cmd('pip','download -d %s %s'%(Path(path),
        #                      " ".join(packages)))
    elif upgrade:
        pkglist = shell('pip3 list -o')
        print(*pkglist, sep='\n')
        for line in pkglist[2:]:
            pkg = line.split()
            if pkg:
                run_pip('install', '-U', pkg[0])
    else:
        if packages:
            pkgs = []
            cached_pkgs = get_pkgs(root)
            for pkg in packages:
                pkg = pkg.replace('-', '_')
                if pkg in cached_pkgs:
                    path, ver = cached_pkgs[pkg]
                    pkgs.append(str(path))
                    print(f'Add pkg {pkg} version: {ver}')
                else:
                    pkgs.append(pkg)
                    info(f'Add pkg {pkg}')
            root.chdir()
            run_pip('install', *pkgs)
            # exec_cmd('pip','install %s'%(" ".join(pkgs)))
        else:
            if Path('setup.py'):
                run_setup('install')
                pyclean()
            else:
                print('Can''t find the file setup.py!')


if __name__ == "__main__":
    py_setup()
