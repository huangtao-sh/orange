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
def py_init(project='',author='',email=''):
    prj_name=os.path.split(os.path.abspath('.'))[-1]
    ver_file='%s/__version__.py'%(prj_name)
    pkg_file='%s/__init__.py'%(prj_name)
    if not os.path.isfile(ver_file):
        stdlib.write_file(ver_file,INITIAL_VERSION)
        print('当前程序版本初始化为：0.1')
        
    if not os.path.isfile(pkg_file):
        contents=INITIAL_FILE.format(project=project,
                                      author=author,
                                      email=email,
                                      date=datetime.datetime.now())
        stdlib.write_file(pkg_file,contents)
        print('已初始化包文件')
    
init_cmd={
    'proc':py_init,
    '-p --project':{
        'help':'项目描述'},
    '-a --author':{
        'help':'作者'},
    '-e --email':{
        'help':'电子邮件'
        },}
    

    
    
