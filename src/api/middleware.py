"""
gRPC middleware for MT5 service layer.

This module provides gRPC interceptors for error handling and request/response
processing in the MT5 gRPC service.
"""

import base64
import logging
from typing import Callable, Any

import grpc

from src.api.exceptions import MT5Exception, MT5ErrorMapper


logger = logging.getLogger(__name__)


class ErrorHandlingInterceptor(grpc.ServerInterceptor):
    """
    gRPC server interceptor for handling MT5 exceptions.

    This interceptor intercepts all RPC calls, catches MT5Exception instances,
    and converts them to appropriate gRPC error responses with proper status codes
    and error messages.
    """

    def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], grpc.RpcMethodHandler
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        """
        Intercept service calls and handle MT5 exceptions.

        This method wraps the RPC handler to catch MT5Exception instances and
        convert them to appropriate gRPC error responses.

        Args:
            continuation: Callable to get the next handler in the chain
            handler_call_details: Details about the RPC call

        Returns:
            A wrapped RpcMethodHandler that handles exceptions
        """
        # Get the original handler from the continuation
        handler = continuation(handler_call_details)
        if handler is None:
            return None

        # Check if the handler is unary-unary
        if handler.unary_unary is not None:
            def wrapper_unary(request: Any, context: grpc.ServicerContext) -> Any:
                try:
                    return handler.unary_unary(request, context)
                except MT5Exception as e:
                    logger.error(
                        f"MT5Exception caught: {e}",
                        extra={
                            "error_code": e.error_code,
                            "description": e.description,
                        },
                    )
                    status_code = MT5ErrorMapper.get_grpc_status_code(
                        e.error_code, e.description
                    )
                    error_message = MT5ErrorMapper.get_error_message(
                        e.error_code, e.description
                    )
                    context.abort(status_code, error_message)
                except Exception as e:
                    logger.exception(
                        f"Unexpected exception in RPC handler: {type(e).__name__}: {e}"
                    )
                    raise

            return grpc.unary_unary_rpc_method_handler(
                wrapper_unary,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        # Check if the handler is unary-stream (server streaming)
        elif handler.unary_stream is not None:
            def wrapper_stream(request: Any, context: grpc.ServicerContext) -> Any:
                try:
                    iterator = handler.unary_stream(request, context)
                    for response in iterator:
                        yield response
                except MT5Exception as e:
                    logger.error(
                        f"MT5Exception caught in stream: {e}",
                        extra={
                            "error_code": e.error_code,
                            "description": e.description,
                        },
                    )
                    status_code = MT5ErrorMapper.get_grpc_status_code(
                        e.error_code, e.description
                    )
                    error_message = MT5ErrorMapper.get_error_message(
                        e.error_code, e.description
                    )
                    context.abort(status_code, error_message)
                except Exception as e:
                    logger.exception(
                        f"Unexpected exception in streaming RPC handler: {type(e).__name__}: {e}"
                    )
                    raise

            return grpc.unary_stream_rpc_method_handler(
                wrapper_stream,
                request_deserializer=handler.request_deserializer,
                response_serializer=handler.response_serializer,
            )

        return handler


class _AbortHandler(grpc.RpcMethodHandler):
    """A gRPC method handler that immediately aborts with UNAUTHENTICATED."""

    def __init__(self):
        self.request_streaming = False
        self.response_streaming = False
        self.unary_unary = self._abort
        self.unary_stream = self._abort
        self.stream_unary = self._abort
        self.stream_stream = self._abort

    def _abort(self, request_or_iterator: Any, context: grpc.ServicerContext) -> Any:
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Unauthenticated")


class AuthenticationInterceptor(grpc.ServerInterceptor):
    """
    gRPC server interceptor for validating client credentials and server settings.
    """

    def __init__(
        self,
        expected_login: str | None = None,
        expected_password: str | None = None,
        expected_server: str | None = None,
    ):
        self.expected_login = expected_login
        self.expected_password = expected_password
        self.expected_server = expected_server

    def intercept_service(
        self,
        continuation: Callable[
            [grpc.HandlerCallDetails], grpc.RpcMethodHandler
        ],
        handler_call_details: grpc.HandlerCallDetails,
    ) -> grpc.RpcMethodHandler:
        # Retrieve metadata
        authorization_header = None
        x_mt5_server_header = None

        if handler_call_details.invocation_metadata:
            for key, val in handler_call_details.invocation_metadata:
                key_lower = key.lower()
                if key_lower == "authorization":
                    authorization_header = val
                elif key_lower == "x-mt5-server":
                    x_mt5_server_header = val

        # Helper to convert metadata values to string
        def _to_str(val: Any) -> str:
            if isinstance(val, bytes):
                return val.decode("utf-8")
            return str(val)

        # Validate Authorization if login/password are configured
        if self.expected_login is not None and self.expected_password is not None:
            auth_ok = False
            if authorization_header:
                auth_str = _to_str(authorization_header)
                if auth_str.lower().startswith("basic "):
                    encoded_creds = auth_str[6:].strip()
                    try:
                        decoded_creds = base64.b64decode(encoded_creds).decode("utf-8")
                        if ":" in decoded_creds:
                            login_part, password_part = decoded_creds.split(":", 1)
                            if login_part == str(self.expected_login) and password_part == self.expected_password:
                                auth_ok = True
                    except Exception:
                        pass
            
            if not auth_ok:
                logger.warning("Authentication failed: invalid or missing Authorization header")
                return _AbortHandler()

        # Validate X-MT5-Server if server is configured
        if self.expected_server is not None:
            server_ok = False
            if x_mt5_server_header:
                server_str = _to_str(x_mt5_server_header)
                if server_str.lower() == str(self.expected_server).lower():
                    server_ok = True
            
            if not server_ok:
                logger.warning(
                    f"Authentication failed: invalid or missing X-MT5-Server header. "
                    f"Expected: {self.expected_server}"
                )
                return _AbortHandler()

        return continuation(handler_call_details)
