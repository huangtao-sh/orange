from orange import Path, HOME
import os
import sys

LINKS = {'bin': 'bin',
         'emacsd/emacs': '.emacs',
         'conf/gitconfig': '.gitconfig',
         'conf/ssh': '.ssh',
         'conf/pypirc': '.pypirc',

         }

WIN32_LINKS = {'conf/pip/pip.conf': 'AppData/Roaming/pip/pip.ini',
               'conf/vimrc_win': '_vimrc',
               }

DARWIN_LINKS = {'conf/vimrc_mac': '.vimrc',
                'conf/pip': '.pip', }


def win_init():
    # 修改注册表，增加.PY 和.PYW 为可执行文件
    from orange.shell.regkey import HKLM, REG_SZ, HKCU, add_path
    with HKCU/'GNU/Emacs' as key:
        key['HOME'] = str(HOME), REG_SZ
        print('设置 Emacs 的 HOME 目录完成。')

    with HKLM/'SYSTEM/CurrentControlSet/Control/Session Manager/Environment' as key:
        pathext = key['PATHEXT'][0]
        for ext in ('.PY', '.PYW'):
            if ext not in set(pathext.split(';')):
                pathext += ';'+ext
        key['PATHEXT'] = pathext, REG_SZ
    bin = str(HOME/'OneDrive/bin')
    add_path(bin, bin)


def do_link():
    if sys.platform == 'win32':
        Path('~/AppData/Roaming/pip').ensure()
        LINKS.update(WIN32_LINKS)
    elif sys.platform == 'darwin':
        LINKS.update(DARWIN_LINKS)

    home = HOME
    src = home / 'OneDrive'

    for source, dest in LINKS.items():
        s = src / source
        d = home / dest
        d >> s
        print(f'创建连接文件：{d} ->{s}')


def main():
    do_link()
    if sys.platform == 'win32':
        win_init()
    elif sys.platform == 'darwin':
        # darwin_init()
        pass


if __name__ == '__main__':
    main()
