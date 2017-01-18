# 项目：标准库函数
# 模块：命令行处理模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-01-18 21:34

from argparse import *
from functools import partial

__all__='command','arg'

class _Command(object):
    def __init__(self,run):
        self.run=run
        self.groups=[]
        self.args=[]
        self._args=()
        self._kw={}
        self.allow_empty=False
        self.parsers=[]
        
    @classmethod
    def wrapper(cls,cmd,*args,**kw):
        def _(fn):
            if not isinstance(fn,cls):
                fn=cls(fn)
            getattr(fn,cmd)(*args,**kw)
            return fn
        return _

    def add_parser(self,parser):
        self.parsers.append(parser)
        
    def add_arg(self,*args,**kw):
        self.args.append((args,kw))

    def command(self,*args,allow_empty=False,**kw):
        self._args,self._kw=args,kw
        self.allow_empty=allow_empty

    def proc_args(self,parser):
        for args,kw in reversed(self.args):
            parser.add_argument(*args,**kw)

    def __call__(self,argv=None):
        import sys
        argv=argv or sys.argv[1:]
        parser=ArgumentParser(*self._args,**self._kw)
        self.proc_args(parser)
        parser.set_defaults(proc=self.run)
        if self.parsers:
            subparsers=parser.add_subparsers(help='Sub command')
            for subparser in self.parsers:
                sub=subparsers.add_parser(subparser.run.__name__,
                            *subparser._args,**subparser._kw)
                subparser.proc_args(sub)
                sub.set_defaults(proc=subparser.run)
        if self.allow_empty or argv:
            kwargs=dict(parser.parse_args(argv)._get_kwargs())
            proc=kwargs.pop('proc',None)
            if proc:
                proc(**kwargs)
        else:
            parser.print_usage()

command=partial(_Command.wrapper,'command')
arg=partial(_Command.wrapper,'add_arg')

