#!/usr/bin/env python3
import os
import sys
from datetime import date,timedelta
from sysconfig import get_path
from tempfile import NamedTemporaryFile,mktemp
from contextlib import contextmanager
import logging
import time
utc_offset=timedelta(seconds=time.timezone)
def utctime(localtime):
    '''将本地时间转换成utc时间'''
    return localtime+utc_offset

def localtime(utctime):
    '''将utc时间转换成本地时间'''
    return utctime-utc_offset

def is_test(file_name=None):
    '''
    判断是否在测试环境。
    '''
    file_name=file_name or sys.argv[0]
    return('test' in file_name)or(not is_installed(file_name))
    
def logger(**kwargs):
    '''
    获取日志接口
    '''
    if not hasattr(logging,'init'):
        kwargs.setdefault('datefmt','%Y-%m-%d %H:%M')
        kwargs.setdefault('format','%(asctime)s %(levelname)s\t'\
                          '%(message)s')
        kwargs.setdefault('level',10 if is_test() else 30)
        logging.basicConfig(**kwargs)
        logging.init=True
    return logging

def is_installed(file_name):
    '''
    确认指定的文件是否已被安装。
    '''
    paths=[get_path(name) for name in ('platlib','scripts')]
    if WINDOWS:
        file_name=file_name.lower()
        paths=[path.lower() for path in paths]
    return any([file_name.startswith(path) for path in paths])

def ensure_path(path):
    '''
    确认指定的文件夹是否存在。如不存在则自动建立此文件夹。
    '''
    path=Path(path)
    if not path.is_dir():
        path.makedir(exist_ok=True)

def join(*args,sep=os.path.sep):
    '''
    join函数的格式化版，可以保持分隔符的统一
    默认在WINDOWS平台下使用“\”，在Linux平台下使用“/”
    '''
    path=os.path.join(*args)
    old_sep='/' if sep=='\\' else '\\'
    return os.path.join(*args).replace(old_sep,sep)

@contextmanager
def get_tmpfile(text=None,writer=None,**kwargs):
    '''
    获取临时文件函数，使用方法如下：
    with get_tmpfile() as name:
        os.system('cat %s'%(name))
    '''
    try:
        name=mktemp(**kwargs)
        if text:
            write_file(name,text)
        if writer:
            with open(name,'w+t') as fn:
                writer.write(fn)
        yield name
    finally:
        if os.path.isfile(name):
            os.remove(name)

def tmpfile(**kwargs):
    '''
    创建带文件名的临时文件，可以通过tmp.name访问文件名。
    可以通过tmp.file读写文件。
    '''
    kwargs.setdefault('mode','w+t')
    return NamedTemporaryFile(**kwargs)

# 写文本文件，使用utf-8编码，不带BOM
def write_file(file_name,text,encoding='utf-8'):
    '''
    采用UTF8格式写文本文件，其中text可以为一段字符串，也可以是列表。
    '''
    file=Path(file_name)
    ensure_path(file.parent)
    with file.open('wb') as fn:
        if type(text) in[tuple,list]:
            text="\n".join(text)
        fn.write(text.encode(encoding=encoding))
        
BOM_CODE={
    BOM_UTF8:'utf_8',
    BOM_LE:'utf_16_le',
    BOM_BE:'utf_16_be',
    }
    
DEFAULT_CODES=['utf8','gbk','utf16','big5']

def decode(d):
    '''
    对指定的二进制，进行智能解码，适配适当的编码。按行返回字符串。
    '''
    for k in BOM_CODE:
        if k==d[:len(k)]:
            text=d[len(k):].decode(BOM_CODE[k])
            return text.splitlines()
    for encoding in DEFAULT_CODES:
        try:
            text=d.decode(encoding)
            return text.splitlines()
        except:
            continue
    raise Exception('解码失败')    

def read_file(file_name):
    '''
    全部读取文件，并进行解码，解码失败则触发异常，并返回字符吕列表。
    '''
    with Path(file_name).open('rb')as fn:
        return decode(fn.read())

# 以源目录为基准，更新目标目录的文件，仅复制需要更新的文件
def smart_copy(src,dest,ignore=None):
    dc=dircmp(src,dest,ignore=ignore)
    #删除目标中不存在的文件
    for f in dc.right_only:
        f=join(dc.right,f)
        if os.path.isdir(f):
            rmtree(f)
        else:
            remove(f)
        print('文件 %s 已被删除。'%(f))
    #拷备目标目录中不存在的文件
    for f in dc.left_only:
        sf=join(dc.left,f)
        if os.path.isdir(sf):
            copytree(sf,join(dc.right,f))
        else:
            copy(sf,dc.right)
        print('文件或目录 %s 已被更新'%(sf))
    #更新不同文件
    for f in dc.diff_files:
        f=join(dc.left,f)
        copy(f,dc.right)
        print('文件 %s 已被更新。'%(f))
    #处理子文件夹
    for d in dc.common_dirs:
        smart_copy(join(dc.left,d),join(dc.right,d))

def leap_year(year):
    '''
    判断是否为闰年。
    '''
    return year%400==0 or(year%4==0 and year%100!=0)
    
def end_of_month(date):
    '''
    判断指定的日期是否为月末。
    '''
    return (date+timedelta(days=1)).day==1
def first_of_month(date):
    '''
    判断指定的日期是否为月初
    '''
    
    return date.day==1

def year_frac(begin,end,basis=0):
    BASIS={
        '30/360':0,
        'ACT/365':1,
        'ACT/360':2,
        'AFI/365':3,
        '30E/360':4,
        'YMD':5,
        }
    if isinstance(basis,str):
        basis=BASIS[mode]
    if basis in (1,2,3):
        days=(end-begin).days
    else:
        days=(end.year-begin.year)*360+(end.month-begin.month)*30
    
    if basis in (4,5):
        d1=30 if begin.day>30 else begin.day
        d2=30 if end.day>30 else end.day
        if basis==5:
            if (end_of_month(end)and(d1>d2)):
                d2=d1
        days+=d2-d1
    if basis ==0:
        d1=30 if end_of_month(begin) else begin.day
        d2=30 if end_of_month(end) else end.day
        if(end.day==31)and(begin.day<30):
            d2=31
        days+=d2-d1
        
    if basis in (0,2,4,5):
        base=360
    elif basis==3:
        base=365
    elif basis==1:
        if end.year==begin.year:
            base=366 if leap_year(begin.year) else 365
        elif(end.year-begin.year==1)and((end.month<begin.month)or(end.month==begin.month and end.day<=begin.day)):
            if(leap_year(begin.year))and(begin<=date(begin.year,2,29)):
                base=366
            elif(leap_year(end.year))and(end>=date(end.year,2,29)):
                base=366
            else:
                base=365
        else:
            base=sum([366 if leap_year(y) else 365 for y in range(begin.year,end.year+1)])/(end.year-begin.year+1)
    return days,days/base
    
def date_add(day,years=0,months=0,days=0,weeks=0):
    '''
    日期加减函数，如果是整年、整月，如无对应日期，则以到期月份的月底
    '''
    m=(day.year+years)*12+day.month+months-1
    try:
        day=day.replace(year=m//12,month=m%12+1)
    except:
        m+=1
        days-=1
        day=day.replace(year=m//12,month=m%12+1,day=1) 
    days+=weeks*7
    if days:
        day=day+timedelta(days=days)
    return day
    
def delta(base,target):
    '''
    比较两个列表的差异。
    '''
    a,b=set(base),set(target)
    return list(a-b),list(b-a),list(a&b),list(a|b)

def read_shell(cmd):
    '''
    执行系统命令，并将执行命令的结果通过管道读取。
    '''
    with os.popen(cmd)as fn:
        k=fn.read()
    return k.splitlines()

def write_shell(cmd,lines):
    '''
    执行系统命令，将指定的文通过管道向该程序输入。
    '''
    with os.popen(cmd,'w') as fn:
        if isinstance(lines,str):
            fn.write(lines)
        elif type(lines)in(tuple,list):
            [fn.write('%s\n'%(x))for x in lines]

def exec_shell(cmd):
    '''
    执行系统命令。
    '''
    return os.system(cmd)

def wlen(s):
    '''
    用于统计字符串的显示宽度，一个汉字或双字节的标点占两个位，
    单字节的字符占一个字节。
    '''
    return sum([2 if ord(x)>127 else 1 for x in s])

def parse_args(template,argv=None,instance=None,
               cls=None,
               print_usage=True,func=None,
               allow_empty=False,proc=None,
               **parser_args):
    '''
    tmplate:参数模板
    argv:系统命令行
    instance：应用实例
    allow_empty：是否允处理空命令行，如果不允许，则空命令时打印用法
    print_usage:同allow_tempty，该参数将会被删除
    fun：同proc,该参数将会被删除
    parser_args:ArgumentParser的参数，如prog,description等。
    '''
    argv=argv or sys.argv[1:] # 如argv为空，则重新获取命令行
    if isinstance(template,dict):
        import stdlib.argparser
        return stdlib.argparser.parse_args(template,argv,cls,
                allow_empty=allow_empty,proc=proc,**parser_args)

    # 以下代码为保持老参数的兼容性
    allow_empty=allow_empty and (not print_usage)
    proc=proc or func
    
    from argparse import ArgumentParser
    parser=ArgumentParser(**parser_args)
    def add_arg(arg=None,**kwargs):
        if isinstance(arg,str):
            if ',' in arg:
                arg=arg.split(',')
            else:
                arg=arg.split()
        parser.add_argument(*arg,**kwargs)
    for arg in template:
        add_arg(**arg)
        
    if not argv and not allow_empty:
        parser.print_usage()
    else:
        namespace=parser.parse_args(argv,instance)
        if instance:
            if hasattr(instance,'run'):
                instance.run()
        else:
            if proc:
                proc(**dict(namespace._get_kwargs()))
            return namespace
        
def __get_des():
    from stdlib.pyDes import des,PAD_PKCS5
    return des(key='huangtao',padmode=PAD_PKCS5)

def encrypt(pwd):
    '''
    可逆加密程序。
    '''
    b=__get_des().encrypt(pwd)
    return "".join(['%02X'%(x)for x in b])

def decrypt(code):
    '''
    解密程序。
    '''
    b=__get_des().decrypt(bytes.fromhex(code))
    return b.decode('utf8')

def get_pinyin(s):
    '''
    获取拼音字母。
    '''
    from pypinyin import pinyin
    return ''.join([x[0] for x in pinyin(s,style=4)])

