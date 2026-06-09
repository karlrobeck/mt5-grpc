import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SymbolRequest(_message.Message):
    __slots__ = ("symbol",)
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    def __init__(self, symbol: _Optional[str] = ...) -> None: ...

class MarketDepthResponse(_message.Message):
    __slots__ = ("success", "entries")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    success: bool
    entries: _containers.RepeatedCompositeFieldContainer[_types_pb2.BookInfo]
    def __init__(self, success: _Optional[bool] = ..., entries: _Optional[_Iterable[_Union[_types_pb2.BookInfo, _Mapping]]] = ...) -> None: ...
