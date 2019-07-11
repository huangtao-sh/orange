# 项目：库函数
# 模块：包管理模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-13 09:13

# 有一台电脑是 win32 的系统，且无法上网，无法自动升级 Python 包。故
# 编写本程序来对这些程序包进行管理
from orange.utils.config import YamlConfig
import sys
import json
from orange import shell, arg, tprint
from orange.pykit import pip, Ver
from collections import defaultdict
from orange.shell import HOME, Path
from .pysetup import pydownload
ROOT = HOME/'OneDrive'
PyLib = ROOT/'pylib'


DefaultConfig = {
    'Local': ['orange_kit', 'gmono', 'glemon', 'lzbg', 'pygui'],
    'Wheel': [],
    'Source': []
}

ConfFile = HOME / 'OneDrive/conf/pypkgs.yaml'    # 配置文件路径

excludes = set(['green-mongo', 'orange-kit', 'coco', 'glemon', 'lzbg'])


def is_connected(url=None):
    '''检查本机是否联网
    '''
    url = url or 'https://pypi.douban.com/simple'
    from urllib.request import urlopen
    try:
        with urlopen(url) as r:
            return r.code == 200
    except:
        return False


def batch_download(config):
    for pkg in config['Wheel']:
        pydownload(pkg, source=False)
    for pkg in config['Source']:
        pydownload(pkg, source=True)


def get_installed_packages():
    pkgs = shell('pip3 list --format json')
    return tuple(pkg['name'] for pkg in json.loads(pkgs[0]))


def get_cached_pkgs():
    for path in PyLib.glob('*.*'):
        print(path)
        verinfo = path.verinfo
        print(verinfo)
        if verinfo:
            name, ver, type_ = verinfo[:3]
            yield name, ver, type_, path


def cleanlib():
    pkg = None
    for r in sorted(get_cached_pkgs(), reverse=True):
        if pkg != r[0]:
            pkg = r[0]
        else:
            r[3].unlink()
            print(f'{r[3]} has been deleted')


def config_pkg(config):
    local = config['Local']
    wheel, source = [], []
    data = []
    for path in PyLib.glob('*.*'):
        verinfo = path.verinfo
        if verinfo:
            name, ver, type_ = verinfo[:3]
            data.append([name, str(ver), type_])
            if type_ == 'Wheel':
                wheel.append(name)
            elif type_ == 'Source' and name not in local:
                source.append(name)
    config['Wheel'] = wheel
    config['Source'] = source
    tprint(data, {0: '20', 1: '10'}, sep='    ')


@arg('-f', '--config', action='store_true', help='获取配置')
@arg('-d', '--download', action='store_true', help='下载包文件')
@arg('-u', '--upgrade', action='store_true', help='升级文件')
@arg('-i', '--install', action='store_true', help='批量安装')
@arg('-c', '--clean', action='store_true', help='清理无用的包')
def main(download=False, upgrade=False, install=False, **options):
    config = YamlConfig(default=DefaultConfig, filename=ConfFile)
    if options['config']:
        config_pkg(config)
    if download:
        batch_download(config)
    if upgrade:
        if is_connected():
            pkglist = shell('pip3 list -o')
            print(*pkglist, sep='\n')
            for line in pkglist[2:]:
                pkg = line.split()
                if pkg:
                    pip('install', '-U', pkg[0])
        else:
            print('未连接互联网，无法升级')

    if install:
        if is_connected():
            pkgs = config['Wheel']+config['Source']
            for pkg in pkgs:
                pip('install', pkg)
        else:
            r = input('未连接互联网，请确认是否安装, Y or N?')
            if r.lower() == 'y':
                for pkg in get_cached_pkgs():
                    pip('install', '--no-deps', '--ignore-installed',
                        pkg[-1])

    if options['clean']:
        cleanlib()
