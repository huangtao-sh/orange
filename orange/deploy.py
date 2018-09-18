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
from orange import Path, Ver, POSIX


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


def _get_requires():
    result = []
    requires = Path('requires.txt')
    if requires:
        for row in requires.lines:
            i = row.find('#')
            if i > -1:
                row = row[:i]
            row = row.strip()
            if row:
                result.append(row)
    return result


def setup(version=None, packages=None, after_install=None,
          scripts=None, install_requires=None,
          cscripts=None, gscripts=None,
          **kwargs):
    if cscripts or gscripts:
        entry_points = kwargs.get('entry_points', {})
        if cscripts:
            entry_points['console_scripts'] = cscripts
        if gscripts:
            entry_points['gui_scripts'] = gscripts
        kwargs['entry_points'] = entry_points
    for k, v in DEFAULT.items():
        kwargs.setdefault(k, v)
    if not packages:
        # 自动搜索包
        packages = setuptools.find_packages(exclude=('testing',
                                                     'scripts'))
    if not version:
        # 自动获取版本
        version = str(Ver.read_file())
    if not install_requires:  # 从repuires.txt 中获取依赖包
        install_requires = _get_requires()
    if not scripts:
        scripts = [str(path) for path in Path('.').glob('scripts/*')]
    # 安装程序
    dist = distutils.core.setup(scripts=scripts, packages=packages,
                                install_requires=install_requires,
                                version=version, **kwargs)
    # 处理脚本
    if 'install' in dist.have_run and POSIX \
            and scripts:
        from sysconfig import get_path
        prefix = Path(get_path('scripts'))
        for script in scripts:
            script_name = prefix/(Path(script).name)
            if script_name.lsuffix in ['.py', '.pyw']\
                    and script_name.exists():
                script_name.replace(script_name.with_suffix(''))
    if 'install' in dist.have_run and after_install:
        after_install(dist)
