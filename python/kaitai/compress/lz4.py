import lz4.frame

class Lz4:
    def decode(self, data):
        return lz4.frame.decompress(data)
