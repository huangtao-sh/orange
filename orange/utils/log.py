import logging
import sys
import os
from orange import Path

name = sys.argv[0] or 'test'

logger = logging.getLogger(name)

path = (Path('%localappdata%/logs') /
        name.split(os.sep)[-1]).with_suffix('.log')

path.parent.ensure()

log = logger.log
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
fatal = logger.fatal


def set_debug(fmt='%(asctime)s %(levelname)s:\t%(message)s', datefmt='%F %T'):
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(logging.FileHandler(str(path)))
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def set_verbose(fmt='%(message)s', datefmt=None):
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)