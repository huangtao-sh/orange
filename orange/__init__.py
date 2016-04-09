# 项目：Python开发工具包
# 模块：工具包
# 作者：黄涛
# 创建：2015-9-2

from .path import Path
from .version import *
from .deploy import *
from .debug import *

__all__=['get_ver','Path',
         'first','last',
         'setup','decorator','trace',
         'classproperty',
         ]

class classproperty:
    def __init__(self,getter):
        self.getter=getter

    def __get__(self,instance,kclass):
        return self.getter(kclass)
                    
        
        
