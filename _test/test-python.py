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
        ('lz4', TestLz4),
        ('zlib', TestZlib),
        ('lzma', TestLzmaLzma),
        ('xz', TestLzmaXz),
    ]

    for alg in algs:
        ext = alg[0]
        test_class = alg[1]

        obj = test_class.from_file('compressed/%s.%s' % (name, ext))
        print(obj.body == uncompressed_data)
