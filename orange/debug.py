# 项目：标准库函数
# 模块：调试模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-12 17:25

from functools import wraps

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
