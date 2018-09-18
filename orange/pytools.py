# 项目：标准函数库
# 模块：Python相关实用命令
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-08-09 07:50
# 修订：2016-03-19
# 修订：2016-5-12
# 修订：2016-9-23 新增pyupload功能，使用run_setup来进行安装调用
# 修改：2018-09-18 20:18 代码优化


from .path import Path
from .deploy import run_setup, pyclean

libpath = str(Path('~/OneDrive/pylib'))


def pyupload():
    run_setup('sdist', '--dist-dir', libpath, 'upload')
    pyclean()


def pysdist():
    run_setup('sdist', '--dist-dir', libpath)
    pyclean()
