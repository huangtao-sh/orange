# 模块：操作系统初始化
# 作者：黄涛
# 创建：2016-3-3

import os
from pathlib import *

# 需要创建符号连接的文件
LINKS=[('bin','bin'),
    ('emacsd/emacs','.emacs'),
    ('conf/gitconfig','.gitconfig'),
    ('ssh','.ssh'),
    ('conf/pip','.pip')
    ]
    
WINDOWS_LINKS=[('conf/vimrc_win','.vimrc'),
               ]
    
POSIX_LINKS=[('conf/vimrc_mac','.vimrc'),
             ]
    
def proc():
    LINKS.extend(WINDOWS_LINKS if os.name=='nt' else POSIX_LINKS)
    home=Path(os.path.expanduser('~')).resolve()
    drive=home / 'OneDrive'
    for source,target in LINKS:
        s=drive / source
        d=home / target
        if not d.exists():
            d.symlink_to(s,s.is_dir())

if __name__=='__main__':
    proc
    
