from orange.utils.data import *

a = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]


@filterer
def _fil(row):
    return row[0] > 4



data = Data(a, itemgetter(1, 2), _fil,
            converter({
                0: lambda x: x+10,
                1: float
            }))


for r in data:
    print(*r)
