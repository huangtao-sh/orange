from orange.utils.sqlite import Connection, trans, db_config, tran, execute, executemany, fetch

db_config('~/a.db')
execute('create table if not exists abc(a text primary key,b)')


@tran
def test():
    executemany('insert into abc values(?,?)', [[5, 2], [6, 4]])


try:
    with trans():
        execute('delete from abc')
        executemany('insert into abc values(?,?)', [[1, 2], [3, 4]])
    test()
except Exception as e:
    print(e)
    print('insert failed')

for r in fetch('select * from abc'):
    print(*r)
