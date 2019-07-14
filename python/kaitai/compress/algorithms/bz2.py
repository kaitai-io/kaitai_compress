import bz2
import typing

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ


class Bz2(KaitaiCompressor):
    __slots__ = ("level",)

    def __init__(self, level: int = 9, *args, **kwargs) -> None:  # pylint:disable=unused-argument
        super().__init__()
        self.level = level

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        decompressor = bz2.BZ2Decompressor()
        return ProcessorContextStub(decompressor.decompress(data))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        compressor = bz2.BZ2Compressor(self.level)
        return ProcessorContextStub(compressor.compress(data) + compressor.flush())
