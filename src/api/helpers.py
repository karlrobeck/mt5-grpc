"""
Conversion utilities from MT5 namedtuples/records to Protobuf messages.

This module provides functions to convert MetaTrader5 Python API return values
(namedtuples and NumPy structured array records) to their corresponding Protobuf
message representations.

Each conversion function handles:
- Field-by-field mapping from MT5 object/record to protobuf message
- Safe dictionary-style or attribute-based field access
- Nested messages (e.g., Mt5AccountInfo inside AccountInfo)
- None/missing values (proto3 default values)
"""

from typing import Optional, Any
from src.stubs import types_pb2


def get_field(obj: Any, name: str) -> Any:
    """
    Safely get field from MT5 result object. Supports dictionary-style access 
    (required for NumPy structured array records) and standard attribute access.
    Dictionary-style access is checked first to avoid collisions with built-in
    NumPy attributes (e.g. '.flags').
    """
    try:
        return obj[name]
    except (KeyError, TypeError, IndexError):
        pass
    try:
        return getattr(obj, name)
    except AttributeError:
        return None


def convert_account_info(mt5_result: Any) -> types_pb2.AccountInfo:
    """
    Convert MT5 AccountInfo to Protobuf AccountInfo message.
    """
    msg = types_pb2.AccountInfo()

    # Generic fields
    val = get_field(mt5_result, "login")
    if val is not None:
        msg.login = int(val)
    val = get_field(mt5_result, "leverage")
    if val is not None:
        msg.leverage = int(val)
    val = get_field(mt5_result, "trade_allowed")
    if val is not None:
        msg.trade_allowed = bool(val)
    val = get_field(mt5_result, "balance")
    if val is not None:
        msg.balance = float(val)
    val = get_field(mt5_result, "credit")
    if val is not None:
        msg.credit = float(val)
    val = get_field(mt5_result, "profit")
    if val is not None:
        msg.profit = float(val)
    val = get_field(mt5_result, "equity")
    if val is not None:
        msg.equity = float(val)
    val = get_field(mt5_result, "margin")
    if val is not None:
        msg.margin = float(val)
    val = get_field(mt5_result, "margin_free")
    if val is not None:
        msg.margin_free = float(val)
    val = get_field(mt5_result, "margin_level")
    if val is not None:
        msg.margin_level = float(val)
    val = get_field(mt5_result, "margin_so_call")
    if val is not None:
        msg.margin_so_call = float(val)
    val = get_field(mt5_result, "margin_so_so")
    if val is not None:
        msg.margin_so_so = float(val)
    val = get_field(mt5_result, "name")
    if val is not None:
        msg.name = str(val)
    val = get_field(mt5_result, "server")
    if val is not None:
        msg.server = str(val)
    val = get_field(mt5_result, "currency")
    if val is not None:
        msg.currency = str(val)
    val = get_field(mt5_result, "company")
    if val is not None:
        msg.company = str(val)

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5AccountInfo()
    val = get_field(mt5_result, "trade_mode")
    if val is not None:
        mt5_msg.trade_mode = int(val)
    val = get_field(mt5_result, "limit_orders")
    if val is not None:
        mt5_msg.limit_orders = int(val)
    val = get_field(mt5_result, "margin_so_mode")
    if val is not None:
        mt5_msg.margin_so_mode = int(val)
    val = get_field(mt5_result, "trade_expert")
    if val is not None:
        mt5_msg.trade_expert = bool(val)
    val = get_field(mt5_result, "margin_mode")
    if val is not None:
        mt5_msg.margin_mode = int(val)
    val = get_field(mt5_result, "currency_digits")
    if val is not None:
        mt5_msg.currency_digits = int(val)
    val = get_field(mt5_result, "fifo_close")
    if val is not None:
        mt5_msg.fifo_close = bool(val)
    val = get_field(mt5_result, "margin_initial")
    if val is not None:
        mt5_msg.margin_initial = float(val)
    val = get_field(mt5_result, "margin_maintenance")
    if val is not None:
        mt5_msg.margin_maintenance = float(val)
    val = get_field(mt5_result, "assets")
    if val is not None:
        mt5_msg.assets = float(val)
    val = get_field(mt5_result, "liabilities")
    if val is not None:
        mt5_msg.liabilities = float(val)
    val = get_field(mt5_result, "commission_blocked")
    if val is not None:
        mt5_msg.commission_blocked = float(val)

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_terminal_info(mt5_result: Any) -> types_pb2.TerminalInfo:
    """
    Convert MT5 TerminalInfo to Protobuf TerminalInfo message.
    """
    msg = types_pb2.TerminalInfo()

    # Generic fields
    val = get_field(mt5_result, "connected")
    if val is not None:
        msg.connected = bool(val)
    val = get_field(mt5_result, "trade_allowed")
    if val is not None:
        msg.trade_allowed = bool(val)
    val = get_field(mt5_result, "ping_last")
    if val is not None:
        msg.ping_last = int(val)
    val = get_field(mt5_result, "company")
    if val is not None:
        msg.company = str(val)
    val = get_field(mt5_result, "name")
    if val is not None:
        msg.name = str(val)

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5TerminalInfo()
    val = get_field(mt5_result, "community_account")
    if val is not None:
        mt5_msg.community_account = bool(val)
    val = get_field(mt5_result, "community_connection")
    if val is not None:
        mt5_msg.community_connection = bool(val)
    val = get_field(mt5_result, "dlls_allowed")
    if val is not None:
        mt5_msg.dlls_allowed = bool(val)
    val = get_field(mt5_result, "tradeapi_disabled")
    if val is not None:
        mt5_msg.tradeapi_disabled = bool(val)
    val = get_field(mt5_result, "email_enabled")
    if val is not None:
        mt5_msg.email_enabled = bool(val)
    val = get_field(mt5_result, "ftp_enabled")
    if val is not None:
        mt5_msg.ftp_enabled = bool(val)
    val = get_field(mt5_result, "notifications_enabled")
    if val is not None:
        mt5_msg.notifications_enabled = bool(val)
    val = get_field(mt5_result, "mqid")
    if val is not None:
        mt5_msg.mqid = bool(val)
    val = get_field(mt5_result, "build")
    if val is not None:
        mt5_msg.build = int(val)
    val = get_field(mt5_result, "maxbars")
    if val is not None:
        mt5_msg.maxbars = int(val)
    val = get_field(mt5_result, "codepage")
    if val is not None:
        mt5_msg.codepage = int(val)
    val = get_field(mt5_result, "community_balance")
    if val is not None:
        mt5_msg.community_balance = float(val)
    val = get_field(mt5_result, "retransmission")
    if val is not None:
        mt5_msg.retransmission = float(val)
    val = get_field(mt5_result, "language")
    if val is not None:
        mt5_msg.language = str(val)
    val = get_field(mt5_result, "path")
    if val is not None:
        mt5_msg.path = str(val)
    val = get_field(mt5_result, "data_path")
    if val is not None:
        mt5_msg.data_path = str(val)
    val = get_field(mt5_result, "commondata_path")
    if val is not None:
        mt5_msg.commondata_path = str(val)

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_symbol_info(mt5_result: Any) -> types_pb2.SymbolInfo:
    """
    Convert MT5 SymbolInfo to Protobuf SymbolInfo message.
    """
    msg = types_pb2.SymbolInfo()

    # Generic numeric fields
    val = get_field(mt5_result, "digits")
    if val is not None:
        msg.digits = int(val)
    val = get_field(mt5_result, "spread")
    if val is not None:
        msg.spread = int(val)
    val = get_field(mt5_result, "spread_float")
    if val is not None:
        msg.spread_float = bool(val)
    val = get_field(mt5_result, "bid")
    if val is not None:
        msg.bid = float(val)
    val = get_field(mt5_result, "ask")
    if val is not None:
        msg.ask = float(val)
    val = get_field(mt5_result, "last")
    if val is not None:
        msg.last = float(val)
    val = get_field(mt5_result, "point")
    if val is not None:
        msg.point = float(val)
    val = get_field(mt5_result, "trade_tick_size")
    if val is not None:
        msg.trade_tick_size = float(val)
    val = get_field(mt5_result, "trade_contract_size")
    if val is not None:
        msg.trade_contract_size = float(val)
    val = get_field(mt5_result, "volume_min")
    if val is not None:
        msg.volume_min = float(val)
    val = get_field(mt5_result, "volume_max")
    if val is not None:
        msg.volume_max = float(val)
    val = get_field(mt5_result, "volume_step")
    if val is not None:
        msg.volume_step = float(val)
    val = get_field(mt5_result, "swap_long")
    if val is not None:
        msg.swap_long = float(val)
    val = get_field(mt5_result, "swap_short")
    if val is not None:
        msg.swap_short = float(val)
    val = get_field(mt5_result, "margin_initial")
    if val is not None:
        msg.margin_initial = float(val)
    val = get_field(mt5_result, "margin_maintenance")
    if val is not None:
        msg.margin_maintenance = float(val)
    val = get_field(mt5_result, "margin_hedged")
    if val is not None:
        msg.margin_hedged = float(val)
    val = get_field(mt5_result, "price_change")
    if val is not None:
        msg.price_change = float(val)
    val = get_field(mt5_result, "price_volatility")
    if val is not None:
        msg.price_volatility = float(val)
    val = get_field(mt5_result, "start_time")
    if val is not None:
        msg.start_time = int(val)
    val = get_field(mt5_result, "expiration_time")
    if val is not None:
        msg.expiration_time = int(val)
    val = get_field(mt5_result, "trade_stops_level")
    if val is not None:
        msg.trade_stops_level = int(val)
    val = get_field(mt5_result, "trade_freeze_level")
    if val is not None:
        msg.trade_freeze_level = int(val)
    val = get_field(mt5_result, "bidhigh")
    if val is not None:
        msg.bidhigh = float(val)
    val = get_field(mt5_result, "bidlow")
    if val is not None:
        msg.bidlow = float(val)
    val = get_field(mt5_result, "askhigh")
    if val is not None:
        msg.askhigh = float(val)
    val = get_field(mt5_result, "asklow")
    if val is not None:
        msg.asklow = float(val)
    val = get_field(mt5_result, "lasthigh")
    if val is not None:
        msg.lasthigh = float(val)
    val = get_field(mt5_result, "lastlow")
    if val is not None:
        msg.lastlow = float(val)
    val = get_field(mt5_result, "volume")
    if val is not None:
        msg.volume = float(val)
    val = get_field(mt5_result, "volume_real")
    if val is not None:
        msg.volume_real = float(val)
    val = get_field(mt5_result, "volumehigh_real")
    if val is not None:
        msg.volumehigh_real = float(val)
    val = get_field(mt5_result, "volumelow_real")
    if val is not None:
        msg.volumelow_real = float(val)

    # Generic string fields
    val = get_field(mt5_result, "currency_base")
    if val is not None:
        msg.currency_base = str(val)
    val = get_field(mt5_result, "currency_profit")
    if val is not None:
        msg.currency_profit = str(val)
    val = get_field(mt5_result, "currency_margin")
    if val is not None:
        msg.currency_margin = str(val)
    val = get_field(mt5_result, "description")
    if val is not None:
        msg.description = str(val)
    val = get_field(mt5_result, "exchange")
    if val is not None:
        msg.exchange = str(val)
    val = get_field(mt5_result, "isin")
    if val is not None:
        msg.isin = str(val)
    val = get_field(mt5_result, "name")
    if val is not None:
        msg.name = str(val)

    # Additional generic numeric fields
    val = get_field(mt5_result, "trade_tick_value")
    if val is not None:
        msg.trade_tick_value = float(val)
    val = get_field(mt5_result, "trade_tick_value_profit")
    if val is not None:
        msg.trade_tick_value_profit = float(val)
    val = get_field(mt5_result, "trade_tick_value_loss")
    if val is not None:
        msg.trade_tick_value_loss = float(val)
    val = get_field(mt5_result, "price_theoretical")
    if val is not None:
        msg.price_theoretical = float(val)
    val = get_field(mt5_result, "price_greeks_delta")
    if val is not None:
        msg.price_greeks_delta = float(val)
    val = get_field(mt5_result, "price_greeks_theta")
    if val is not None:
        msg.price_greeks_theta = float(val)
    val = get_field(mt5_result, "price_greeks_gamma")
    if val is not None:
        msg.price_greeks_gamma = float(val)
    val = get_field(mt5_result, "price_greeks_vega")
    if val is not None:
        msg.price_greeks_vega = float(val)
    val = get_field(mt5_result, "price_greeks_rho")
    if val is not None:
        msg.price_greeks_rho = float(val)
    val = get_field(mt5_result, "price_greeks_omega")
    if val is not None:
        msg.price_greeks_omega = float(val)
    val = get_field(mt5_result, "price_sensitivity")
    if val is not None:
        msg.price_sensitivity = float(val)
    val = get_field(mt5_result, "basis")
    if val is not None:
        msg.basis = str(val)
    val = get_field(mt5_result, "trade_accrued_interest")
    if val is not None:
        msg.trade_accrued_interest = float(val)
    val = get_field(mt5_result, "trade_face_value")
    if val is not None:
        msg.trade_face_value = float(val)
    val = get_field(mt5_result, "trade_liquidity_rate")
    if val is not None:
        msg.trade_liquidity_rate = float(val)

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5SymbolInfo()
    val = get_field(mt5_result, "custom")
    if val is not None:
        mt5_msg.custom = bool(val)
    val = get_field(mt5_result, "chart_mode")
    if val is not None:
        mt5_msg.chart_mode = int(val)
    val = get_field(mt5_result, "select")
    if val is not None:
        mt5_msg.select = bool(val)
    val = get_field(mt5_result, "visible")
    if val is not None:
        mt5_msg.visible = bool(val)
    val = get_field(mt5_result, "trade_calc_mode")
    if val is not None:
        mt5_msg.trade_calc_mode = int(val)
    val = get_field(mt5_result, "trade_mode")
    if val is not None:
        mt5_msg.trade_mode = int(val)
    val = get_field(mt5_result, "trade_exemode")
    if val is not None:
        mt5_msg.trade_exemode = int(val)
    val = get_field(mt5_result, "swap_mode")
    if val is not None:
        mt5_msg.swap_mode = int(val)
    val = get_field(mt5_result, "swap_rollover3days")
    if val is not None:
        mt5_msg.swap_rollover3days = int(val)
    val = get_field(mt5_result, "margin_hedged_use_leg")
    if val is not None:
        mt5_msg.margin_hedged_use_leg = bool(val)
    val = get_field(mt5_result, "expiration_mode")
    if val is not None:
        mt5_msg.expiration_mode = int(val)
    val = get_field(mt5_result, "filling_mode")
    if val is not None:
        mt5_msg.filling_mode = int(val)
    val = get_field(mt5_result, "order_mode")
    if val is not None:
        mt5_msg.order_mode = int(val)
    val = get_field(mt5_result, "order_gtc_mode")
    if val is not None:
        mt5_msg.order_gtc_mode = int(val)
    val = get_field(mt5_result, "session_deals")
    if val is not None:
        mt5_msg.session_deals = int(val)
    val = get_field(mt5_result, "session_buy_orders")
    if val is not None:
        mt5_msg.session_buy_orders = int(val)
    val = get_field(mt5_result, "session_sell_orders")
    if val is not None:
        mt5_msg.session_sell_orders = int(val)
    val = get_field(mt5_result, "ticks_bookdepth")
    if val is not None:
        mt5_msg.ticks_bookdepth = int(val)
    val = get_field(mt5_result, "volumehigh")
    if val is not None:
        mt5_msg.volumehigh = int(val)
    val = get_field(mt5_result, "volumelow")
    if val is not None:
        mt5_msg.volumelow = int(val)
    val = get_field(mt5_result, "time")
    if val is not None:
        mt5_msg.time = int(val)
    val = get_field(mt5_result, "volume_limit")
    if val is not None:
        mt5_msg.volume_limit = float(val)
    val = get_field(mt5_result, "session_volume")
    if val is not None:
        mt5_msg.session_volume = float(val)
    val = get_field(mt5_result, "session_turnover")
    if val is not None:
        mt5_msg.session_turnover = float(val)
    val = get_field(mt5_result, "session_interest")
    if val is not None:
        mt5_msg.session_interest = float(val)
    val = get_field(mt5_result, "session_buy_orders_volume")
    if val is not None:
        mt5_msg.session_buy_orders_volume = float(val)
    val = get_field(mt5_result, "session_sell_orders_volume")
    if val is not None:
        mt5_msg.session_sell_orders_volume = float(val)
    val = get_field(mt5_result, "session_open")
    if val is not None:
        mt5_msg.session_open = float(val)
    val = get_field(mt5_result, "session_close")
    if val is not None:
        mt5_msg.session_close = float(val)
    val = get_field(mt5_result, "session_aw")
    if val is not None:
        mt5_msg.session_aw = float(val)
    val = get_field(mt5_result, "session_price_settlement")
    if val is not None:
        mt5_msg.session_price_settlement = float(val)
    val = get_field(mt5_result, "session_price_limit_min")
    if val is not None:
        mt5_msg.session_price_limit_min = float(val)
    val = get_field(mt5_result, "session_price_limit_max")
    if val is not None:
        mt5_msg.session_price_limit_max = float(val)
    val = get_field(mt5_result, "option_mode")
    if val is not None:
        mt5_msg.option_mode = int(val)
    val = get_field(mt5_result, "option_right")
    if val is not None:
        mt5_msg.option_right = int(val)
    val = get_field(mt5_result, "option_strike")
    if val is not None:
        mt5_msg.option_strike = float(val)
    val = get_field(mt5_result, "category")
    if val is not None:
        mt5_msg.category = str(val)
    val = get_field(mt5_result, "bank")
    if val is not None:
        mt5_msg.bank = str(val)
    val = get_field(mt5_result, "formula")
    if val is not None:
        mt5_msg.formula = str(val)
    val = get_field(mt5_result, "page")
    if val is not None:
        mt5_msg.page = str(val)
    val = get_field(mt5_result, "path")
    if val is not None:
        mt5_msg.path = str(val)

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_tick(mt5_result: Any) -> types_pb2.Tick:
    """
    Convert MT5 Tick to Protobuf Tick message.
    """
    msg = types_pb2.Tick()

    # Generic fields
    val = get_field(mt5_result, "time")
    if val is not None:
        msg.time = int(val)
    val = get_field(mt5_result, "bid")
    if val is not None:
        msg.bid = float(val)
    val = get_field(mt5_result, "ask")
    if val is not None:
        msg.ask = float(val)
    val = get_field(mt5_result, "last")
    if val is not None:
        msg.last = float(val)
    val = get_field(mt5_result, "volume")
    if val is not None:
        msg.volume = float(val)
    val = get_field(mt5_result, "time_msc")
    if val is not None:
        msg.time_msc = int(val)
    val = get_field(mt5_result, "volume_real")
    if val is not None:
        msg.volume_real = float(val)

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5Tick()
    val = get_field(mt5_result, "flags")
    if val is not None:
        mt5_msg.flags = int(val)

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_rate(mt5_result: Any) -> types_pb2.Rate:
    """
    Convert MT5 Rate (OHLCV) to Protobuf Rate message.
    """
    msg = types_pb2.Rate()

    val = get_field(mt5_result, "time")
    if val is not None:
        msg.time = int(val)
    val = get_field(mt5_result, "open")
    if val is not None:
        msg.open = float(val)
    val = get_field(mt5_result, "high")
    if val is not None:
        msg.high = float(val)
    val = get_field(mt5_result, "low")
    if val is not None:
        msg.low = float(val)
    val = get_field(mt5_result, "close")
    if val is not None:
        msg.close = float(val)
    val = get_field(mt5_result, "tick_volume")
    if val is not None:
        msg.tick_volume = int(val)
    val = get_field(mt5_result, "spread")
    if val is not None:
        msg.spread = int(val)
    val = get_field(mt5_result, "real_volume")
    if val is not None:
        msg.real_volume = int(val)

    return msg


def convert_trade_order(mt5_result: Any) -> types_pb2.TradeOrder:
    """
    Convert MT5 TradeOrder to Protobuf TradeOrder message.
    """
    msg = types_pb2.TradeOrder()

    # Generic fields
    val = get_field(mt5_result, "ticket")
    if val is not None:
        msg.ticket = int(val)
    val = get_field(mt5_result, "time_setup")
    if val is not None:
        msg.time_setup = int(val)
    val = get_field(mt5_result, "time_setup_msc")
    if val is not None:
        msg.time_setup_msc = int(val)
    val = get_field(mt5_result, "time_done")
    if val is not None:
        msg.time_done = int(val)
    val = get_field(mt5_result, "time_done_msc")
    if val is not None:
        msg.time_done_msc = int(val)
    val = get_field(mt5_result, "time_expiration")
    if val is not None:
        msg.time_expiration = int(val)
    val = get_field(mt5_result, "volume_current")
    if val is not None:
        msg.volume_current = float(val)
    val = get_field(mt5_result, "volume_initial")
    if val is not None:
        msg.volume_initial = float(val)
    val = get_field(mt5_result, "price_open")
    if val is not None:
        msg.price_open = float(val)
    val = get_field(mt5_result, "sl")
    if val is not None:
        msg.sl = float(val)
    val = get_field(mt5_result, "tp")
    if val is not None:
        msg.tp = float(val)
    val = get_field(mt5_result, "price_current")
    if val is not None:
        msg.price_current = float(val)
    val = get_field(mt5_result, "price_stoplimit")
    if val is not None:
        msg.price_stoplimit = float(val)
    val = get_field(mt5_result, "symbol")
    if val is not None:
        msg.symbol = str(val)
    val = get_field(mt5_result, "comment")
    if val is not None:
        msg.comment = str(val)
    val = get_field(mt5_result, "external_id")
    if val is not None:
        msg.external_id = str(val)
    val = get_field(mt5_result, "position_id")
    if val is not None:
        msg.position_id = int(val)

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5TradeOrder()
    val = get_field(mt5_result, "type")
    if val is not None:
        mt5_msg.type = int(val)
    val = get_field(mt5_result, "type_time")
    if val is not None:
        mt5_msg.type_time = int(val)
    val = get_field(mt5_result, "type_filling")
    if val is not None:
        mt5_msg.type_filling = int(val)
    val = get_field(mt5_result, "state")
    if val is not None:
        mt5_msg.state = int(val)
    val = get_field(mt5_result, "magic")
    if val is not None:
        mt5_msg.magic = int(val)
    val = get_field(mt5_result, "position_by_id")
    if val is not None:
        mt5_msg.position_by_id = int(val)
    val = get_field(mt5_result, "reason")
    if val is not None:
        mt5_msg.reason = int(val)

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_trade_position(mt5_result: Any) -> types_pb2.TradePosition:
    """
    Convert MT5 TradePosition to Protobuf TradePosition message.
    """
    msg = types_pb2.TradePosition()

    # Generic fields
    val = get_field(mt5_result, "ticket")
    if val is not None:
        msg.ticket = int(val)
    val = get_field(mt5_result, "time")
    if val is not None:
        msg.time = int(val)
    val = get_field(mt5_result, "time_msc")
    if val is not None:
        msg.time_msc = int(val)
    val = get_field(mt5_result, "time_update")
    if val is not None:
        msg.time_update = int(val)
    val = get_field(mt5_result, "time_update_msc")
    if val is not None:
        msg.time_update_msc = int(val)
    val = get_field(mt5_result, "volume")
    if val is not None:
        msg.volume = float(val)
    val = get_field(mt5_result, "price_open")
    if val is not None:
        msg.price_open = float(val)
    val = get_field(mt5_result, "sl")
    if val is not None:
        msg.sl = float(val)
    val = get_field(mt5_result, "tp")
    if val is not None:
        msg.tp = float(val)
    val = get_field(mt5_result, "price_current")
    if val is not None:
        msg.price_current = float(val)
    val = get_field(mt5_result, "swap")
    if val is not None:
        msg.swap = float(val)
    val = get_field(mt5_result, "profit")
    if val is not None:
        msg.profit = float(val)
    val = get_field(mt5_result, "symbol")
    if val is not None:
        msg.symbol = str(val)
    val = get_field(mt5_result, "comment")
    if val is not None:
        msg.comment = str(val)
    val = get_field(mt5_result, "external_id")
    if val is not None:
        msg.external_id = str(val)

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5TradePosition()
    val = get_field(mt5_result, "type")
    if val is not None:
        mt5_msg.type = int(val)
    val = get_field(mt5_result, "magic")
    if val is not None:
        mt5_msg.magic = int(val)
    val = get_field(mt5_result, "identifier")
    if val is not None:
        mt5_msg.identifier = int(val)
    val = get_field(mt5_result, "reason")
    if val is not None:
        mt5_msg.reason = int(val)

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_trade_deal(mt5_result: Any) -> types_pb2.TradeDeal:
    """
    Convert MT5 TradeDeal to Protobuf TradeDeal message.
    """
    msg = types_pb2.TradeDeal()

    # Generic fields
    val = get_field(mt5_result, "ticket")
    if val is not None:
        msg.ticket = int(val)
    val = get_field(mt5_result, "order")
    if val is not None:
        msg.order = int(val)
    val = get_field(mt5_result, "time")
    if val is not None:
        msg.time = int(val)
    val = get_field(mt5_result, "time_msc")
    if val is not None:
        msg.time_msc = int(val)
    val = get_field(mt5_result, "volume")
    if val is not None:
        msg.volume = float(val)
    val = get_field(mt5_result, "price")
    if val is not None:
        msg.price = float(val)
    val = get_field(mt5_result, "commission")
    if val is not None:
        msg.commission = float(val)
    val = get_field(mt5_result, "swap")
    if val is not None:
        msg.swap = float(val)
    val = get_field(mt5_result, "profit")
    if val is not None:
        msg.profit = float(val)
    val = get_field(mt5_result, "fee")
    if val is not None:
        msg.fee = float(val)
    val = get_field(mt5_result, "symbol")
    if val is not None:
        msg.symbol = str(val)
    val = get_field(mt5_result, "comment")
    if val is not None:
        msg.comment = str(val)
    val = get_field(mt5_result, "external_id")
    if val is not None:
        msg.external_id = str(val)
    val = get_field(mt5_result, "position_id")
    if val is not None:
        msg.position_id = int(val)

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5TradeDeal()
    val = get_field(mt5_result, "type")
    if val is not None:
        mt5_msg.type = int(val)
    val = get_field(mt5_result, "entry")
    if val is not None:
        mt5_msg.entry = int(val)
    val = get_field(mt5_result, "magic")
    if val is not None:
        mt5_msg.magic = int(val)
    val = get_field(mt5_result, "reason")
    if val is not None:
        mt5_msg.reason = int(val)

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_book_info(mt5_result: Any) -> types_pb2.BookInfo:
    """
    Convert MT5 BookInfo to Protobuf BookInfo message.
    """
    msg = types_pb2.BookInfo()

    # Generic fields
    val = get_field(mt5_result, "price")
    if val is not None:
        msg.price = float(val)
    val = get_field(mt5_result, "volume")
    if val is not None:
        msg.volume = float(val)
    val = get_field(mt5_result, "volume_dbl")
    if val is not None:
        msg.volume_dbl = float(val)

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5BookInfo()
    val = get_field(mt5_result, "type")
    if val is not None:
        mt5_msg.type = int(val)

    msg.mt5.CopyFrom(mt5_msg)
    return msg
