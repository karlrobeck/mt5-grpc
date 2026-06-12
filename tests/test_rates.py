import pytest
import grpc
from src.stubs import rates_pb2, types_pb2

class MockObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_copy_rates_from_success(grpc_server, mt5_mock):
    mock_rate = MockObject(
        time=1600000000,
        open=1.1000,
        high=1.1050,
        low=1.0950,
        close=1.1020,
        tick_volume=150,
        spread=8,
        real_volume=2000
    )
    mt5_mock.copy_rates_from.return_value = (mock_rate,)

    req = rates_pb2.RatesFromRequest(symbol="EURUSD", timeframe=1, date_from=1600000000, count=10)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=rates_pb2.DESCRIPTOR.services_by_name['RatesService'].methods_by_name['CopyRatesFrom'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.rates) == 1
    assert response.rates[0].open == 1.1000
    mt5_mock.copy_rates_from.assert_called_once_with("EURUSD", 1, 1600000000, 10)

def test_copy_rates_from_failure(grpc_server, mt5_mock):
    mt5_mock.copy_rates_from.return_value = None
    mt5_mock.last_error.return_value = (1000, "Copy rates failed")

    req = rates_pb2.RatesFromRequest(symbol="EURUSD", timeframe=1, date_from=1600000000, count=10)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=rates_pb2.DESCRIPTOR.services_by_name['RatesService'].methods_by_name['CopyRatesFrom'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.INTERNAL
    assert "Copy rates failed" in details

def test_copy_rates_from_pos_success(grpc_server, mt5_mock):
    mock_rate = MockObject(
        time=1600000000,
        open=1.1000,
        high=1.1050,
        low=1.0950,
        close=1.1020,
        tick_volume=150,
        spread=8,
        real_volume=2000
    )
    mt5_mock.copy_rates_from_pos.return_value = (mock_rate,)

    req = rates_pb2.RatesFromPosRequest(symbol="EURUSD", timeframe=1, start_pos=0, count=10)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=rates_pb2.DESCRIPTOR.services_by_name['RatesService'].methods_by_name['CopyRatesFromPos'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.rates) == 1
    mt5_mock.copy_rates_from_pos.assert_called_once_with("EURUSD", 1, 0, 10)

def test_copy_rates_range_success(grpc_server, mt5_mock):
    mock_rate = MockObject(
        time=1600000000,
        open=1.1000,
        high=1.1050,
        low=1.0950,
        close=1.1020,
        tick_volume=150,
        spread=8,
        real_volume=2000
    )
    mt5_mock.copy_rates_range.return_value = (mock_rate,)

    req = rates_pb2.RatesRangeRequest(symbol="EURUSD", timeframe=1, date_from=1600000000, date_to=1600010000)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=rates_pb2.DESCRIPTOR.services_by_name['RatesService'].methods_by_name['CopyRatesRange'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.rates) == 1
    mt5_mock.copy_rates_range.assert_called_once_with("EURUSD", 1, 1600000000, 1600010000)
