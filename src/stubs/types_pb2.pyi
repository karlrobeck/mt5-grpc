import enums_pb2 as _enums_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccountInfo(_message.Message):
    __slots__ = ("login", "leverage", "trade_allowed", "balance", "credit", "profit", "equity", "margin", "margin_free", "margin_level", "margin_so_call", "margin_so_so", "name", "server", "currency", "company", "mt5")
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    LEVERAGE_FIELD_NUMBER: _ClassVar[int]
    TRADE_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    CREDIT_FIELD_NUMBER: _ClassVar[int]
    PROFIT_FIELD_NUMBER: _ClassVar[int]
    EQUITY_FIELD_NUMBER: _ClassVar[int]
    MARGIN_FIELD_NUMBER: _ClassVar[int]
    MARGIN_FREE_FIELD_NUMBER: _ClassVar[int]
    MARGIN_LEVEL_FIELD_NUMBER: _ClassVar[int]
    MARGIN_SO_CALL_FIELD_NUMBER: _ClassVar[int]
    MARGIN_SO_SO_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    login: int
    leverage: int
    trade_allowed: bool
    balance: float
    credit: float
    profit: float
    equity: float
    margin: float
    margin_free: float
    margin_level: float
    margin_so_call: float
    margin_so_so: float
    name: str
    server: str
    currency: str
    company: str
    mt5: Mt5AccountInfo
    def __init__(self, login: _Optional[int] = ..., leverage: _Optional[int] = ..., trade_allowed: _Optional[bool] = ..., balance: _Optional[float] = ..., credit: _Optional[float] = ..., profit: _Optional[float] = ..., equity: _Optional[float] = ..., margin: _Optional[float] = ..., margin_free: _Optional[float] = ..., margin_level: _Optional[float] = ..., margin_so_call: _Optional[float] = ..., margin_so_so: _Optional[float] = ..., name: _Optional[str] = ..., server: _Optional[str] = ..., currency: _Optional[str] = ..., company: _Optional[str] = ..., mt5: _Optional[_Union[Mt5AccountInfo, _Mapping]] = ...) -> None: ...

class Mt5AccountInfo(_message.Message):
    __slots__ = ("trade_mode", "limit_orders", "margin_so_mode", "trade_expert", "margin_mode", "currency_digits", "fifo_close", "margin_initial", "margin_maintenance", "assets", "liabilities", "commission_blocked")
    TRADE_MODE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_ORDERS_FIELD_NUMBER: _ClassVar[int]
    MARGIN_SO_MODE_FIELD_NUMBER: _ClassVar[int]
    TRADE_EXPERT_FIELD_NUMBER: _ClassVar[int]
    MARGIN_MODE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_DIGITS_FIELD_NUMBER: _ClassVar[int]
    FIFO_CLOSE_FIELD_NUMBER: _ClassVar[int]
    MARGIN_INITIAL_FIELD_NUMBER: _ClassVar[int]
    MARGIN_MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    ASSETS_FIELD_NUMBER: _ClassVar[int]
    LIABILITIES_FIELD_NUMBER: _ClassVar[int]
    COMMISSION_BLOCKED_FIELD_NUMBER: _ClassVar[int]
    trade_mode: _enums_pb2.AccountTradeMode
    limit_orders: int
    margin_so_mode: _enums_pb2.AccountStopoutMode
    trade_expert: bool
    margin_mode: _enums_pb2.AccountMarginMode
    currency_digits: int
    fifo_close: bool
    margin_initial: float
    margin_maintenance: float
    assets: float
    liabilities: float
    commission_blocked: float
    def __init__(self, trade_mode: _Optional[_Union[_enums_pb2.AccountTradeMode, str]] = ..., limit_orders: _Optional[int] = ..., margin_so_mode: _Optional[_Union[_enums_pb2.AccountStopoutMode, str]] = ..., trade_expert: _Optional[bool] = ..., margin_mode: _Optional[_Union[_enums_pb2.AccountMarginMode, str]] = ..., currency_digits: _Optional[int] = ..., fifo_close: _Optional[bool] = ..., margin_initial: _Optional[float] = ..., margin_maintenance: _Optional[float] = ..., assets: _Optional[float] = ..., liabilities: _Optional[float] = ..., commission_blocked: _Optional[float] = ...) -> None: ...

class TerminalInfo(_message.Message):
    __slots__ = ("connected", "trade_allowed", "ping_last", "company", "name", "mt5")
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    TRADE_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    PING_LAST_FIELD_NUMBER: _ClassVar[int]
    COMPANY_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    connected: bool
    trade_allowed: bool
    ping_last: int
    company: str
    name: str
    mt5: Mt5TerminalInfo
    def __init__(self, connected: _Optional[bool] = ..., trade_allowed: _Optional[bool] = ..., ping_last: _Optional[int] = ..., company: _Optional[str] = ..., name: _Optional[str] = ..., mt5: _Optional[_Union[Mt5TerminalInfo, _Mapping]] = ...) -> None: ...

class Mt5TerminalInfo(_message.Message):
    __slots__ = ("community_account", "community_connection", "dlls_allowed", "tradeapi_disabled", "email_enabled", "ftp_enabled", "notifications_enabled", "mqid", "build", "maxbars", "codepage", "community_balance", "retransmission", "language", "path", "data_path", "commondata_path")
    COMMUNITY_ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    DLLS_ALLOWED_FIELD_NUMBER: _ClassVar[int]
    TRADEAPI_DISABLED_FIELD_NUMBER: _ClassVar[int]
    EMAIL_ENABLED_FIELD_NUMBER: _ClassVar[int]
    FTP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATIONS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    MQID_FIELD_NUMBER: _ClassVar[int]
    BUILD_FIELD_NUMBER: _ClassVar[int]
    MAXBARS_FIELD_NUMBER: _ClassVar[int]
    CODEPAGE_FIELD_NUMBER: _ClassVar[int]
    COMMUNITY_BALANCE_FIELD_NUMBER: _ClassVar[int]
    RETRANSMISSION_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DATA_PATH_FIELD_NUMBER: _ClassVar[int]
    COMMONDATA_PATH_FIELD_NUMBER: _ClassVar[int]
    community_account: bool
    community_connection: bool
    dlls_allowed: bool
    tradeapi_disabled: bool
    email_enabled: bool
    ftp_enabled: bool
    notifications_enabled: bool
    mqid: bool
    build: int
    maxbars: int
    codepage: int
    community_balance: float
    retransmission: float
    language: str
    path: str
    data_path: str
    commondata_path: str
    def __init__(self, community_account: _Optional[bool] = ..., community_connection: _Optional[bool] = ..., dlls_allowed: _Optional[bool] = ..., tradeapi_disabled: _Optional[bool] = ..., email_enabled: _Optional[bool] = ..., ftp_enabled: _Optional[bool] = ..., notifications_enabled: _Optional[bool] = ..., mqid: _Optional[bool] = ..., build: _Optional[int] = ..., maxbars: _Optional[int] = ..., codepage: _Optional[int] = ..., community_balance: _Optional[float] = ..., retransmission: _Optional[float] = ..., language: _Optional[str] = ..., path: _Optional[str] = ..., data_path: _Optional[str] = ..., commondata_path: _Optional[str] = ...) -> None: ...

class SymbolInfo(_message.Message):
    __slots__ = ("digits", "spread", "spread_float", "bid", "ask", "last", "point", "trade_tick_size", "trade_contract_size", "volume_min", "volume_max", "volume_step", "swap_long", "swap_short", "margin_initial", "margin_maintenance", "margin_hedged", "price_change", "price_volatility", "start_time", "expiration_time", "trade_stops_level", "trade_freeze_level", "bidhigh", "bidlow", "askhigh", "asklow", "lasthigh", "lastlow", "volume", "volume_real", "volumehigh_real", "volumelow_real", "currency_base", "currency_profit", "currency_margin", "description", "exchange", "isin", "name", "trade_tick_value", "trade_tick_value_profit", "trade_tick_value_loss", "price_theoretical", "price_greeks_delta", "price_greeks_theta", "price_greeks_gamma", "price_greeks_vega", "price_greeks_rho", "price_greeks_omega", "price_sensitivity", "basis", "trade_accrued_interest", "trade_face_value", "trade_liquidity_rate", "mt5")
    DIGITS_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FLOAT_FIELD_NUMBER: _ClassVar[int]
    BID_FIELD_NUMBER: _ClassVar[int]
    ASK_FIELD_NUMBER: _ClassVar[int]
    LAST_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    TRADE_TICK_SIZE_FIELD_NUMBER: _ClassVar[int]
    TRADE_CONTRACT_SIZE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_MIN_FIELD_NUMBER: _ClassVar[int]
    VOLUME_MAX_FIELD_NUMBER: _ClassVar[int]
    VOLUME_STEP_FIELD_NUMBER: _ClassVar[int]
    SWAP_LONG_FIELD_NUMBER: _ClassVar[int]
    SWAP_SHORT_FIELD_NUMBER: _ClassVar[int]
    MARGIN_INITIAL_FIELD_NUMBER: _ClassVar[int]
    MARGIN_MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    MARGIN_HEDGED_FIELD_NUMBER: _ClassVar[int]
    PRICE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    PRICE_VOLATILITY_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    TRADE_STOPS_LEVEL_FIELD_NUMBER: _ClassVar[int]
    TRADE_FREEZE_LEVEL_FIELD_NUMBER: _ClassVar[int]
    BIDHIGH_FIELD_NUMBER: _ClassVar[int]
    BIDLOW_FIELD_NUMBER: _ClassVar[int]
    ASKHIGH_FIELD_NUMBER: _ClassVar[int]
    ASKLOW_FIELD_NUMBER: _ClassVar[int]
    LASTHIGH_FIELD_NUMBER: _ClassVar[int]
    LASTLOW_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_REAL_FIELD_NUMBER: _ClassVar[int]
    VOLUMEHIGH_REAL_FIELD_NUMBER: _ClassVar[int]
    VOLUMELOW_REAL_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_BASE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_PROFIT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_MARGIN_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_FIELD_NUMBER: _ClassVar[int]
    ISIN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TRADE_TICK_VALUE_FIELD_NUMBER: _ClassVar[int]
    TRADE_TICK_VALUE_PROFIT_FIELD_NUMBER: _ClassVar[int]
    TRADE_TICK_VALUE_LOSS_FIELD_NUMBER: _ClassVar[int]
    PRICE_THEORETICAL_FIELD_NUMBER: _ClassVar[int]
    PRICE_GREEKS_DELTA_FIELD_NUMBER: _ClassVar[int]
    PRICE_GREEKS_THETA_FIELD_NUMBER: _ClassVar[int]
    PRICE_GREEKS_GAMMA_FIELD_NUMBER: _ClassVar[int]
    PRICE_GREEKS_VEGA_FIELD_NUMBER: _ClassVar[int]
    PRICE_GREEKS_RHO_FIELD_NUMBER: _ClassVar[int]
    PRICE_GREEKS_OMEGA_FIELD_NUMBER: _ClassVar[int]
    PRICE_SENSITIVITY_FIELD_NUMBER: _ClassVar[int]
    BASIS_FIELD_NUMBER: _ClassVar[int]
    TRADE_ACCRUED_INTEREST_FIELD_NUMBER: _ClassVar[int]
    TRADE_FACE_VALUE_FIELD_NUMBER: _ClassVar[int]
    TRADE_LIQUIDITY_RATE_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    digits: int
    spread: int
    spread_float: bool
    bid: float
    ask: float
    last: float
    point: float
    trade_tick_size: float
    trade_contract_size: float
    volume_min: float
    volume_max: float
    volume_step: float
    swap_long: float
    swap_short: float
    margin_initial: float
    margin_maintenance: float
    margin_hedged: float
    price_change: float
    price_volatility: float
    start_time: int
    expiration_time: int
    trade_stops_level: int
    trade_freeze_level: int
    bidhigh: float
    bidlow: float
    askhigh: float
    asklow: float
    lasthigh: float
    lastlow: float
    volume: float
    volume_real: float
    volumehigh_real: float
    volumelow_real: float
    currency_base: str
    currency_profit: str
    currency_margin: str
    description: str
    exchange: str
    isin: str
    name: str
    trade_tick_value: float
    trade_tick_value_profit: float
    trade_tick_value_loss: float
    price_theoretical: float
    price_greeks_delta: float
    price_greeks_theta: float
    price_greeks_gamma: float
    price_greeks_vega: float
    price_greeks_rho: float
    price_greeks_omega: float
    price_sensitivity: float
    basis: str
    trade_accrued_interest: float
    trade_face_value: float
    trade_liquidity_rate: float
    mt5: Mt5SymbolInfo
    def __init__(self, digits: _Optional[int] = ..., spread: _Optional[int] = ..., spread_float: _Optional[bool] = ..., bid: _Optional[float] = ..., ask: _Optional[float] = ..., last: _Optional[float] = ..., point: _Optional[float] = ..., trade_tick_size: _Optional[float] = ..., trade_contract_size: _Optional[float] = ..., volume_min: _Optional[float] = ..., volume_max: _Optional[float] = ..., volume_step: _Optional[float] = ..., swap_long: _Optional[float] = ..., swap_short: _Optional[float] = ..., margin_initial: _Optional[float] = ..., margin_maintenance: _Optional[float] = ..., margin_hedged: _Optional[float] = ..., price_change: _Optional[float] = ..., price_volatility: _Optional[float] = ..., start_time: _Optional[int] = ..., expiration_time: _Optional[int] = ..., trade_stops_level: _Optional[int] = ..., trade_freeze_level: _Optional[int] = ..., bidhigh: _Optional[float] = ..., bidlow: _Optional[float] = ..., askhigh: _Optional[float] = ..., asklow: _Optional[float] = ..., lasthigh: _Optional[float] = ..., lastlow: _Optional[float] = ..., volume: _Optional[float] = ..., volume_real: _Optional[float] = ..., volumehigh_real: _Optional[float] = ..., volumelow_real: _Optional[float] = ..., currency_base: _Optional[str] = ..., currency_profit: _Optional[str] = ..., currency_margin: _Optional[str] = ..., description: _Optional[str] = ..., exchange: _Optional[str] = ..., isin: _Optional[str] = ..., name: _Optional[str] = ..., trade_tick_value: _Optional[float] = ..., trade_tick_value_profit: _Optional[float] = ..., trade_tick_value_loss: _Optional[float] = ..., price_theoretical: _Optional[float] = ..., price_greeks_delta: _Optional[float] = ..., price_greeks_theta: _Optional[float] = ..., price_greeks_gamma: _Optional[float] = ..., price_greeks_vega: _Optional[float] = ..., price_greeks_rho: _Optional[float] = ..., price_greeks_omega: _Optional[float] = ..., price_sensitivity: _Optional[float] = ..., basis: _Optional[str] = ..., trade_accrued_interest: _Optional[float] = ..., trade_face_value: _Optional[float] = ..., trade_liquidity_rate: _Optional[float] = ..., mt5: _Optional[_Union[Mt5SymbolInfo, _Mapping]] = ...) -> None: ...

class Mt5SymbolInfo(_message.Message):
    __slots__ = ("custom", "chart_mode", "select", "visible", "trade_calc_mode", "trade_mode", "trade_exemode", "swap_mode", "swap_rollover3days", "margin_hedged_use_leg", "expiration_mode", "filling_mode", "order_mode", "order_gtc_mode", "session_deals", "session_buy_orders", "session_sell_orders", "ticks_bookdepth", "volumehigh", "volumelow", "time", "volume_limit", "session_volume", "session_turnover", "session_interest", "session_buy_orders_volume", "session_sell_orders_volume", "session_open", "session_close", "session_aw", "session_price_settlement", "session_price_limit_min", "session_price_limit_max", "option_mode", "option_right", "option_strike", "category", "bank", "formula", "page", "path")
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    CHART_MODE_FIELD_NUMBER: _ClassVar[int]
    SELECT_FIELD_NUMBER: _ClassVar[int]
    VISIBLE_FIELD_NUMBER: _ClassVar[int]
    TRADE_CALC_MODE_FIELD_NUMBER: _ClassVar[int]
    TRADE_MODE_FIELD_NUMBER: _ClassVar[int]
    TRADE_EXEMODE_FIELD_NUMBER: _ClassVar[int]
    SWAP_MODE_FIELD_NUMBER: _ClassVar[int]
    SWAP_ROLLOVER3DAYS_FIELD_NUMBER: _ClassVar[int]
    MARGIN_HEDGED_USE_LEG_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_MODE_FIELD_NUMBER: _ClassVar[int]
    FILLING_MODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_MODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_GTC_MODE_FIELD_NUMBER: _ClassVar[int]
    SESSION_DEALS_FIELD_NUMBER: _ClassVar[int]
    SESSION_BUY_ORDERS_FIELD_NUMBER: _ClassVar[int]
    SESSION_SELL_ORDERS_FIELD_NUMBER: _ClassVar[int]
    TICKS_BOOKDEPTH_FIELD_NUMBER: _ClassVar[int]
    VOLUMEHIGH_FIELD_NUMBER: _ClassVar[int]
    VOLUMELOW_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SESSION_VOLUME_FIELD_NUMBER: _ClassVar[int]
    SESSION_TURNOVER_FIELD_NUMBER: _ClassVar[int]
    SESSION_INTEREST_FIELD_NUMBER: _ClassVar[int]
    SESSION_BUY_ORDERS_VOLUME_FIELD_NUMBER: _ClassVar[int]
    SESSION_SELL_ORDERS_VOLUME_FIELD_NUMBER: _ClassVar[int]
    SESSION_OPEN_FIELD_NUMBER: _ClassVar[int]
    SESSION_CLOSE_FIELD_NUMBER: _ClassVar[int]
    SESSION_AW_FIELD_NUMBER: _ClassVar[int]
    SESSION_PRICE_SETTLEMENT_FIELD_NUMBER: _ClassVar[int]
    SESSION_PRICE_LIMIT_MIN_FIELD_NUMBER: _ClassVar[int]
    SESSION_PRICE_LIMIT_MAX_FIELD_NUMBER: _ClassVar[int]
    OPTION_MODE_FIELD_NUMBER: _ClassVar[int]
    OPTION_RIGHT_FIELD_NUMBER: _ClassVar[int]
    OPTION_STRIKE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    BANK_FIELD_NUMBER: _ClassVar[int]
    FORMULA_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    custom: bool
    chart_mode: _enums_pb2.SymbolChartMode
    select: bool
    visible: bool
    trade_calc_mode: _enums_pb2.SymbolCalcMode
    trade_mode: _enums_pb2.SymbolTradeMode
    trade_exemode: _enums_pb2.SymbolTradeExecution
    swap_mode: _enums_pb2.SymbolSwapMode
    swap_rollover3days: _enums_pb2.DayOfWeek
    margin_hedged_use_leg: bool
    expiration_mode: int
    filling_mode: int
    order_mode: int
    order_gtc_mode: _enums_pb2.SymbolOrderGtcMode
    session_deals: int
    session_buy_orders: int
    session_sell_orders: int
    ticks_bookdepth: int
    volumehigh: int
    volumelow: int
    time: int
    volume_limit: float
    session_volume: float
    session_turnover: float
    session_interest: float
    session_buy_orders_volume: float
    session_sell_orders_volume: float
    session_open: float
    session_close: float
    session_aw: float
    session_price_settlement: float
    session_price_limit_min: float
    session_price_limit_max: float
    option_mode: _enums_pb2.SymbolOptionMode
    option_right: _enums_pb2.SymbolOptionRight
    option_strike: float
    category: str
    bank: str
    formula: str
    page: str
    path: str
    def __init__(self, custom: _Optional[bool] = ..., chart_mode: _Optional[_Union[_enums_pb2.SymbolChartMode, str]] = ..., select: _Optional[bool] = ..., visible: _Optional[bool] = ..., trade_calc_mode: _Optional[_Union[_enums_pb2.SymbolCalcMode, str]] = ..., trade_mode: _Optional[_Union[_enums_pb2.SymbolTradeMode, str]] = ..., trade_exemode: _Optional[_Union[_enums_pb2.SymbolTradeExecution, str]] = ..., swap_mode: _Optional[_Union[_enums_pb2.SymbolSwapMode, str]] = ..., swap_rollover3days: _Optional[_Union[_enums_pb2.DayOfWeek, str]] = ..., margin_hedged_use_leg: _Optional[bool] = ..., expiration_mode: _Optional[int] = ..., filling_mode: _Optional[int] = ..., order_mode: _Optional[int] = ..., order_gtc_mode: _Optional[_Union[_enums_pb2.SymbolOrderGtcMode, str]] = ..., session_deals: _Optional[int] = ..., session_buy_orders: _Optional[int] = ..., session_sell_orders: _Optional[int] = ..., ticks_bookdepth: _Optional[int] = ..., volumehigh: _Optional[int] = ..., volumelow: _Optional[int] = ..., time: _Optional[int] = ..., volume_limit: _Optional[float] = ..., session_volume: _Optional[float] = ..., session_turnover: _Optional[float] = ..., session_interest: _Optional[float] = ..., session_buy_orders_volume: _Optional[float] = ..., session_sell_orders_volume: _Optional[float] = ..., session_open: _Optional[float] = ..., session_close: _Optional[float] = ..., session_aw: _Optional[float] = ..., session_price_settlement: _Optional[float] = ..., session_price_limit_min: _Optional[float] = ..., session_price_limit_max: _Optional[float] = ..., option_mode: _Optional[_Union[_enums_pb2.SymbolOptionMode, str]] = ..., option_right: _Optional[_Union[_enums_pb2.SymbolOptionRight, str]] = ..., option_strike: _Optional[float] = ..., category: _Optional[str] = ..., bank: _Optional[str] = ..., formula: _Optional[str] = ..., page: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class Tick(_message.Message):
    __slots__ = ("time", "bid", "ask", "last", "volume", "time_msc", "volume_real", "mt5")
    TIME_FIELD_NUMBER: _ClassVar[int]
    BID_FIELD_NUMBER: _ClassVar[int]
    ASK_FIELD_NUMBER: _ClassVar[int]
    LAST_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    TIME_MSC_FIELD_NUMBER: _ClassVar[int]
    VOLUME_REAL_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    time: int
    bid: float
    ask: float
    last: float
    volume: float
    time_msc: int
    volume_real: float
    mt5: Mt5Tick
    def __init__(self, time: _Optional[int] = ..., bid: _Optional[float] = ..., ask: _Optional[float] = ..., last: _Optional[float] = ..., volume: _Optional[float] = ..., time_msc: _Optional[int] = ..., volume_real: _Optional[float] = ..., mt5: _Optional[_Union[Mt5Tick, _Mapping]] = ...) -> None: ...

class Mt5Tick(_message.Message):
    __slots__ = ("flags",)
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: int
    def __init__(self, flags: _Optional[int] = ...) -> None: ...

class Rate(_message.Message):
    __slots__ = ("time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume")
    TIME_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    TICK_VOLUME_FIELD_NUMBER: _ClassVar[int]
    SPREAD_FIELD_NUMBER: _ClassVar[int]
    REAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    time: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: int
    spread: int
    real_volume: int
    def __init__(self, time: _Optional[int] = ..., open: _Optional[float] = ..., high: _Optional[float] = ..., low: _Optional[float] = ..., close: _Optional[float] = ..., tick_volume: _Optional[int] = ..., spread: _Optional[int] = ..., real_volume: _Optional[int] = ...) -> None: ...

class BookInfo(_message.Message):
    __slots__ = ("price", "volume", "volume_dbl", "mt5")
    PRICE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_DBL_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    price: float
    volume: float
    volume_dbl: float
    mt5: Mt5BookInfo
    def __init__(self, price: _Optional[float] = ..., volume: _Optional[float] = ..., volume_dbl: _Optional[float] = ..., mt5: _Optional[_Union[Mt5BookInfo, _Mapping]] = ...) -> None: ...

class Mt5BookInfo(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: _enums_pb2.BookType
    def __init__(self, type: _Optional[_Union[_enums_pb2.BookType, str]] = ...) -> None: ...

class TradeOrder(_message.Message):
    __slots__ = ("ticket", "time_setup", "time_setup_msc", "time_done", "time_done_msc", "time_expiration", "volume_current", "volume_initial", "price_open", "sl", "tp", "price_current", "price_stoplimit", "symbol", "comment", "external_id", "position_id", "mt5")
    TICKET_FIELD_NUMBER: _ClassVar[int]
    TIME_SETUP_FIELD_NUMBER: _ClassVar[int]
    TIME_SETUP_MSC_FIELD_NUMBER: _ClassVar[int]
    TIME_DONE_FIELD_NUMBER: _ClassVar[int]
    TIME_DONE_MSC_FIELD_NUMBER: _ClassVar[int]
    TIME_EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    VOLUME_CURRENT_FIELD_NUMBER: _ClassVar[int]
    VOLUME_INITIAL_FIELD_NUMBER: _ClassVar[int]
    PRICE_OPEN_FIELD_NUMBER: _ClassVar[int]
    SL_FIELD_NUMBER: _ClassVar[int]
    TP_FIELD_NUMBER: _ClassVar[int]
    PRICE_CURRENT_FIELD_NUMBER: _ClassVar[int]
    PRICE_STOPLIMIT_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    ticket: int
    time_setup: int
    time_setup_msc: int
    time_done: int
    time_done_msc: int
    time_expiration: int
    volume_current: float
    volume_initial: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    price_stoplimit: float
    symbol: str
    comment: str
    external_id: str
    position_id: int
    mt5: Mt5TradeOrder
    def __init__(self, ticket: _Optional[int] = ..., time_setup: _Optional[int] = ..., time_setup_msc: _Optional[int] = ..., time_done: _Optional[int] = ..., time_done_msc: _Optional[int] = ..., time_expiration: _Optional[int] = ..., volume_current: _Optional[float] = ..., volume_initial: _Optional[float] = ..., price_open: _Optional[float] = ..., sl: _Optional[float] = ..., tp: _Optional[float] = ..., price_current: _Optional[float] = ..., price_stoplimit: _Optional[float] = ..., symbol: _Optional[str] = ..., comment: _Optional[str] = ..., external_id: _Optional[str] = ..., position_id: _Optional[int] = ..., mt5: _Optional[_Union[Mt5TradeOrder, _Mapping]] = ...) -> None: ...

class Mt5TradeOrder(_message.Message):
    __slots__ = ("type", "type_time", "type_filling", "state", "magic", "position_by_id", "reason")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_TIME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FILLING_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    POSITION_BY_ID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    type: _enums_pb2.OrderType
    type_time: _enums_pb2.OrderTypeTime
    type_filling: _enums_pb2.OrderTypeFilling
    state: _enums_pb2.OrderState
    magic: int
    position_by_id: int
    reason: _enums_pb2.OrderReason
    def __init__(self, type: _Optional[_Union[_enums_pb2.OrderType, str]] = ..., type_time: _Optional[_Union[_enums_pb2.OrderTypeTime, str]] = ..., type_filling: _Optional[_Union[_enums_pb2.OrderTypeFilling, str]] = ..., state: _Optional[_Union[_enums_pb2.OrderState, str]] = ..., magic: _Optional[int] = ..., position_by_id: _Optional[int] = ..., reason: _Optional[_Union[_enums_pb2.OrderReason, str]] = ...) -> None: ...

class TradePosition(_message.Message):
    __slots__ = ("ticket", "time", "time_msc", "time_update", "time_update_msc", "volume", "price_open", "sl", "tp", "price_current", "swap", "profit", "symbol", "comment", "external_id", "mt5")
    TICKET_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TIME_MSC_FIELD_NUMBER: _ClassVar[int]
    TIME_UPDATE_FIELD_NUMBER: _ClassVar[int]
    TIME_UPDATE_MSC_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    PRICE_OPEN_FIELD_NUMBER: _ClassVar[int]
    SL_FIELD_NUMBER: _ClassVar[int]
    TP_FIELD_NUMBER: _ClassVar[int]
    PRICE_CURRENT_FIELD_NUMBER: _ClassVar[int]
    SWAP_FIELD_NUMBER: _ClassVar[int]
    PROFIT_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    ticket: int
    time: int
    time_msc: int
    time_update: int
    time_update_msc: int
    volume: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    swap: float
    profit: float
    symbol: str
    comment: str
    external_id: str
    mt5: Mt5TradePosition
    def __init__(self, ticket: _Optional[int] = ..., time: _Optional[int] = ..., time_msc: _Optional[int] = ..., time_update: _Optional[int] = ..., time_update_msc: _Optional[int] = ..., volume: _Optional[float] = ..., price_open: _Optional[float] = ..., sl: _Optional[float] = ..., tp: _Optional[float] = ..., price_current: _Optional[float] = ..., swap: _Optional[float] = ..., profit: _Optional[float] = ..., symbol: _Optional[str] = ..., comment: _Optional[str] = ..., external_id: _Optional[str] = ..., mt5: _Optional[_Union[Mt5TradePosition, _Mapping]] = ...) -> None: ...

class Mt5TradePosition(_message.Message):
    __slots__ = ("type", "magic", "identifier", "reason")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    IDENTIFIER_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    type: _enums_pb2.PositionType
    magic: int
    identifier: int
    reason: _enums_pb2.PositionReason
    def __init__(self, type: _Optional[_Union[_enums_pb2.PositionType, str]] = ..., magic: _Optional[int] = ..., identifier: _Optional[int] = ..., reason: _Optional[_Union[_enums_pb2.PositionReason, str]] = ...) -> None: ...

class TradeDeal(_message.Message):
    __slots__ = ("ticket", "order", "time", "time_msc", "volume", "price", "commission", "swap", "profit", "fee", "symbol", "comment", "external_id", "position_id", "mt5")
    TICKET_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    TIME_MSC_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    COMMISSION_FIELD_NUMBER: _ClassVar[int]
    SWAP_FIELD_NUMBER: _ClassVar[int]
    PROFIT_FIELD_NUMBER: _ClassVar[int]
    FEE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_ID_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    ticket: int
    order: int
    time: int
    time_msc: int
    volume: float
    price: float
    commission: float
    swap: float
    profit: float
    fee: float
    symbol: str
    comment: str
    external_id: str
    position_id: int
    mt5: Mt5TradeDeal
    def __init__(self, ticket: _Optional[int] = ..., order: _Optional[int] = ..., time: _Optional[int] = ..., time_msc: _Optional[int] = ..., volume: _Optional[float] = ..., price: _Optional[float] = ..., commission: _Optional[float] = ..., swap: _Optional[float] = ..., profit: _Optional[float] = ..., fee: _Optional[float] = ..., symbol: _Optional[str] = ..., comment: _Optional[str] = ..., external_id: _Optional[str] = ..., position_id: _Optional[int] = ..., mt5: _Optional[_Union[Mt5TradeDeal, _Mapping]] = ...) -> None: ...

class Mt5TradeDeal(_message.Message):
    __slots__ = ("type", "entry", "magic", "reason")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    type: _enums_pb2.DealType
    entry: _enums_pb2.DealEntry
    magic: int
    reason: _enums_pb2.DealReason
    def __init__(self, type: _Optional[_Union[_enums_pb2.DealType, str]] = ..., entry: _Optional[_Union[_enums_pb2.DealEntry, str]] = ..., magic: _Optional[int] = ..., reason: _Optional[_Union[_enums_pb2.DealReason, str]] = ...) -> None: ...

class TradeRequest(_message.Message):
    __slots__ = ("symbol", "volume", "price", "stoplimit", "sl", "tp", "deviation", "expiration", "comment", "order", "position", "mt5")
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    STOPLIMIT_FIELD_NUMBER: _ClassVar[int]
    SL_FIELD_NUMBER: _ClassVar[int]
    TP_FIELD_NUMBER: _ClassVar[int]
    DEVIATION_FIELD_NUMBER: _ClassVar[int]
    EXPIRATION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    MT5_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    volume: float
    price: float
    stoplimit: float
    sl: float
    tp: float
    deviation: int
    expiration: int
    comment: str
    order: int
    position: int
    mt5: Mt5TradeRequest
    def __init__(self, symbol: _Optional[str] = ..., volume: _Optional[float] = ..., price: _Optional[float] = ..., stoplimit: _Optional[float] = ..., sl: _Optional[float] = ..., tp: _Optional[float] = ..., deviation: _Optional[int] = ..., expiration: _Optional[int] = ..., comment: _Optional[str] = ..., order: _Optional[int] = ..., position: _Optional[int] = ..., mt5: _Optional[_Union[Mt5TradeRequest, _Mapping]] = ...) -> None: ...

class Mt5TradeRequest(_message.Message):
    __slots__ = ("action", "magic", "type", "type_filling", "type_time", "position_by")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    MAGIC_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FILLING_FIELD_NUMBER: _ClassVar[int]
    TYPE_TIME_FIELD_NUMBER: _ClassVar[int]
    POSITION_BY_FIELD_NUMBER: _ClassVar[int]
    action: _enums_pb2.TradeRequestAction
    magic: int
    type: _enums_pb2.OrderType
    type_filling: _enums_pb2.OrderTypeFilling
    type_time: _enums_pb2.OrderTypeTime
    position_by: int
    def __init__(self, action: _Optional[_Union[_enums_pb2.TradeRequestAction, str]] = ..., magic: _Optional[int] = ..., type: _Optional[_Union[_enums_pb2.OrderType, str]] = ..., type_filling: _Optional[_Union[_enums_pb2.OrderTypeFilling, str]] = ..., type_time: _Optional[_Union[_enums_pb2.OrderTypeTime, str]] = ..., position_by: _Optional[int] = ...) -> None: ...

class TradeCheckResult(_message.Message):
    __slots__ = ("retcode", "balance", "equity", "profit", "margin", "margin_free", "margin_level", "comment", "request")
    RETCODE_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    EQUITY_FIELD_NUMBER: _ClassVar[int]
    PROFIT_FIELD_NUMBER: _ClassVar[int]
    MARGIN_FIELD_NUMBER: _ClassVar[int]
    MARGIN_FREE_FIELD_NUMBER: _ClassVar[int]
    MARGIN_LEVEL_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    retcode: int
    balance: float
    equity: float
    profit: float
    margin: float
    margin_free: float
    margin_level: float
    comment: str
    request: TradeRequest
    def __init__(self, retcode: _Optional[int] = ..., balance: _Optional[float] = ..., equity: _Optional[float] = ..., profit: _Optional[float] = ..., margin: _Optional[float] = ..., margin_free: _Optional[float] = ..., margin_level: _Optional[float] = ..., comment: _Optional[str] = ..., request: _Optional[_Union[TradeRequest, _Mapping]] = ...) -> None: ...

class TradeSendResult(_message.Message):
    __slots__ = ("retcode", "deal", "order", "volume", "price", "bid", "ask", "comment", "request_id", "retcode_external", "request")
    RETCODE_FIELD_NUMBER: _ClassVar[int]
    DEAL_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_FIELD_NUMBER: _ClassVar[int]
    ASK_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RETCODE_EXTERNAL_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    retcode: int
    deal: int
    order: int
    volume: float
    price: float
    bid: float
    ask: float
    comment: str
    request_id: int
    retcode_external: int
    request: TradeRequest
    def __init__(self, retcode: _Optional[int] = ..., deal: _Optional[int] = ..., order: _Optional[int] = ..., volume: _Optional[float] = ..., price: _Optional[float] = ..., bid: _Optional[float] = ..., ask: _Optional[float] = ..., comment: _Optional[str] = ..., request_id: _Optional[int] = ..., retcode_external: _Optional[int] = ..., request: _Optional[_Union[TradeRequest, _Mapping]] = ...) -> None: ...
