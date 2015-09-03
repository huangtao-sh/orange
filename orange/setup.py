# 项目：Pytohon工具包
# 模块：安装模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-09-03 16:02
import os
import sys
from stdlib import exec_shell,parse_args
from stdlib.pytools import get_package
def real_path(path):
    return os.path.abspath(os.path.expanduser(path))

def exec_cmd(cmd,argument,sudo=False):
    if os.name=='posix':
        cmd='%s3'%(cmd)
    cmdline='%s %s'%(cmd,argument)
    if sudo and sys.platform.startswith('linux'):
        cmdline='sudo %s'%(cmdline)
    exec_shell(cmdline)

def python_setup(argv=None):
    proc=setup_cmd.pop('proc')
    parse_args(setup_cmd,argv,allow_empty=True,proc=proc)

def py_setup(packages,path,download):
    path=real_path(path)
    if download:
        exec_cmd('pip','install -d %s %s'%(path,
                             " ".join(packages)))
    else:
        if packages:
            pkgs=[]
            for pkg in packages:
                pkg_path=get_package(pkg,path)
                if pkg_path:
                    pkgs.append('"%s"'%(pkg_path))
                else:
                    pkgs.append(pkg)
            exec_cmd('pip','install %s'%(" ".join(pkgs)))
        else:
            if os.path.isfile('setup.py'):
                exec_cmd('python','setup.py install',sudo=True)
            else:
                print('Can''t find the file setup.py!')
            
setup_cmd={
    'proc':py_setup,
    'packages':{'help':'python包',
                'nargs':'*',
                'metavar':'package',},
    '-p --path':{'help':'指定的路径',
                 'default':'~/OneDrive/pylib',},
    '-d --download':{'help':'下载指定的包',
                     'action':'store_true',}}
        
