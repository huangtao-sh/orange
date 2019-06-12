from orange.tools.hclient import Crawler
from orange import Path, HOME, sh
from orange.tools.neteasesong import get_songid, get_song_info

name = '001-100'
source = HOME/'Downloads'
#dest = HOME/'Music/iTunes/iTunes Media/Automatically Add to iTunes.localized'
dest = HOME/'Music/Album'


def convert():
    for song in (source/name).rglob('*.flac'):
        dstdir = dest/(song.parent - source)
        dstdir.ensure(True)
        dstname = (dstdir / song.name).with_suffix('.m4a')
        cmd = f'ffmpeg -i "{song}" -acodec alac "{dstname}"'
        sh > cmd
        break


convert()
