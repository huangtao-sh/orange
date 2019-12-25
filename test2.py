from orange import Data


def create():
    for i in range(10):
        yield 'a0', 'b1', 'c2', 'd3', 'e4'


d = Data(create(), include=(0, 2))
for r in d:
    print(r)