"""
MT5 gRPC Account Service implementation.

This module implements the AccountService gRPC servicer, providing access to
MetaTrader5 account and terminal information through gRPC endpoints.
"""

import logging
from typing import Any

import MetaTrader5 as mt5
from google.protobuf import empty_pb2

from api.exceptions import MT5Exception
from api.helpers import convert_account_info, convert_terminal_info
from stubs.account_pb2_grpc import AccountServiceServicer
from stubs import types_pb2

logger = logging.getLogger(__name__)


class AccountService(AccountServiceServicer):
    """
    Implements AccountService gRPC servicer for trading account information.
    
    Provides methods to retrieve account and terminal information from MetaTrader5
    and converts them to protobuf messages for gRPC responses.
    """

    def GetAccountInfo(
        self, request: empty_pb2.Empty, context: Any
    ) -> types_pb2.AccountInfo:
        """
        Get current trading account information.

        Args:
            request: Empty protobuf message
            context: gRPC context

        Returns:
            AccountInfo protobuf message with account details

        Raises:
            MT5Exception: If account info retrieval fails
        """
        logger.debug("GetAccountInfo called")
        result = mt5.account_info()
        
        if not result:
            last_error = mt5.last_error()
            logger.error(
                "Failed to retrieve account info: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])
        
        logger.debug("Successfully retrieved account info")
        return convert_account_info(result)

    def GetTerminalInfo(
        self, request: empty_pb2.Empty, context: Any
    ) -> types_pb2.TerminalInfo:
        """
        Get terminal connection and configuration information.

        Args:
            request: Empty protobuf message
            context: gRPC context

        Returns:
            TerminalInfo protobuf message with terminal details

        Raises:
            MT5Exception: If terminal info retrieval fails
        """
        logger.debug("GetTerminalInfo called")
        result = mt5.terminal_info()
        
        if not result:
            last_error = mt5.last_error()
            logger.error(
                "Failed to retrieve terminal info: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])
        
        logger.debug("Successfully retrieved terminal info")
        return convert_terminal_info(result)
