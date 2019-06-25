from functools import wraps
from orange import now
from pymongo import MongoClient


def timeit(func):
    @wraps(func)
    def _(*args, **kw):
        start = now()
        func(*args, **kw)
        print(f'耗时：{now()-start}')

    return _


client = MongoClient(port=27017)
db = client.test
collection = db.test

collection.drop()

times = 1000000


@timeit
def testa():
    data = []
    for i in range(times):
        data.append({'a': f'abc{i}', 'b': i})
    collection.insert_many(data)


testa()

client = MongoClient(port=27018)
db = client.test
collection = db.test

collection.drop()


@timeit
def testb():
    data = []
    for i in range(times):
        data.append({'a': f'abc{i}', 'b': i})
    collection.insert_many(data)


testb()