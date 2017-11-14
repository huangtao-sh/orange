# 项目：标准库函数
# 模块：配置mongodb数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-11-19 10:18

import sys
import re
import platform
from orange.deploy import *
from orange import exec_shell,read_shell
from orange.pyver import Ver,get_cur_ver

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
MONGOFILES=('mongo.exe','mongod.exe','mongodump.exe',\
                'mongoexport.exe','mongoimport.exe')

SERVERNAME='MongoDb'
def win_deploy():
    print('停止 MongoDb 服务')
    exec_shell('sc stop %s'%(SERVERNAME))
    cur_prg_path=get_cur_ver(Path('%PROGRAMFILES%/MongoDB').rglob('bin'))
    print('最新版程序安装路径：%s'%(cur_prg_path))
    dest=Path('%windir%')
    for exefile in MONGOFILES:
        dexefile=dest/exefile
        if not dexefile.exists():
            dexefile.symlink_to(cur_prg_path/exefile)
            print('连接 %s 到 %s 成功'%(dexefile,cur_prg_path/exefile))
    
    root=get_path(SERVERNAME,False)[0]
    data_path=root / 'data'
    if not data_path.exists():
        data_path.ensure()
        print('创建数据目录：%s'%(data_path))   
    config_file=root/'mongo.conf'
    if not config_file.exists():
        config={
            'dbpath':data_path.as_posix(),
            'logpath':root.as_posix(),
            'engine':'wiredTiger'}
        if platform.architecture()[0]!='64bit':
            config['engine']='mmapv1'
            print('本机使用32位处理器，使用 mmapv1 引擎')
        config_file.text=MONGOCONFIG.format(**config)
        print('写入配置文件 %s '%(config_file))        
    print('删除服务配置')
    exec_shell('sc delete %s'%(SERVERNAME))
    print('重新配置服务')
    cmd='%s --install --serviceName "%s" --config "%s"'%(
        'mongod.exe',SERVERNAME,config_file)
    print(cmd)
    exec_shell(cmd)
    print('启动 MongoDB 服务')
    exec_shell('sc start %s'%(SERVERNAME))
    input('Press any key to continue')

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
