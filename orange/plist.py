# 项目：标准库函数
# 模块：macos的plist生成器
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-09-06 23:27

import sys
from lxml.etree import *
from orange.parseargs import *
from orange import *
import sys

PATTERN='''<?xml version="1.0"?>  
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">  
<plist version="1.0"/>  
'''

def create_xml(filename,**kw):
    root=XML(PATTERN)
    def add(parent,val,key=None):
        if key:
            SubElement(parent,'key').text=key
        if isinstance(val,dict):
            t=SubElement(parent,'dict')
            for k,v in val.items():
                add(t,v,k)
        elif isinstance(val,bool):
            SubElement(parent,'true' if val else 'false')
        elif isinstance(val,str):
            SubElement(parent,'string').text=val
        elif isinstance(val,(list,tuple)):
            a=SubElement(parent,'array')
            for i in val:
                add(a,i)
    add(root,kw)
    ElementTree(root).write(filename,pretty_print=True,xml_declaration=True,
          encoding='UTF-8')

def create_plist(filename,label,*args):
    filename=str(Path(filename).with_suffix('.plist'))
    create_xml(filename,KeepAlive=True,ProgramArguments=args,
               Label=label)

def main():
    args=sys.argv
    if len(args)<4:
        print('Usage:\n'
        '\t%s plist-file-name label program args'%(args[0]))
    else:
        create_plist(*args[1:])
    

if __name__=='__main__':
    main()
