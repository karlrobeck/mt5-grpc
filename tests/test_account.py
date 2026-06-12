import pytest
import grpc
from google.protobuf import empty_pb2
from src.stubs import account_pb2, types_pb2

class MockObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_get_account_info_success(grpc_server, mt5_mock):
    mock_info = MockObject(
        login=123456,
        leverage=100,
        trade_allowed=True,
        balance=10000.0,
        credit=0.0,
        profit=500.0,
        equity=10500.0,
        margin=1000.0,
        margin_free=9500.0,
        margin_level=1050.0,
        margin_so_call=50.0,
        margin_so_so=30.0,
        name="Test User",
        server="MT5-Server",
        currency="USD",
        company="Mock Broker",
        trade_mode=1,
        limit_orders=200,
        margin_so_mode=0,
        trade_expert=True,
        margin_mode=1,
        currency_digits=2,
        fifo_close=False,
        margin_initial=0.0,
        margin_maintenance=0.0,
        assets=0.0,
        liabilities=0.0,
        commission_blocked=0.0
    )
    mt5_mock.account_info.return_value = mock_info

    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=account_pb2.DESCRIPTOR.services_by_name['AccountService'].methods_by_name['GetAccountInfo'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.login == 123456
    assert response.balance == 10000.0
    assert response.name == "Test User"
    mt5_mock.account_info.assert_called_once()

def test_get_account_info_failure(grpc_server, mt5_mock):
    mt5_mock.account_info.return_value = None
    mt5_mock.last_error.return_value = (-1, "Terminal disconnected")

    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=account_pb2.DESCRIPTOR.services_by_name['AccountService'].methods_by_name['GetAccountInfo'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.UNAVAILABLE
    assert "Terminal disconnected" in details

def test_get_terminal_info_success(grpc_server, mt5_mock):
    mock_term = MockObject(
        community_connection=True,
        connected=True,
        dlls_allowed=True,
        trade_allowed=True,
        trade_expert=True,
        email_enabled=False,
        ftp_enabled=False,
        notifications_enabled=False,
        mqid=False,
        build=3550,
        maxbars=100000,
        codepage=1252,
        ping_last=50000,
        rank=100,
        company="Mock Broker",
        name="MetaTrader 5",
        language="English",
        path="C:\\Program Files\\MT5",
        data_path="C:\\Users\\Mock\\AppData",
        commondata_path="C:\\Users\\Mock\\AppData\\Common"
    )
    mt5_mock.terminal_info.return_value = mock_term

    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=account_pb2.DESCRIPTOR.services_by_name['AccountService'].methods_by_name['GetTerminalInfo'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.name == "MetaTrader 5"
    assert response.mt5.build == 3550
    mt5_mock.terminal_info.assert_called_once()
