#!/usr/bin/env python3
from stdlib._setup import setup
console_scripts=['pytool=orange:main',
                 'dos2uix=orange.path:Dos2Unix.main',
                 'sysinit=orange.sysinit:proc']
scripts=['orange/pytest.py']
setup(
        name='orange',
        platforms='any',
        scripts=scripts,
        description='orange',
        long_description='orange',
        url='https://github.com/huangtao-sh/orange.git',
        entry_points={'console_scripts':console_scripts},
        license='GPL',
        )
