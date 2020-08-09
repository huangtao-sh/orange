from orange import arg, Path


@arg("src", help='源目录')
@arg("dest", help="存放打包文件目录")
@arg("-p", "--passwd", nargs='?', help="压缩包密码")
def main(src, dest, passwd=None):
    src = Path(src).absolute()
    dest = Path(dest).absolute()
    for path in src:
        if path.is_dir():
            path.rar(dest, passwd)
