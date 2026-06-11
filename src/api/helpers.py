"""
Conversion utilities from MT5 namedtuples to Protobuf messages.

This module provides functions to convert MetaTrader5 Python API return values
(namedtuples) to their corresponding Protobuf message representations.

Each conversion function handles:
- Field-by-field mapping from MT5 object to protobuf message
- Nested messages (e.g., Mt5AccountInfo inside AccountInfo)
- None/missing values (proto3 default values)
"""

from typing import Optional, Any
from src.stubs import types_pb2


def convert_account_info(mt5_result: Any) -> types_pb2.AccountInfo:
    """
    Convert MT5 AccountInfo namedtuple to Protobuf AccountInfo message.

    Args:
        mt5_result: MT5 AccountInfo namedtuple from mt5.account_info()

    Returns:
        types_pb2.AccountInfo: Protobuf message with generic and MT5-specific fields
    """
    msg = types_pb2.AccountInfo()

    # Generic fields
    if hasattr(mt5_result, "login"):
        msg.login = int(mt5_result.login) if mt5_result.login else 0
    if hasattr(mt5_result, "leverage"):
        msg.leverage = int(mt5_result.leverage) if mt5_result.leverage else 0
    if hasattr(mt5_result, "trade_allowed"):
        msg.trade_allowed = bool(mt5_result.trade_allowed)
    if hasattr(mt5_result, "balance"):
        msg.balance = float(mt5_result.balance) if mt5_result.balance else 0.0
    if hasattr(mt5_result, "credit"):
        msg.credit = float(mt5_result.credit) if mt5_result.credit else 0.0
    if hasattr(mt5_result, "profit"):
        msg.profit = float(mt5_result.profit) if mt5_result.profit else 0.0
    if hasattr(mt5_result, "equity"):
        msg.equity = float(mt5_result.equity) if mt5_result.equity else 0.0
    if hasattr(mt5_result, "margin"):
        msg.margin = float(mt5_result.margin) if mt5_result.margin else 0.0
    if hasattr(mt5_result, "margin_free"):
        msg.margin_free = float(mt5_result.margin_free) if mt5_result.margin_free else 0.0
    if hasattr(mt5_result, "margin_level"):
        msg.margin_level = (
            float(mt5_result.margin_level) if mt5_result.margin_level else 0.0
        )
    if hasattr(mt5_result, "margin_so_call"):
        msg.margin_so_call = (
            float(mt5_result.margin_so_call) if mt5_result.margin_so_call else 0.0
        )
    if hasattr(mt5_result, "margin_so_so"):
        msg.margin_so_so = (
            float(mt5_result.margin_so_so) if mt5_result.margin_so_so else 0.0
        )
    if hasattr(mt5_result, "name"):
        msg.name = str(mt5_result.name) if mt5_result.name else ""
    if hasattr(mt5_result, "server"):
        msg.server = str(mt5_result.server) if mt5_result.server else ""
    if hasattr(mt5_result, "currency"):
        msg.currency = str(mt5_result.currency) if mt5_result.currency else ""
    if hasattr(mt5_result, "company"):
        msg.company = str(mt5_result.company) if mt5_result.company else ""

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5AccountInfo()
    if hasattr(mt5_result, "trade_mode"):
        mt5_msg.trade_mode = int(mt5_result.trade_mode) if mt5_result.trade_mode else 0
    if hasattr(mt5_result, "limit_orders"):
        mt5_msg.limit_orders = (
            int(mt5_result.limit_orders) if mt5_result.limit_orders else 0
        )
    if hasattr(mt5_result, "margin_so_mode"):
        mt5_msg.margin_so_mode = (
            int(mt5_result.margin_so_mode) if mt5_result.margin_so_mode else 0
        )
    if hasattr(mt5_result, "trade_expert"):
        mt5_msg.trade_expert = bool(mt5_result.trade_expert)
    if hasattr(mt5_result, "margin_mode"):
        mt5_msg.margin_mode = (
            int(mt5_result.margin_mode) if mt5_result.margin_mode else 0
        )
    if hasattr(mt5_result, "currency_digits"):
        mt5_msg.currency_digits = (
            int(mt5_result.currency_digits) if mt5_result.currency_digits else 0
        )
    if hasattr(mt5_result, "fifo_close"):
        mt5_msg.fifo_close = bool(mt5_result.fifo_close)
    if hasattr(mt5_result, "margin_initial"):
        mt5_msg.margin_initial = (
            float(mt5_result.margin_initial) if mt5_result.margin_initial else 0.0
        )
    if hasattr(mt5_result, "margin_maintenance"):
        mt5_msg.margin_maintenance = (
            float(mt5_result.margin_maintenance)
            if mt5_result.margin_maintenance
            else 0.0
        )
    if hasattr(mt5_result, "assets"):
        mt5_msg.assets = float(mt5_result.assets) if mt5_result.assets else 0.0
    if hasattr(mt5_result, "liabilities"):
        mt5_msg.liabilities = (
            float(mt5_result.liabilities) if mt5_result.liabilities else 0.0
        )
    if hasattr(mt5_result, "commission_blocked"):
        mt5_msg.commission_blocked = (
            float(mt5_result.commission_blocked)
            if mt5_result.commission_blocked
            else 0.0
        )

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_terminal_info(mt5_result: Any) -> types_pb2.TerminalInfo:
    """
    Convert MT5 TerminalInfo namedtuple to Protobuf TerminalInfo message.

    Args:
        mt5_result: MT5 TerminalInfo namedtuple from mt5.terminal_info()

    Returns:
        types_pb2.TerminalInfo: Protobuf message with terminal status and configuration
    """
    msg = types_pb2.TerminalInfo()

    # Generic fields
    if hasattr(mt5_result, "connected"):
        msg.connected = bool(mt5_result.connected)
    if hasattr(mt5_result, "trade_allowed"):
        msg.trade_allowed = bool(mt5_result.trade_allowed)
    if hasattr(mt5_result, "ping_last"):
        msg.ping_last = int(mt5_result.ping_last) if mt5_result.ping_last else 0
    if hasattr(mt5_result, "company"):
        msg.company = str(mt5_result.company) if mt5_result.company else ""
    if hasattr(mt5_result, "name"):
        msg.name = str(mt5_result.name) if mt5_result.name else ""

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5TerminalInfo()
    if hasattr(mt5_result, "community_account"):
        mt5_msg.community_account = bool(mt5_result.community_account)
    if hasattr(mt5_result, "community_connection"):
        mt5_msg.community_connection = bool(mt5_result.community_connection)
    if hasattr(mt5_result, "dlls_allowed"):
        mt5_msg.dlls_allowed = bool(mt5_result.dlls_allowed)
    if hasattr(mt5_result, "tradeapi_disabled"):
        mt5_msg.tradeapi_disabled = bool(mt5_result.tradeapi_disabled)
    if hasattr(mt5_result, "email_enabled"):
        mt5_msg.email_enabled = bool(mt5_result.email_enabled)
    if hasattr(mt5_result, "ftp_enabled"):
        mt5_msg.ftp_enabled = bool(mt5_result.ftp_enabled)
    if hasattr(mt5_result, "notifications_enabled"):
        mt5_msg.notifications_enabled = bool(mt5_result.notifications_enabled)
    if hasattr(mt5_result, "mqid"):
        mt5_msg.mqid = bool(mt5_result.mqid)
    if hasattr(mt5_result, "build"):
        mt5_msg.build = int(mt5_result.build) if mt5_result.build else 0
    if hasattr(mt5_result, "maxbars"):
        mt5_msg.maxbars = int(mt5_result.maxbars) if mt5_result.maxbars else 0
    if hasattr(mt5_result, "codepage"):
        mt5_msg.codepage = int(mt5_result.codepage) if mt5_result.codepage else 0
    if hasattr(mt5_result, "community_balance"):
        mt5_msg.community_balance = (
            float(mt5_result.community_balance)
            if mt5_result.community_balance
            else 0.0
        )
    if hasattr(mt5_result, "retransmission"):
        mt5_msg.retransmission = (
            float(mt5_result.retransmission) if mt5_result.retransmission else 0.0
        )
    if hasattr(mt5_result, "language"):
        mt5_msg.language = str(mt5_result.language) if mt5_result.language else ""
    if hasattr(mt5_result, "path"):
        mt5_msg.path = str(mt5_result.path) if mt5_result.path else ""
    if hasattr(mt5_result, "data_path"):
        mt5_msg.data_path = str(mt5_result.data_path) if mt5_result.data_path else ""
    if hasattr(mt5_result, "commondata_path"):
        mt5_msg.commondata_path = (
            str(mt5_result.commondata_path) if mt5_result.commondata_path else ""
        )

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_symbol_info(mt5_result: Any) -> types_pb2.SymbolInfo:
    """
    Convert MT5 SymbolInfo namedtuple to Protobuf SymbolInfo message.

    Args:
        mt5_result: MT5 SymbolInfo namedtuple from mt5.symbol_info()

    Returns:
        types_pb2.SymbolInfo: Protobuf message with symbol market data and configuration
    """
    msg = types_pb2.SymbolInfo()

    # Generic numeric fields
    if hasattr(mt5_result, "digits"):
        msg.digits = int(mt5_result.digits) if mt5_result.digits else 0
    if hasattr(mt5_result, "spread"):
        msg.spread = int(mt5_result.spread) if mt5_result.spread else 0
    if hasattr(mt5_result, "spread_float"):
        msg.spread_float = bool(mt5_result.spread_float)
    if hasattr(mt5_result, "bid"):
        msg.bid = float(mt5_result.bid) if mt5_result.bid else 0.0
    if hasattr(mt5_result, "ask"):
        msg.ask = float(mt5_result.ask) if mt5_result.ask else 0.0
    if hasattr(mt5_result, "last"):
        msg.last = float(mt5_result.last) if mt5_result.last else 0.0
    if hasattr(mt5_result, "point"):
        msg.point = float(mt5_result.point) if mt5_result.point else 0.0
    if hasattr(mt5_result, "trade_tick_size"):
        msg.trade_tick_size = (
            float(mt5_result.trade_tick_size) if mt5_result.trade_tick_size else 0.0
        )
    if hasattr(mt5_result, "trade_contract_size"):
        msg.trade_contract_size = (
            float(mt5_result.trade_contract_size)
            if mt5_result.trade_contract_size
            else 0.0
        )
    if hasattr(mt5_result, "volume_min"):
        msg.volume_min = (
            float(mt5_result.volume_min) if mt5_result.volume_min else 0.0
        )
    if hasattr(mt5_result, "volume_max"):
        msg.volume_max = (
            float(mt5_result.volume_max) if mt5_result.volume_max else 0.0
        )
    if hasattr(mt5_result, "volume_step"):
        msg.volume_step = (
            float(mt5_result.volume_step) if mt5_result.volume_step else 0.0
        )
    if hasattr(mt5_result, "swap_long"):
        msg.swap_long = float(mt5_result.swap_long) if mt5_result.swap_long else 0.0
    if hasattr(mt5_result, "swap_short"):
        msg.swap_short = (
            float(mt5_result.swap_short) if mt5_result.swap_short else 0.0
        )
    if hasattr(mt5_result, "margin_initial"):
        msg.margin_initial = (
            float(mt5_result.margin_initial) if mt5_result.margin_initial else 0.0
        )
    if hasattr(mt5_result, "margin_maintenance"):
        msg.margin_maintenance = (
            float(mt5_result.margin_maintenance)
            if mt5_result.margin_maintenance
            else 0.0
        )
    if hasattr(mt5_result, "margin_hedged"):
        msg.margin_hedged = (
            float(mt5_result.margin_hedged) if mt5_result.margin_hedged else 0.0
        )
    if hasattr(mt5_result, "price_change"):
        msg.price_change = (
            float(mt5_result.price_change) if mt5_result.price_change else 0.0
        )
    if hasattr(mt5_result, "price_volatility"):
        msg.price_volatility = (
            float(mt5_result.price_volatility) if mt5_result.price_volatility else 0.0
        )
    if hasattr(mt5_result, "start_time"):
        msg.start_time = int(mt5_result.start_time) if mt5_result.start_time else 0
    if hasattr(mt5_result, "expiration_time"):
        msg.expiration_time = (
            int(mt5_result.expiration_time) if mt5_result.expiration_time else 0
        )
    if hasattr(mt5_result, "trade_stops_level"):
        msg.trade_stops_level = (
            int(mt5_result.trade_stops_level) if mt5_result.trade_stops_level else 0
        )
    if hasattr(mt5_result, "trade_freeze_level"):
        msg.trade_freeze_level = (
            int(mt5_result.trade_freeze_level) if mt5_result.trade_freeze_level else 0
        )
    if hasattr(mt5_result, "bidhigh"):
        msg.bidhigh = float(mt5_result.bidhigh) if mt5_result.bidhigh else 0.0
    if hasattr(mt5_result, "bidlow"):
        msg.bidlow = float(mt5_result.bidlow) if mt5_result.bidlow else 0.0
    if hasattr(mt5_result, "askhigh"):
        msg.askhigh = float(mt5_result.askhigh) if mt5_result.askhigh else 0.0
    if hasattr(mt5_result, "asklow"):
        msg.asklow = float(mt5_result.asklow) if mt5_result.asklow else 0.0
    if hasattr(mt5_result, "lasthigh"):
        msg.lasthigh = float(mt5_result.lasthigh) if mt5_result.lasthigh else 0.0
    if hasattr(mt5_result, "lastlow"):
        msg.lastlow = float(mt5_result.lastlow) if mt5_result.lastlow else 0.0
    if hasattr(mt5_result, "volume"):
        msg.volume = float(mt5_result.volume) if mt5_result.volume else 0.0
    if hasattr(mt5_result, "volume_real"):
        msg.volume_real = (
            float(mt5_result.volume_real) if mt5_result.volume_real else 0.0
        )
    if hasattr(mt5_result, "volumehigh_real"):
        msg.volumehigh_real = (
            float(mt5_result.volumehigh_real) if mt5_result.volumehigh_real else 0.0
        )
    if hasattr(mt5_result, "volumelow_real"):
        msg.volumelow_real = (
            float(mt5_result.volumelow_real) if mt5_result.volumelow_real else 0.0
        )

    # Generic string fields
    if hasattr(mt5_result, "currency_base"):
        msg.currency_base = (
            str(mt5_result.currency_base) if mt5_result.currency_base else ""
        )
    if hasattr(mt5_result, "currency_profit"):
        msg.currency_profit = (
            str(mt5_result.currency_profit) if mt5_result.currency_profit else ""
        )
    if hasattr(mt5_result, "currency_margin"):
        msg.currency_margin = (
            str(mt5_result.currency_margin) if mt5_result.currency_margin else ""
        )
    if hasattr(mt5_result, "description"):
        msg.description = (
            str(mt5_result.description) if mt5_result.description else ""
        )
    if hasattr(mt5_result, "exchange"):
        msg.exchange = str(mt5_result.exchange) if mt5_result.exchange else ""
    if hasattr(mt5_result, "isin"):
        msg.isin = str(mt5_result.isin) if mt5_result.isin else ""
    if hasattr(mt5_result, "name"):
        msg.name = str(mt5_result.name) if mt5_result.name else ""

    # Additional generic numeric fields
    if hasattr(mt5_result, "trade_tick_value"):
        msg.trade_tick_value = (
            float(mt5_result.trade_tick_value) if mt5_result.trade_tick_value else 0.0
        )
    if hasattr(mt5_result, "trade_tick_value_profit"):
        msg.trade_tick_value_profit = (
            float(mt5_result.trade_tick_value_profit)
            if mt5_result.trade_tick_value_profit
            else 0.0
        )
    if hasattr(mt5_result, "trade_tick_value_loss"):
        msg.trade_tick_value_loss = (
            float(mt5_result.trade_tick_value_loss)
            if mt5_result.trade_tick_value_loss
            else 0.0
        )
    if hasattr(mt5_result, "price_theoretical"):
        msg.price_theoretical = (
            float(mt5_result.price_theoretical)
            if mt5_result.price_theoretical
            else 0.0
        )
    if hasattr(mt5_result, "price_greeks_delta"):
        msg.price_greeks_delta = (
            float(mt5_result.price_greeks_delta)
            if mt5_result.price_greeks_delta
            else 0.0
        )
    if hasattr(mt5_result, "price_greeks_theta"):
        msg.price_greeks_theta = (
            float(mt5_result.price_greeks_theta)
            if mt5_result.price_greeks_theta
            else 0.0
        )
    if hasattr(mt5_result, "price_greeks_gamma"):
        msg.price_greeks_gamma = (
            float(mt5_result.price_greeks_gamma)
            if mt5_result.price_greeks_gamma
            else 0.0
        )
    if hasattr(mt5_result, "price_greeks_vega"):
        msg.price_greeks_vega = (
            float(mt5_result.price_greeks_vega) if mt5_result.price_greeks_vega else 0.0
        )
    if hasattr(mt5_result, "price_greeks_rho"):
        msg.price_greeks_rho = (
            float(mt5_result.price_greeks_rho) if mt5_result.price_greeks_rho else 0.0
        )
    if hasattr(mt5_result, "price_greeks_omega"):
        msg.price_greeks_omega = (
            float(mt5_result.price_greeks_omega)
            if mt5_result.price_greeks_omega
            else 0.0
        )
    if hasattr(mt5_result, "price_sensitivity"):
        msg.price_sensitivity = (
            float(mt5_result.price_sensitivity) if mt5_result.price_sensitivity else 0.0
        )
    if hasattr(mt5_result, "basis"):
        msg.basis = str(mt5_result.basis) if mt5_result.basis else ""
    if hasattr(mt5_result, "trade_accrued_interest"):
        msg.trade_accrued_interest = (
            float(mt5_result.trade_accrued_interest)
            if mt5_result.trade_accrued_interest
            else 0.0
        )
    if hasattr(mt5_result, "trade_face_value"):
        msg.trade_face_value = (
            float(mt5_result.trade_face_value) if mt5_result.trade_face_value else 0.0
        )
    if hasattr(mt5_result, "trade_liquidity_rate"):
        msg.trade_liquidity_rate = (
            float(mt5_result.trade_liquidity_rate)
            if mt5_result.trade_liquidity_rate
            else 0.0
        )

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5SymbolInfo()
    if hasattr(mt5_result, "custom"):
        mt5_msg.custom = bool(mt5_result.custom)
    if hasattr(mt5_result, "chart_mode"):
        mt5_msg.chart_mode = (
            int(mt5_result.chart_mode) if mt5_result.chart_mode else 0
        )
    if hasattr(mt5_result, "select"):
        mt5_msg.select = bool(mt5_result.select)
    if hasattr(mt5_result, "visible"):
        mt5_msg.visible = bool(mt5_result.visible)
    if hasattr(mt5_result, "trade_calc_mode"):
        mt5_msg.trade_calc_mode = (
            int(mt5_result.trade_calc_mode) if mt5_result.trade_calc_mode else 0
        )
    if hasattr(mt5_result, "trade_mode"):
        mt5_msg.trade_mode = (
            int(mt5_result.trade_mode) if mt5_result.trade_mode else 0
        )
    if hasattr(mt5_result, "trade_exemode"):
        mt5_msg.trade_exemode = (
            int(mt5_result.trade_exemode) if mt5_result.trade_exemode else 0
        )
    if hasattr(mt5_result, "swap_mode"):
        mt5_msg.swap_mode = (
            int(mt5_result.swap_mode) if mt5_result.swap_mode else 0
        )
    if hasattr(mt5_result, "swap_rollover3days"):
        mt5_msg.swap_rollover3days = (
            int(mt5_result.swap_rollover3days) if mt5_result.swap_rollover3days else 0
        )
    if hasattr(mt5_result, "margin_hedged_use_leg"):
        mt5_msg.margin_hedged_use_leg = bool(mt5_result.margin_hedged_use_leg)
    if hasattr(mt5_result, "expiration_mode"):
        mt5_msg.expiration_mode = (
            int(mt5_result.expiration_mode) if mt5_result.expiration_mode else 0
        )
    if hasattr(mt5_result, "filling_mode"):
        mt5_msg.filling_mode = (
            int(mt5_result.filling_mode) if mt5_result.filling_mode else 0
        )
    if hasattr(mt5_result, "order_mode"):
        mt5_msg.order_mode = (
            int(mt5_result.order_mode) if mt5_result.order_mode else 0
        )
    if hasattr(mt5_result, "order_gtc_mode"):
        mt5_msg.order_gtc_mode = (
            int(mt5_result.order_gtc_mode) if mt5_result.order_gtc_mode else 0
        )
    if hasattr(mt5_result, "session_deals"):
        mt5_msg.session_deals = (
            int(mt5_result.session_deals) if mt5_result.session_deals else 0
        )
    if hasattr(mt5_result, "session_buy_orders"):
        mt5_msg.session_buy_orders = (
            int(mt5_result.session_buy_orders) if mt5_result.session_buy_orders else 0
        )
    if hasattr(mt5_result, "session_sell_orders"):
        mt5_msg.session_sell_orders = (
            int(mt5_result.session_sell_orders) if mt5_result.session_sell_orders else 0
        )
    if hasattr(mt5_result, "ticks_bookdepth"):
        mt5_msg.ticks_bookdepth = (
            int(mt5_result.ticks_bookdepth) if mt5_result.ticks_bookdepth else 0
        )
    if hasattr(mt5_result, "volumehigh"):
        mt5_msg.volumehigh = (
            int(mt5_result.volumehigh) if mt5_result.volumehigh else 0
        )
    if hasattr(mt5_result, "volumelow"):
        mt5_msg.volumelow = (
            int(mt5_result.volumelow) if mt5_result.volumelow else 0
        )
    if hasattr(mt5_result, "time"):
        mt5_msg.time = int(mt5_result.time) if mt5_result.time else 0
    if hasattr(mt5_result, "volume_limit"):
        mt5_msg.volume_limit = (
            float(mt5_result.volume_limit) if mt5_result.volume_limit else 0.0
        )
    if hasattr(mt5_result, "session_volume"):
        mt5_msg.session_volume = (
            float(mt5_result.session_volume) if mt5_result.session_volume else 0.0
        )
    if hasattr(mt5_result, "session_turnover"):
        mt5_msg.session_turnover = (
            float(mt5_result.session_turnover) if mt5_result.session_turnover else 0.0
        )
    if hasattr(mt5_result, "session_interest"):
        mt5_msg.session_interest = (
            float(mt5_result.session_interest) if mt5_result.session_interest else 0.0
        )
    if hasattr(mt5_result, "session_buy_orders_volume"):
        mt5_msg.session_buy_orders_volume = (
            float(mt5_result.session_buy_orders_volume)
            if mt5_result.session_buy_orders_volume
            else 0.0
        )
    if hasattr(mt5_result, "session_sell_orders_volume"):
        mt5_msg.session_sell_orders_volume = (
            float(mt5_result.session_sell_orders_volume)
            if mt5_result.session_sell_orders_volume
            else 0.0
        )
    if hasattr(mt5_result, "session_open"):
        mt5_msg.session_open = (
            float(mt5_result.session_open) if mt5_result.session_open else 0.0
        )
    if hasattr(mt5_result, "session_close"):
        mt5_msg.session_close = (
            float(mt5_result.session_close) if mt5_result.session_close else 0.0
        )
    if hasattr(mt5_result, "session_aw"):
        mt5_msg.session_aw = (
            float(mt5_result.session_aw) if mt5_result.session_aw else 0.0
        )
    if hasattr(mt5_result, "session_price_settlement"):
        mt5_msg.session_price_settlement = (
            float(mt5_result.session_price_settlement)
            if mt5_result.session_price_settlement
            else 0.0
        )
    if hasattr(mt5_result, "session_price_limit_min"):
        mt5_msg.session_price_limit_min = (
            float(mt5_result.session_price_limit_min)
            if mt5_result.session_price_limit_min
            else 0.0
        )
    if hasattr(mt5_result, "session_price_limit_max"):
        mt5_msg.session_price_limit_max = (
            float(mt5_result.session_price_limit_max)
            if mt5_result.session_price_limit_max
            else 0.0
        )
    if hasattr(mt5_result, "option_mode"):
        mt5_msg.option_mode = (
            int(mt5_result.option_mode) if mt5_result.option_mode else 0
        )
    if hasattr(mt5_result, "option_right"):
        mt5_msg.option_right = (
            int(mt5_result.option_right) if mt5_result.option_right else 0
        )
    if hasattr(mt5_result, "option_strike"):
        mt5_msg.option_strike = (
            float(mt5_result.option_strike) if mt5_result.option_strike else 0.0
        )
    if hasattr(mt5_result, "category"):
        mt5_msg.category = str(mt5_result.category) if mt5_result.category else ""
    if hasattr(mt5_result, "bank"):
        mt5_msg.bank = str(mt5_result.bank) if mt5_result.bank else ""
    if hasattr(mt5_result, "formula"):
        mt5_msg.formula = str(mt5_result.formula) if mt5_result.formula else ""
    if hasattr(mt5_result, "page"):
        mt5_msg.page = str(mt5_result.page) if mt5_result.page else ""
    if hasattr(mt5_result, "path"):
        mt5_msg.path = str(mt5_result.path) if mt5_result.path else ""

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_tick(mt5_result: Any) -> types_pb2.Tick:
    """
    Convert MT5 Tick namedtuple to Protobuf Tick message.

    Args:
        mt5_result: MT5 Tick namedtuple from mt5.symbol_info_tick()

    Returns:
        types_pb2.Tick: Protobuf message with tick market data
    """
    msg = types_pb2.Tick()

    # Generic fields
    if hasattr(mt5_result, "time"):
        msg.time = int(mt5_result.time) if mt5_result.time else 0
    if hasattr(mt5_result, "bid"):
        msg.bid = float(mt5_result.bid) if mt5_result.bid else 0.0
    if hasattr(mt5_result, "ask"):
        msg.ask = float(mt5_result.ask) if mt5_result.ask else 0.0
    if hasattr(mt5_result, "last"):
        msg.last = float(mt5_result.last) if mt5_result.last else 0.0
    if hasattr(mt5_result, "volume"):
        msg.volume = float(mt5_result.volume) if mt5_result.volume else 0.0
    if hasattr(mt5_result, "time_msc"):
        msg.time_msc = int(mt5_result.time_msc) if mt5_result.time_msc else 0
    if hasattr(mt5_result, "volume_real"):
        msg.volume_real = (
            float(mt5_result.volume_real) if mt5_result.volume_real else 0.0
        )

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5Tick()
    if hasattr(mt5_result, "flags"):
        mt5_msg.flags = int(mt5_result.flags) if mt5_result.flags else 0

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_rate(mt5_result: Any) -> types_pb2.Rate:
    """
    Convert MT5 Rate (OHLCV) namedtuple to Protobuf Rate message.

    Args:
        mt5_result: MT5 Rate namedtuple from copy_rates_* functions

    Returns:
        types_pb2.Rate: Protobuf message with OHLCV bar data
    """
    msg = types_pb2.Rate()

    if hasattr(mt5_result, "time"):
        msg.time = int(mt5_result.time) if mt5_result.time else 0
    if hasattr(mt5_result, "open"):
        msg.open = float(mt5_result.open) if mt5_result.open else 0.0
    if hasattr(mt5_result, "high"):
        msg.high = float(mt5_result.high) if mt5_result.high else 0.0
    if hasattr(mt5_result, "low"):
        msg.low = float(mt5_result.low) if mt5_result.low else 0.0
    if hasattr(mt5_result, "close"):
        msg.close = float(mt5_result.close) if mt5_result.close else 0.0
    if hasattr(mt5_result, "tick_volume"):
        msg.tick_volume = (
            int(mt5_result.tick_volume) if mt5_result.tick_volume else 0
        )
    if hasattr(mt5_result, "spread"):
        msg.spread = int(mt5_result.spread) if mt5_result.spread else 0
    if hasattr(mt5_result, "real_volume"):
        msg.real_volume = (
            int(mt5_result.real_volume) if mt5_result.real_volume else 0
        )

    return msg


def convert_trade_order(mt5_result: Any) -> types_pb2.TradeOrder:
    """
    Convert MT5 TradeOrder namedtuple to Protobuf TradeOrder message.

    Args:
        mt5_result: MT5 TradeOrder namedtuple from orders_get() or history_orders_get()

    Returns:
        types_pb2.TradeOrder: Protobuf message with pending order data
    """
    msg = types_pb2.TradeOrder()

    # Generic fields
    if hasattr(mt5_result, "ticket"):
        msg.ticket = int(mt5_result.ticket) if mt5_result.ticket else 0
    if hasattr(mt5_result, "time_setup"):
        msg.time_setup = int(mt5_result.time_setup) if mt5_result.time_setup else 0
    if hasattr(mt5_result, "time_setup_msc"):
        msg.time_setup_msc = (
            int(mt5_result.time_setup_msc) if mt5_result.time_setup_msc else 0
        )
    if hasattr(mt5_result, "time_done"):
        msg.time_done = int(mt5_result.time_done) if mt5_result.time_done else 0
    if hasattr(mt5_result, "time_done_msc"):
        msg.time_done_msc = (
            int(mt5_result.time_done_msc) if mt5_result.time_done_msc else 0
        )
    if hasattr(mt5_result, "time_expiration"):
        msg.time_expiration = (
            int(mt5_result.time_expiration) if mt5_result.time_expiration else 0
        )
    if hasattr(mt5_result, "volume_current"):
        msg.volume_current = (
            float(mt5_result.volume_current) if mt5_result.volume_current else 0.0
        )
    if hasattr(mt5_result, "volume_initial"):
        msg.volume_initial = (
            float(mt5_result.volume_initial) if mt5_result.volume_initial else 0.0
        )
    if hasattr(mt5_result, "price_open"):
        msg.price_open = (
            float(mt5_result.price_open) if mt5_result.price_open else 0.0
        )
    if hasattr(mt5_result, "sl"):
        msg.sl = float(mt5_result.sl) if mt5_result.sl else 0.0
    if hasattr(mt5_result, "tp"):
        msg.tp = float(mt5_result.tp) if mt5_result.tp else 0.0
    if hasattr(mt5_result, "price_current"):
        msg.price_current = (
            float(mt5_result.price_current) if mt5_result.price_current else 0.0
        )
    if hasattr(mt5_result, "price_stoplimit"):
        msg.price_stoplimit = (
            float(mt5_result.price_stoplimit) if mt5_result.price_stoplimit else 0.0
        )
    if hasattr(mt5_result, "symbol"):
        msg.symbol = str(mt5_result.symbol) if mt5_result.symbol else ""
    if hasattr(mt5_result, "comment"):
        msg.comment = str(mt5_result.comment) if mt5_result.comment else ""
    if hasattr(mt5_result, "external_id"):
        msg.external_id = (
            str(mt5_result.external_id) if mt5_result.external_id else ""
        )
    if hasattr(mt5_result, "position_id"):
        msg.position_id = int(mt5_result.position_id) if mt5_result.position_id else 0

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5TradeOrder()
    if hasattr(mt5_result, "type"):
        mt5_msg.type = int(mt5_result.type) if mt5_result.type else 0
    if hasattr(mt5_result, "type_time"):
        mt5_msg.type_time = (
            int(mt5_result.type_time) if mt5_result.type_time else 0
        )
    if hasattr(mt5_result, "type_filling"):
        mt5_msg.type_filling = (
            int(mt5_result.type_filling) if mt5_result.type_filling else 0
        )
    if hasattr(mt5_result, "state"):
        mt5_msg.state = int(mt5_result.state) if mt5_result.state else 0
    if hasattr(mt5_result, "magic"):
        mt5_msg.magic = int(mt5_result.magic) if mt5_result.magic else 0
    if hasattr(mt5_result, "position_by_id"):
        mt5_msg.position_by_id = (
            int(mt5_result.position_by_id) if mt5_result.position_by_id else 0
        )
    if hasattr(mt5_result, "reason"):
        mt5_msg.reason = int(mt5_result.reason) if mt5_result.reason else 0

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_trade_position(mt5_result: Any) -> types_pb2.TradePosition:
    """
    Convert MT5 TradePosition namedtuple to Protobuf TradePosition message.

    Args:
        mt5_result: MT5 TradePosition namedtuple from positions_get()

    Returns:
        types_pb2.TradePosition: Protobuf message with open position data
    """
    msg = types_pb2.TradePosition()

    # Generic fields
    if hasattr(mt5_result, "ticket"):
        msg.ticket = int(mt5_result.ticket) if mt5_result.ticket else 0
    if hasattr(mt5_result, "time"):
        msg.time = int(mt5_result.time) if mt5_result.time else 0
    if hasattr(mt5_result, "time_msc"):
        msg.time_msc = int(mt5_result.time_msc) if mt5_result.time_msc else 0
    if hasattr(mt5_result, "time_update"):
        msg.time_update = int(mt5_result.time_update) if mt5_result.time_update else 0
    if hasattr(mt5_result, "time_update_msc"):
        msg.time_update_msc = (
            int(mt5_result.time_update_msc) if mt5_result.time_update_msc else 0
        )
    if hasattr(mt5_result, "volume"):
        msg.volume = float(mt5_result.volume) if mt5_result.volume else 0.0
    if hasattr(mt5_result, "price_open"):
        msg.price_open = (
            float(mt5_result.price_open) if mt5_result.price_open else 0.0
        )
    if hasattr(mt5_result, "sl"):
        msg.sl = float(mt5_result.sl) if mt5_result.sl else 0.0
    if hasattr(mt5_result, "tp"):
        msg.tp = float(mt5_result.tp) if mt5_result.tp else 0.0
    if hasattr(mt5_result, "price_current"):
        msg.price_current = (
            float(mt5_result.price_current) if mt5_result.price_current else 0.0
        )
    if hasattr(mt5_result, "swap"):
        msg.swap = float(mt5_result.swap) if mt5_result.swap else 0.0
    if hasattr(mt5_result, "profit"):
        msg.profit = float(mt5_result.profit) if mt5_result.profit else 0.0
    if hasattr(mt5_result, "symbol"):
        msg.symbol = str(mt5_result.symbol) if mt5_result.symbol else ""
    if hasattr(mt5_result, "comment"):
        msg.comment = str(mt5_result.comment) if mt5_result.comment else ""
    if hasattr(mt5_result, "external_id"):
        msg.external_id = (
            str(mt5_result.external_id) if mt5_result.external_id else ""
        )

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5TradePosition()
    if hasattr(mt5_result, "type"):
        mt5_msg.type = int(mt5_result.type) if mt5_result.type else 0
    if hasattr(mt5_result, "magic"):
        mt5_msg.magic = int(mt5_result.magic) if mt5_result.magic else 0
    if hasattr(mt5_result, "identifier"):
        mt5_msg.identifier = int(mt5_result.identifier) if mt5_result.identifier else 0
    if hasattr(mt5_result, "reason"):
        mt5_msg.reason = int(mt5_result.reason) if mt5_result.reason else 0

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_trade_deal(mt5_result: Any) -> types_pb2.TradeDeal:
    """
    Convert MT5 TradeDeal namedtuple to Protobuf TradeDeal message.

    Args:
        mt5_result: MT5 TradeDeal namedtuple from history_deals_get()

    Returns:
        types_pb2.TradeDeal: Protobuf message with deal history data
    """
    msg = types_pb2.TradeDeal()

    # Generic fields
    if hasattr(mt5_result, "ticket"):
        msg.ticket = int(mt5_result.ticket) if mt5_result.ticket else 0
    if hasattr(mt5_result, "order"):
        msg.order = int(mt5_result.order) if mt5_result.order else 0
    if hasattr(mt5_result, "time"):
        msg.time = int(mt5_result.time) if mt5_result.time else 0
    if hasattr(mt5_result, "time_msc"):
        msg.time_msc = int(mt5_result.time_msc) if mt5_result.time_msc else 0
    if hasattr(mt5_result, "volume"):
        msg.volume = float(mt5_result.volume) if mt5_result.volume else 0.0
    if hasattr(mt5_result, "price"):
        msg.price = float(mt5_result.price) if mt5_result.price else 0.0
    if hasattr(mt5_result, "commission"):
        msg.commission = (
            float(mt5_result.commission) if mt5_result.commission else 0.0
        )
    if hasattr(mt5_result, "swap"):
        msg.swap = float(mt5_result.swap) if mt5_result.swap else 0.0
    if hasattr(mt5_result, "profit"):
        msg.profit = float(mt5_result.profit) if mt5_result.profit else 0.0
    if hasattr(mt5_result, "fee"):
        msg.fee = float(mt5_result.fee) if mt5_result.fee else 0.0
    if hasattr(mt5_result, "symbol"):
        msg.symbol = str(mt5_result.symbol) if mt5_result.symbol else ""
    if hasattr(mt5_result, "comment"):
        msg.comment = str(mt5_result.comment) if mt5_result.comment else ""
    if hasattr(mt5_result, "external_id"):
        msg.external_id = (
            str(mt5_result.external_id) if mt5_result.external_id else ""
        )
    if hasattr(mt5_result, "position_id"):
        msg.position_id = int(mt5_result.position_id) if mt5_result.position_id else 0

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5TradeDeal()
    if hasattr(mt5_result, "type"):
        mt5_msg.type = int(mt5_result.type) if mt5_result.type else 0
    if hasattr(mt5_result, "entry"):
        mt5_msg.entry = int(mt5_result.entry) if mt5_result.entry else 0
    if hasattr(mt5_result, "magic"):
        mt5_msg.magic = int(mt5_result.magic) if mt5_result.magic else 0
    if hasattr(mt5_result, "reason"):
        mt5_msg.reason = int(mt5_result.reason) if mt5_result.reason else 0

    msg.mt5.CopyFrom(mt5_msg)
    return msg


def convert_book_info(mt5_result: Any) -> types_pb2.BookInfo:
    """
    Convert MT5 BookInfo namedtuple to Protobuf BookInfo message.

    Args:
        mt5_result: MT5 BookInfo namedtuple from mt5.market_book_get()

    Returns:
        types_pb2.BookInfo: Protobuf message with market depth entry data
    """
    msg = types_pb2.BookInfo()

    # Generic fields
    if hasattr(mt5_result, "price"):
        msg.price = float(mt5_result.price) if mt5_result.price else 0.0
    if hasattr(mt5_result, "volume"):
        msg.volume = float(mt5_result.volume) if mt5_result.volume else 0.0
    if hasattr(mt5_result, "volume_dbl"):
        msg.volume_dbl = (
            float(mt5_result.volume_dbl) if mt5_result.volume_dbl else 0.0
        )

    # MT5-specific nested message
    mt5_msg = types_pb2.Mt5BookInfo()
    if hasattr(mt5_result, "type"):
        mt5_msg.type = int(mt5_result.type) if mt5_result.type else 0

    msg.mt5.CopyFrom(mt5_msg)
    return msg
