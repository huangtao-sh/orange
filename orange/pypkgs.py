# 项目：库函数
# 模块：包管理模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-13 09:13

# 有一台电脑是 win32 的系统，且无法上网，无法自动升级 Python 包。故
# 编写本程序来对这些程序包进行管理

from orange import Path, shell, arg
import json
from orange.deploy import run_pip
from pip._internal.pep425tags import get_supported
import sys

ROOT = Path('~/OneDrive')
ConfFile = ROOT / 'conf/pypkgs.conf'
PyLib = ROOT / 'pylib'

excludes = set(['green-mongo', 'orange-kit', 'coco', 'glemon', 'lzbg'])


def batch_download():
    with ConfFile.open('r')as f:
        conf = json.load(f)
    packages = set(conf['packages'])-excludes
    params = conf['params']
    param = ' '.join(f'--{key}={value}' for key, value in params.items())
    for pkg in packages:
        result = run_pip('download', '-d', str(PyLib), param, pkg)
        if result:
            run_pip('download', '-d', str(PyLib),
                    pkg, **{'no-binary': ':all:'})


def get_installed_packages():
    pkgs = shell('pip3 list --format json')
    return tuple(pkg['name'] for pkg in json.loads(pkgs[0]))


def config_pkg():
    packages = get_installed_packages()
    t = get_supported()[0]
    params = {
        'implementation': t[0][:2],
        'python-version': t[0][2:],
        'abi': t[1],
        'platform': 'win32',
        'only-binary': ':all:'
    }
    conf = {'packages': packages,
            'params': params}
    with ConfFile.open('w')as f:
        json.dump(conf, f, indent='    ')
    print('写配置文件成功！')


@arg('-c', '--config', action='store_true', help='获取配置')
@arg('-d', '--download', action='store_true', help='下载包文件')
@arg('-u', '--upgrade', action='store_true', help='升级文件')
@arg('-i', '--install', action='store_true', help='批量安装')
def main(config=False, download=False, upgrade=False, install=False):
    if config:
        config_pkg()
    if download:
        batch_download()
    if upgrade:
        pkglist = shell('pip3 list -o')
        print(*pkglist, sep='\n')
        for line in pkglist[2:]:
            pkg = line.split()
            if pkg:
                run_pip('install', '-U', pkg[0])
    if install:
        with ConfFile.open('r')as f:
            conf = json.load(f)
        packages = set(conf['packages'])-excludes-set(get_installed_packages())
        packages.add('python-docx')
        if packages:
            run_pip('install', *packages)
