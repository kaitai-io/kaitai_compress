import lzma

class LzmaLzma:
    def __init__(self):
        self.decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_ALONE)

    def decode(self, data):
        return self.decompressor.decompress(data)
