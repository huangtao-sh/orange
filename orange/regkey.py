# 项目：standard library
# 模块：winreg
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-11-24 19:03

from winreg import *
from orange import *
from sysconfig import *
HKLM=HKEY_LOCAL_MACHINE
HKCU=HKEY_CURRENT_USER
HKU=HKEY_USERS

class RegKey(object):
    __slots__='_cache','_key'
    def __init__(self,key,subkey):
        self._cache={}
        self._key=CreateKey(key,subkey)

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.close()

    def __getitem__(self,name):
        if name not in self._cache:
            try:
                val=QueryValueEx(self._key,name)
            except:
                val=None
            self._cache[name]=val
        return self._cache.get(name)

    def close(self):
        if self._key:
            CloseKey(self._key)
        
    @property
    def value(self):
        return QueryValue(self._key,None)

    @value.setter
    def value(self,value):
        return SetKey(self._key,REG_SZ,value)
        
    def __setattr__(self,name,value):
        if name in self.__slots__:
            super().__setattr__(name,value)
        else:
            self.__setitem__(name,value)

    def __setitem__(self,name,value):
        ensure(isinstance(value,(list,tuple))and(len(value)==2),
               '值的格式应为值,类型')
        ensure(value[-1],set([REG_SZ,REG_EXPAND_SZ,REG_DWORD]),
               '类型必须为REG_SZ、REG_EXPAND_SZ或REG_DWORD之一！')
        if SetValueEx(self._key,name,0,*reversed(value)):
            self._cache[name]=value

    def __delitem__(self,name):
        DeleteValue(self._key,name)

    def iter_keys(self,func=EnumKey):
        i=0
        try:
            while 1:
                yield func(self._key,i)
                i+=1
        except:
            pass

    def iter_values(self):
        return self.iter_keys(func=EnumValue)

    __getattr__=__getitem__

'''
            
path=r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'

pp=";".join([get_path('stdlib'),get_path('data') +r'\DLLS',
             get_path('purelib')])
exts='.PY','.PYW'

with RegKey(HKLM,path) as key:
    pythonpath=key.PYTHONPATH
    if not pythonpath or pythonpath!=pp:
        key.PYTHONPATH=pp,REG_SZ
        
    pathext=key.PATHEXT
    for ext in exts:
        if ext not in set(pathext.split(';')):
            pathext+=';%s'%(ext)
        if pathext!=key.PATHEXT:
            print('新增PATHEXT变量')
            key.PATHEXT=pathext
''' 
    
