from google.protobuf import empty_pb2 as _empty_pb2
import types_pb2 as _types_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrdersRequest(_message.Message):
    __slots__ = ("symbol", "group", "ticket")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    group: str
    ticket: int
    def __init__(self, symbol: _Optional[str] = ..., group: _Optional[str] = ..., ticket: _Optional[int] = ...) -> None: ...

class OrdersTotalResponse(_message.Message):
    __slots__ = ("total",)
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    total: int
    def __init__(self, total: _Optional[int] = ...) -> None: ...

class OrdersResponse(_message.Message):
    __slots__ = ("orders",)
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[_types_pb2.TradeOrder]
    def __init__(self, orders: _Optional[_Iterable[_Union[_types_pb2.TradeOrder, _Mapping]]] = ...) -> None: ...

class PositionsRequest(_message.Message):
    __slots__ = ("symbol", "group", "ticket")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    group: str
    ticket: int
    def __init__(self, symbol: _Optional[str] = ..., group: _Optional[str] = ..., ticket: _Optional[int] = ...) -> None: ...

class PositionsTotalResponse(_message.Message):
    __slots__ = ("total",)
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    total: int
    def __init__(self, total: _Optional[int] = ...) -> None: ...

class PositionsResponse(_message.Message):
    __slots__ = ("positions",)
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    positions: _containers.RepeatedCompositeFieldContainer[_types_pb2.TradePosition]
    def __init__(self, positions: _Optional[_Iterable[_Union[_types_pb2.TradePosition, _Mapping]]] = ...) -> None: ...

class HistoryRangeRequest(_message.Message):
    __slots__ = ("date_from", "date_to")
    DATE_FROM_FIELD_NUMBER: _ClassVar[int]
    DATE_TO_FIELD_NUMBER: _ClassVar[int]
    date_from: int
    date_to: int
    def __init__(self, date_from: _Optional[int] = ..., date_to: _Optional[int] = ...) -> None: ...

class HistoryOrdersRequest(_message.Message):
    __slots__ = ("date_from", "date_to", "group", "ticket", "position")
    DATE_FROM_FIELD_NUMBER: _ClassVar[int]
    DATE_TO_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    date_from: int
    date_to: int
    group: str
    ticket: int
    position: int
    def __init__(self, date_from: _Optional[int] = ..., date_to: _Optional[int] = ..., group: _Optional[str] = ..., ticket: _Optional[int] = ..., position: _Optional[int] = ...) -> None: ...

class HistoryDealsRequest(_message.Message):
    __slots__ = ("date_from", "date_to", "group", "ticket", "position")
    DATE_FROM_FIELD_NUMBER: _ClassVar[int]
    DATE_TO_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    date_from: int
    date_to: int
    group: str
    ticket: int
    position: int
    def __init__(self, date_from: _Optional[int] = ..., date_to: _Optional[int] = ..., group: _Optional[str] = ..., ticket: _Optional[int] = ..., position: _Optional[int] = ...) -> None: ...

class HistoryOrdersTotalResponse(_message.Message):
    __slots__ = ("total",)
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    total: int
    def __init__(self, total: _Optional[int] = ...) -> None: ...

class HistoryOrdersResponse(_message.Message):
    __slots__ = ("orders",)
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    orders: _containers.RepeatedCompositeFieldContainer[_types_pb2.TradeOrder]
    def __init__(self, orders: _Optional[_Iterable[_Union[_types_pb2.TradeOrder, _Mapping]]] = ...) -> None: ...

class HistoryDealsTotalResponse(_message.Message):
    __slots__ = ("total",)
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    total: int
    def __init__(self, total: _Optional[int] = ...) -> None: ...

class HistoryDealsResponse(_message.Message):
    __slots__ = ("deals",)
    DEALS_FIELD_NUMBER: _ClassVar[int]
    deals: _containers.RepeatedCompositeFieldContainer[_types_pb2.TradeDeal]
    def __init__(self, deals: _Optional[_Iterable[_Union[_types_pb2.TradeDeal, _Mapping]]] = ...) -> None: ...

class CalcMarginRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _types_pb2.TradeRequest
    def __init__(self, request: _Optional[_Union[_types_pb2.TradeRequest, _Mapping]] = ...) -> None: ...

class CalcMarginResponse(_message.Message):
    __slots__ = ("margin",)
    MARGIN_FIELD_NUMBER: _ClassVar[int]
    margin: float
    def __init__(self, margin: _Optional[float] = ...) -> None: ...

class CalcProfitRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _types_pb2.TradeRequest
    def __init__(self, request: _Optional[_Union[_types_pb2.TradeRequest, _Mapping]] = ...) -> None: ...

class CalcProfitResponse(_message.Message):
    __slots__ = ("profit",)
    PROFIT_FIELD_NUMBER: _ClassVar[int]
    profit: float
    def __init__(self, profit: _Optional[float] = ...) -> None: ...

class CheckOrderRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _types_pb2.TradeRequest
    def __init__(self, request: _Optional[_Union[_types_pb2.TradeRequest, _Mapping]] = ...) -> None: ...

class SendOrderRequest(_message.Message):
    __slots__ = ("request",)
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    request: _types_pb2.TradeRequest
    def __init__(self, request: _Optional[_Union[_types_pb2.TradeRequest, _Mapping]] = ...) -> None: ...
