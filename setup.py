#!/usr/bin/env python3
from orange import setup
requires=['xlrd',
          'lxml',
          'pypinyin',
    ]
console_scripts=['dos2unix=orange.path:dos2unix',
                 'pytest=orange.pytools:pytest',
                 'pysdist=orange.pytools:pysdist',
                 'canshu=orange.ggcs:canshu',
                 'mongodb=orange.mongodb:main',
                 'sysinit=orange.sysinit:proc']
setup(
        name='orange',
        platforms='any',
        description='orange',
        install_requires=requires,
        long_description='orange',
        url='https://github.com/huangtao-sh/orange.git',
        entry_points={'console_scripts':console_scripts},
        license='GPL',
        )
