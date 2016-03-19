# 项目：Pytohon工具包
# 模块：安装模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-09-03 16:02
# 修改：2016-03-08 16:47
import os
import sys
from orange.stdlib import exec_shell
from orange.path import Path
from orange.debug import *
from orange.parseargs import *
# from stdlib.pytools import pyclean
import re

RootPath='~/OneDrive/pylib'
Pattern=re.compile(r'\d+(\.\d+)*([ab]\d+)?')

def find_ver(path):
    v=Pattern.search(path.name)
    if v:
        return Ver(v.group())

def exec_cmd(cmd,argument,sudo=False):
    if os.name=='posix':
        cmd='%s3'%(cmd)
    cmdline='%s %s'%(cmd,argument)
    if sudo and sys.platform.startswith('linux'):
        cmdline='sudo %s'%(cmdline)
    exec_shell(cmdline)

def py_setup(packages,path,download):
    root=Path(path)
    if download:
        exec_cmd('pip','install -d %s %s'%(path,
                             " ".join(packages)))
    else:
        if packages:
            pkgs=[]
            for pkg in packages:
                pkg_path,pkg_ver=None,Ver('0.0')
                for file in root.glob('%s*'%(pkg)):
                    log.info('Process file %s'%(file.name))
                    ver=find_ver(file)
                    log.info('Get ver %s'%(ver))
                    if ver>pkg_ver:
                        pkg_path=file
                        pkg_ver=ver
                if pkg_path:
                    if fileext(pkg_path,True) in ('.zip','.whl','.gz'):
                        pkgs.append('"%s"'%(pkg_path))
                        log.info('Add file %s'%(pkg_path.name))
                    else:
                        print('%s 不是正常的包文件'%(pkg_path.name))
                else:
                    pkgs.append(pkg)
                    log.info('Add pkg %s'%(pkg))
            exec_cmd('pip','install %s'%(" ".join(pkgs)))
        else:
            if Path('setup.py').exists():
                exec_cmd('python','setup.py install',sudo=True)
                pyclean()
            else:
                print('Can''t find the file setup.py!')

pysetup=Parser(
    Argument(
        'packages',
        help='python package',
        nargs='*',
        metavar='package'),
    Argument('-p','--path',
             default=RootPath,
             help='指定的目录'),
    Argument('-d','--download',
             help='默认的包目录',
             action='store_true'),
    proc=py_setup,
    allow_empty=True)
if __name__=="__main__":
    pysetup()
