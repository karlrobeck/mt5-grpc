from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Tick(_message.Message):
    __slots__ = ("time", "bid", "ask", "volume")
    TIME_FIELD_NUMBER: _ClassVar[int]
    BID_FIELD_NUMBER: _ClassVar[int]
    ASK_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    time: int
    bid: float
    ask: float
    volume: int
    def __init__(self, time: _Optional[int] = ..., bid: _Optional[float] = ..., ask: _Optional[float] = ..., volume: _Optional[int] = ...) -> None: ...

class LastTickRequest(_message.Message):
    __slots__ = ("symbol",)
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    def __init__(self, symbol: _Optional[str] = ...) -> None: ...
