from orange.utils.sqlite import Connection, trans, db_config, tran, execute, executemany, fetch, loadfile
from orange import Path, Data
db_config('~/a.db')
execute('create table if not exists abc(a text primary key,b)')


def test():
    executemany('insert into abc values(?,?)', [[5, 2], [6, 4]])


path = Path('~/abc.txt')
data = Data(path.iter_csv(encoding='gbk'),
            filter=lambda x: x[0].startswith('a'))

with Connection('~/a.db') as db:
    db.loadfile(path, data, 'abc')
    #db.executemany('insert into abc values(?,?)',_Path('~/abc.txt'))

for r in fetch('select * from abc'):
    print(*r)
