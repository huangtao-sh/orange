# 项目：标准库函数
# 模块：运行库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-04-13 20:46
# 修改：2018-09-09 新增 tprint 功能
# 修改：2018-09-12 10:19 新增 shell、cformat、tprint 功能


import os
import warnings
from functools import wraps
from .regex import R


def deprecate(func):
    '''进行废弃声明，使用方法：

    @deprecate(new_func)
    def depr_func(*arg,**kw):
        pass
    '''
    func = func.__name__ if hasattr(func, '__name__') else func

    def _(fn):
        @wraps(fn)
        def new_func(*args, **kw):
            warnings.warn(
                '%s will be deprecated, Please use %s replaced!' % (
                    fn.__name__, func), DeprecationWarning, stacklevel=2)
            return fn(*args, **kw)
        return new_func
    return _


def deprecation(func, replace=''):
    '''DeprecationWarning'''
    message = "%s 已被弃用" % (func)
    if replace:
        message += "，请使用 %s 替代" % (replace)
    warnings.warn(message, DeprecationWarning, stacklevel=2)


_Digit = R/r'\d+'


def cformat(value, format_spec=''):
    '''对字符串进行格式化，
    解决设定宽度后，汉字无法对齐的问题'''
    if isinstance(value, str)and _Digit/format_spec:
        d = int(tuple(_Digit/format_spec)[0]) - \
            sum(1 for x in value if ord(x) > 127)
        format_spec = _Digit/format_spec % str(d)
    return format(value, format_spec)


@deprecate('cformat')
def cstr(arg, width=None, align='left'):
    '''
    用于转换成字符串，增加如下功能：
    width:总宽度
    align:left:左对齐，right:右对齐，center:居中
    '''
    s = str(arg)
    if width:
        align = align.lower()
        s = s.strip()
        x = width-wlen(s)
        if x > 0:
            if align == 'right':
                s = ' '*x+s
            elif align == 'left':
                s += ' '*x
            else:
                l = x//2
                r = x-l
                s = ' '*l+s+' '*r
    return s


def tprint(data, format_spec={}, sep=' '):
    '''按行格式化打印，可以指定每列的宽度和对齐方式。
    其中格式为： <23，前面是对齐方式，右边是宽度。中间用,隔开，如"^23,>19"
    左对齐：     <
    居中对齐：   ^
    右对齐：     > 可者省略
    '''
    if isinstance(format_spec, (tuple, list)):
        for row in data:
            x = sep.join(cformat(k, f)for k, f in zip(row, format_spec))
            print(x)
    elif isinstance(format_spec, dict):
        for row in data:
            x = sep.join(cformat(k, format_spec.get(i, ''))
                         for i, k in enumerate(row))
            print(x)


class classproperty:
    '''类属性，用法：
    class A:
        @classproperty
        def name(cls):
              return cls.__name__

    A.name
    A().name
    '''

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, kclass):
        return self.getter(kclass)


class cachedproperty:
    '''类属性，用法：
    class A:
        @classproperty
        def name(cls):
              return cls.__name__

    A.name
    A().name
    '''

    def __init__(self, getter):
        self.getter = getter
        self.cache = {}

    def __get__(self, instance, kclass):
        if kclass not in self.cache:
            self.cache[kclass] = self.getter(kclass)
        return self.cache[kclass]


class _Shell():
    '''执行系统命令，
    使用方法：
    1.直接在终端上执行命令，并显示结果。
      shell > 'dir'
      注： result = shell >'dir'
          result 为系统返回的结果，一般 0 为正确执行
    2.获取执行结果。
      result = shell('dir')
      这里返回的是 dir 执行的输出
    '''

    def __gt__(self, cmd):
        return os.system(cmd)

    def __call__(self, cmd, input=None):
        mode = 'w' if input else 'r'
        with os.popen(cmd, mode)as f:
            if input:
                if isinstance(input, (tuple, list)):
                    input = '\n'.join(input)
                f.write(input)
            else:
                return f.read().splitlines()


shell = _Shell()


def run_cmd(cmd, *args, **options):
    '''
    执行 cmd 命令，并带 params 以及 options 参数
    '''
    params = []
    for k, v in options.items():
        if len(k) == 1:
            params.append(f'-{k}')
        else:
            params.append(f'--{k}')
        if v:
            params.append(v)
    params = [cmd, *args, *params]
    cmd = " ".join([f'"{x}"' if " " in x else x for x in params])
    print(cmd)
    return shell > cmd


@deprecate('shell')
def read_shell(cmd):
    '''
    执行系统命令，并将执行命令的结果通过管道读取。
    '''
    with os.popen(cmd)as fn:
        k = fn.read()
    return k.splitlines()


@deprecate('shell')
def write_shell(cmd, lines):
    '''
    执行系统命令，将指定的文通过管道向该程序输入。
    '''
    with os.popen(cmd, 'w') as fn:
        if isinstance(lines, str):
            fn.write(lines)
        elif isinstance(lines, (tuple, list)):
            [fn.write('%s\n' % (x))for x in lines]


@deprecate('shell')
def exec_shell(cmd):
    '''
    执行系统命令。
    '''
    # deprecation('exec_shell', 'shell')
    return os.system(cmd)


def wlen(s):
    '''
    用于统计字符串的显示宽度，一个汉字或双字节的标点占两个位，
    单字节的字符占一个字节。
    '''
    return len(s.encode('gbk', errors='ignore'))


_des = None


def __get_des():
    from .pyDes import des, PAD_PKCS5
    global _des
    if _des is None:
        _des = des(key='huangtao', padmode=PAD_PKCS5)
    return _des


def encrypt(pwd):
    '''
    可逆加密程序。
    '''
    b = __get_des().encrypt(pwd)
    return "".join(['%02X' % (x)for x in b])


def decrypt(code):
    '''
    解密程序。
    '''
    b = __get_des().decrypt(bytes.fromhex(code))
    return b.decode('utf8')


def get_py(s, style=4, sep=''):
    '''
    获取拼音字母。
    '''
    from pypinyin.core import phrase_pinyin
    return sep.join([x[0] for x in phrase_pinyin(s, style, None)])


class _PY(type):

    def __truediv__(self, s):
        return get_py(s)

    def __or__(self, s):
        return get_py(s, style=0, sep=' ')


class PY(metaclass=_PY):
    '''以一种高逼格的方式获取拼音
    获取拼音首字母：  PY/'我们'   ===>   'wm'
    获取拼音：       PY|'我们'   ===>    'wo men'
    '''
    pass


generator = type((x for x in 'hello'))


def split(data, size=1000):
    '''拆分数据，其中datas应为list,size为每批数据的数量'''
    if isinstance(data, generator):
        data = tuple(data)
    length = len(data)
    i = 0
    for i in range(size, length, size):
        yield data[i - size:i]
    else:
        yield data[i:]
