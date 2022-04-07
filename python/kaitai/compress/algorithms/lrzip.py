import typing
from enum import IntEnum

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ


class LRZip(KaitaiCompressor):
    __slots__ = ("algo",)

    lrzip = None
    Algos = None

    @classmethod
    def initLib(cls):
        import lrzip

        self.__class__.lrzip = lrzip
        prefix = "LRZIP_MODE_COMPRESS_"
        self.__class__.Algos = IntEnum("A", sorted(((k[len(prefix) :].lower(), getattr(lrzip, k)) for k in dir(lrzip) if k[: len(prefix)] == prefix), key=lambda x: x[1]))

    def __init__(self, algo: typing.Union[int, str] = "none", *args, **kwargs) -> None:  # pylint:disable=unused-argument
        if self.__class__.lrzip is None:
            self.__class__.initLib()
        if isinstance(algo, str):
            algo = self.__class__.Algos[algo.lower()]
        else:
            algo = self.__class__.Algos(algo)
        self.algo = algo
        super().__init__()

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.lrzip.decompress(data))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.__class__.lrzip.compress(data, compressMode=self.algo))
