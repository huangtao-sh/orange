from lxml.etree import *
from orange.parseargs import *
from orange import *

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

def create_plist(filename=None,label=None,program=None,args=None):
    label=label or Path(program[0]).name
    filename=filename or label
    filename=str(Path(filename).with_suffix('.plist'))
    if args:
        program.extend(args)
    print(label,filename,*program)
    return 
    create_xml(filename,KeepAlive=True,ProgramArguments=args,
               Label=label)

def proc(filename=None,label=None,program=None,args=None):
    print(filename,label,program,args)
    

main=Parser(
    Arg('-l','--label',metavar='label',help='程序标签'),
    Arg('-f','--filename',metavar='filename',help='文件名'),
    Arg('program',nargs=1,help='程序命令'),
    Arg('args',nargs='*',metavar='arg',help='程序的参数'),
    proc=create_plist)

if __name__=='__main__':
    main()
