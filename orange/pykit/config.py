
# 项目：   Python 包管理软件
# 模块：   参数配置
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-16 21:15

from orange.shell.path import HOME
import atexit
import yaml

ConfFile = HOME / 'OneDrive/conf/pypkgs.yaml'    # 配置文件路径

_config = {}
if ConfFile:
    with ConfFile.open('r', encoding='utf8')as f:
        _config = yaml.load(f)                   # 读取配置文件
config = _config.copy()                  


@atexit.register
def save_config():
    if config != _config:
        with ConfFile.open('w', encoding='utf8')as f:
            yaml.dump(config, f, width=4, default_flow_style=False) #保存配置文件
