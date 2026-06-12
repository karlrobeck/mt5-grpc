import pytest
import grpc
from src.stubs import market_depth_pb2, types_pb2

class MockObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_subscribe_market_depth_success(grpc_server, mt5_mock):
    mt5_mock.market_book_add.return_value = True

    req = market_depth_pb2.SymbolRequest(symbol="EURUSD")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_depth_pb2.DESCRIPTOR.services_by_name['MarketDepthService'].methods_by_name['SubscribeMarketDepth'],
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
    mt5_mock.market_book_add.assert_called_once_with("EURUSD")

def test_subscribe_market_depth_failure(grpc_server, mt5_mock):
    mt5_mock.market_book_add.return_value = False
    mt5_mock.last_error.return_value = (1000, "Sub failed")

    req = market_depth_pb2.SymbolRequest(symbol="EURUSD")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_depth_pb2.DESCRIPTOR.services_by_name['MarketDepthService'].methods_by_name['SubscribeMarketDepth'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.INTERNAL
    assert "Sub failed" in details

def test_get_depth_success(grpc_server, mt5_mock):
    mock_entry = MockObject(
        type=1, # BOOK_TYPE_SELL
        price=1.1234,
        volume=10,
        volume_dbl=10.0
    )
    mt5_mock.market_book_get.return_value = (mock_entry,)

    req = market_depth_pb2.SymbolRequest(symbol="EURUSD")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_depth_pb2.DESCRIPTOR.services_by_name['MarketDepthService'].methods_by_name['GetMarketDepth'],
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
    assert len(response.entries) == 1
    assert response.entries[0].price == 1.1234
    assert response.entries[0].mt5.type == 1
    mt5_mock.market_book_get.assert_called_once_with("EURUSD")

def test_get_depth_failure(grpc_server, mt5_mock):
    mt5_mock.market_book_get.return_value = None
    mt5_mock.last_error.return_value = (1000, "Get depth failed")

    req = market_depth_pb2.SymbolRequest(symbol="EURUSD")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_depth_pb2.DESCRIPTOR.services_by_name['MarketDepthService'].methods_by_name['GetMarketDepth'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.INTERNAL
    assert "Get depth failed" in details

def test_unsubscribe_market_depth_success(grpc_server, mt5_mock):
    mt5_mock.market_book_release.return_value = True

    req = market_depth_pb2.SymbolRequest(symbol="EURUSD")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=market_depth_pb2.DESCRIPTOR.services_by_name['MarketDepthService'].methods_by_name['UnsubscribeMarketDepth'],
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
    mt5_mock.market_book_release.assert_called_once_with("EURUSD")
