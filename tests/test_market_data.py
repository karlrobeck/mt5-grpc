import pytest
import grpc
from google.protobuf import empty_pb2
from src.stubs import market_data_pb2, types_pb2

class MockObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_get_symbols_total_success(grpc_server, mt5_mock):
    mt5_mock.symbols_total.return_value = 42

    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_data_pb2.DESCRIPTOR.services_by_name['MarketDataService'].methods_by_name['GetSymbolsTotal'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.total == 42
    mt5_mock.symbols_total.assert_called_once()

def test_get_symbols_total_failure(grpc_server, mt5_mock):
    mt5_mock.symbols_total.return_value = None
    mt5_mock.last_error.return_value = (1000, "Failed count")

    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_data_pb2.DESCRIPTOR.services_by_name['MarketDataService'].methods_by_name['GetSymbolsTotal'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.INTERNAL
    assert "Failed count" in details

def test_get_symbols_success(grpc_server, mt5_mock):
    mock_symbol = MockObject(
        name="EURUSD",
        select=True,
        visible=True,
        session_deals=0,
        session_buy_orders=0,
        session_sell_orders=0,
        volume=0,
        volumehigh=0,
        volumelow=0,
        time=1600000000,
        digits=5,
        spread=10,
        spread_float=True,
        ticks_bookdepth=10,
        trade_mode=1,
        trade_state=0,
        trade_execution=2,
        volume_real=0.0,
        volumehigh_real=0.0,
        volumelow_real=0.0,
        option_mode=0,
        option_right=0,
        bid=1.1234,
        bidhigh=1.1250,
        bidlow=1.1220,
        ask=1.1235,
        askhigh=1.1251,
        asklow=1.1221,
        last=0.0,
        lasthigh=0.0,
        lastlow=0.0,
        volume_min=0.01,
        volume_max=100.0,
        volume_step=0.01,
        volume_limit=0,
        swap_long=-5.0,
        swap_short=2.0,
        swap_mode=0,
        swap_rollover3days=3,
        margin_initial=0.0,
        margin_maintenance=0.0,
        margin_hedged=0.0,
        margin_required=0.0,
        freeze_level=0.0,
        point=0.00001,
        trade_tick_value=1.0,
        trade_tick_value_profit=1.0,
        trade_tick_value_loss=1.0,
        trade_tick_size=0.00001,
        trade_contract_size=100000.0,
        trade_accrued_interest=0.0,
        trade_face_value=0.0,
        trade_liquidity_rate=0.0,
        price_strike=0.0,
        custom=False,
        chart_mode=0,
        exist=True,
        path="Forex\\EURUSD",
        description="Euro vs US Dollar",
        group="Forex",
        basis="",
        category="",
        currency_base="EUR",
        currency_profit="USD",
        currency_margin="EUR",
        bank="",
        isin="",
        order_mode=0,
        price_tier_limit=0.0,
        trade_stops_level=0,
        trade_freeze_level=0,
        price_volatility=0.0,
        start_time=0,
        expiration_time=0
    )
    mt5_mock.symbols_get.return_value = (mock_symbol,)

    req = market_data_pb2.SymbolsRequest(group="Forex")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_data_pb2.DESCRIPTOR.services_by_name['MarketDataService'].methods_by_name['GetSymbols'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.symbols) == 1
    assert response.symbols[0].name == "EURUSD"
    mt5_mock.symbols_get.assert_called_once_with(group="Forex")

def test_get_symbol_info_success(grpc_server, mt5_mock):
    mock_symbol = MockObject(
        name="GBPUSD",
        select=True,
        visible=True,
        digits=5,
        spread=12,
        spread_float=True,
        trade_mode=1,
        bid=1.3120,
        ask=1.3121,
        point=0.00001,
        trade_tick_size=0.00001,
        trade_contract_size=100000.0,
        volume_min=0.01,
        volume_max=100.0,
        volume_step=0.01,
        swap_long=-6.0,
        swap_short=1.5,
        margin_initial=0.0,
        path="Forex\\GBPUSD",
        description="Great Britain Pound vs US Dollar",
        group="Forex",
        currency_base="GBP",
        currency_profit="USD",
        currency_margin="GBP"
    )
    mt5_mock.symbol_info.return_value = mock_symbol

    req = market_data_pb2.SymbolRequest(symbol="GBPUSD")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_data_pb2.DESCRIPTOR.services_by_name['MarketDataService'].methods_by_name['GetSymbolInfo'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.name == "GBPUSD"
    mt5_mock.symbol_info.assert_called_once_with("GBPUSD")

def test_select_symbol_success(grpc_server, mt5_mock):
    mt5_mock.symbol_select.return_value = True

    req = market_data_pb2.SelectSymbolRequest(symbol="EURUSD", enable=True)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_data_pb2.DESCRIPTOR.services_by_name['MarketDataService'].methods_by_name['SelectSymbol'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.success is True
    mt5_mock.symbol_select.assert_called_once_with("EURUSD", True)
