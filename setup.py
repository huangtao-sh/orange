#!/usr/bin/env python3
from orange.deploy import setup
console_scripts=['dos2uix=orange.path:Dos2Unix.main',
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
