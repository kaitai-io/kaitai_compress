import typing

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ


class Implode(KaitaiCompressor):
    """PKWare implode format"""

    __slots__ = ("dictionarySize", "compressionType")

    def __init__(self, dictionarySize: int = 4096, compressionType: int = 0, *args, **kwargs) -> None:  # pylint:disable=unused-argument
        super().__init__()

        try:
            from pklib_base import CompressionType
        except ImportError:
            pass
        else:
            if isinstance(compressionType, str):
                compressionType = CompressionType[compressionType.lower()]
            else:
                compressionType = CompressionType(compressionType)

        self.compressionType = compressionType
        self.dictionarySize = dictionarySize

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        import pkblast

        return ProcessorContextStub(pkblast.decompressBytesWholeToBytes(data)[1])

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        from pkimplode import compressBytesChunkedToBytes

        return ProcessorContextStub(compressBytesChunkedToBytes(data, compressionType=self.compressionType, dictionarySize=self.dictionarySize,))
