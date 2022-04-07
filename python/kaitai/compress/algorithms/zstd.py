import typing

from ..core import KaitaiCompressor, ProcessorContextStub

default_dict_size = 110 << 10  # 110 KiB


def splitDataIntoPredefinedCountOfChunks(data: typing.Iterator[typing.Any], count: int = 7) -> typing.Iterable[bytes]:
    data = list(data)
    while len(data) < count:
        spl = max(range(len(data)), key=lambda i: len(data[i]))
        d = data[spl]
        sl = len(d) // 2
        d1 = d[:sl]
        d2 = d[sl:]
        data[spl] = d1
        data.insert(spl + 1, d2)
    return data


# pylint:disable=arguments-differ


class Zstd(KaitaiCompressor):
    __slots__ = ("decompressor", "compressor", "dictTrainerParams",)
    zstd = None

    def __init__(self, format: typing.Union[int, str] = "zstd1", log_window_size: typing.Optional[int] = None, dictionary: typing.Optional[typing.Union[bytes, int]] = None, level: int = 0, should_write_checksum: bool = True, should_write_uncompressed_size: bool = True, should_write_dict_id: bool = True, strategy: typing.Optional[typing.Union[int, str]] = None, hash_log_size: typing.Optional[int] = None, match_min_size: typing.Optional[int] = None, chain_log_size: typing.Optional[int] = None, search_log_size: typing.Optional[int] = None, overlap_log_size: typing.Optional[int] = None, target_length: typing.Optional[int] = None, ldm: typing.Optional[bool] = None, ldm_hash_log_size: typing.Optional[int] = None, ldm_match_min_size: typing.Optional[int] = None, ldm_bucket_size_log: typing.Optional[int] = None, ldm_hash_rate_log: typing.Optional[int] = None, job_size: typing.Optional[int] = None, force_max_window: typing.Optional[int] = None) -> None:  # pylint:disable=redefined-builtin,too-many-arguments,too-many-locals,unused-argument,too-many-branches,too-many-statements
        super().__init__()
        if self.__class__.zstd is None:
            import zstandard as zstd  # pylint:disable=import-outside-toplevel

            self.__class__.zstd = zstd
        if isinstance(format, str):
            format = getattr(self.__class__.zstd, "FORMAT_" + format.upper())

        if level == 0:
            level = self.__class__.zstd.MAX_COMPRESSION_LEVEL

        decompressorParams = {"format": format}
        compressorParamsDict = {"threads": -1, "format": format}
        compressorParams = {}

        if dictionary:
            if isinstance(dictionary, int) and dictionary != 0:
                raise ValueError("Only 0 is used to indicate there is no data")
            dic = self.__class__.zstd.ZstdCompressionDict(dictionary, dict_type=self.__class__.zstd.DICT_TYPE_RAWCONTENT)
            dic.precompute_compress(level=level)
            decompressorParams["dict_data"] = compressorParams["dict_data"] = dic

        if log_window_size is not None:
            decompressorParams["max_window_size"] = 2 ** log_window_size
            compressorParamsDict["window_log"] = log_window_size

        self.decompressor = self.__class__.zstd.ZstdDecompressor(**decompressorParams)

        compressorParamsDict["write_checksum"] = should_write_checksum
        compressorParamsDict["write_content_size"] = should_write_uncompressed_size
        compressorParamsDict["write_dict_id"] = should_write_dict_id

        if strategy is not None:
            if isinstance(strategy, str):
                strategy = getattr(self.__class__.zstd, "STRATEGY_" + strategy.upper())
            compressorParamsDict["strategy"] = strategy

        if hash_log_size is not None:
            compressorParamsDict["hash_log"] = hash_log_size
        if match_min_size is not None:
            compressorParamsDict["min_match"] = match_min_size

        if chain_log_size is not None:
            compressorParamsDict["chain_log"] = chain_log_size
        if search_log_size is not None:
            compressorParamsDict["search_log"] = search_log_size
        if overlap_log_size is not None:
            compressorParamsDict["overlap_log"] = overlap_log_size
        if target_length is not None:
            compressorParamsDict["target_length"] = target_length
        if ldm is not None:
            compressorParamsDict["enable_ldm"] = ldm
            if ldm:
                if ldm_hash_log_size is not None:
                    compressorParamsDict["ldm_hash_log"] = ldm_hash_log_size
                if ldm_match_min_size is not None:
                    compressorParamsDict["ldm_min_match"] = ldm_match_min_size
                if ldm_bucket_size_log is not None:
                    compressorParamsDict["ldm_bucket_size_log"] = ldm_bucket_size_log
                if ldm_hash_rate_log is not None:
                    compressorParamsDict["ldm_hash_rate_log"] = ldm_hash_rate_log
        if job_size is not None:
            compressorParamsDict["job_size"] = job_size
        if force_max_window is not None:
            compressorParamsDict["force_max_window"] = force_max_window

        compressorParams["compression_params"] = self.__class__.zstd.ZstdCompressionParameters.from_level(level, **compressorParamsDict)
        self.compressor = self.zstd.ZstdCompressor(**compressorParams)
        self.dictTrainerParams = {
            "threads": 2,
            #"threads": compressorParamsDict["threads"],
            #"threads": 0,
            #"level": level,
            "level": 1,
            #"dict_size": None,  # int
            #"k": None,  # segment_size, int
            #"d": None,  # dmer_size,int
            "dict_id": 0,  # int
            #"steps": None,  # int
            "notifications": 0,
            #"notifications": 4,
        }

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.decompressor.decompress(data))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        return ProcessorContextStub(self.compressor.compress(data))

    def compute_optimal_dict(self, data: typing.Iterable[typing.Union[bytes, bytearray]], dict_size: typing.Optional[int] = None, *args, **kwargs):
        data = splitDataIntoPredefinedCountOfChunks(data, 7)
        if dict_size is None:
            dict_size = default_dict_size
        if dict_size < 256:
            dict_size = 256
        dict_data = self.__class__.zstd.train_dictionary(dict_size, samples=data, **self.dictTrainerParams)
        return dict_data.as_bytes()
