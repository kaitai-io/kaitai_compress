#!/usr/bin/env python3

from glob import glob
from os.path import basename
import re

from test_lz4 import TestLz4
from test_lzma_lzma import TestLzmaLzma
from test_lzma_raw import TestLzmaRaw
from test_lzma_xz import TestLzmaXz
from test_zlib import TestZlib

for uncompressed_fn in glob('uncompressed/*.dat'):
    name = re.sub(r'.dat$', '', basename(uncompressed_fn))
    print(name)

    f = open(uncompressed_fn, 'rb')
    uncompressed_data = f.read()
    f.close()

    algs = [
        (TestLz4, 'lz4'),
        (TestLzmaLzma, 'lzma'),
#        (TestLzmaRaw, 'lzma_raw'), # requires filters= to be set
        (TestLzmaXz, 'xz'),
        (TestZlib, 'zlib'),
    ]

    for alg in algs:
        test_class = alg[0]
        ext = alg[1]

        obj = test_class.from_file('compressed/%s.%s' % (name, ext))
        print(obj.body == uncompressed_data)
