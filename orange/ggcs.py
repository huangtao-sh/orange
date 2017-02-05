# 项目：标准库函数
# 模块：公共参数查询
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-05-20 16:45

from orange.parseargs import *
from orange import *
import re

def extract_str(s):
    if s.startswith('"')and s.endswith('"'):
        s=s[1:-1]
    return s.strip()

def query_canshu(category,query):
    TYPE={'jym':'transactions_output.csv',
          'km':'ggkmzd.del',
          'jg':'ggjgm.del',
          'gy':'users_output.csv',
          'user':'users_output.csv',}
    root=Path('~/OneDrive/工作/参数备份/')
    files=[filename for filename in root.rglob(TYPE[category])]
    if files:
        filename=max(files)
        print('file "%s" was selected!'%(filename.name))
        for line in filename.lines:
            if query in line:
                print(",".join([extract_str(x)for x in\
                                line.split(',')]))

canshu=Parser(
    Argument('-c','--category'),
    Argument('query'),
    proc=query_canshu)
