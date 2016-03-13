# 项目：标准库函数
# 模块：调试模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-12 17:25

from functools import wraps
import logging

def decorator(decorator):
    def _decorator(func):
        @wraps(func)
        def __decorator(*args,**kwargs):
            return decorator(func,*args,**kwargs)
        return __decorator
    return _decorator

@decorator
def trace(func,*args,**kwargs):
    print('The function %s is called'%(func.__name__))
    print('With arguments %s %s'%(args,kwargs))
    result=func(*args,**kwargs)
    print('The result is %s'%(result))
    return result


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
        kwargs.setdefault('format','%(asctime)s %(levelname)-9s\t'\
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

