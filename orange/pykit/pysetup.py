# 项目：工具函数库
# 模块：python模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-28 21:52

from orange.shell import Path, sh, POSIX, HOME
from orange.utils import R

libpath = HOME/'OneDrive/pylib'


def run_cmd(cmd: str, *args, **kw)->int:
    return sh(cmd, *args, capture_output=False, **kw)


def pysetup(*args)->int:
    if not Path('setup.py'):
        print('Can''t find file setup.py!')
        exit(1)
    cmd = 'python3 setup.py' if POSIX else 'setup'
    return run_cmd(cmd, *args)


def pip(*args)->int:
    return run_cmd('pip3', *args)


def pyupload():
    pysdist('upload')


def pysdist(*args):
    pysetup('sdist',  '--dist-dir', libpath, *args)
    pyclean()


def pyclean():
    Patterns = ('build', 'dist', R/r'.*?egg-info')
    for path in Path('.'):
        if path.is_dir() and path.name in Patterns:
            path.rmtree()
            print(f'Path {path} have been deleted!')
    return


def py_setup():
    pysetup('install')
    pyclean()


if __name__ == '__main__':
    py_setup()
