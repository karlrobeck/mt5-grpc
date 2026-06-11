"""
gRPC middleware for MT5 service layer.

This module provides gRPC interceptors for error handling and request/response
processing in the MT5 gRPC service.
"""

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

        # Create a wrapper function for the actual RPC call
        def wrapper(request: Any, context: grpc.ServicerContext) -> Any:
            """
            Wrapper function that executes the handler with exception handling.

            Args:
                request: The request message
                context: The gRPC context

            Returns:
                The response from the handler

            Raises:
                grpc.RpcError: If an MT5Exception is caught
            """
            try:
                # Call the original handler
                return handler.unary_unary(request, context)
            except MT5Exception as e:
                # Log the MT5 error details
                logger.error(
                    f"MT5Exception caught: {e}",
                    extra={
                        "error_code": e.error_code,
                        "description": e.description,
                    },
                )

                # Map MT5 error code to gRPC status code
                status_code = MT5ErrorMapper.get_grpc_status_code(
                    e.error_code, e.description
                )

                # Generate error message
                error_message = MT5ErrorMapper.get_error_message(
                    e.error_code, e.description
                )

                # Abort with appropriate gRPC status
                context.abort(status_code, error_message)
            except Exception as e:
                # Log any other exceptions and re-raise
                logger.exception(
                    f"Unexpected exception in RPC handler: {type(e).__name__}: {e}"
                )
                raise

        # Return a new handler with the wrapped function
        return grpc.unary_unary_rpc_method_handler(
            wrapper,
            request_deserializer=handler.request_deserializer,
            response_serializer=handler.response_serializer,
        )
