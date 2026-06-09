from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class Timeframe(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TIMEFRAME_UNSPECIFIED: _ClassVar[Timeframe]
    TIMEFRAME_M1: _ClassVar[Timeframe]
    TIMEFRAME_M2: _ClassVar[Timeframe]
    TIMEFRAME_M3: _ClassVar[Timeframe]
    TIMEFRAME_M4: _ClassVar[Timeframe]
    TIMEFRAME_M5: _ClassVar[Timeframe]
    TIMEFRAME_M6: _ClassVar[Timeframe]
    TIMEFRAME_M10: _ClassVar[Timeframe]
    TIMEFRAME_M12: _ClassVar[Timeframe]
    TIMEFRAME_M15: _ClassVar[Timeframe]
    TIMEFRAME_M20: _ClassVar[Timeframe]
    TIMEFRAME_M30: _ClassVar[Timeframe]
    TIMEFRAME_H1: _ClassVar[Timeframe]
    TIMEFRAME_H2: _ClassVar[Timeframe]
    TIMEFRAME_H3: _ClassVar[Timeframe]
    TIMEFRAME_H4: _ClassVar[Timeframe]
    TIMEFRAME_H6: _ClassVar[Timeframe]
    TIMEFRAME_H8: _ClassVar[Timeframe]
    TIMEFRAME_H12: _ClassVar[Timeframe]
    TIMEFRAME_D1: _ClassVar[Timeframe]
    TIMEFRAME_W1: _ClassVar[Timeframe]
    TIMEFRAME_MN1: _ClassVar[Timeframe]

class OrderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_TYPE_BUY: _ClassVar[OrderType]
    ORDER_TYPE_SELL: _ClassVar[OrderType]
    ORDER_TYPE_BUY_LIMIT: _ClassVar[OrderType]
    ORDER_TYPE_SELL_LIMIT: _ClassVar[OrderType]
    ORDER_TYPE_BUY_STOP: _ClassVar[OrderType]
    ORDER_TYPE_SELL_STOP: _ClassVar[OrderType]
    ORDER_TYPE_BUY_STOP_LIMIT: _ClassVar[OrderType]
    ORDER_TYPE_SELL_STOP_LIMIT: _ClassVar[OrderType]
    ORDER_TYPE_CLOSE_BY: _ClassVar[OrderType]

class OrderTypeFilling(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_FILLING_FOK: _ClassVar[OrderTypeFilling]
    ORDER_FILLING_IOC: _ClassVar[OrderTypeFilling]
    ORDER_FILLING_RETURN: _ClassVar[OrderTypeFilling]
    ORDER_FILLING_BOC: _ClassVar[OrderTypeFilling]

class OrderTypeTime(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_TIME_GTC: _ClassVar[OrderTypeTime]
    ORDER_TIME_DAY: _ClassVar[OrderTypeTime]
    ORDER_TIME_SPECIFIED: _ClassVar[OrderTypeTime]
    ORDER_TIME_SPECIFIED_DAY: _ClassVar[OrderTypeTime]

class OrderState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_STATE_STARTED: _ClassVar[OrderState]
    ORDER_STATE_PLACED: _ClassVar[OrderState]
    ORDER_STATE_CANCELED: _ClassVar[OrderState]
    ORDER_STATE_PARTIAL: _ClassVar[OrderState]
    ORDER_STATE_FILLED: _ClassVar[OrderState]
    ORDER_STATE_REJECTED: _ClassVar[OrderState]
    ORDER_STATE_EXPIRED: _ClassVar[OrderState]
    ORDER_STATE_REQUEST_ADD: _ClassVar[OrderState]
    ORDER_STATE_REQUEST_MODIFY: _ClassVar[OrderState]
    ORDER_STATE_REQUEST_CANCEL: _ClassVar[OrderState]

class TradeRequestAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRADE_ACTION_UNSPECIFIED: _ClassVar[TradeRequestAction]
    TRADE_ACTION_DEAL: _ClassVar[TradeRequestAction]
    TRADE_ACTION_PENDING: _ClassVar[TradeRequestAction]
    TRADE_ACTION_SLTP: _ClassVar[TradeRequestAction]
    TRADE_ACTION_MODIFY: _ClassVar[TradeRequestAction]
    TRADE_ACTION_REMOVE: _ClassVar[TradeRequestAction]
    TRADE_ACTION_CLOSE_BY: _ClassVar[TradeRequestAction]

class DealType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEAL_TYPE_BUY: _ClassVar[DealType]
    DEAL_TYPE_SELL: _ClassVar[DealType]
    DEAL_TYPE_BALANCE: _ClassVar[DealType]
    DEAL_TYPE_CREDIT: _ClassVar[DealType]
    DEAL_TYPE_CHARGE: _ClassVar[DealType]
    DEAL_TYPE_CORRECTION: _ClassVar[DealType]
    DEAL_TYPE_BONUS: _ClassVar[DealType]
    DEAL_TYPE_COMMISSION: _ClassVar[DealType]
    DEAL_TYPE_COMMISSION_DAILY: _ClassVar[DealType]
    DEAL_TYPE_COMMISSION_MONTHLY: _ClassVar[DealType]
    DEAL_TYPE_COMMISSION_AGENT_DAILY: _ClassVar[DealType]
    DEAL_TYPE_COMMISSION_AGENT_MONTHLY: _ClassVar[DealType]
    DEAL_TYPE_INTEREST: _ClassVar[DealType]
    DEAL_TYPE_BUY_CANCELED: _ClassVar[DealType]
    DEAL_TYPE_SELL_CANCELED: _ClassVar[DealType]
    DEAL_DIVIDEND: _ClassVar[DealType]
    DEAL_DIVIDEND_FRANKED: _ClassVar[DealType]
    DEAL_TAX: _ClassVar[DealType]

class DealEntry(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEAL_ENTRY_IN: _ClassVar[DealEntry]
    DEAL_ENTRY_OUT: _ClassVar[DealEntry]
    DEAL_ENTRY_INOUT: _ClassVar[DealEntry]
    DEAL_ENTRY_OUT_BY: _ClassVar[DealEntry]

class CopyTicks(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COPY_TICKS_UNSPECIFIED: _ClassVar[CopyTicks]
    COPY_TICKS_ALL: _ClassVar[CopyTicks]
    COPY_TICKS_INFO: _ClassVar[CopyTicks]
    COPY_TICKS_TRADE: _ClassVar[CopyTicks]

class BookType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BOOK_TYPE_UNSPECIFIED: _ClassVar[BookType]
    BOOK_TYPE_SELL: _ClassVar[BookType]
    BOOK_TYPE_BUY: _ClassVar[BookType]
    BOOK_TYPE_SELL_MARKET: _ClassVar[BookType]
    BOOK_TYPE_BUY_MARKET: _ClassVar[BookType]

class TradeRetcode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TRADE_RETCODE_UNSPECIFIED: _ClassVar[TradeRetcode]
    TRADE_RETCODE_REQUOTE: _ClassVar[TradeRetcode]
    TRADE_RETCODE_REJECT: _ClassVar[TradeRetcode]
    TRADE_RETCODE_CANCEL: _ClassVar[TradeRetcode]
    TRADE_RETCODE_PLACED: _ClassVar[TradeRetcode]
    TRADE_RETCODE_DONE: _ClassVar[TradeRetcode]
    TRADE_RETCODE_DONE_PARTIAL: _ClassVar[TradeRetcode]
    TRADE_RETCODE_ERROR: _ClassVar[TradeRetcode]
    TRADE_RETCODE_TIMEOUT: _ClassVar[TradeRetcode]
    TRADE_RETCODE_INVALID: _ClassVar[TradeRetcode]
    TRADE_RETCODE_INVALID_VOLUME: _ClassVar[TradeRetcode]
    TRADE_RETCODE_INVALID_PRICE: _ClassVar[TradeRetcode]
    TRADE_RETCODE_INVALID_STOPS: _ClassVar[TradeRetcode]
    TRADE_RETCODE_TRADE_DISABLED: _ClassVar[TradeRetcode]
    TRADE_RETCODE_MARKET_CLOSED: _ClassVar[TradeRetcode]
    TRADE_RETCODE_NO_MONEY: _ClassVar[TradeRetcode]
    TRADE_RETCODE_PRICE_CHANGED: _ClassVar[TradeRetcode]
    TRADE_RETCODE_PRICE_OFF: _ClassVar[TradeRetcode]
    TRADE_RETCODE_INVALID_EXPIRATION: _ClassVar[TradeRetcode]
    TRADE_RETCODE_ORDER_CHANGED: _ClassVar[TradeRetcode]
    TRADE_RETCODE_TOO_MANY_REQUESTS: _ClassVar[TradeRetcode]
    TRADE_RETCODE_NO_CHANGES: _ClassVar[TradeRetcode]
    TRADE_RETCODE_SERVER_DISABLES_AT: _ClassVar[TradeRetcode]
    TRADE_RETCODE_CLIENT_DISABLES_AT: _ClassVar[TradeRetcode]
    TRADE_RETCODE_LOCKED: _ClassVar[TradeRetcode]
    TRADE_RETCODE_FROZEN: _ClassVar[TradeRetcode]
    TRADE_RETCODE_INVALID_FILL: _ClassVar[TradeRetcode]
    TRADE_RETCODE_CONNECTION: _ClassVar[TradeRetcode]
    TRADE_RETCODE_ONLY_REAL: _ClassVar[TradeRetcode]
    TRADE_RETCODE_LIMIT_ORDERS: _ClassVar[TradeRetcode]
    TRADE_RETCODE_LIMIT_VOLUME: _ClassVar[TradeRetcode]
    TRADE_RETCODE_INVALID_ORDER: _ClassVar[TradeRetcode]
    TRADE_RETCODE_POSITION_CLOSED: _ClassVar[TradeRetcode]
    TRADE_RETCODE_INVALID_CLOSE_VOLUME: _ClassVar[TradeRetcode]
    TRADE_RETCODE_CLOSE_ORDER_EXIST: _ClassVar[TradeRetcode]
    TRADE_RETCODE_LIMIT_POSITIONS: _ClassVar[TradeRetcode]
    TRADE_RETCODE_REJECT_CANCEL: _ClassVar[TradeRetcode]
    TRADE_RETCODE_LONG_ONLY: _ClassVar[TradeRetcode]
    TRADE_RETCODE_SHORT_ONLY: _ClassVar[TradeRetcode]
    TRADE_RETCODE_CLOSE_ONLY: _ClassVar[TradeRetcode]
    TRADE_RETCODE_FIFO_CLOSE: _ClassVar[TradeRetcode]

class PositionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POSITION_TYPE_BUY: _ClassVar[PositionType]
    POSITION_TYPE_SELL: _ClassVar[PositionType]

class PositionReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    POSITION_REASON_CLIENT: _ClassVar[PositionReason]
    POSITION_REASON_MOBILE: _ClassVar[PositionReason]
    POSITION_REASON_WEB: _ClassVar[PositionReason]
    POSITION_REASON_EXPERT: _ClassVar[PositionReason]

class OrderReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORDER_REASON_CLIENT: _ClassVar[OrderReason]
    ORDER_REASON_MOBILE: _ClassVar[OrderReason]
    ORDER_REASON_WEB: _ClassVar[OrderReason]
    ORDER_REASON_EXPERT: _ClassVar[OrderReason]
    ORDER_REASON_SL: _ClassVar[OrderReason]
    ORDER_REASON_TP: _ClassVar[OrderReason]
    ORDER_REASON_SO: _ClassVar[OrderReason]

class DealReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEAL_REASON_CLIENT: _ClassVar[DealReason]
    DEAL_REASON_MOBILE: _ClassVar[DealReason]
    DEAL_REASON_WEB: _ClassVar[DealReason]
    DEAL_REASON_EXPERT: _ClassVar[DealReason]
    DEAL_REASON_SL: _ClassVar[DealReason]
    DEAL_REASON_TP: _ClassVar[DealReason]
    DEAL_REASON_SO: _ClassVar[DealReason]
    DEAL_REASON_ROLLOVER: _ClassVar[DealReason]
    DEAL_REASON_VMARGIN: _ClassVar[DealReason]
    DEAL_REASON_SPLIT: _ClassVar[DealReason]

class SymbolCalcMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYMBOL_CALC_MODE_FOREX: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_FUTURES: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_CFD: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_CFDINDEX: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_CFDLEVERAGE: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_EXCH_STOCKS: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_EXCH_FUTURES: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_EXCH_OPTIONS: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_EXCH_OPTIONS_MARGIN: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_EXCH_BONDS: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_EXCH_BONDS_MOEX: _ClassVar[SymbolCalcMode]
    SYMBOL_CALC_MODE_SERV_COLLATERAL: _ClassVar[SymbolCalcMode]

class SymbolTradeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYMBOL_TRADE_MODE_DISABLED: _ClassVar[SymbolTradeMode]
    SYMBOL_TRADE_MODE_LONGONLY: _ClassVar[SymbolTradeMode]
    SYMBOL_TRADE_MODE_SHORTONLY: _ClassVar[SymbolTradeMode]
    SYMBOL_TRADE_MODE_CLOSEONLY: _ClassVar[SymbolTradeMode]
    SYMBOL_TRADE_MODE_FULL: _ClassVar[SymbolTradeMode]

class SymbolTradeExecution(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYMBOL_TRADE_EXECUTION_REQUEST: _ClassVar[SymbolTradeExecution]
    SYMBOL_TRADE_EXECUTION_INSTANT: _ClassVar[SymbolTradeExecution]
    SYMBOL_TRADE_EXECUTION_MARKET: _ClassVar[SymbolTradeExecution]
    SYMBOL_TRADE_EXECUTION_EXCHANGE: _ClassVar[SymbolTradeExecution]

class SymbolSwapMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYMBOL_SWAP_MODE_DISABLED: _ClassVar[SymbolSwapMode]
    SYMBOL_SWAP_MODE_POINTS: _ClassVar[SymbolSwapMode]
    SYMBOL_SWAP_MODE_CURRENCY_SYMBOL: _ClassVar[SymbolSwapMode]
    SYMBOL_SWAP_MODE_CURRENCY_MARGIN: _ClassVar[SymbolSwapMode]
    SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT: _ClassVar[SymbolSwapMode]
    SYMBOL_SWAP_MODE_INTEREST_CURRENT: _ClassVar[SymbolSwapMode]
    SYMBOL_SWAP_MODE_INTEREST_OPEN: _ClassVar[SymbolSwapMode]
    SYMBOL_SWAP_MODE_REOPEN_CURRENT: _ClassVar[SymbolSwapMode]
    SYMBOL_SWAP_MODE_REOPEN_BID: _ClassVar[SymbolSwapMode]

class SymbolChartMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYMBOL_CHART_MODE_BID: _ClassVar[SymbolChartMode]
    SYMBOL_CHART_MODE_LAST: _ClassVar[SymbolChartMode]

class SymbolOrderGtcMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYMBOL_ORDERS_GTC: _ClassVar[SymbolOrderGtcMode]
    SYMBOL_ORDERS_DAILY: _ClassVar[SymbolOrderGtcMode]
    SYMBOL_ORDERS_DAILY_NO_STOPS: _ClassVar[SymbolOrderGtcMode]

class SymbolOptionRight(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYMBOL_OPTION_RIGHT_CALL: _ClassVar[SymbolOptionRight]
    SYMBOL_OPTION_RIGHT_PUT: _ClassVar[SymbolOptionRight]

class SymbolOptionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SYMBOL_OPTION_MODE_EUROPEAN: _ClassVar[SymbolOptionMode]
    SYMBOL_OPTION_MODE_AMERICAN: _ClassVar[SymbolOptionMode]

class DayOfWeek(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DAY_OF_WEEK_SUNDAY: _ClassVar[DayOfWeek]
    DAY_OF_WEEK_MONDAY: _ClassVar[DayOfWeek]
    DAY_OF_WEEK_TUESDAY: _ClassVar[DayOfWeek]
    DAY_OF_WEEK_WEDNESDAY: _ClassVar[DayOfWeek]
    DAY_OF_WEEK_THURSDAY: _ClassVar[DayOfWeek]
    DAY_OF_WEEK_FRIDAY: _ClassVar[DayOfWeek]
    DAY_OF_WEEK_SATURDAY: _ClassVar[DayOfWeek]

class AccountTradeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACCOUNT_TRADE_MODE_DEMO: _ClassVar[AccountTradeMode]
    ACCOUNT_TRADE_MODE_CONTEST: _ClassVar[AccountTradeMode]
    ACCOUNT_TRADE_MODE_REAL: _ClassVar[AccountTradeMode]

class AccountStopoutMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACCOUNT_STOPOUT_MODE_PERCENT: _ClassVar[AccountStopoutMode]
    ACCOUNT_STOPOUT_MODE_MONEY: _ClassVar[AccountStopoutMode]

class AccountMarginMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACCOUNT_MARGIN_MODE_RETAIL_NETTING: _ClassVar[AccountMarginMode]
    ACCOUNT_MARGIN_MODE_EXCHANGE: _ClassVar[AccountMarginMode]
    ACCOUNT_MARGIN_MODE_RETAIL_HEDGING: _ClassVar[AccountMarginMode]

class ResError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RES_E_UNSPECIFIED: _ClassVar[ResError]
    RES_S_OK: _ClassVar[ResError]
    RES_E_FAIL: _ClassVar[ResError]
    RES_E_INVALID_PARAMS: _ClassVar[ResError]
    RES_E_NO_MEMORY: _ClassVar[ResError]
    RES_E_NOT_FOUND: _ClassVar[ResError]
    RES_E_INVALID_VERSION: _ClassVar[ResError]
    RES_E_AUTH_FAILED: _ClassVar[ResError]
    RES_E_UNSUPPORTED: _ClassVar[ResError]
    RES_E_AUTO_TRADING_DISABLED: _ClassVar[ResError]
    RES_E_INTERNAL_FAIL: _ClassVar[ResError]
    RES_E_INTERNAL_FAIL_SEND: _ClassVar[ResError]
    RES_E_INTERNAL_FAIL_RECEIVE: _ClassVar[ResError]
    RES_E_INTERNAL_FAIL_INIT: _ClassVar[ResError]
    RES_E_INTERNAL_FAIL_CONNECT: _ClassVar[ResError]
    RES_E_INTERNAL_FAIL_TIMEOUT: _ClassVar[ResError]
TIMEFRAME_UNSPECIFIED: Timeframe
TIMEFRAME_M1: Timeframe
TIMEFRAME_M2: Timeframe
TIMEFRAME_M3: Timeframe
TIMEFRAME_M4: Timeframe
TIMEFRAME_M5: Timeframe
TIMEFRAME_M6: Timeframe
TIMEFRAME_M10: Timeframe
TIMEFRAME_M12: Timeframe
TIMEFRAME_M15: Timeframe
TIMEFRAME_M20: Timeframe
TIMEFRAME_M30: Timeframe
TIMEFRAME_H1: Timeframe
TIMEFRAME_H2: Timeframe
TIMEFRAME_H3: Timeframe
TIMEFRAME_H4: Timeframe
TIMEFRAME_H6: Timeframe
TIMEFRAME_H8: Timeframe
TIMEFRAME_H12: Timeframe
TIMEFRAME_D1: Timeframe
TIMEFRAME_W1: Timeframe
TIMEFRAME_MN1: Timeframe
ORDER_TYPE_BUY: OrderType
ORDER_TYPE_SELL: OrderType
ORDER_TYPE_BUY_LIMIT: OrderType
ORDER_TYPE_SELL_LIMIT: OrderType
ORDER_TYPE_BUY_STOP: OrderType
ORDER_TYPE_SELL_STOP: OrderType
ORDER_TYPE_BUY_STOP_LIMIT: OrderType
ORDER_TYPE_SELL_STOP_LIMIT: OrderType
ORDER_TYPE_CLOSE_BY: OrderType
ORDER_FILLING_FOK: OrderTypeFilling
ORDER_FILLING_IOC: OrderTypeFilling
ORDER_FILLING_RETURN: OrderTypeFilling
ORDER_FILLING_BOC: OrderTypeFilling
ORDER_TIME_GTC: OrderTypeTime
ORDER_TIME_DAY: OrderTypeTime
ORDER_TIME_SPECIFIED: OrderTypeTime
ORDER_TIME_SPECIFIED_DAY: OrderTypeTime
ORDER_STATE_STARTED: OrderState
ORDER_STATE_PLACED: OrderState
ORDER_STATE_CANCELED: OrderState
ORDER_STATE_PARTIAL: OrderState
ORDER_STATE_FILLED: OrderState
ORDER_STATE_REJECTED: OrderState
ORDER_STATE_EXPIRED: OrderState
ORDER_STATE_REQUEST_ADD: OrderState
ORDER_STATE_REQUEST_MODIFY: OrderState
ORDER_STATE_REQUEST_CANCEL: OrderState
TRADE_ACTION_UNSPECIFIED: TradeRequestAction
TRADE_ACTION_DEAL: TradeRequestAction
TRADE_ACTION_PENDING: TradeRequestAction
TRADE_ACTION_SLTP: TradeRequestAction
TRADE_ACTION_MODIFY: TradeRequestAction
TRADE_ACTION_REMOVE: TradeRequestAction
TRADE_ACTION_CLOSE_BY: TradeRequestAction
DEAL_TYPE_BUY: DealType
DEAL_TYPE_SELL: DealType
DEAL_TYPE_BALANCE: DealType
DEAL_TYPE_CREDIT: DealType
DEAL_TYPE_CHARGE: DealType
DEAL_TYPE_CORRECTION: DealType
DEAL_TYPE_BONUS: DealType
DEAL_TYPE_COMMISSION: DealType
DEAL_TYPE_COMMISSION_DAILY: DealType
DEAL_TYPE_COMMISSION_MONTHLY: DealType
DEAL_TYPE_COMMISSION_AGENT_DAILY: DealType
DEAL_TYPE_COMMISSION_AGENT_MONTHLY: DealType
DEAL_TYPE_INTEREST: DealType
DEAL_TYPE_BUY_CANCELED: DealType
DEAL_TYPE_SELL_CANCELED: DealType
DEAL_DIVIDEND: DealType
DEAL_DIVIDEND_FRANKED: DealType
DEAL_TAX: DealType
DEAL_ENTRY_IN: DealEntry
DEAL_ENTRY_OUT: DealEntry
DEAL_ENTRY_INOUT: DealEntry
DEAL_ENTRY_OUT_BY: DealEntry
COPY_TICKS_UNSPECIFIED: CopyTicks
COPY_TICKS_ALL: CopyTicks
COPY_TICKS_INFO: CopyTicks
COPY_TICKS_TRADE: CopyTicks
BOOK_TYPE_UNSPECIFIED: BookType
BOOK_TYPE_SELL: BookType
BOOK_TYPE_BUY: BookType
BOOK_TYPE_SELL_MARKET: BookType
BOOK_TYPE_BUY_MARKET: BookType
TRADE_RETCODE_UNSPECIFIED: TradeRetcode
TRADE_RETCODE_REQUOTE: TradeRetcode
TRADE_RETCODE_REJECT: TradeRetcode
TRADE_RETCODE_CANCEL: TradeRetcode
TRADE_RETCODE_PLACED: TradeRetcode
TRADE_RETCODE_DONE: TradeRetcode
TRADE_RETCODE_DONE_PARTIAL: TradeRetcode
TRADE_RETCODE_ERROR: TradeRetcode
TRADE_RETCODE_TIMEOUT: TradeRetcode
TRADE_RETCODE_INVALID: TradeRetcode
TRADE_RETCODE_INVALID_VOLUME: TradeRetcode
TRADE_RETCODE_INVALID_PRICE: TradeRetcode
TRADE_RETCODE_INVALID_STOPS: TradeRetcode
TRADE_RETCODE_TRADE_DISABLED: TradeRetcode
TRADE_RETCODE_MARKET_CLOSED: TradeRetcode
TRADE_RETCODE_NO_MONEY: TradeRetcode
TRADE_RETCODE_PRICE_CHANGED: TradeRetcode
TRADE_RETCODE_PRICE_OFF: TradeRetcode
TRADE_RETCODE_INVALID_EXPIRATION: TradeRetcode
TRADE_RETCODE_ORDER_CHANGED: TradeRetcode
TRADE_RETCODE_TOO_MANY_REQUESTS: TradeRetcode
TRADE_RETCODE_NO_CHANGES: TradeRetcode
TRADE_RETCODE_SERVER_DISABLES_AT: TradeRetcode
TRADE_RETCODE_CLIENT_DISABLES_AT: TradeRetcode
TRADE_RETCODE_LOCKED: TradeRetcode
TRADE_RETCODE_FROZEN: TradeRetcode
TRADE_RETCODE_INVALID_FILL: TradeRetcode
TRADE_RETCODE_CONNECTION: TradeRetcode
TRADE_RETCODE_ONLY_REAL: TradeRetcode
TRADE_RETCODE_LIMIT_ORDERS: TradeRetcode
TRADE_RETCODE_LIMIT_VOLUME: TradeRetcode
TRADE_RETCODE_INVALID_ORDER: TradeRetcode
TRADE_RETCODE_POSITION_CLOSED: TradeRetcode
TRADE_RETCODE_INVALID_CLOSE_VOLUME: TradeRetcode
TRADE_RETCODE_CLOSE_ORDER_EXIST: TradeRetcode
TRADE_RETCODE_LIMIT_POSITIONS: TradeRetcode
TRADE_RETCODE_REJECT_CANCEL: TradeRetcode
TRADE_RETCODE_LONG_ONLY: TradeRetcode
TRADE_RETCODE_SHORT_ONLY: TradeRetcode
TRADE_RETCODE_CLOSE_ONLY: TradeRetcode
TRADE_RETCODE_FIFO_CLOSE: TradeRetcode
POSITION_TYPE_BUY: PositionType
POSITION_TYPE_SELL: PositionType
POSITION_REASON_CLIENT: PositionReason
POSITION_REASON_MOBILE: PositionReason
POSITION_REASON_WEB: PositionReason
POSITION_REASON_EXPERT: PositionReason
ORDER_REASON_CLIENT: OrderReason
ORDER_REASON_MOBILE: OrderReason
ORDER_REASON_WEB: OrderReason
ORDER_REASON_EXPERT: OrderReason
ORDER_REASON_SL: OrderReason
ORDER_REASON_TP: OrderReason
ORDER_REASON_SO: OrderReason
DEAL_REASON_CLIENT: DealReason
DEAL_REASON_MOBILE: DealReason
DEAL_REASON_WEB: DealReason
DEAL_REASON_EXPERT: DealReason
DEAL_REASON_SL: DealReason
DEAL_REASON_TP: DealReason
DEAL_REASON_SO: DealReason
DEAL_REASON_ROLLOVER: DealReason
DEAL_REASON_VMARGIN: DealReason
DEAL_REASON_SPLIT: DealReason
SYMBOL_CALC_MODE_FOREX: SymbolCalcMode
SYMBOL_CALC_MODE_FUTURES: SymbolCalcMode
SYMBOL_CALC_MODE_CFD: SymbolCalcMode
SYMBOL_CALC_MODE_CFDINDEX: SymbolCalcMode
SYMBOL_CALC_MODE_CFDLEVERAGE: SymbolCalcMode
SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE: SymbolCalcMode
SYMBOL_CALC_MODE_EXCH_STOCKS: SymbolCalcMode
SYMBOL_CALC_MODE_EXCH_FUTURES: SymbolCalcMode
SYMBOL_CALC_MODE_EXCH_OPTIONS: SymbolCalcMode
SYMBOL_CALC_MODE_EXCH_OPTIONS_MARGIN: SymbolCalcMode
SYMBOL_CALC_MODE_EXCH_BONDS: SymbolCalcMode
SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX: SymbolCalcMode
SYMBOL_CALC_MODE_EXCH_BONDS_MOEX: SymbolCalcMode
SYMBOL_CALC_MODE_SERV_COLLATERAL: SymbolCalcMode
SYMBOL_TRADE_MODE_DISABLED: SymbolTradeMode
SYMBOL_TRADE_MODE_LONGONLY: SymbolTradeMode
SYMBOL_TRADE_MODE_SHORTONLY: SymbolTradeMode
SYMBOL_TRADE_MODE_CLOSEONLY: SymbolTradeMode
SYMBOL_TRADE_MODE_FULL: SymbolTradeMode
SYMBOL_TRADE_EXECUTION_REQUEST: SymbolTradeExecution
SYMBOL_TRADE_EXECUTION_INSTANT: SymbolTradeExecution
SYMBOL_TRADE_EXECUTION_MARKET: SymbolTradeExecution
SYMBOL_TRADE_EXECUTION_EXCHANGE: SymbolTradeExecution
SYMBOL_SWAP_MODE_DISABLED: SymbolSwapMode
SYMBOL_SWAP_MODE_POINTS: SymbolSwapMode
SYMBOL_SWAP_MODE_CURRENCY_SYMBOL: SymbolSwapMode
SYMBOL_SWAP_MODE_CURRENCY_MARGIN: SymbolSwapMode
SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT: SymbolSwapMode
SYMBOL_SWAP_MODE_INTEREST_CURRENT: SymbolSwapMode
SYMBOL_SWAP_MODE_INTEREST_OPEN: SymbolSwapMode
SYMBOL_SWAP_MODE_REOPEN_CURRENT: SymbolSwapMode
SYMBOL_SWAP_MODE_REOPEN_BID: SymbolSwapMode
SYMBOL_CHART_MODE_BID: SymbolChartMode
SYMBOL_CHART_MODE_LAST: SymbolChartMode
SYMBOL_ORDERS_GTC: SymbolOrderGtcMode
SYMBOL_ORDERS_DAILY: SymbolOrderGtcMode
SYMBOL_ORDERS_DAILY_NO_STOPS: SymbolOrderGtcMode
SYMBOL_OPTION_RIGHT_CALL: SymbolOptionRight
SYMBOL_OPTION_RIGHT_PUT: SymbolOptionRight
SYMBOL_OPTION_MODE_EUROPEAN: SymbolOptionMode
SYMBOL_OPTION_MODE_AMERICAN: SymbolOptionMode
DAY_OF_WEEK_SUNDAY: DayOfWeek
DAY_OF_WEEK_MONDAY: DayOfWeek
DAY_OF_WEEK_TUESDAY: DayOfWeek
DAY_OF_WEEK_WEDNESDAY: DayOfWeek
DAY_OF_WEEK_THURSDAY: DayOfWeek
DAY_OF_WEEK_FRIDAY: DayOfWeek
DAY_OF_WEEK_SATURDAY: DayOfWeek
ACCOUNT_TRADE_MODE_DEMO: AccountTradeMode
ACCOUNT_TRADE_MODE_CONTEST: AccountTradeMode
ACCOUNT_TRADE_MODE_REAL: AccountTradeMode
ACCOUNT_STOPOUT_MODE_PERCENT: AccountStopoutMode
ACCOUNT_STOPOUT_MODE_MONEY: AccountStopoutMode
ACCOUNT_MARGIN_MODE_RETAIL_NETTING: AccountMarginMode
ACCOUNT_MARGIN_MODE_EXCHANGE: AccountMarginMode
ACCOUNT_MARGIN_MODE_RETAIL_HEDGING: AccountMarginMode
RES_E_UNSPECIFIED: ResError
RES_S_OK: ResError
RES_E_FAIL: ResError
RES_E_INVALID_PARAMS: ResError
RES_E_NO_MEMORY: ResError
RES_E_NOT_FOUND: ResError
RES_E_INVALID_VERSION: ResError
RES_E_AUTH_FAILED: ResError
RES_E_UNSUPPORTED: ResError
RES_E_AUTO_TRADING_DISABLED: ResError
RES_E_INTERNAL_FAIL: ResError
RES_E_INTERNAL_FAIL_SEND: ResError
RES_E_INTERNAL_FAIL_RECEIVE: ResError
RES_E_INTERNAL_FAIL_INIT: ResError
RES_E_INTERNAL_FAIL_CONNECT: ResError
RES_E_INTERNAL_FAIL_TIMEOUT: ResError
