import sys
from unittest.mock import MagicMock

# Create and register the mock MetaTrader5 module BEFORE importing api modules
mock_mt5 = MagicMock()
# Setup defaults
mock_mt5.initialize.return_value = True
mock_mt5.shutdown.return_value = True
mock_mt5.last_error.return_value = (1, "Success")
sys.modules['MetaTrader5'] = mock_mt5

import pytest
import grpc
from grpc_testing import server_from_dictionary, strict_real_time

# gRPC stub imports
from src.stubs import (
    account_pb2,
    market_data_pb2,
    market_depth_pb2,
    rates_pb2,
    ticks_pb2,
    trade_pb2
)

# gRPC servicer imports
from src.api.account import AccountService
from src.api.market_data import MarketDataService
from src.api.market_depth import MarketDepthService
from src.api.rates import RatesService
from src.api.ticks import TicksService
from src.api.trade import TradeService

# gRPC middleware imports
from src.api.middleware import AuthenticationInterceptor, ErrorHandlingInterceptor


class InterceptedServicer:
    """
    A wrapper servicer that runs the gRPC server interceptor pipeline for grpc-testing.
    """
    def __init__(self, servicer, interceptors):
        self._servicer = servicer
        self._interceptors = interceptors

    def __getattr__(self, name):
        original_method = getattr(self._servicer, name, None)
        if original_method is None or not callable(original_method):
            raise AttributeError(f"'{self._servicer.__class__.__name__}' object has no attribute '{name}'")

        def wrapped(request, context):
            class MockHandlerCallDetails:
                def __init__(self, method_name, metadata):
                    self.method = method_name
                    self.invocation_metadata = metadata

            import inspect
            is_stream = inspect.isgeneratorfunction(original_method)

            class MockRpcMethodHandler(grpc.RpcMethodHandler):
                def __init__(self):
                    self.request_streaming = False
                    self.response_streaming = is_stream
                    if is_stream:
                        self.unary_unary = None
                        self.unary_stream = original_method
                    else:
                        self.unary_unary = original_method
                        self.unary_stream = None
                    self.stream_unary = None
                    self.stream_stream = None
                    self.request_deserializer = MagicMock()
                    self.response_serializer = MagicMock()

            # Get invocation metadata from context (handling cases where context has no metadata)
            metadata = context.invocation_metadata() if hasattr(context, 'invocation_metadata') else []
            if metadata is None:
                metadata = []

            method_path = f"/{self._servicer.__class__.__name__}/{name}"
            details = MockHandlerCallDetails(method_path, metadata)

            # Build interceptor chain
            def get_continuation(index):
                if index >= len(self._interceptors):
                    return lambda d: MockRpcMethodHandler()
                return lambda d: self._interceptors[index].intercept_service(
                    get_continuation(index + 1), d
                )

            resolved_handler = get_continuation(0)(details)

            # Invoke the correct method handler
            if is_stream:
                handler_func = resolved_handler.unary_stream or resolved_handler.unary_unary
            else:
                handler_func = resolved_handler.unary_unary or resolved_handler.unary_stream

            return handler_func(request, context)

        return wrapped


@pytest.fixture
def mt5_mock():
    """Fixture to access and configure the MetaTrader5 mock."""
    mock_mt5.reset_mock()
    mock_mt5.initialize.return_value = True
    mock_mt5.shutdown.return_value = True
    mock_mt5.last_error.return_value = (1, "Success")
    return mock_mt5


@pytest.fixture(scope='module')
def grpc_server():
    """In-memory gRPC server fixture with all servicers wrapped in interceptors."""
    # Setup test-specific authenticating interceptor
    auth_interceptor = AuthenticationInterceptor(
        expected_login="123456",
        expected_password="password123",
        expected_server="MT5-Server"
    )
    error_interceptor = ErrorHandlingInterceptor()
    interceptors = [auth_interceptor, error_interceptor]

    servicers = {
        account_pb2.DESCRIPTOR.services_by_name['AccountService']: InterceptedServicer(AccountService(), interceptors),
        market_data_pb2.DESCRIPTOR.services_by_name['MarketDataService']: InterceptedServicer(MarketDataService(), interceptors),
        market_depth_pb2.DESCRIPTOR.services_by_name['MarketDepthService']: InterceptedServicer(MarketDepthService(), interceptors),
        rates_pb2.DESCRIPTOR.services_by_name['RatesService']: InterceptedServicer(RatesService(), interceptors),
        ticks_pb2.DESCRIPTOR.services_by_name['TickService']: InterceptedServicer(TicksService(), interceptors),
        trade_pb2.DESCRIPTOR.services_by_name['TradeService']: InterceptedServicer(TradeService(), interceptors),
    }

    return server_from_dictionary(servicers, strict_real_time())
