#!/usr/bin/env python3
from setuptools import setup,find_packages
#from stdlib.__version__ import version
version='0.0.1'
setup(
        name='orange',
        version=version,
        author='Huang tao',
        author_email='huangtao.jh@gmail.com',
        platforms='any',
        description='orange',
        long_description='orange',
        entry_points={'console_scripts':[
            'pytool=orange:main',
            ]},
        packages=find_packages(exclude=['testing']),
        license='GPL',
        )
