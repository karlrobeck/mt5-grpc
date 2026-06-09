import enums_pb2 as _enums_pb2
import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RatesFromRequest(_message.Message):
    __slots__ = ("symbol", "timeframe", "date_from", "count")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TIMEFRAME_FIELD_NUMBER: _ClassVar[int]
    DATE_FROM_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    timeframe: _enums_pb2.Timeframe
    date_from: int
    count: int
    def __init__(self, symbol: _Optional[str] = ..., timeframe: _Optional[_Union[_enums_pb2.Timeframe, str]] = ..., date_from: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class RatesFromPosRequest(_message.Message):
    __slots__ = ("symbol", "timeframe", "start_pos", "count")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TIMEFRAME_FIELD_NUMBER: _ClassVar[int]
    START_POS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    timeframe: _enums_pb2.Timeframe
    start_pos: int
    count: int
    def __init__(self, symbol: _Optional[str] = ..., timeframe: _Optional[_Union[_enums_pb2.Timeframe, str]] = ..., start_pos: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class RatesRangeRequest(_message.Message):
    __slots__ = ("symbol", "timeframe", "date_from", "date_to")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TIMEFRAME_FIELD_NUMBER: _ClassVar[int]
    DATE_FROM_FIELD_NUMBER: _ClassVar[int]
    DATE_TO_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    timeframe: _enums_pb2.Timeframe
    date_from: int
    date_to: int
    def __init__(self, symbol: _Optional[str] = ..., timeframe: _Optional[_Union[_enums_pb2.Timeframe, str]] = ..., date_from: _Optional[int] = ..., date_to: _Optional[int] = ...) -> None: ...

class RatesResponse(_message.Message):
    __slots__ = ("rates",)
    RATES_FIELD_NUMBER: _ClassVar[int]
    rates: _containers.RepeatedCompositeFieldContainer[_types_pb2.Rate]
    def __init__(self, rates: _Optional[_Iterable[_Union[_types_pb2.Rate, _Mapping]]] = ...) -> None: ...
