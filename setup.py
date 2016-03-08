#!/usr/bin/env python3
from stdlib._setup import setup
console_scripts=['pytool=orange:main',
                 'sysinit=orange.sysinit:proc']
scripts=['orange/pysetup.py','orange/pytest.py']
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
