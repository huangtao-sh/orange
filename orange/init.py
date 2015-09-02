# 项目：Python开发工具包
# 模块：工具包
# 作者：黄涛
# 创建：2015-9-2

import datetime
import os
import stdlib

INITIAL_VERSION='version="0.1"'
INITIAL_FILE='''# 项目：{project}
# 作者：{author}
# 邮件：{email}
# 创建：{date:%Y-%m-%d}
'''
SETUP_FILE='''#!/usr/bin/env python3
from setuptools import setup,find_packages
from {prj_name}.__version__ import version
setup(
        name='{prj_name}',
        version=version,
        author='{author}',
        author_email='{email}',
        platforms='any',
        description='{project}',
        long_description='{project}',
        entry_points={'console_scripts':[
            # 'cmd_name=package:function',
            ]},
        packages=find_packages(exclude=['testing']),
        license='GPL',
        )
'''
TESTING_PKG='''from .test_sample import *
'''
TEST_SAMPLE='''import unittest
class TestSample(unittest.TestCase):
    def setUp(self)):
        pass

    def tearDown(self):
        pass

    def test_sample(self):
        a='this is a test.'
        self.assertEqual(a,a)
'''

def py_init(project='',author='',email=''):
    prj_name=os.path.split(os.path.abspath('.'))[-1]
    ver_file='%s/__version__.py'%(prj_name)
    pkg_file='%s/__init__.py'%(prj_name)
    # 生成setup.py文件
    if not os.path.isfile('setup.py'):
        stdlib.write_file('setup.py',SETUP_FILE.format(\
            author=author,prj_name=prj_name,
            project=project,email=email))
        print('已生成setup.py')
        
    # 创建包目录
    if not os.path.isdir(prj_name):
        os.mkdir(prj_name)
    # 生成初始化版本文件    
    if not os.path.isfile(ver_file):
        stdlib.write_file(ver_file,INITIAL_VERSION)
        print('当前程序版本初始化为：0.1')
    # 生成初始化包文件
    if not os.path.isfile(pkg_file):
        contents=INITIAL_FILE.format(project=project,
                                      author=author,
                                      email=email,
                                      date=datetime.datetime.now())
        stdlib.write_file(pkg_file,contents)
        print('已初始化包文件')

    if not os.path.isdir('testing'):
        os.mkdir('testing')
        stdlib.write_file(os.path.join('testing','__init__.py'),
                          TESTING_PKG)
        stdlib.write_file(os.path.join('testing','test_sample.py'),
                          TESTING_SAMPLE)       
        
init_cmd={
    'proc':py_init,
    '-p --project':{
        'help':'项目描述'},
    '-a --author':{
        'help':'作者'},
    '-e --email':{
        'help':'电子邮件'
        },}
    

    
    
