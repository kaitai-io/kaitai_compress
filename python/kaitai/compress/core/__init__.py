import typing
from abc import ABC, abstractmethod

# pylint:disable=unused-argument


class KaitaiProcessorContext(ABC):
    __slots__ = ()

    @abstractmethod
    def __call__(self, slce: slice, *args, **kwargs) -> bytes:
        raise NotImplementedError("Please implement process")


class ProcessorContextStub(KaitaiProcessorContext):
    """A dummy implementation for non-seekable streams. Just decompresses all the data and saves it."""

    __slots__ = ("data",)

    def __init__(self, data: typing.Union[bytes, bytearray], *args, **kwargs) -> None:
        self.data = data

    def __call__(self, slc: slice, *args, **kwargs) -> bytes:
        return self.data[slc]


class KaitaiProcessor(ABC):
    """The base processor class"""

    __slots__ = ()

    def decode(self, data: typing.Union[bytes, bytearray], *args, **kwargs) -> bytes:
        """The method implementing compatibility to legacy API. Gonna be removed somewhen."""
        return self.process(data, *args, **kwargs)(slice(None, None, None))

    @abstractmethod
    def process(self, data: typing.Union[bytes, bytearray]) -> KaitaiProcessorContext:
        raise NotImplementedError("Please implement process")

    def unprocess(self, data: typing.Union[bytes, bytearray]) -> KaitaiProcessorContext:
        raise NotImplementedError(self.__class__.__name__ + " processing is not invertible")

    def extract_args(self, data: typing.Union[bytes, bytearray], *args, **kwargs) -> tuple:
        raise NotImplementedError("Cannot get args of " + self.__class__.__name__)


class KaitaiCompressor(KaitaiProcessor):
    __slots__ = ()

    def compute_optimal_dict(self, data: typing.Iterable[typing.Union[bytes, bytearray]], *args, **kwargs):
        raise NotImplementedError(self.__class__.__name__ + " has no function for creation of custom dictionaries")
