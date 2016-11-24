from pathlib import *
import os
import sys

LINKS={'bin':'bin',
       'emacsd/emacs':'.emacs',
       'conf/gitconfig':'.gitconfig',
       'conf/ssh':'.ssh',
       'conf/pypirc':'.pypirc',
       'conf/pip':'.pip',
       }
    
WIN32_LINKS={'conf/pip':'AppData/Roaming/pip',
           'conf/vimrc_win':'_vimrc',
           }
    
DARWIN_LINKS={'conf/vimrc_mac':'.vimrc',}

def win_init():
    # 修改注册表，增加.PY 和.PYW 为可执行文件
    pass

def do_link():
    if sys.platform=='win32':
        LINKS.update(WIN32_LINKS)
    elif sys.platform=='darwin':
        LINKS.update(DARWIN_LINKS)

    home=Path(os.path.expanduser('~'))
    src=home / 'OneDrive'

    for source,dest in LINKS.items():
        s= src / source
        d= home /dest
        if not d.exists()and s.exists():
            d.symlink_to(s,s.is_dir())
            print('创建连接文件：%s -> %s'%(d,s))
def main():
    do_link()
    if sys.platform=='win32':
        win_init()
    elif sys.platform=='darwin':
        darwin_init()
        
if __name__=='__main__':
    main()

