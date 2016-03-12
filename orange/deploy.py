# 项目：标准库函数
# 模块：安装模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-12 18:05

import setuptools
import os
from orange import Path,get_ver

def setup(version=None,packages=None,
          scripts=None,
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
    if not scripts:
        scripts=[str(path) for path in Path('.').glob('scripts/*')]
    # 安装程序 
    setuptools.setup(scripts=scripts,packages=packages,
                     version=version,**kwargs)
    # 处理脚本
    if scripts and os.name=='posix':
        from sysconfig import get_path
        prefix=Path(get_path('scripts'))
        for script in scripts:
            script_name=prefix/Path(script).name
            if script_name.suffix.lower() in ['.py','.pyw']\
              and script_name.exists():
                script_name.replace(script_name.with_suffix(''))

