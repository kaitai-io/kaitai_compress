import typing

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ


class LZJB(KaitaiCompressor):
    __slots__ = ()

    lzjb = None

    def __init__(self, *args, **kwargs) -> None:  # pylint:disable=unused-argument
        if self.__class__.lzjb is None:
            import lzjb

            self.__class__.lzjb = lzjb
        super().__init__()

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.lzjb.decompress(data))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.lzjb.compress(data))
