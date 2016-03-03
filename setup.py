#!/usr/bin/env python3
from setuptools import setup,find_packages
import orange.__version__
console_scripts=['pytool=orange:main',
                 'sysinit=orange.sysinit:proc']
scripts=['orange/pysetup.py','orange/pytest.py']
setup(
        name='orange',
        version=orange.__version__.version,
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
