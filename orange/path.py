# 项目：standard python lib
# 模块：path and file
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-11 12:21
# 修改：2016-04-13 21:01

import pathlib
import os
from codecs import BOM_UTF8,BOM_LE,BOM_BE
from .parseargs import Parser,Argument

BOM_CODE={
    BOM_UTF8:'utf_8',
    BOM_LE:'utf_16_le',
    BOM_BE:'utf_16_be',
    }
    
DEFAULT_CODES='utf8','gbk','utf16','big5'

def is_installed(file_name):
    '''
    确认指定的文件是否已被安装。
    '''
    from sysconfig import get_path
    paths=[get_path(name) for name in ('platlib','scripts')]
    if os.name=='nt':
        file_name=file_name.lower()
        paths=[path.lower() for path in paths]
    return any([file_name.startswith(path) for path in paths])

def is_dev(cmd=None):
    import sys
    cmd=cmd or sys.argv[0]
    return 'test' in cmd or (not is_installed(cmd))

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

class Path(pathlib.Path):
    def __new__(cls,*args,**kwargs):
        if cls is Path:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        if len(args) and isinstance(args[0],str)and args[0].startswith('~'):
            args=list(args)
            args[0]=os.path.expanduser(args[0])
        self = cls._from_parts(args, init=False)
        if not self._flavour.is_supported:
            raise NotImplementedError("cannot instantiate %r on "\
                "your system"% (cls.__name__,))
        self._init()
        return self

    def read(self,*args,**kwargs):
        with self.open(*args,**kwargs)as fn:
            return fn.read()

    def ensure(self,parents=True):
        if not self.exists():
            self.mkdir(parents=parents)            
        
    @property
    def lines(self):
        return decode(self.read('rb'))

    @lines.setter
    def lines(self,lines):
        self.write(*lines)
        
    def write(self,*lines,text=None,data=None,encoding='utf8',
              parents=False):
        if parents:
            self.parent.ensure()
        if lines:
            text="\n".join(lines)
        if text:
            data=text.encode(encoding)
        if data:
            with self.open('wb')as fn:
                fn.write(data)

    def rmtree(self):
        import shutil
        shutil.rmtree(str(self))
        
class PosixPath(Path,pathlib.PurePosixPath):
    __slot__=()

class WindowsPath(Path,pathlib.PureWindowsPath):
    __slot__=()

def convert(files):
    for file in files:
        Path(file).lines=Path(file).lines
        print('转换文件"%s"成功'%(file))

dos2unix=Parser(
    Argument('files',nargs='*',help='待转换的文件',metavar='file'),
    description='Windows 格式文件转换为 Unix 文件格式',
    proc=convert)
