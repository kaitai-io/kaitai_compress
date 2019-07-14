import typing

try:
    import lzma
except ImportError:
    import processports.lzma as lzma

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ

modifiersMapping = {"e": lzma.PRESET_EXTREME}


class Lzma(KaitaiCompressor):
    __slots__ = ("decompressor_params", "compressor_params")

    def __init__(self, algo: int = 2, level: int = 9, format: typing.Optional[typing.Union[str, int]] = lzma.FORMAT_AUTO, check: typing.Optional[typing.Union[str, int]] = -1, modifiers: str = "e", dict_size: typing.Optional[int] = None, literal_context_bits: typing.Optional[int] = None, literal_position_bits: typing.Optional[int] = None, position_bits: typing.Optional[int] = None, match_finder: typing.Optional[str] = "bt4", mode: typing.Optional[str] = "normal", additional_filters: typing.Iterable[typing.Dict[str, typing.Any]] = (), *args, **kwargs) -> None:  # pylint:disable=redefined-builtin,too-many-arguments,too-many-locals,unused-argument,too-many-branches
        super().__init__()
        if isinstance(format, str):
            format = getattr(lzma, "FORMAT_" + format.upper())

        if isinstance(check, str):
            check = getattr(lzma, "CHECK_" + check.upper())

        filters = list(additional_filters)
        if algo > -1:
            if isinstance(modifiers, str):
                modifiersNum = 0
                for m in modifiers:
                    modifiersNum |= modifiersMapping[m]
                modifiers = modifiersNum
                del modifiersNum

            lzmaFilter = {
                "id": "lzma" + str(algo),
                "preset": level | modifiers,
            }

            if dict_size is not None:
                lzmaFilter["dict"] = (dict_size,)
            if literal_context_bits is not None:
                lzmaFilter["lc"] = literal_context_bits
            if literal_position_bits is not None:
                lzmaFilter["lp"] = literal_position_bits
            if position_bits is not None:
                lzmaFilter["pb"] = position_bits
            if match_finder is not None:
                if isinstance(match_finder, str):
                    match_finder = getattr(lzma, "MF_" + match_finder.upper())
                lzmaFilter["mf"] = match_finder
            if mode is not None:
                if isinstance(mode, str):
                    mode = getattr(lzma, "MODE_" + mode.upper())
                lzmaFilter["mode"] = mode
            filters.append(lzmaFilter)

        for f in filters:
            if isinstance(f["id"], str):
                f["id"] = getattr(lzma, "FILTER_" + f["id"].upper())

        compressorParams = {
            "format": format,
            "check": check,
            "preset": None,  # set in filters
            "filters": filters,
        }
        decompressorParams = {
            "format": format,
            "memlimit": None,
        }

        if format is lzma.FORMAT_RAW:
            decompressorParams["filters"] = filters

        self.decompressor_params = decompressorParams

        if "format" not in compressorParams or compressorParams["format"] == lzma.FORMAT_AUTO:
            compressorParams["format"] = lzma.FORMAT_XZ  # TODO: detect from stream
        self.compressor_params = compressorParams

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        decompressor = lzma.LZMADecompressor(**self.decompressor_params)
        return ProcessorContextStub(decompressor.decompress(data))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        compressor = lzma.LZMACompressor(**self.compressor_params)
        return ProcessorContextStub(compressor.compress(data) + compressor.flush())
