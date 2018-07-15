import zlib

class Zlib:
    def decode(self, data):
        return zlib.decompress(data)
