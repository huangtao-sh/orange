from orange.utils.sqlite import Connection, trans, db_config, tran, execute, executemany, fetch, loadfile
from orange import Path
db_config('~/a.db')
execute('create table if not exists abc(a text primary key,b)')


def test():
    executemany('insert into abc values(?,?)', [[5, 2], [6, 4]])


class _Path(Path):
    def __iter__(self):
        return self.iter_csv()



with Connection('~/a.db') as db:
    db.loadfile(_Path('~/abc.txt'), 'abc')
    #db.executemany('insert into abc values(?,?)',_Path('~/abc.txt'))

for r in fetch('select * from abc'):
    print(*r)
