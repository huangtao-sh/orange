# 项目：标准库函数
# 模块：音乐标签
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2019-02-23 14:03

import mutagen

TAGS = 'album', 'artist', 'title', 'tracknumber'
APETAGS = 'album', 'artist', 'title', 'track'
APEMIME = 'audio/ape'


class MusicTag(dict):
    __slots__ = '_file', '_is_ape'

    def __init__(self, path):
        file = mutagen.File(path, easy=True)
        if file:
            self._file = file
            self._is_ape = APEMIME in self._file.mime
            if self.is_ape:
                pass

    @property
    def is_ape(self):
        return self._is_ape

    def save(self):
        self._file.save()
