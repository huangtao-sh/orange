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
        run_pip('download', '-d', str(PyLib), param, pkg)


def config_pkg():
    pkgs = shell('pip3 list --format json')
    packages = [pkg['name'] for pkg in json.loads(pkgs[0])]
    t = get_supported()[0]
    params = {
        'implementation': t[0][:2],
        'python-version': t[0][2:],
        'abi': t[1],
        'platform': t[2],
        'only-binary': ':all:'
    }
    conf = {'packages': packages,
            'params': params}
    with ConfFile.open('w')as f:
        json.dump(conf, f)
    print('写配置文件成功！')


@arg('-c', '--config', action='store_true', help='获取配置')
@arg('-d', '--download', action='store_true', help='下载包文件')
@arg('-u', '--upgrade', action='store_true', help='升级文件')
def main(config=False, download=False, upgrade=False):
    if config:
        if sys.platform == 'win32':
            config_pkg()
        else:
            print('请在不联网的机器上使用此功能')
    if download:
        if sys.platform == 'win32':
            print('请在联网的机器上使用此功能')
        else:
            batch_download()
    if upgrade:
        if sys.platform == 'win32':
            print('请在联网的机器上使用此功能')
        else:
            pkglist = shell('pip3 list -o')
            print(*pkglist, sep='\n')
            for line in pkglist[2:]:
                pkg = line.split()
                if pkg:
                    run_pip('install', '-U', pkg[0])
    

