# 项目：标准库函数
# 模块：命令行处理
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-10 16:40

from argparse import ArgumentParser
import sys

class Parser:
    subparsers=()
    arguments=()
    allow_empty=False
    name=None
    kwargs={}
    subkwargs={}

    @classmethod
    def main(cls,argv=None):
        cls.parser=ArgumentParser(**cls.kwargs)
        cls.add_arguments()
        argv=argv or sys.argv[1:]
        if argv or cls.allow_empty:
            args=dict(cls.parser.parse_args(argv)._get_kwargs())
            proc=args.pop('proc',None)
            if proc:
                proc(**args)
        else:
            cls.parser.print_usage()
        
    @classmethod
    def add_arguments(cls):
        for arg in cls.arguments:
            cls.parser.add_argument(*arg.args,**arg.kwargs)
        if cls.subparsers:
            subparsers=cls.parser.add_subparsers(**cls.subkwargs)
            for subparser in cls.subparsers:
                if not subparser.name:
                    subparser.name=subparser.__name__.lower()
                subparser.parser=subparsers.add_parser(subparser.name,
                                                       **subparser.kwargs)
                subparser.add_arguments()
        else:
            cls.parser.set_defaults(proc=cls.run)

    @classmethod
    def run(cls,*args,**kwargs):
        print('running')
        print(args)
        print(kwargs)

class Argument:
    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs

Arg=Argument

