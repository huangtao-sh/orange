#!/usr/bin/env python3
import os
from orange import setup

console_scripts = [
    'conv=orange.utils.path:convert',
    'pysdist=orange.pykit.pysetup:pysdist',
    'pyupload=orange.pykit.pysetup:pyupload',
    'canshu=orange.tools.ggcs:canshu',
    'pyver=orange.pykit.pyver:VersionMgr.main',
    'plist=orange.tools.plist:main',
    'pyinit=orange.tools.init:main',
    'gclone=orange.tools.gclone:proc',
    'fkgfw=orange.tools.fkgfw:main',
    'sysinit=orange.tools.sysinit:main',
    'pkg=orange.pykit.pypkgs:main',
    'dppy=orange.tools.deppython:PythonUpgrade.main',  # 部署 python
    'dpmongo=orange.tools.mongodb:main',  # 部署 mongodb
    'sxtm=orange.tools.math:main',
    'cleanwork=orange.shell.path:clean_trash',
    'imgbak=orange.tools.imgbackup:main',
    'musicdl=orange.tools.neteasesong:main',
    'dvd=orange.tools.dvd:main',
    'repare=orange.shell.path:repare_filename',
    'aml=orange.shell.path:add_music_lib',
    'sql=orange.utils.sqlite:execsql',
    'py=orange.utils:py',
    'pack=orange.tools.pack:main',
]

scripts = ['scripts/pytest.py']

if os.name == 'posix':
    console_scripts.append('pysetup=orange.pykit.pysetup:pyinstall')
else:
    scripts.append('orange/pykit/pysetup.py')

setup(
    name='orange_kit',
    platforms='any',
    description='orange',
    long_description='orange',
    url='https://github.com/huangtao-sh/orange.git',
    scripts=scripts,
    cscripts=console_scripts,
    license='GPL',
)
