# 项目：standard python lib
# 模块：path and file
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-11 12:21

import pathlib
import os
from codecs import BOM_UTF8,BOM_LE,BOM_BE
from .argparser import Parser,Arg

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

class Path(pathlib.Path):
    def __new__(cls,path,*args,**kwargs):
        if cls is Path:
            cls = WindowsPath if os.name == 'nt' else PosixPath
        if isinstance(path,str)and path.startswith('~'):
            path=os.path.expanduser(path)
        args=list(args)
        args.insert(0,path)
        self = cls._from_parts(args, init=False)
        if not self._flavour.is_supported:
            raise NotImplementedError("cannot instantiate %r on your system"
                                      % (cls.__name__,))
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

    def write(self,*lines,text=None,data=None,encoding='utf8',parents=False):
        if parents:
            self.parent.ensure()
        if lines:
            text="\n".join(lines)
        if text:
            data=text.encode(encoding)
        if data:
            with self.open('wb')as fn:
                fn.write(data)
        
class PosixPath(Path,pathlib.PurePosixPath):
    __slot__=()

class WindowsPath(Path,pathlib.PureWindowsPath):
    __slot__=()

class Dos2Unix(Parser):
    arguments=[Arg('files',nargs='*',help='待转换的文件',metavar='file')]
    @classmethod
    def run(cls,files):
        for file in files:
            Path(file).write(*Path(file).lines)
            print('转换文件 %s 成功'%(file))
