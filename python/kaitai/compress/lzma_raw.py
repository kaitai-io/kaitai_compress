import lzma

class LzmaRaw:
    def __init__(self):
        self.decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_RAW)

    def decode(self, data):
        return self.decompressor.decompress(data)
