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

logging.basicConfig(format='%(asctime)s %(levelname)-8s: %(message)s',
                    filename=str(path),
                    datefmt='%F %T')


def set_debug():
    logger.setLevel(logging.DEBUG)


def set_verbose(fmt='%(message)s'):
    if logger.level =0 or logger.level> logging.INFO:
        logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt=fmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)