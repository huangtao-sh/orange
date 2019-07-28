from orange.utils.data import *
from orange import Path

a = Path(r'C:\Users\huangtao\OneDrive\工作\参数备份\运营管理2019-06\fhnbhzz.del')


@filterer
def _fil(row):
    print('filter1', row)
    return row[0].startswith('331')


@filterer
def fil2(row):
    print('filter2', row)
    return True


@converter
def conv(row):
    print('converter', row)
    return row


data = a.iter_csv(_fil, fil2, conv, encoding='gbk', errors='ignore')

for i, r in zip(range(20), data):
    print(*r)
