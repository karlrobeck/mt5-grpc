import enums_pb2 as _enums_pb2
import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TickFromRequest(_message.Message):
    __slots__ = ("symbol", "date_from", "count", "flags")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    DATE_FROM_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    date_from: int
    count: int
    flags: _enums_pb2.CopyTicks
    def __init__(self, symbol: _Optional[str] = ..., date_from: _Optional[int] = ..., count: _Optional[int] = ..., flags: _Optional[_Union[_enums_pb2.CopyTicks, str]] = ...) -> None: ...

class TickRangeRequest(_message.Message):
    __slots__ = ("symbol", "date_from", "date_to", "flags")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    DATE_FROM_FIELD_NUMBER: _ClassVar[int]
    DATE_TO_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    date_from: int
    date_to: int
    flags: _enums_pb2.CopyTicks
    def __init__(self, symbol: _Optional[str] = ..., date_from: _Optional[int] = ..., date_to: _Optional[int] = ..., flags: _Optional[_Union[_enums_pb2.CopyTicks, str]] = ...) -> None: ...

class TicksResponse(_message.Message):
    __slots__ = ("ticks",)
    TICKS_FIELD_NUMBER: _ClassVar[int]
    ticks: _containers.RepeatedCompositeFieldContainer[_types_pb2.Tick]
    def __init__(self, ticks: _Optional[_Iterable[_Union[_types_pb2.Tick, _Mapping]]] = ...) -> None: ...

class ListenToSymbolsRequest(_message.Message):
    __slots__ = ("symbols",)
    SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    symbols: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, symbols: _Optional[_Iterable[str]] = ...) -> None: ...

class StreamTickResponse(_message.Message):
    __slots__ = ("symbol", "ticks")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TICKS_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    ticks: _types_pb2.Tick
    def __init__(self, symbol: _Optional[str] = ..., ticks: _Optional[_Union[_types_pb2.Tick, _Mapping]] = ...) -> None: ...
