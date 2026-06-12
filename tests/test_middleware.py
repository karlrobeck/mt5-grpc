import pytest
import grpc
from google.protobuf import empty_pb2
from src.stubs import account_pb2

def test_auth_missing_metadata(grpc_server):
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=account_pb2.DESCRIPTOR.services_by_name['AccountService'].methods_by_name['GetAccountInfo'],
        invocation_metadata=[],
        request=empty_pb2.Empty(),
        timeout=1.0
    )
    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.UNAUTHENTICATED
    assert "Unauthenticated" in details

def test_auth_wrong_credentials(grpc_server):
    # Base64 of 'wrong_user:wrong_pass' is 'd3JvbmdfdXNlcjp3cm9uZ19wYXNz'
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=account_pb2.DESCRIPTOR.services_by_name['AccountService'].methods_by_name['GetAccountInfo'],
        invocation_metadata=[
            ('authorization', 'Basic d3JvbmdfdXNlcjp3cm9uZ19wYXNz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )
    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.UNAUTHENTICATED

def test_auth_wrong_server_header(grpc_server):
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=account_pb2.DESCRIPTOR.services_by_name['AccountService'].methods_by_name['GetAccountInfo'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'WRONG-SERVER')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )
    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.UNAUTHENTICATED

def test_error_mapping_terminal_disconnected(grpc_server, mt5_mock):
    mt5_mock.account_info.return_value = None
    mt5_mock.last_error.return_value = (1001, "The terminal disconnected from broker")

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

def test_error_mapping_invalid_symbol(grpc_server, mt5_mock):
    mt5_mock.account_info.return_value = None
    mt5_mock.last_error.return_value = (1002, "Symbol not found in MarketWatch")

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
    assert code == grpc.StatusCode.NOT_FOUND

def test_error_mapping_insufficient_funds(grpc_server, mt5_mock):
    mt5_mock.account_info.return_value = None
    mt5_mock.last_error.return_value = (1003, "Not enough money/margin to perform trade")

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
    assert code == grpc.StatusCode.FAILED_PRECONDITION

def test_error_mapping_negative_code(grpc_server, mt5_mock):
    mt5_mock.account_info.return_value = None
    mt5_mock.last_error.return_value = (-5, "Login authorization failed")

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
    assert code == grpc.StatusCode.UNAUTHENTICATED

def test_error_mapping_general_internal(grpc_server, mt5_mock):
    mt5_mock.account_info.return_value = None
    mt5_mock.last_error.return_value = (999, "Some general MT5 error occurred")

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
    assert code == grpc.StatusCode.INTERNAL
