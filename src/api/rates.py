"""
MT5 gRPC Rates Service implementation.

This module implements the RatesService gRPC servicer, providing access to
MetaTrader5 rate (OHLCV bar) data through gRPC endpoints.

The service handles:
- Retrieving bars starting from a specific date (CopyRatesFrom)
- Retrieving bars starting from a specific index position (CopyRatesFromPos)
- Retrieving bars within a date range (CopyRatesRange)

All methods return rate data converted from MT5's NumPy arrays to protobuf messages.
"""

import logging
from typing import Any

import MetaTrader5 as mt5

from src.stubs.rates_pb2_grpc import RatesServiceServicer
from src.stubs import rates_pb2, types_pb2
from src.api.exceptions import MT5Exception
from src.api.helpers import convert_rate

logger = logging.getLogger(__name__)


class RatesService(RatesServiceServicer):
    """
    Implements RatesService gRPC servicer for market rate (OHLCV) data.
    
    Provides methods to retrieve historical rate data from MetaTrader5
    and converts NumPy structured arrays to protobuf messages for gRPC responses.
    """

    def CopyRatesFrom(
        self, request: rates_pb2.RatesFromRequest, context: Any
    ) -> rates_pb2.RatesResponse:
        """
        Get bars starting from a specific date.

        Args:
            request: RatesFromRequest with symbol, timeframe, date_from, and count
            context: gRPC context for error handling

        Returns:
            RatesResponse containing list of Rate messages

        Raises:
            MT5Exception: If MT5 API call fails or invalid parameters provided
        """
        logger.debug(
            "CopyRatesFrom called: symbol=%s, timeframe=%d, date_from=%d, count=%d",
            request.symbol,
            request.timeframe,
            request.date_from.seconds,
            request.count,
        )
        
        result = mt5.copy_rates_from(
            request.symbol, request.timeframe, request.date_from.seconds, request.count
        )
        
        if result is None or (hasattr(result, "__len__") and len(result) == 0 and result is None):
            last_error = mt5.last_error()
            logger.error(
                "Failed to copy rates from: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])
        
        # Convert NumPy array to list of Rate messages
        rates = [convert_rate(rate) for rate in result]
        
        logger.debug("Successfully copied %d rates from", len(rates))
        return rates_pb2.RatesResponse(rates=rates)

    def CopyRatesFromPos(
        self, request: rates_pb2.RatesFromPosRequest, context: Any
    ) -> rates_pb2.RatesResponse:
        """
        Get bars starting from a specific index position.

        Args:
            request: RatesFromPosRequest with symbol, timeframe, start_pos, and count
            context: gRPC context for error handling

        Returns:
            RatesResponse containing list of Rate messages

        Raises:
            MT5Exception: If MT5 API call fails or invalid parameters provided
        """
        logger.debug(
            "CopyRatesFromPos called: symbol=%s, timeframe=%d, start_pos=%d, count=%d",
            request.symbol,
            request.timeframe,
            request.start_pos,
            request.count,
        )
        
        result = mt5.copy_rates_from_pos(
            request.symbol, request.timeframe, request.start_pos, request.count
        )
        
        if result is None or (hasattr(result, "__len__") and len(result) == 0 and result is None):
            last_error = mt5.last_error()
            logger.error(
                "Failed to copy rates from pos: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])
        
        # Convert NumPy array to list of Rate messages
        rates = [convert_rate(rate) for rate in result]
        
        logger.debug("Successfully copied %d rates from pos", len(rates))
        return rates_pb2.RatesResponse(rates=rates)

    def CopyRatesRange(
        self, request: rates_pb2.RatesRangeRequest, context: Any
    ) -> rates_pb2.RatesResponse:
        """
        Get bars within a date range.

        Args:
            request: RatesRangeRequest with symbol, timeframe, date_from, and date_to
            context: gRPC context for error handling

        Returns:
            RatesResponse containing list of Rate messages

        Raises:
            MT5Exception: If MT5 API call fails or invalid parameters provided
        """
        logger.debug(
            "CopyRatesRange called: symbol=%s, timeframe=%d, date_from=%d, date_to=%d",
            request.symbol,
            request.timeframe,
            request.date_from.seconds,
            request.date_to.seconds,
        )
        
        result = mt5.copy_rates_range(
            request.symbol, request.timeframe, request.date_from.seconds, request.date_to.seconds
        )
        
        if result is None or (hasattr(result, "__len__") and len(result) == 0 and result is None):
            last_error = mt5.last_error()
            logger.error(
                "Failed to copy rates range: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])
        
        # Convert NumPy array to list of Rate messages
        rates = [convert_rate(rate) for rate in result]
        
        logger.debug("Successfully copied %d rates in range", len(rates))
        return rates_pb2.RatesResponse(rates=rates)
