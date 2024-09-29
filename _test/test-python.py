#!/usr/bin/env python3

from pathlib import Path
import re
import unittest

from test_lz4 import TestLz4
from test_lzma_lzma import TestLzmaLzma
from test_lzma_raw import TestLzmaRaw
from test_lzma_xz import TestLzmaXz
from test_zlib import TestZlib
from test_snappy import TestSnappy
from test_brotli import TestBrotli
from test_zstd import TestZstd
from test_implode_binary import TestImplodeBinary
from test_implode_ascii import TestImplodeAscii

cwd = Path(".").absolute()
this_dir = Path(__file__).absolute().parent.relative_to(cwd)
compressed_dir = this_dir / "compressed"
uncompressed_dir = this_dir / "uncompressed"


class SimpleTests(unittest.TestCase):
    def testCompressors(self):
        for uncompressed_fn in uncompressed_dir.glob("*.dat"):
            name = uncompressed_fn.stem
            print(name)

            uncompressed_data = uncompressed_fn.read_bytes()

            algs = [
                (TestLz4, "lz4"),
                (TestLzmaLzma, "lzma"),
                # (TestLzmaRaw, 'lzma_raw'), # requires filters= to be set
                (TestLzmaXz, "xz"),
                (TestZlib, "zlib"),
                (TestSnappy, "snappy"),
                (TestBrotli, "br"),
                (TestZstd, "zst"),
                (TestImplodeBinary, "binary.implode"),
                (TestImplodeAscii, "ascii.implode"),
            ]

            for test_class, ext in algs:
                compressed_fn = compressed_dir / (name + "." + ext)
                with self.subTest(test_class=test_class, file=compressed_fn):
                    obj = test_class.from_file(str(compressed_fn))
                    self.assertEqual(obj.body, uncompressed_data)


if __name__ == "__main__":
    unittest.main()
