# 项目：standard library
# 模块：fuck gfw
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-02-05 19:16
# 修订：2017-02-22
'''
功夫网是档在我们和外部世界之间的一堵墙。幸好有好人提供了一把梯子，供我们翻墙
'''
from orange import *
import os

url='git@github.com:racaljk/hosts.git'

def main():
    if os.name=='posix':
        path=Path('~/.fkgfw')
        dest=Path('/private/etc/hosts')
    else:
        path=Path('%appdata%/fkgfw')
        dest=Path('%SystemRoot%/System32/drivers/etc/hosts')
    path.ensure()
    os.chdir(str(path))
    if not (path / 'hosts').exists():
        os.system('git clone %s'%(url))
    else:
        os.chdir(str(path /'hosts'))
        os.system('git pull')
        
    if os.name=='posix':
        os.system('sudo cp %s %s'%(path/'hosts/hosts',dest))
    else:
        dest.text=(path/'hosts/hosts').text
        os.system('ipconfig /flushdns')
    print(*dest.lines[:5],sep='\n')
    
if __name__=='__main__':
    main()
    

    
