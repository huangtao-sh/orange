from winreg import *
from orange import *
from sysconfig import *

__all__='RegKey','HKLM','HKCU','HKU','REG_BINARY',\
        'REG_DWORD','REG_EXPAND_SZ','REG_SZ'

class RegKey(object):
    __slots__='_items','_key'
    def __init__(self,key,subkey=None):
        self._items={}
        self._key=key
        if subkey:
            self/subkey

    def __truediv__(self,subkey):
        subkey=subkey.replace('/','\\')
        self._key=CreateKey(self._key,subkey)
        return self
    
    def __enter__(self):
        return self

    def __exit__(self,*args):
        self._key.Close()

    def __getitem__(self,name):
        if name not in self._items:
            try:
                val=QueryValueEx(self._key,name)
            except:
                val=None,None
            self._items[name]=val
        return self._items.get(name)

    @property
    def value(self):
        return QueryValue(self._key,None)

    @value.setter
    def value(self,val):
        return SetValue(self._key,REG_SZ,val)
        
    def __setitem__(self,name,value):
        ensure(isinstance(value,(list,tuple))and(len(value)==2),
               '值的格式应为值,类型')
        ensure(value[-1],set([REG_SZ,REG_EXPAND_SZ,REG_DWORD]),
               '类型必须为REG_SZ、REG_EXPAND_SZ或REG_DWORD之一！')
        if SetValueEx(self._key,name,0,*reversed(value)):
            self._items[name]=value

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

HKLM=RegKey(HKEY_LOCAL_MACHINE)
HKCU=RegKey(HKEY_CURRENT_USER)
HKU=RegKey(HKEY_USERS)
