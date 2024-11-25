import zlib

try:
    from isal import isal_zlib as zlib
except ImportError:
    pass

class Zlib:
    def decode(self, data):
        return zlib.decompress(data)
