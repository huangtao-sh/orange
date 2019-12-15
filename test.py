from pkgutil import get_data
from orange import Path

SERVERNAME = 'MongoDb'
MONGOCONFIG = get_data('orange', 'data/mongo.yaml')
MONGOCONFIG = MONGOCONFIG.decode()


def win_deploy():
    import platform
    root = Path('~')
    #root.ensure()
    data_path = root / 'data'
    if not data_path:
        data_path.ensure()
        print('创建数据目录：%s' % (data_path))
    config_file = root / 'mongo.txt'
    config = {
        'dbpath': data_path.as_posix(),
        'logpath': root.as_posix(),
        'engine': 'wiredTiger'
    }
    if platform.architecture()[0] != '64bit':
        config['engine'] = 'mmapv1'
        print('本机使用32位处理器，使用 mmapv1 引擎')
    print(MONGOCONFIG.format(**config).encode())
    config_file.write_bytes(MONGOCONFIG.format(**config).encode())
    print(config_file.read_bytes())


win_deploy()