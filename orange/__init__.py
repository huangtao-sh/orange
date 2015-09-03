# 项目：Python开发工具包
# 模块：工具包
# 作者：黄涛
# 创建：2015-9-2
from stdlib import parse_args
from .init import init_cmd
from .pysetup import setup_cmd

parsers={'init':init_cmd,
         'setup':setup_cmd,}
template={'parsers':parsers}

def main(argv=None):
    parse_args(template,argv,allow_empty=False,
               description='Python 工具包')
