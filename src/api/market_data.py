"""
MT5 gRPC Market Data Service Implementation.

This module provides the MarketDataService servicer implementation for retrieving
symbol information and managing MarketWatch selections through the MT5 API.

The service handles:
- Retrieving total symbol count
- Fetching filtered symbol lists
- Getting detailed symbol information
- Managing symbol selection in MarketWatch
"""

from typing import Optional
import MetaTrader5 as mt5

from src.stubs.market_data_pb2_grpc import MarketDataServiceServicer
from src.stubs import market_data_pb2, types_pb2
from src.api.exceptions import MT5Exception
from src.api.helpers import convert_symbol_info, convert_tick


class MarketDataService(MarketDataServiceServicer):
    """
    gRPC service for market data operations.

    Implements methods for retrieving symbol information and managing MarketWatch
    from the MetaTrader5 API through gRPC endpoints.
    """

    def GetSymbolsTotal(self, request, context) -> market_data_pb2.SymbolsTotalResponse:
        """
        Get total count of all available symbols.

        Args:
            request: google.protobuf.empty_pb2.Empty request (unused)
            context: gRPC context for error handling

        Returns:
            SymbolsTotalResponse with the total count of symbols

        Raises:
            MT5Exception: If MT5 API call fails
        """
        result = mt5.symbols_total()

        if not result:
            error_code, description = mt5.last_error()
            raise MT5Exception(error_code, description)

        return market_data_pb2.SymbolsTotalResponse(total=result)

    def GetSymbols(self, request, context) -> market_data_pb2.SymbolsResponse:
        """
        Get list of symbols, optionally filtered by group.

        Args:
            request: SymbolsRequest with optional group filter
            context: gRPC context for error handling

        Returns:
            SymbolsResponse containing list of SymbolInfo messages

        Raises:
            MT5Exception: If MT5 API call fails
        """
        # Convert empty string to None for group parameter
        group = request.group if request.group else None

        result = mt5.symbols_get(group=group)

        if result is None:
            error_code, description = mt5.last_error()
            raise MT5Exception(error_code, description)

        # Convert each symbol to protobuf format
        symbols = [convert_symbol_info(symbol) for symbol in result]

        return market_data_pb2.SymbolsResponse(symbols=symbols)

    def GetSymbolInfo(self, request, context) -> types_pb2.SymbolInfo:
        """
        Get detailed information for a specific symbol.

        Args:
            request: SymbolRequest with symbol name
            context: gRPC context for error handling

        Returns:
            SymbolInfo protobuf message with detailed symbol data

        Raises:
            MT5Exception: If MT5 API call fails or symbol not found
        """
        result = mt5.symbol_info(request.symbol)

        if result is None:
            error_code, description = mt5.last_error()
            raise MT5Exception(error_code, description)

        return convert_symbol_info(result)

    def GetSymbolInfoTick(self, request, context) -> types_pb2.Tick:
        """
        Get the last tick for a specific symbol.

        Args:
            request: SymbolRequest with symbol name
            context: gRPC context for error handling

        Returns:
            Tick protobuf message with the latest tick data

        Raises:
            MT5Exception: If MT5 API call fails or tick not found
        """
        result = mt5.symbol_info_tick(request.symbol)

        if result is None:
            error_code, description = mt5.last_error()
            raise MT5Exception(error_code, description)

        return convert_tick(result)

    def SelectSymbol(
        self, request, context
    ) -> market_data_pb2.SelectSymbolResponse:
        """
        Add or remove symbol from MarketWatch.

        Args:
            request: SelectSymbolRequest with symbol name and enable flag
            context: gRPC context for error handling

        Returns:
            SelectSymbolResponse indicating success/failure of operation

        Raises:
            MT5Exception: If MT5 API call fails
        """
        result = mt5.symbol_select(request.symbol, request.enable)

        if not result:
            error_code, description = mt5.last_error()
            raise MT5Exception(error_code, description)

        return market_data_pb2.SelectSymbolResponse(success=result)
