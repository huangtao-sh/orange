#!/usr/bin/env python3
from orange import setup
console_scripts=['dos2unix=orange.path:Dos2Unix.main',
                 'sysinit=orange.sysinit:proc']
setup(
        name='orange',
        platforms='any',
        description='orange',
        long_description='orange',
        url='https://github.com/huangtao-sh/orange.git',
        entry_points={'console_scripts':console_scripts},
        license='GPL',
        )
