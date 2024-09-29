import typing

from ..core import KaitaiCompressor, ProcessorContextStub

# pylint:disable=arguments-differ


class Lz4(KaitaiCompressor):
    __slots__ = ("compressorParams",)
    lz4Frame = None

    def __init__(self, block_size: typing.Optional[int] = None, should_link_blocks: bool = True, compression_level: typing.Optional[int] = None, frame_checksum: bool = False, block_checksum: bool = False, *args, **kwargs) -> None:  # pylint:disable=unused-argument,too-many-arguments
        super().__init__()
        if self.__class__.lz4Frame is None:
            import lz4.frame  # pylint:disable=import-outside-toplevel

            self.__class__.lz4Frame = lz4.frame

        if compression_level is None:
            compression_level = self.__class__.lz4Frame.COMPRESSIONLEVEL_MAX
        if block_size is None:
            block_size = self.__class__.lz4Frame.BLOCKSIZE_MAX4MB
        self.compressorParams = {
            "block_size": block_size,
            "block_linked": should_link_blocks,
            "compression_level": compression_level,
            "content_checksum": frame_checksum,
            "block_checksum": block_checksum,
            "return_bytearray": False
        }

    def process(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        obj = self.__class__.lz4Frame.LZ4FrameDecompressor(return_bytearray=False)
        return ProcessorContextStub(obj.decompress(data))

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> ProcessorContextStub:
        obj = self.__class__.lz4Frame.LZ4FrameCompressor(**self.compressorParams)
        return ProcessorContextStub(obj.begin(len(data)) + obj.compress(data) + obj.flush())

    def extract_args(self, data: typing.Union[bytes, bytearray]):
        res = self.__class__.lz4Frame.get_frame_info(data)
        return (res["block_size"], res["linker"], res["compression_level"], res["content_checksum"], res["block_checksum"])
