#!/usr/bin/env python3
from setuptools import setup,find_packages
from orange.__version__ import version
import os.path
import sysconfig
import glob
console_scripts=['pytool=orange:main',]
script_path=sysconfig.get_path('scripts')
if not glob.glob('%s/pysetup*'%(script_path)):
    console_scripts.append('pysetup=orange.setup:python_setup')

setup(
        name='orange',
        version=version,
        author='Huang tao',
        author_email='huangtao.jh@gmail.com',
        platforms='any',
        description='orange',
        long_description='orange',
        url='https://github.com/huangtao-sh/orange.git',
        entry_points={'console_scripts':console_scripts},
        packages=find_packages(exclude=['testing']),
        license='GPL',
        )
