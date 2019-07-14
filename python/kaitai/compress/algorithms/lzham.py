import typing

from ..core import KaitaiCompressor, ProcessorContextStub

raise NotImplementedError("The python bindings for lzham and lzham itself has bad security and design issues. It must be fixed first.")

"""LZHAM
Must Read: https://github.com/richgel999/lzham_codec

uncompressed: 1
table_update_rate: # at default settings
    3: 0.0103
    8: 0.0105 # default
    20: 0.0106
level: # "table_update_rate":20, "dict_size_log2": 26
    1: 0.0108
    4: 0.0104
highest:
lzma: 0.008 # at highest settings
"""
# pylint:disable=arguments-differ


class LZHAM(KaitaiCompressor):
    __slots__ = ("decompressor", "compressor", "dictTrainerParams",)
    lzham = None

    def __init__(self, level: int = 1, dict_size_log2: int = 26, table_update_rate: int = 20, max_helper_threads: int = 0, check_adler32: bool = False, table_max_update_interval: int = 0, table_update_interval_slow_rate: int = 0, *args, **kwargs) -> None:  # pylint:disable=redefined-builtin,too-many-arguments,too-many-locals,unused-argument,too-many-branches,too-many-statements
        super().__init__()
        if self.__class__.lzham is None:
            import lzham  # pylint:disable=import-outside-toplevel

            self.__class__.lzham = lzham

        commonFilters = {"table_update_rate": table_update_rate, "dict_size_log2": dict_size_log2, "table_max_update_interval": table_max_update_interval, "table_update_interval_slow_rate": table_update_interval_slow_rate}

        compFilters = {"level": level, "max_helper_threads": max_helper_threads}
        compFilters.update(commonFilters)

        decompFilters = {"compute_adler32_during_decomp": check_adler32, "unbuffered_decompression": True}
        decompFilters.update(commonFilters)

        self.compressor = lzham.LZHAMCompressor(compFilters)
        self.decompressor = lzham.LZHAMDecompressor(decompFilters)

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.decompressor.decompress(data))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.compressor.compress(data))
