import pytest
import grpc
from unittest.mock import patch
from google.protobuf.timestamp_pb2 import Timestamp
from src.stubs import ticks_pb2, types_pb2

class MockObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_copy_ticks_from_success(grpc_server, mt5_mock):
    mock_tick = MockObject(
        time=1600000000,
        bid=1.1234,
        ask=1.1235,
        last=0.0,
        volume=10,
        time_msc=1600000000123,
        flags=1,
        volume_real=10.0
    )
    mt5_mock.copy_ticks_from.return_value = (mock_tick,)

    req = ticks_pb2.TickFromRequest(symbol="EURUSD", date_from=Timestamp(seconds=1600000000), count=10, flags=1)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=ticks_pb2.DESCRIPTOR.services_by_name['TickService'].methods_by_name['CopyTicksFrom'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.ticks) == 1
    assert response.ticks[0].bid == 1.1234
    mt5_mock.copy_ticks_from.assert_called_once_with("EURUSD", 1600000000, 10, 1)

def test_copy_ticks_from_failure(grpc_server, mt5_mock):
    mt5_mock.copy_ticks_from.return_value = None
    mt5_mock.last_error.return_value = (1000, "Copy ticks failed")

    req = ticks_pb2.TickFromRequest(symbol="EURUSD", date_from=Timestamp(seconds=1600000000), count=10, flags=1)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=ticks_pb2.DESCRIPTOR.services_by_name['TickService'].methods_by_name['CopyTicksFrom'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.INTERNAL
    assert "Copy ticks failed" in details

def test_copy_ticks_range_success(grpc_server, mt5_mock):
    mock_tick = MockObject(
        time=1600000000,
        bid=1.1234,
        ask=1.1235,
        last=0.0,
        volume=10,
        time_msc=1600000000123,
        flags=1,
        volume_real=10.0
    )
    mt5_mock.copy_ticks_range.return_value = (mock_tick,)

    req = ticks_pb2.TickRangeRequest(symbol="EURUSD", date_from=Timestamp(seconds=1600000000), date_to=Timestamp(seconds=1600010000), flags=1)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=ticks_pb2.DESCRIPTOR.services_by_name['TickService'].methods_by_name['CopyTicksRange'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.ticks) == 1
    mt5_mock.copy_ticks_range.assert_called_once_with("EURUSD", 1600000000, 1600010000, 1)

def test_listen_to_symbols_success(grpc_server, mt5_mock):
    mt5_mock.terminal_info.return_value = MockObject(ping_last=10000)
    mt5_mock.symbol_info.return_value = MockObject(select=True)
    
    mock_tick = MockObject(
        time=1600000000,
        bid=1.1234,
        ask=1.1235,
        last=0.0,
        volume=0,
        time_msc=1600000000123,
        flags=1,
        volume_real=0.0
    )
    mt5_mock.symbol_info_tick.return_value = mock_tick

    req = ticks_pb2.ListenToSymbolsRequest(symbols=["EURUSD"])
    
    with patch('time.sleep') as mock_sleep:
        rpc = grpc_server.invoke_unary_stream(
            method_descriptor=ticks_pb2.DESCRIPTOR.services_by_name['TickService'].methods_by_name['ListenToSymbols'],
            invocation_metadata=[
                ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
                ('x-mt5-server', 'MT5-Server')
            ],
            request=req,
            timeout=1.0
        )
        
        response = rpc.take_response()
        assert response.symbol == "EURUSD"
        assert response.ticks.bid == 1.1234
        
        rpc.cancel()
