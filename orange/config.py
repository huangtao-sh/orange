# 项目：标准库函数
# 模块：参数配置模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-05-10 11:34

from orange import encrypt,decrypt,Path
from configparser import *
from contextlib import contextmanager

class Section:
    def __init__(self,cofig,parser,name):
        self.__dict__['_config']=config
        self.__dict__['_name']=name
        self.__dict__['_parser']=parser

    @property
    def options(self):
        return self._parser.options(self._name)

    def __getattr__(self,name):
        value=self._parser.get(self._name,name)
        if name in ('passwd','password'):
            value=decrypt(value)
        return value

    def __setattr__(self,name,value):
        if name in ('passwd','password'):
            value=encrypt(value)
        self._parser.set(self._name,name,value)
        if self._config.autosave:
            self._config.save()

    def __repr__(self):
        return 'Section("%s")'%(self._name)

    def __iter__(self):
        for option in self.options:
            yield option,getattr(self,option)

    def items(self):
        return {option:value for option,value in self}
    
class Config:
    def __init__(self):
        self.__dict__['parser']=ConfigParser()
        self.__dict__['autosave']=True

    def __getattr__(self,name):
        if not self.parser.has_section(name):
            self.parser.add_section(name)
        return Section(self,self.parser,name)

    __getitem__=__getattr__
    
    @contextmanager
    def update(self,section=None):
        try:
            self.__dict__['autosave']=False
            yield self[section] if section else self
        finally:
            self.__dict__['autosave']=True
            self.save()

    def save(self):
        print('save')
        self.parser.write(Path('~/a.ini').open('w',encoding='utf8'))
        
config=Config()
config.database.host='13'

with config.update('database') as db:
    db.host='localhost'
    db.user='hunter'

def ab(**kw):
    for i,k in kw.items():
        print('%s--%s'%(i,k))



ab(**config.database.items())
config.database.host='abc'
