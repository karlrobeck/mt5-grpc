"""
MT5 gRPC Market Depth Service implementation.

This module provides the MarketDepthService servicer implementation for subscribing
to and retrieving market depth (order book) information through the MT5 API.

The service handles:
- Subscribing to market depth updates for a symbol
- Retrieving current market depth data (order book)
- Unsubscribing from market depth updates
"""

from typing import Any
import MetaTrader5 as mt5

from src.stubs.market_depth_pb2_grpc import MarketDepthServiceServicer
from src.stubs import market_depth_pb2, types_pb2
from src.api.exceptions import MT5Exception
from src.api.helpers import convert_book_info


class MarketDepthService(MarketDepthServiceServicer):
    """
    gRPC service for market depth (order book) operations.

    Implements methods for subscribing to, retrieving, and unsubscribing from
    market depth information from the MetaTrader5 API through gRPC endpoints.
    Market depth operations require subscription first before data can be retrieved.
    """

    def SubscribeMarketDepth(
        self, request: market_depth_pb2.SymbolRequest, context: Any
    ) -> market_depth_pb2.MarketDepthResponse:
        """
        Subscribe to market depth changes for a symbol.

        Initiates subscription to market depth updates for the specified symbol.
        This must be called before GetDepth can retrieve data for the symbol.

        Args:
            request: SymbolRequest with symbol name
            context: gRPC context for error handling

        Returns:
            MarketDepthResponse indicating subscription success

        Raises:
            MT5Exception: If subscription fails
        """
        result = mt5.market_book_add(request.symbol)

        if not result:
            error_code, description = mt5.last_error()
            raise MT5Exception(error_code, description)

        return market_depth_pb2.MarketDepthResponse(success=result)

    def GetDepth(
        self, request: market_depth_pb2.SymbolRequest, context: Any
    ) -> market_depth_pb2.MarketDepthResponse:
        """
        Get current market depth (order book) for a symbol.

        Retrieves the current market depth data for a subscribed symbol.
        The symbol must be subscribed to first via SubscribeMarketDepth.

        Args:
            request: SymbolRequest with symbol name
            context: gRPC context for error handling

        Returns:
            MarketDepthResponse containing list of BookInfo entries

        Raises:
            MT5Exception: If symbol not subscribed or market depth unavailable
        """
        result = mt5.market_book_get(request.symbol)

        if result is None or not result:
            error_code, description = mt5.last_error()
            raise MT5Exception(error_code, description)

        # Convert each BookInfo namedtuple to protobuf message
        depth_entries = [convert_book_info(entry) for entry in result]

        return market_depth_pb2.MarketDepthResponse(
            success=True, entries=depth_entries
        )

    def UnsubscribeMarketDepth(
        self, request: market_depth_pb2.SymbolRequest, context: Any
    ) -> market_depth_pb2.MarketDepthResponse:
        """
        Unsubscribe from market depth updates for a symbol.

        Stops subscription to market depth updates for the specified symbol.

        Args:
            request: SymbolRequest with symbol name
            context: gRPC context for error handling

        Returns:
            MarketDepthResponse indicating unsubscribe success

        Raises:
            MT5Exception: If unsubscribe fails
        """
        result = mt5.market_book_release(request.symbol)

        if not result:
            error_code, description = mt5.last_error()
            raise MT5Exception(error_code, description)

        return market_depth_pb2.MarketDepthResponse(success=result)
