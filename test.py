from orange import Path
from orange.utils.log import debug, info, error, fatal, warning, set_debug, set_verbose

txt = '''
a    bsdf
b    dsfaafasd
c    adsf
'''


with Path.tempfile(data=txt, suffix=".csv")as f:
    for r in f.read_data(quote='"', offsets=(0,5),skip_header=False,columns=(0,1)):
        print(r)
