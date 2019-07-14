import typing

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ


class LZSS(KaitaiCompressor):
    __slots__ = ()

    lzss = None

    def __init__(self, *args, **kwargs) -> None:  # pylint:disable=unused-argument
        if self.__class__.lzss is None:
            import lzss

            self.__class__.lzss = lzss
        super().__init__()

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.lzss.decompress(data))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.lzss.compress(data))
