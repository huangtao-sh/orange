from orange import Path
import zipfile


path = Path(r"C:/Users/huangtao/OneDrive/工作/参数备份").find('运营参数*.zip')
with zipfile.ZipFile(path)as z:
    for fileinfo in z.filelist:
        if not (fileinfo.flag_bits & 0x0800):
            fileinfo.filename = fileinfo.filename.encode(
                'cp437').decode('gbk')
            z.NameToInfo[fileinfo.filename] = fileinfo
        print(fileinfo.filename)
    with z.open('运营参数2019-11/users_output.csv')as f:
        for r in f:
            print(r.decode('gbk'))