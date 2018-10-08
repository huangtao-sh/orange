# 项目：工具库函数
# 模块：版本
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-09-29 12:07

import re
from distutils.version import StrictVersion

SEGMENT = {'major': 0, 'm': 0,
           'minor': 1, 'n': 1,
           'micro': 2, 'o': 2,
           'patch': 2, 'p': 2,
           'dev': 3, 'd': 3,
           '#': 4, }


class Ver(StrictVersion):
    version_re = re.compile(r'.*?(\d+) \. (\d+) (\. (\d+))? ([ab](\d+))?',
                            re.VERBOSE | re.ASCII)

    def _cmp(self, other):
        if isinstance(other, str):
            other = Ver(other)
        elif not other:
            other = Ver('0.0')
        return super()._cmp(other)

    '''自定义版本管理程序
    增加upgrade功能
    '''

    def upgrade(self, segment=4):
        from orange import ensure
        '''升级版本号
        其中参数 segment可以为：
        major:升级主版本号
        minor:升级小版本号
        patch:升级补丁版本号
        dev:升级开发版本号
        #:升级开发版本序号
        '''
        if isinstance(segment, str):
            segment = SEGMENT.get(segment.lower(), 4)
        if segment < 3:
            ensure(not self.prerelease,
                   '开发版本号不允许直接升级正式版本号！')
        else:
            ensure(self.prerelease, '正式版本号不允许升级开发版本号')
        if segment == 4:
            self.prerelease = self.prerelease[0], self.prerelease[1]+1
        elif segment == 3:
            if self.prerelease[0] == 'a':
                self.prerelease = 'b', 1
            else:
                self.prerelease = None
        else:
            self.prerelease = 'a', 1
            nv = [0]*3
            nv[:segment+1] = self.version[:segment+1]
            nv[segment] += 1
            self.version = nv
        return self
