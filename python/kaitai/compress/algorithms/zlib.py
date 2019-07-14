import typing
import zlib
from enum import IntEnum

from ..core import KaitaiCompressor, ProcessorContextStub


class Container(IntEnum):
    raw = -1
    zlib = 1
    gzip = 16


containerWLenTransformers = {
    Container.raw: lambda x: -x,
    Container.zlib: lambda x: x,
    Container.gzip: lambda x: Container.gzip.value + x
}

# pylint:disable=arguments-differ


class VanillaZlib(KaitaiCompressor):
    __slots__ = ("compressorParams", "decompressorParams", "dO", "cO")

    def __init__(self, containerType: Container = Container.zlib, log_window_size: int = 15, zdict: typing.Optional[bytes] = None, level: int = -1, mem_level: typing.Union[str, int] = "DEF_MEM_LEVEL", strategy: typing.Union[str, int] = "DEFAULT_STRATEGY", method: typing.Optional[typing.Union[str, int]] = "deflated", *args, **kwargs) -> None:  # pylint:disable=too-many-arguments,unused-argument
        super().__init__()
        # containerType = Container(containerType)
        self.compressorParams = {}
        self.decompressorParams = {}
        if method is not None:
            if isinstance(method, str):
                method = getattr(zlib, method.upper())
            self.compressorParams["method"] = method

        if mem_level is not None:
            if isinstance(mem_level, str):
                mem_level = getattr(zlib, mem_level)
            self.compressorParams["memLevel"] = mem_level

        if strategy is not None:
            if isinstance(strategy, str):
                strategy = getattr(zlib, "Z_" + strategy.upper())
            self.compressorParams["strategy"] = strategy

        self.compressorParams["level"] = level
        self.decompressorParams["wbits"] = self.compressorParams["wbits"] = containerWLenTransformers[containerType](log_window_size)

        if zdict is not None:
            self.decompressorParams["zdict"] = self.compressorParams["zdict"] = zdict

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        dO = zlib.decompressobj(**self.decompressorParams)
        return ProcessorContextStub(dO.decompress(data) + dO.flush())

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        cO = zlib.compressobj(**self.compressorParams)
        return ProcessorContextStub(cO.compress(data) + cO.flush())


Zlib = VanillaZlib

try:
    import zopfli

    containerZopfliRemap = {Container.raw: zopfli.ZOPFLI_FORMAT_DEFLATE, Container.zlib: zopfli.ZOPFLI_FORMAT_ZLIB, Container.gzip: zopfli.ZOPFLI_FORMAT_GZIP}

    class ZopfliZlib(VanillaZlib):
        __slots__ = ("zopfliCompressorParams",)

        def __init__(self, containerType: Container = Container.zlib, log_window_size: int = 15, zdict: typing.Optional[bytes] = None, level: int = -1, mem_level: typing.Union[str, int] = "DEF_MEM_LEVEL", strategy: typing.Union[str, int] = "DEFAULT_STRATEGY", method: typing.Optional[typing.Union[str, int]] = "deflated", *args, **kwargs) -> None:  # pylint:disable=too-many-arguments,unused-argument
            super().__init__(containerType, log_window_size, zdict, level, mem_level, strategy, method, *args, **kwargs)

            self.zopfliCompressorParams = {
                "verbose": False,
                "iterations": 15,
                "block_splitting": True,
                "block_splitting_max": 15,
                "format": containerZopfliRemap[containerType]
            }

        def compressZopfli(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
            cO = zopfli.ZopfliCompressor(**self.zopfliCompressorParams)
            return ProcessorContextStub(cO.compress(data) + cO.flush())

        def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
            if self.compressorParams.get("zdict", None) is not None and self.compressorParams.get("wbits", None) == 15:
                return self.compressZopfli(data)
            else:
                return super().unprocess(data)

    Zlib = ZopfliZlib

except ImportError:
    pass
