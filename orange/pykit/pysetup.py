# 项目：工具函数库
# 模块：python模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-28 21:52

import sysconfig
from orange.shell import Path, sh, POSIX, HOME
from orange.utils.click import command, arg
from orange.pykit.config import config
from orange.pykit.version import Ver

libpath = HOME/'OneDrive/pylib'


def run_cmd(cmd: str, *args, **kw) -> int:
    return sh(cmd, *args, capture_output=False, **kw)


def pyclean():
    Patterns = ('build', 'dist', '*egg-info')
    for path in filter(
            lambda path: any(map(path.match, Patterns)), Path('.')):
        path.rmtree()
        print(f'Path {path} have been deleted!')


def pysetup(*args) -> int:
    if not Path('setup.py'):
        print('Can''t find file setup.py!')
        exit(1)
    cmd = 'python3 setup.py' if POSIX else 'setup'
    run_cmd(cmd, *args)
    pyclean()


def pip(*args) -> int:
    return run_cmd('pip3', *args)


def pyupload():
    pysdist('upload')


def pysdist(*args):
    pysetup('sdist', '--dist-dir', libpath, *args)


ver = sysconfig._PY_VERSION_SHORT_NO_DOT
BINARY_PARAMS = {
    'implementation': 'cp',
    'platform': 'win32',
    'python-version': ver,
    'abi': f'cp{ver}m',
    'only-binary': ':all:',
}


def pydownload(*pkgs, source=True):
    if source:
        pip('download', *pkgs, '-d', str(libpath),
            '--no-binary=:all:', '--no-deps')
    else:
        pip('download', *pkgs, '-d', str(libpath), '--no-deps',
            *(f'--{k}={v}'for k, v in BINARY_PARAMS.items()))


@command(allow_empty=True)
@arg('packages', help='python package', nargs='*', metavar='package')
@arg('-p', '--path', default=libpath, help='指定的目录')
@arg('-d', '--download', help='默认的包目录', action='store_true')
@arg('-b', '--binary', action='store_true', help='下载二进制程序包')
def pyinstall(packages=None, path=None, download=None, upgrade=False, binary=False):
    root = Path(path)
    if download:
        pydownload(*packages, source=not binary)
    else:
        if packages:
            pkgs = []
            for pkg in packages:
                filename = root.find(f'{pkg}*', key=Ver)
                if filename:
                    pkgs.append(filename)
                else:
                    pkgs.append(pkg)
            pip('install', *pkgs)
        else:
            if Path('setup.py'):
                pysetup('install')
            else:
                print('Can''t find the file setup.py!')


if __name__ == '__main__':
    pyinstall()
