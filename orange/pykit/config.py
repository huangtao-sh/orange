
# 项目：   Python 包管理软件
# 模块：   参数配置
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-01-16 21:15

from orange.utils.config import YamlConfig
from orange.shell.path import HOME

DefaultConfig = {
    'Local': ['orange_kit', 'gmono', 'glemon', 'lzbg', 'pygui'],
    'Wheel': [],
    'Source': []
}

ConfFile = HOME / 'OneDrive/conf/pypkgs.yaml'    # 配置文件路径

config = YamlConfig(default=DefaultConfig, filename=ConfFile)
