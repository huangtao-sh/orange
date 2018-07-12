#!/usr/bin/env python3
import os
from orange import setup

console_scripts = ['conv=orange.path:convert',
                   'pysdist=orange.pytools:pysdist',
                   'pyupload=orange.pytools:pyupload',
                   'canshu=orange.ggcs:canshu',
                   'pyver=orange.pyver:VersionMgr.main',
                   'plist=orange.plist:main',
                   'pyinit=orange.init:main',
                   'gclone=orange.gclone:proc',
                   'mongodeploy=orange.mongodb:main',
                   'fkgfw=orange.fkgfw:main',
                   'sysinit=orange.sysinit:main']

scripts = ['scripts/pytest.py']

if os.name == 'posix':
    console_scripts.append('pysetup=orange.pysetup:py_setup')
else:
    scripts.append('orange/pysetup.py')

setup(
    name='orange-kit',
    platforms='any',
    description='orange',
    long_description='orange',
    url='https://github.com/huangtao-sh/orange.git',
    scripts=scripts,
    cscripts=console_scripts,
    # entry_points={'console_scripts':console_scripts},
        license='GPL',
)
