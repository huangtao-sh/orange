# 项目：标准库函数
# 模块：程序版本模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-11 12:59

from orange.path import Path
from distutils.version import StrictVersion as Ver

first=lambda x:x and x[0]
last=lambda x:x and x[-1]

def get_ver():
    ver_file=first(list(Path(".").glob("*/__version__.py")))
    if ver_file:
        for line in ver_file.lines:
            if line.startswith('version'):
                return line.split('"')[1]

def upgrade_ver(ver,segment='#'):
    if not isinstance(ver,Ver):
        v=Ver(ver)
    if isinstance(segment,str):
        segment={'major':0,
                 'm':0,
                 'minor':1,
                 'n':1,
                 'micro':2,
                 'o':2,
                 'dev':3,
                 'd':3,
                 '#':4,}.get(segment.lower(),4)
    if(v.prelease and segment<4)or(not v.prelease and segment>=4):
        raise Exception('版本升级失败')
    if segment==5:
        v.prelease=v.prelease[0],v.prelease[1]+1
    elif segment==4:
        if v.prelease[0]=='a':
            v.prelease='b',1
        else
            v.prelease=None
    else
        v.prelease='a',1
        v.version=v.version[:segment],v.version[segment]+1,(0,0,0).version[segment:]
    return v
        
            
        
            
    
