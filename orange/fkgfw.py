# 项目：standard library
# 模块：fuck gfw
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-02-05 19:16

'''
功夫网是档在我们和外部世界之间的一堵墙。幸好有好人提供了一把梯子，供我们翻墙
'''
from orange.gclone import proc
from orange import *
import os

repos='hosts',
user='racaljk'

def main():
    if os.name=='posix':
        path=Path('~/.fkgfw')
        dest=Path('/etc/hosts/hosts')
    else:
        path=Path('%appdata%/fkgfw')
        dest=Path('%SystemRoot%/System32/drivers/etc/hosts')
    path.ensure()
    os.chdir(str(path))
    if (path / '.git').exists():
        proc(repos=repos,user=user)
    else:
        os.chdir((path /'hosts'))
        s=read_shell('git status')[-1]
        if 'clean' in s:
            print('数据无更新，退出程序！')
            return
    dest.text=(path/'hosts/hosts').text
    print(dest.text)
    if os.name=='nt':
        os.system('ipconfig /flushdns')
    
    
if __name__=='__main__':
    main()
    

    
