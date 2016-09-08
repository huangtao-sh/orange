# 项目：标准库函数
# 模块：安装模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-12 18:05

import distutils.core
import os
from orange import Path,get_ver
import setuptools

def run_setup(*args):
    distutils.core.run_setup('setup.py',args)

def setup(version=None,packages=None,
          scripts=None,install_requires=None,
          **kwargs):
    kwargs.setdefault('author','huangtao') # 设置默认的用户
    # 设置默认邮箱
    kwargs.setdefault('author_email','huangtao.sh@icloud.com')
    # 设置默认平台
    kwargs.setdefault('platforms','any')
    # 设置默认授权
    kwargs.setdefault('license','GPL')
    if not packages:
        # 自动搜索包
        packages=setuptools.find_packages(exclude=('testing',
                                                   'scripts'))
    if not version:
        # 自动获取版本
        version=get_ver()
    if not install_requires:
        requires=[*fn.lines for fn in  Path('.').\
                  rglob('requires.txt')]
        requires=[x.strip() for x in requires if not \
                  x.strip().startswith('#')]
    if not scripts:
        scripts=[str(path) for path in Path('.').glob('scripts/*')]
    # 安装程序 
    d=distutils.core.setup(scripts=scripts,packages=packages,
            install_requires=install_requires,
            version=version,**kwargs)
    # 处理脚本
    if 'install' in d.has_run() and os.name=='posix'\
      and scripts:
        from sysconfig import get_path
        prefix=Path(get_path('scripts'))
        for script in scripts:
            script_name=prefix/Path(script).name
            if script_name.suffix.lower() in ['.py','.pyw']\
              and script_name.exists():
                script_name.replace(script_name.pname)

