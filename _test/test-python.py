#!/usr/bin/env python3

from glob import glob
from os.path import basename
import re

from test_lz4 import TestLz4
from test_zlib import TestZlib

for uncompressed_fn in glob('uncompressed/*.dat'):
    name = re.sub(r'.dat$', '', basename(uncompressed_fn))
    print(name)

    f = open(uncompressed_fn, 'rb')
    uncompressed_data = f.read()
    f.close()

    obj = TestLz4.from_file('compressed/%s.lz4' % (name))
    print(obj.body == uncompressed_data)

    obj = TestZlib.from_file('compressed/%s.zlib' % (name))
    print(obj.body == uncompressed_data)
