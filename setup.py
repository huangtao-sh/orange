#!/usr/bin/env python3
from setuptools import setup,find_packages
from orange.__version__ import version
console_scripts=['pytool=orange:main',]
scripts=['orange/pysetup.py','orange/pytest.py']
setup(
        name='orange',
        version=version,
        author='Huang tao',
        author_email='huangtao.jh@gmail.com',
        platforms='any',
        scripts=scripts,
        description='orange',
        long_description='orange',
        url='https://github.com/huangtao-sh/orange.git',
        entry_points={'console_scripts':console_scripts},
        packages=find_packages(exclude=['testing']),
        license='GPL',
        )
import stdlib.setup
stdlib.setup.create_cmd(scripts)
