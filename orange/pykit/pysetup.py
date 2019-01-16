# 项目：工具函数库
# 模块：python模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-28 21:52

from orange.shell import Path, sh, POSIX, HOME
from orange.utils.click import command, arg

libpath = HOME/'OneDrive/pylib'


def run_cmd(cmd: str, *args, **kw)->int:
    return sh(cmd, *args, capture_output=False, **kw)


def pyclean():
    Patterns = ('build', 'dist', '*egg-info')
    for path in filter(
            lambda path: any(map(path.match, Patterns)), Path('.')):
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


@command(allow_empty=True)
@arg('packages', help='python package', nargs='*', metavar='package')
@arg('-p', '--path', default=libpath, help='指定的目录')
@arg('-d', '--download', help='默认的包目录', action='store_true')
def pyinstall(packages=None, path=None, download=None, upgrade=False):
    root = Path(path)
    if download:
        pip('download', '-d', str(root), *packages)
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
            pip('install', *pkgs)
        else:
            if Path('setup.py'):
                pysetup('install')
            else:
                print('Can''t find the file setup.py!')


if __name__ == '__main__':
    pyinstall()
