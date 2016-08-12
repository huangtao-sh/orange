# 项目：公共库函数
# 模块：在mac下安装mongodb数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-08-10 16:03

from orange import *
from orange.parseargs import *

INSTALL_PATH=Path('/usr/local')
TARGET=INSTALL_PATH / 'mongodb'
START_FILE=Path('~/Library/LaunchAgents/com.mongodb.plist')

START_LINES='''<?xml version="1.0" encoding="UTF-8"?>  
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">  
<plist version="1.0">  
  <dict>  
    <key>KeepAlive</key>  
    <true/>  
    <key>Label</key>  
    <string>com.mongodb.mongod</string>  
    <key>ProgramArguments</key>  
    <array>  
    <string>/usr/local/mongodb/bin/mongod</string>  
    </array>    
  </dict>  
</plist> 
'''

def proc(file=None):
    if not file:
        file=max(list(Path('~/Downloads').glob('mongodb-osx*.tgz')))
    if file:
        exec_shell('tar -xzf %s -C %s'%(file,INSTALL_PATH))
        dir=max(list(INSTALL_PATH.glob('mongodb-osx*')))
        if TARGET.exists():
            TARGET.unlink()
        TARGET.symlink_to(dir.name)

        if not START_FILE.exists():
            START_FILE.lines=START_LINES.split('\n')

main=Parser(
    Arg('-f','--file',help='指定的安装文件'),
    proc=proc,allow_empty=True,
    )

if __name__=='__main__':
    main()
