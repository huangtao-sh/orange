# 项目：Python开发工具包
# 模块：工具包
# 作者：黄涛
# 创建：2015-9-2
from stdlib import parse_args
from .init import init_cmd
from .path import Path
from .argparser import Parser,Argument,Arg

__all__=['get_ver','Path','Parser','Argument','Arg']

parsers={'init':init_cmd}
template={'parsers':parsers}

def main(argv=None):
    parse_args(template,argv,allow_empty=False,
               description='Python 工具包')

def get_ver():
    ver_file=list(Path(".").glob("*/__version__.py"))
    if ver_file:
        with ver_file[0].open(encoding='utf8')as fn:
            for line in fn.read().splitlines():
                if line.startswith('version'):
                    return line.split('"')[1]
            
        
        
