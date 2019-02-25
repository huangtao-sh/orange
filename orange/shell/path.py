# 项目：standard python lib
# 模块：path and file
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-11 12:21
# 修改：2016-04-13 21:01
# 修改：2016-08-13 新增__iter__ 和 extractall功能
# 修订：2016-11-19
# 修订：2018-05-25 增加write_tables功能
# 修订：2018-09-12 为 Path 增加 verinfo 功能
# 修改：2018-09-16 09:00 增加 link_to  功能 以及 >> 和 << 操作符
# 修订：2018-09-18 20:04 修正 __iter__ 的bug.
# 修改：2019-02-23 13:42 增加音乐文件的 metadata 及 tags 功能


import pathlib
import os
from codecs import BOM_UTF8, BOM_LE, BOM_BE
from orange.utils import command, arg
from tempfile import TemporaryDirectory, NamedTemporaryFile
from .shell import POSIX, sh
from contextlib import contextmanager


class TempDir(TemporaryDirectory):
    __slots__ = ()

    def __enter__(self):
        return Path(self.name)


tempdir = TempDir


@contextmanager
def tempfile(data=None, writer=None, **kw):
    if data:
        kw['mode'] = 'wb' if isinstance(data, bytes) else 'w'
    kw['delete'] = False
    try:
        with NamedTemporaryFile(**kw) as f:
            if data:
                f.write(data)
            if callable(writer):
                writer(f)
            tmp = Path(f.name)
        yield tmp
    finally:
        tmp.unlink()


BOM_CODE = {
    BOM_UTF8: 'utf_8',
    BOM_LE: 'utf_16_le',
    BOM_BE: 'utf_16_be',
}

DEFAULT_CODES = 'utf8', 'gbk', 'utf16', 'big5'


def is_installed(file_name: str) -> bool:
    '''
    确认指定的文件是否已被安装。
    '''
    if file_name:
        from sysconfig import get_path
        paths = [str(Path(get_path(name)).resolve())
                 for name in ('platlib', 'scripts')]
        if POSIX:
            paths.append('/usr')
        cmdfile = Path(file_name).resolve()
        return any(map(str(cmdfile).startswith, paths))


def is_dev(cmd: str = None) -> bool:
    import sys
    cmd = cmd or sys.argv[0]
    if('wsgi' in cmd):
        return False
    return 'test' in cmd or (not is_installed(cmd))


def decode(d: bytes) -> str:
    '''
    对指定的二进制，进行智能解码，适配适当的编码。按行返回字符串。
    '''
    for k in BOM_CODE:
        if k == d[:len(k)]:
            return d[len(k):].decode(BOM_CODE[k])
    for encoding in DEFAULT_CODES:
        try:
            return d.decode(encoding)
        except:
            pass
    raise Exception('解码失败')


_Parent = pathlib.WindowsPath if os.name == 'nt' else pathlib.PosixPath


class Path(_Parent):
    __slots__ = ('_music_meta')

    def __bool__(self):
        '''判断文件是否存在'''
        return self.exists()

    @classmethod
    def tempdir(cls, *args, **kw):
        return TempDir(*args, **kw)

    @classmethod
    def tempfile(cls, data=None, writer=None, suffix=None, **kw):
        return tempfile(data=data, writer=writer, suffix=suffix, **kw)

    def __new__(cls, path='.', *args, **kwargs):
        if isinstance(path, str):
            if path.startswith('~'):  # 支持用户目录开头
                path = os.path.expanduser(path)
            elif path[0] in('%', '$'):  # 支持环境变量转义
                path = os.path.expandvars(path)
        return super().__new__(cls, path, *args, **kwargs)

    def read(self, *args, **kwargs):
        '''以指定的参数读取文件'''
        with self.open(*args, **kwargs)as fn:
            return fn.read()

    def ensure(self, parents: bool = True):
        '''确保目录存在，如果目录不存在则直接创建'''
        if not self.exists():
            self.mkdir(parents=parents)

    @property
    def text(self):
        '''读取文件，并返回字符串'''
        return decode(self.read('rb'))

    @text.setter
    def text(self, text: str):
        '''写入文本文件'''
        self.write(text=text)

    @property
    def lines(self):
        '''按行读取文件'''
        return self.text.splitlines()

    @lines.setter
    def lines(self, lines: 'iterable'):
        '''按行写入文件'''
        self.write(lines)

    def write(self, content=None, text=None, data=None, encoding='utf8',
              parents=False):
        '''写文件'''
        if parents:
            self.parent.ensure()
        data = content or text or data
        if isinstance(content, (tuple, list)):
            data = '\n'.join(content)
        if isinstance(data, str):
            with self.open('w', encoding=encoding)as f:
                f.write(data)
        elif isinstance(data, bytes):
            with self.open('wb')as f:
                f.write(data)

    @property
    def worksheets(self):
        import xlrd
        with xlrd.open_workbook(filename=str(self)) as book:
            return book.sheets()

    def sheets(self, index=None):
        ''' 提供读取指定worksheet的功能，其中index可以为序号，
            也可以为表的名称。'''
        import xlrd
        book = xlrd.open_workbook(filename=str(self))
        if isinstance(index, int):
            sheet = book.sheet_by_index(index)
        elif isinstance(index, str):
            sheet = book.sheet_by_name(index)
        return sheet and sheet._cell_values

    def iter_sheets(self):
        '''如果指定的文件为excel文件，则可以迭代读取本文件的数据。
        返回：表的索引、表名、数据'''
        import xlrd
        book = xlrd.open_workbook(filename=str(self))
        for index, sheet in enumerate(book.sheets()):
            yield index, sheet.name, sheet._cell_values

    def iter_csv(self, encoding=None, errors=None, dialect='excel', **kw):
        import csv

        def reader():
            with self.open(encoding=encoding, errors=errors) as f:
                yield from f

        return csv.reader(reader()if encoding else self.lines, dialect=dialect, **kw)

    @property
    def xmlroot(self):
        '''如果指定的文件为xml文件，则返回本文件的根元素'''
        from xml.etree.ElementTree import fromstring
        return fromstring(self.text)

    def __iter__(self):
        '''根据文件的不同，迭代返回不同的内容。支持如下文件：
        1、文本文件，按行返回文本
        2、Excel文件，返回表索引、表名及表中数据
        3、目录，则返回本目录下所有文件
        4、del文件，按行返回数据。
        5、csv文件，按行返回数据。
        '''
        if self.is_dir():
            yield from self.iterdir()
        suffix = self.lsuffix
        if suffix.startswith('.xls'):
            yield from self.iter_sheets()
        elif suffix == '.xml':
            yield from self.xmlroot
        elif suffix in('.del', '.csv'):
            yield from self.iter_csv()

    def extractall(self, path='.', members=None):
        def conv_members(members, sep='/'):
            if members:
                repl_sep = '\\' if sep == '/' else '/'
                return tuple(map(lambda x: x.replace(repl_sep, sep), members))

        name = self.name.lower()
        if name.endswith('.rar'):
            members = conv_members(members, '/' if POSIX else '\\')
            members = " ".join(members) if members else ""
            sh > f'unrar x {self} {members} {path}'
        elif any(map(name.endswith, ('.tar.gz', '.tgz', '.gz'))):
            import tarfile
            with tarfile.open(str(self), 'r')as f:
                members = conv_members(members, '/')
                members = tuple(map(f.getmember, members)
                                )if members else f.getmembers()
                f.extractall(path, members)
        elif name.endswith('.zip'):
            import zipfile
            with zipfile.ZipFile(str(self))as f:
                members = conv_members(members, '/')
                for fileinfo in f.filelist:
                    if not (fileinfo.flag_bits and 0x0800):
                        fileinfo.filename = fileinfo.filename.encode(
                            'cp437').decode('gbk')
                        f.NameToInfo[fileinfo.filename] = fileinfo
                f.extractall(path, members)

    def pack(self, tarfilename: str, **kw):
        '''
        把指定的文件或目录打包成一个压缩文件，
        文件格式为： .tgz
        其中: kw 为 add 参数，可以为：
        arcname=None, specifies an alternative name for the file in the archive.
        recursive=True, 是否包括子目录
        filter=None ，一个函数，过滤不需要的文件
        '''
        import tarfile
        tarfilename = str(Path(tarfilename).with_suffix('.tgz'))
        with tarfile.open(tarfilename, 'w:gz')as f:
            if self.is_dir():
                cwd, name = self, '.'
            else:
                cwd, name = self.parent, self.name
            cwd.chdir()
            f.add(name, **kw)

    @property
    def lsuffix(self):
        '''返回小写的扩展名'''
        return self.suffix.lower()

    @property
    def pname(self):
        '''返回不带扩展名的文件名'''
        return self.with_suffix("").name

    def rmtree(self):
        '''删除整个目录'''
        import shutil
        shutil.rmtree(str(self))

    def chdir(self):
        if self.is_dir():
            os.chdir(str(self))

    def __sub__(self, other):
        return self.relative_to(other)

    def write_xlsx(self, *args, force: bool = False, formats: dict = None,
                   writer=None, **kw):
        if self and not force:
            s = input('%s 已存在，请确认是否覆盖，Y or N?\n' % self.name)
            if s.upper() != 'Y':
                return
        from orange.xlsx import Book
        if callable(writer):
            with Book(str(self), formats=formats)as book:
                writer(book, *args, **kw)
        else:
            return Book(str(self), formats=formats, **kw)

    @property
    def mtime(self):
        '''文件修改时间'''
        return int(self.lstat().st_mtime)

    @property
    def ctime(self):
        '''文件创建时间'''
        return int(self.lstat().st_ctime)

    @property
    def uri(self):
        '''统一网址'''
        ur = self.resolve().as_uri()
        return ur if POSIX else ur.lower()

    @property
    def fullname(self):
        path = str(self.absolute())
        return path if POSIX else path.lower()

    def link_to(self, target: 'Path'):
        '''
            创建文件或目录连接
            由 self 连接到 target
            如果 self 指向的文件已存在：是 target 则自动忽略，否则重新建立连接。
        '''
        if self.is_symlink():
            if self.resolve() == target.resolve():  # 连接已存在，则忽略
                return
            self.unlink()
        if self:
            return
        return self.symlink_to(target, target.is_dir())

    def __rshift__(self, target: 'Path'):
        '''
          Path('a.txt') >> Path('b.txt')
          把 a.txt 连接到 b.txt 上
        '''
        return self.link_to(Path(target))

    def __lshift__(self, target: 'Path'):
        '''
          Path('a.txt') << Path('b.txt')
          把 b.txt 连接到 a.txt 上
        '''
        Path(target).link_to(self)

    @property
    def verinfo(self):
        from orange.pykit.version import Ver
        if self.match('*.tar.gz', '*.zip'):
            type_ = 'Source'
            d = self.name.split('-')
            version = Ver(d[-1])
            name = '_'.join(d[:-1])
            return name, version, type_
        elif self.match('*.whl'):
            type_ = 'Wheel'
            d = self.name.split('-')
            attrs = dict(zip(('version', 'abi', 'platform'), d[-3:]))
            version = Ver(d[-4])
            name = '_'.join(d[:-4])
            return name, version, type_, attrs

    @property
    def atime(self):
        '''文件访问时间'''
        return int(self.lstat().st_atime)

    def write_tables(self, *tables,  **kw):
        '''
        写入多张表格，支持以下参数：
        formats:预设格式
        tables:为列表，每个table为字典，参数值如下：
        pos:位置
        columns:表格格式
        data:数据
        sheet:表格名称
        '''
        def writer(book, *tables):
            for table in tables:
                pos = table.pop('pos', 'A1')
                book.add_table(pos, **table)

        self.write_xlsx(writer=writer, *tables, **kw)

    def match(self, *patterns):
        return any(map(super().match, patterns))

    def find(self, pattern: str, key=None, reverse: bool = True) -> 'Path':
        result = tuple(sorted(self.rglob(pattern), key=key, reverse=reverse))
        if result:
            return result[0]

    @property
    def music_tags(self):
        from orange.utils.musictag import MusicTag
        return MusicTag(self)


HOME = Path.home()


@command(description='Windows 格式文件转换为 Unix 文件格式')
@arg('files', nargs='*', help='待转换的文件', metavar='file')
def convert(files):
    for file in files:
        Path(file).lines = Path(file).lines
        print('转换文件"%s"成功' % (file))


def clean_trash():
    from contextlib import suppress
    Patterns = ('._.DS_Store',
                '.DS_Store',
                '._*',
                '~$*',
                'Thumbs.db',
                '*.tmp',
                'Icon?')
    print('开始清查系统垃圾文件！')
    ROOT = HOME / 'OneDrive/工作'
    for file_ in ROOT.rglob('*.*'):
        if any(map(file_.match, Patterns)):
            with suppress(PermissionError):
                file_.unlink()
                print(f'删除文件 {file_.name}')
