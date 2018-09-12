#!/usr/bin/env python3
# 项目：克隆github.com上的项目
# 模块：命令行模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-06-11 12:28
# 修订：2016-11-18 采用Parser来分析参数
# 修改：2018-09-12 10:35 采用 shell 来处理命令行

#from stdlib import parse_args,exec_shell
from orange import arg, shell, Path
import sys


@arg('repos', nargs='+', metavar='repo', help="要下载的软件仓库，可以为多个")
@arg('-u', '--user', nargs='?', help='要下载的用户名,默认为本人的仓库')
def proc(repos=None, user=None, protocol='SSH'):
    if user is None:
        from configparser import ConfigParser
        config = ConfigParser()
        config.read([str(Path('~/.gitconfig'))])
        try:
            user = config.get('user', 'name')
        except:
            raise Exception('用户不存在！')
    protocol = protocol.upper()
    URL = f'git@github.com:{user}' if protocol == 'SSH' else \
        f'https://github.com/{user}'
    for repo in repos:
        url = '%s/%s.git' % (URL, repo)
        print('cloning', url)
        shell > f'git clone {url}'
