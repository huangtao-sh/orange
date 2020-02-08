from orange.datautil import Data
import unittest
import asyncio


def run(coro):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro)


def gen_datas(count=100):
    for i in range(count):
        yield [i, f'b{i}', f'c{i}', f'd{i}']


class TestData2(unittest.TestCase):
    def test_include(self):
        d = list(Data(gen_datas(), include=(0, 1)))
        self.assertListEqual(d[0], [0, 'b0'])

    def tets_exclude(self):
        d = list(Data(gen_datas(), exclude=(0, 1)))
        self.assertListEqual(d[0], ['c0', 'd0'])

    def test_filter(self):
        d = list(Data(gen_datas(), include=(0, 1),
                      filter=lambda row: row[0] > 50))
        self.assertListEqual(d[0], [51, 'b51'],
                             )

    def test_converter(self):
        d = list(Data(gen_datas(), include=(0, 1),
                      filter=lambda row: row[0] > 50,
                      converter={1: lambda x: x+'hello'}
                      ))
        self.assertListEqual(d[0], [51, 'b51hello'])

    def test_pipelines(self):
        pipelines = (
            ('include', (0, 1)),
            ('filter', lambda row: row[0] > 50),
            ('converter', {1: lambda x: x+'hello'})
        )
        d = list(Data(gen_datas(), pipelines))
        self.assertListEqual(d[0], [51, 'b51hello'])


class GenData():
    def __init__(self, count=100):
        self.count = count

    async def __aiter__(self):
        for i in range(self.count):
            yield [i, f'b{i}', f'c{i}', f'd{i}']


class TestSyncData(unittest.TestCase):
    def test_include(self):
        async def _():
            async for d in Data(GenData(), include=(0, 1)):
                self.assertListEqual(d, [0, 'b0'])
                break
        run(_())

    def tets_exclude(self):
        async def _():
            async for d in Data(GenData(), exclude=(0, 1)):
                self.assertListEqual(d, ['c0', 'd0'])
                break
        run(_())

    def test_filter(self):
        async def _():
            async for d in Data(GenData(), include=(0, 1),
                                filter=lambda row: row[0] > 50):
                self.assertListEqual(d, [51, 'b51'])
                break
        run(_())

    def test_converter(self):
        async def _():
            async for d in Data(GenData(), include=(0, 1),
                                filter=lambda row: row[0] > 50,
                                converter={1: lambda x: x+'hello'}
                                ):
                self.assertListEqual(d, [51, 'b51hello'])
                break
        run(_())

        def _conv(row):
            row[1] = row[1]+'hello'
            return row

        async def _():
            async for d in Data(GenData(), include=(0, 1),
                                filter=lambda row: row[0] > 50,
                                converter=_conv
                                ):
                self.assertListEqual(d, [51, 'b51hello'])
                break
        run(_())

    def test_pipelines(self):
        pipelines = (
            ('include', (0, 1)),
            ('filter', lambda row: row[0] > 50),
            ('converter', {1: lambda x: x+'hello'})
        )

        async def _():
            async for d in Data(GenData(), pipelines):
                self.assertListEqual(d, [51, 'b51hello'])
                break
        run(_())
