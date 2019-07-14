import typing

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ


class Brotli(KaitaiCompressor):
    __slots__ = ("compressorParams", "decompressorParams")
    brotli = None

    def __init__(self, level: typing.Optional[int] = None, mode: typing.Optional[str] = "generic", log_window_size: typing.Optional[int] = None, log_block_size: typing.Optional[int] = None, dictionary: typing.Optional[bytes] = None) -> None:  # pylint:disable=redefined-builtin,too-many-arguments,too-many-locals,unused-argument
        super().__init__()
        if self.__class__.brotli is None:
            import brotli  # pylint:disable=import-outside-toplevel

            self.__class__.brotli = brotli
        self.compressorParams = {}
        self.decompressorParams = {}

        if mode is not None:
            if isinstance(mode, str):
                mode = getattr(self.__class__.brotli, "MODE_" + mode.upper())
            self.compressorParams["mode"] = mode

        if level is not None:
            self.compressorParams["quality"] = level

        if log_window_size is not None:
            self.compressorParams["lgwin"] = log_window_size

        if log_block_size is not None:
            self.compressorParams["lgblock"] = log_block_size

        if dictionary is not None:
            self.decompressorParams["dictionary"] = self.compressorParams["dictionary"] = dictionary

    # new API
    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.brotli.decompress(bytes(data), **self.decompressorParams))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.brotli.compress(data, **self.compressorParams))
