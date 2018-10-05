# 项目：工具函数库
# 模块：python模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-28 21:52

from orange.shell import Path, sh, POSIX, HOME

libpath = HOME/'OneDrive/pylib'


def run_cmd(cmd: str, *args, **kw)->int:
    return sh(cmd, *args, capture_output=False, **kw)


def pyclean():
    Patterns = ('build', 'dist', '*egg-info')
    for path in filter(
            lambda path: path.is_dir() and tuple(filter(path.match, Patterns)), Path('.')):
        path.rmtree()
        print(f'Path {path} have been deleted!')


def pysetup(*args)->int:
    if not Path('setup.py'):
        print('Can''t find file setup.py!')
        exit(1)
    cmd = 'python3 setup.py' if POSIX else 'setup'
    run_cmd(cmd, *args)
    pyclean()


def pip(*args)->int:
    return run_cmd('pip3', *args)


def pyupload():
    pysdist('upload')


def pysdist(*args):
    pysetup('sdist', '--dist-dir', libpath, *args)


def pyinstall():
    pysetup('install')


if __name__ == '__main__':
    pyinstall()
