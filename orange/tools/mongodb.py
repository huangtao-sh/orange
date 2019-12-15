# 项目：标准库函数
# 模块：配置mongodb数据库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-11-19 10:18
# 修订：2018-10-25 重写安装程序
# 修订：2019-12-15 09:35 修改写配置文件功能

from orange.pykit.pyver import Ver, get_cur_ver
from orange import sh, Path
from pkgutil import get_data

MONGOFILES = ('mongo.exe', 'mongod.exe', 'mongodump.exe', 'mongoexport.exe',
              'mongoimport.exe')

SERVERNAME = 'MongoDb'
MONGOCONFIG = get_data('orange', 'data/mongo.yaml').decode()


def win_deploy():
    import platform
    root = Path('%Programdata%/Mongodb')
    root.ensure()
    data_path = root / 'data'
    if not data_path:
        data_path.ensure()
        print('创建数据目录：%s' % (data_path))
    config_file = root / 'mongo.conf'
    config = {
        'dbpath': data_path.as_posix(),
        'logpath': root.as_posix(),
        'engine': 'wiredTiger'
    }
    if platform.architecture()[0] != '64bit':
        config['engine'] = 'mmapv1'
        print('本机使用32位处理器，使用 mmapv1 引擎')
    result = sh(f'sc query {SERVERNAME}')
    if not result[0]:
        sh > 'sc stop {SERVERNAME}'
        print('停止 MongoDb 服务')
    config_file.write_bytes(MONGOCONFIG.format(**config).encode())
    prg_path = Path('%PROGRAMFILES%/MongoDB').find('bin')
    print(f'最新版程序安装路径为：{prg_path}')
    dest = Path('%windir%')
    for exefile in MONGOFILES:
        (dest / exefile) >> (prg_path / exefile)
        print('连接 %s 到 %s 成功' % (dest / exefile, prg_path / exefile))
    print('删除服务配置')
    sh > f'sc delete {SERVERNAME}'
    print('重新配置服务')
    sh > f'mongod --install --serviceName {SERVERNAME} --config "{config_file}"'
    print('启动 MongoDB 服务')
    sh > f'sc start {SERVERNAME}'
    input('Press any key to continue')


def darwin_deploy():
    config = {
        'dbpath': '/usr/local/var/mongodb',
        'logpath': 'usr/local/var/log',
        'engine': 'wiredTiger'
    }
    config_path = Path('/usr/local/etc/mongod.conf')
    plist_file = Path('/Library/LaunchDaemons/com.mongodb.plist')
    config_path.text = MONGOCONFIG.format(**config)
    plist_file.text = get_data('orange', 'data/mongo.plist').decode()


def linux_deploy():
    dbpath = '/var/local/mongodb'
    logpath = '/var/log'
    Path(dbpath).ensure()
    config = {'dbpath': dbpath, 'logpath': logpath}
    config_path = Path('/usr/local/etc/mongod.conf')
    MONGOCONFIG = get_data('orange', 'data/mongo_linux.yaml').decode()
    config_path.text = MONGOCONFIG.format(**config)


def main():
    import sys
    if sys.platform == 'win32':
        win_deploy()
    elif sys.platform == 'darwin':
        darwin_deploy()
    elif sys.platform == 'linux':
        linux_deploy()
    else:
        print('操作系统%下的配置未实现')
