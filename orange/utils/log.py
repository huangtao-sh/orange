# 项目：   工具库
# 模块：   日志模块
# 作者：   黄涛
# License: GPL
# Email:   huangtao.sh@icloud.com
# 创建：2019-07-20 22:26

import logging
import sys
import os
from pathlib import Path

from .datetime_ import datetime
today = datetime.now() % '%F'

name = sys.argv[0] or 'test'

logger = logging.getLogger(name)


if os.name == 'nt':
    path = Path(os.path.expandvars(f'%localappdata%/logs/{today}'))
else:
    path = Path(os.path.expanduser(f'~/.logs/{today}'))
if not os.path.exists(path):
    os.mkdir(path)
path = (path / name.split(os.sep)[-1]).with_suffix('.log')
logging.basicConfig(format='%(asctime)s %(levelname)-8s: %(message)s',
                    filename=str(path),
                    datefmt='%F %T')
log = logger.log
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
fatal = logger.fatal
critical = logger.critical
warn = logger.warn


def set_debug(level=logging.DEBUG):
    logger.setLevel(level)


def set_verbose(fmt='%(message)s'):
    if logger.level == 0 or logger.level > logging.INFO:
        logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt=fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
