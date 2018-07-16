import lzma

class LzmaXz:
    def __init__(self):
        self.decompressor = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
    
    def decode(self, data):
        return self.decompressor.decompress(data)
