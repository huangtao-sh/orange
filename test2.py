from orange import Path, groupby
from collections import defaultdict
from orange.xlsx import Header

ROOT = Path(r'~/Documents')


def split():
    path = ROOT.find('abc.*')
    data = path.sheets('sjsqhd201912236416_1')
    widthes = 25, 25, 53, 35, 19, 70, 35, 20, 20, 20, 20, 20, 20
    Headers = tuple(
        Header(header, width) for header, width in zip(data[0], widthes))
    dest1 = ROOT / '拆分数据'
    dest1.ensure()
    for br, data in groupby(
            map(lambda row: [x.strip() for x in row], data[1:]), 4):
        path = dest1 / br
        path.ensure()
        with (path / f'核查问题账户反洗钱信息（汇总）.xlsx').write_xlsx(force=True) as book:
            book.add_table('A1', '企业信息', data=data, columns=Headers)
            print(f'核查问题账户反洗钱信息.xlsx  完成！')
        for zh, d in groupby(data, 3):
            with (path /
                  f'核查问题账户反洗钱信息（{zh}）.xlsx').write_xlsx(force=True) as book:
                book.add_table('A1', '企业信息', data=d, columns=Headers)
                print(f'核查问题账户反洗钱信息（{zh}）.xlsx  完成！')


def pack():
    dest1 = ROOT / '拆分数据'
    dest2 = ROOT / '下发数据'
    dest2.ensure()
    for r in dest1.glob('*'):
        if r.is_dir():
            r.rar(dest2)


split()
pack()
