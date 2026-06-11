"""
MT5 gRPC Ticks Service Implementation.

This module provides the TicksService servicer implementation for retrieving
tick data (market ticks) from the MetaTrader5 API through gRPC endpoints.

The service handles:
- Getting ticks starting from a specific date (CopyTicksFrom)
- Getting ticks within a date range (CopyTicksRange)
"""

import logging
from typing import Any
import MetaTrader5 as mt5

from stubs.ticks_pb2_grpc import TickServiceServicer
from stubs import ticks_pb2, types_pb2
from api.exceptions import MT5Exception
from api.helpers import convert_tick

# Configure logging for this module
logger = logging.getLogger(__name__)


class TicksService(TickServiceServicer):
    """
    gRPC service for tick data operations.

    Implements methods for retrieving tick data (market ticks) from the
    MetaTrader5 API through gRPC endpoints. Ticks represent individual
    market price updates for a given symbol.
    """

    def CopyTicksFrom(
        self, request: ticks_pb2.TickFromRequest, context: Any
    ) -> ticks_pb2.TicksResponse:
        """
        Get ticks starting from a specific date.

        Retrieves tick data for a symbol starting from a specified date/time,
        with a maximum count of ticks to retrieve.

        Args:
            request: TickFromRequest with symbol, date_from, count, and flags
            context: gRPC context for error handling

        Returns:
            TicksResponse containing list of Tick messages

        Raises:
            MT5Exception: If MT5 API call fails
        """
        logger.debug(
            f"CopyTicksFrom: symbol={request.symbol}, date_from={request.date_from}, "
            f"count={request.count}, flags={request.flags}"
        )

        # Call MT5 API to get ticks starting from a specific date
        result = mt5.copy_ticks_from(
            request.symbol, request.date_from, request.count, request.flags
        )

        # Check if result is falsy (None or empty array)
        if result is None or (hasattr(result, '__len__') and len(result) == 0):
            if result is None:
                error_code, description = mt5.last_error()
                logger.error(
                    f"CopyTicksFrom failed: error_code={error_code}, description={description}"
                )
                raise MT5Exception(error_code, description)
            # Empty result is not an error, return empty list
            logger.debug(f"CopyTicksFrom returned empty result for {request.symbol}")
            return ticks_pb2.TicksResponse(ticks=[])

        # Convert each tick record to protobuf format
        ticks = [convert_tick(tick) for tick in result]
        logger.debug(f"CopyTicksFrom returned {len(ticks)} ticks for {request.symbol}")

        return ticks_pb2.TicksResponse(ticks=ticks)

    def CopyTicksRange(
        self, request: ticks_pb2.TickRangeRequest, context: Any
    ) -> ticks_pb2.TicksResponse:
        """
        Get ticks within a date range.

        Retrieves tick data for a symbol within a specified date/time range.
        Returns all ticks that occur between date_from and date_to (inclusive).

        Args:
            request: TickRangeRequest with symbol, date_from, date_to, and flags
            context: gRPC context for error handling

        Returns:
            TicksResponse containing list of Tick messages

        Raises:
            MT5Exception: If MT5 API call fails
        """
        logger.debug(
            f"CopyTicksRange: symbol={request.symbol}, date_from={request.date_from}, "
            f"date_to={request.date_to}, flags={request.flags}"
        )

        # Call MT5 API to get ticks within a date range
        result = mt5.copy_ticks_range(
            request.symbol, request.date_from, request.date_to, request.flags
        )

        # Check if result is falsy (None or empty array)
        if result is None or (hasattr(result, '__len__') and len(result) == 0):
            if result is None:
                error_code, description = mt5.last_error()
                logger.error(
                    f"CopyTicksRange failed: error_code={error_code}, description={description}"
                )
                raise MT5Exception(error_code, description)
            # Empty result is not an error, return empty list
            logger.debug(
                f"CopyTicksRange returned empty result for {request.symbol} "
                f"between {request.date_from} and {request.date_to}"
            )
            return ticks_pb2.TicksResponse(ticks=[])

        # Convert each tick record to protobuf format
        ticks = [convert_tick(tick) for tick in result]
        logger.debug(
            f"CopyTicksRange returned {len(ticks)} ticks for {request.symbol}"
        )

        return ticks_pb2.TicksResponse(ticks=ticks)
