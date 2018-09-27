# 项目：标准库函数
# 模块：安装模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-12 18:05
# 修改：2018-09-12 10:29 采用 shell 执行系统命令


import distutils.core
import setuptools
from .htutil import shell, run_cmd
from .shell import Path, POSIX
from .utils import R
from collections import ChainMap
from .version import Ver


def get_path(pkg, user=True):
    ''' 返回指定包的参数配置目录和数据目录'''
    if POSIX:
        if user:
            root = Path('~')
            return root, root / ('.%s' % (pkg))
        else:
            root = Path('/usr/local')
            return root/'etc', root/'var'/pkg
    else:
        if user:
            root = Path('~/AppData')
            return root / 'Roaming', root / 'Local' / pkg
        else:
            root = Path('%programdata%') / pkg
            return root, root


def run_pip(*args, **options):
    return run_cmd('pip3', *args, **options)


def run_setup(*args, **options):
    cmd = 'python3 setup.py' if POSIX else 'setup'
    return run_cmd(*cmd.split(' '), *args, **options)


def pyclean():
    for path in ('build', 'dist', '*egg-info'):
        for p in Path('.').glob(path):
            p.rmtree()
            print(f'Path {p} have been deleted!')


DEFAULT = {'author': 'huangtao',
           'author_email': 'huangtao.sh@icloud.com',
           'platforms': 'any',
           'license': 'GPL', }


def find_package(path='.', exclude=None):
    result = {}
    path = Path(path)
    packages = [".".join(p.parts[:-1])for p in path.rglob('__init__.py')]
    if exclude:
        packages = tuple(set(packages)-set(exclude))
    if packages:
        result['packages'] = packages
    data = {}
    for pkg in filter(lambda x: "." not in x, packages):
        root = path/pkg
        filelist = [str(p-root)for p in root.rglob('*.*')
                    if p.lsuffix not in ('.py', '.pyw', '.pyc')]
        if filelist:
            data[pkg] = filelist
    if data:
        result['package_data'] = data
    requirefile = Path('requires.txt')
    if requirefile:
        comm = R/r'#.*'
        requires = tuple(filter(None,
                                map(lambda x: (comm/x % '').strip(), requirefile.lines)))
        if requires:
            result['install_requires'] = requires
    scriptpath = Path('scripts')
    if scriptpath:
        scripts = [str(path) for path in Path('.').glob('scripts/*')]
        if scripts:
            result['scripts'] = scripts
    ver = Ver.read_file()
    if ver:
        result['version'] = str(ver)
    return result


def setup(after_install=None,
          cscripts=None, gscripts=None,
          **kwargs):
    if cscripts or gscripts:
        entry_points = kwargs.get('entry_points', {})
        if cscripts:
            entry_points['console_scripts'] = cscripts
        if gscripts:
            entry_points['gui_scripts'] = gscripts
        kwargs['entry_points'] = entry_points

    kwargs = ChainMap(kwargs,
                      find_package(exclude=('testing', 'scripts')),
                      DEFAULT)

    # 安装程序
    dist = distutils.core.setup(**kwargs)
    # 处理脚本
    scripts = kwargs.get('scripts', None)
    if 'install' in dist.have_run and POSIX \
            and scripts:
        prefix = Path('/usr/local/bin')
        for script in scripts:
            script_name = prefix/(Path(script).name)
            if script_name.lsuffix in ('.py', '.pyw')\
                    and script_name.exists():
                script_name.replace(script_name.with_suffix(''))
    if 'install' in dist.have_run and after_install:
        after_install(dist)
