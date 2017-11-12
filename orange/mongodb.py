# 项目：标准库函数
# 模块：配置mongodb数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-11-19 10:18

import sys
import re
from orange.deploy import *
from orange import exec_shell,read_shell
from orange.pyver import Ver


MONGOCONFIG='''
systemLog:
  destination: file
  path: "{logpath}/mongodb.log"
  logAppend: true
storage:
  dbPath: "{dbpath}"
  directoryPerDB: true
  engine: "{engine}"
net:
  bindIp: 127.0.0.1
  port: 27017
'''

Pattern=re.compile(r'\d+(\.\d+)*([ab]\d+)?')
def find_ver(path):
    v=Pattern.search(path.name)
    if v:
        return Ver(v.group())

SERVERNAME='MongoDb'
def win_deploy():
    print('停止 MongoDb 服务……')
    exec_shell('sc stop %s'%(SERVERNAME))
    k=input('请安装新版本的 MongoDb 服务器程序\n安装完成后按回车继续')
    s=list((sorted(Path("%PROGRAMFILES%/MongoDB").rglob('bin'),key=lambda x:find_ver(x))))
    s=s and s[-1]
    from orange.regkey import add_path
    add_path(str(s),'MongoDB')
    print('设置路 Windows 搜索路径成功')
    
    root=get_path(SERVERNAME,False)[0]
    data=root / 'data'
    if not data.exists():
        data.ensure()
        print('创建目录：%s'%(data))
    config={
        'dbpath':(str(data)).replace("\\","/"),
        'logpath':(str(root)).replace("\\","/"),
        'engine':'wiredTiger'}
    config_file=MONGOCONFIG.format(**config)
    (root/'mongo.ini').text=config_file
    print('写入配置文件成功')

    cmd='mongod --install --serviceName "%s" --config "%s"'%(SERVERNAME,root/'mongo.ini')
    exec_shell(cmd)
    exec_shell('sc start %s'%(SERVERNAME))
    print('%s 服务安装成功！'%(SERVERNAME))

def darwin_deploy():
    pass
    
def main():
    import sys
    if sys.platform=='win32':
        win_deploy()
    elif sys.platform=='darwin':
        darwin_deploy()
    else:
        print('操作系统%下的配置未实现')

if __name__=='__main__':
    main()
