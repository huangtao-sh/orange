# 项目：工具库函数
# 模块：版本
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-29 12:07

import re
from distutils.version import StrictVersion


class Ver(StrictVersion):
    version_re = re.compile(r'.*?(\d+) \. (\d+) (\. (\d+))? ([ab](\d+))?',
                            re.VERBOSE | re.ASCII)

    def _cmp(self, other):
        if isinstance(other, str):
            other = Ver(other)
        elif not other:
            other = Ver('0.0')
        return super()._cmp(other)
