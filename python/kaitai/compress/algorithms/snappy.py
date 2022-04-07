import typing

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ


class Snappy(KaitaiCompressor):
    __slots__ = ()
    snappy = None

    def __init__(self) -> None:
        super().__init__()
        if self.__class__.snappy is None:
            import snappy  # pylint:disable=import-outside-toplevel

            self.__class__.snappy = snappy

    # new API
    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.snappy.decompress(bytes(data)))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.snappy.compress(data))
