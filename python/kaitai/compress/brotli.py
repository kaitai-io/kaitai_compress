import brotli

class Brotli:
    def decode(self, data):
        return brotli.decompress(data)
