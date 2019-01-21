# 项目：   标准库函数
# 模块：   存档文件
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-18 19:26

import yaml 
import atexit
from orange import Path,info
from collections import ChainMap
from orange import decrypt, encrypt

def is_passwd(name):
    return name.lower() in {'passwd', 'password'}

class BaseConfig(object):
    __slots__='config','_config','backup'
    def __init__(self,default=None,**kw):
        self.config=self.load(**kw) or {}      # 从文件中加载配置
        self.backup=self.config.copy()         # 对参数进行备份
        self._config=ChainMap(self.config,default or {})  # 处理默认参数
        atexit.register(self.exit)                        # 注程程序退出处理程序

    def load(self,**kw):                       # 加载文件，子类应实现此方法
        raise Exception('子类未实现 load 方法')

    def save(self,**kw):
        raise Exception('子类未实现 save 方法') # 保存文件，子类应实现此方法
    
    def __setitem__(self,name,value):          # 设置参数
        if isinstance(value,dict):
            value={k:encrypt(v)if is_passwd(k)else v for k,v in value.items()}
        self.config[name]=value

    def __getitem__(self,name):                # 读取参数
        v=self._config[name]
        if isinstance(v,dict):
            v={k:decrypt(v)if is_passwd(k)else v for k,v in v.items()}
        return v

    def exit(self):                            # 程序退出函数
        if self.backup!=self.config:
            self.save()                        # 当备份配置与配置不一致时，调用子娄的保存方法

class YamlConfig(BaseConfig):
    __slots__='file',

    def load(self,filename):
        self.file=Path(filename)
        if self.file:
            with self.file.open('r',encoding='utf8')as f:
                return yaml.load(f)
               
    def save(self):
        with self.file.open('w',encoding='utf8')as f:
            yaml.dump(self.config,f,default_flow_style=False,indent=2)
