"""
MT5 gRPC service exception handling and error mapping.

This module provides comprehensive error handling for the MT5 gRPC service layer,
including custom exceptions and mappings between MT5 error codes and gRPC status codes.
"""

from typing import Dict, Tuple
import grpc


class MT5Exception(Exception):
    """
    Custom exception for MT5 gRPC service errors.

    Attributes:
        error_code: The MT5 error code integer
        description: Human-readable error description
    """

    def __init__(self, error_code: int, description: str) -> None:
        """
        Initialize MT5Exception.

        Args:
            error_code: The MT5 error code (integer)
            description: Human-readable description of the error
        """
        self.error_code = error_code
        self.description = description
        super().__init__(self.__str__())

    def __str__(self) -> str:
        """
        Return formatted string representation of the exception.

        Returns:
            Formatted error message with code and description
        """
        return f"MT5Exception(code={self.error_code}, description={self.description})"

    def __repr__(self) -> str:
        """Return detailed representation of the exception."""
        return self.__str__()


class MT5ErrorMapper:
    """
    Maps MT5 error codes to gRPC StatusCode values and provides error messaging.

    This class encapsulates the logic for translating MetaTrader5 error codes
    and descriptions into appropriate gRPC status codes for service responses.
    """

    # Known error patterns in descriptions for NOT_FOUND status
    _INVALID_SYMBOL_PATTERNS: Dict[str, bool] = {
        "unknown symbol": True,
        "invalid symbol": True,
        "symbol not found": True,
        "no such symbol": True,
    }

    # Error code constants
    _RES_S_OK: int = 1
    _RES_E_FAIL: int = -1

    # Keywords for margin/funds errors
    _MARGIN_FUND_KEYWORDS: Tuple[str, ...] = (
        "margin",
        "insufficient funds",
        "not enough money",
        "balance",
        "equity",
    )

    @staticmethod
    def get_grpc_status_code(
        error_code: int, description: str = ""
    ) -> grpc.StatusCode:
        """
        Map MT5 error code to appropriate gRPC StatusCode.

        Args:
            error_code: MT5 error code integer
            description: Optional error description string

        Returns:
            Appropriate grpc.StatusCode for the error

        Mapping rules:
            - Code 1 (RES_S_OK) → OK
            - Code -1 (RES_E_FAIL) → INTERNAL
            - Negative codes (account login errors) → UNAUTHENTICATED
            - Invalid symbol patterns in description → NOT_FOUND
            - Margin/funds keywords in description → FAILED_PRECONDITION
            - "terminal disconnected" in description → UNAVAILABLE
            - Unknown errors → INTERNAL
        """
        description_lower = description.lower()

        # Check for successful result
        if error_code == MT5ErrorMapper._RES_S_OK:
            return grpc.StatusCode.OK

        # Check for terminal disconnected
        if "terminal disconnected" in description_lower:
            return grpc.StatusCode.UNAVAILABLE

        # Check for invalid symbol patterns
        for pattern in MT5ErrorMapper._INVALID_SYMBOL_PATTERNS:
            if pattern in description_lower:
                return grpc.StatusCode.NOT_FOUND

        # Check for margin/funds errors
        for keyword in MT5ErrorMapper._MARGIN_FUND_KEYWORDS:
            if keyword in description_lower:
                return grpc.StatusCode.FAILED_PRECONDITION

        # Check for authentication errors (negative codes < 0)
        if error_code < 0:
            return grpc.StatusCode.UNAUTHENTICATED

        # Default to internal error
        return grpc.StatusCode.INTERNAL

    @staticmethod
    def get_error_message(error_code: int, description: str) -> str:
        """
        Generate a formatted error message from MT5 error code and description.

        Args:
            error_code: MT5 error code integer
            description: Error description string

        Returns:
            Formatted error message suitable for gRPC error details
        """
        if not description:
            description = "Unknown error"

        return f"MT5 Error Code {error_code}: {description}"
