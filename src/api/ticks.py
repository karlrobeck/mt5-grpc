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

from src.stubs.ticks_pb2_grpc import TickServiceServicer
from src.stubs import ticks_pb2, types_pb2
from src.api.exceptions import MT5Exception
from src.api.helpers import convert_tick

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
            request.symbol, request.date_from.seconds, request.count, request.flags
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
            request.symbol, request.date_from.seconds, request.date_to.seconds, request.flags
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

    def ListenToSymbols(
        self, request: ticks_pb2.ListenToSymbolsRequest, context: Any
    ) -> Any:
        """
        Stream real-time tick updates for a list of symbols.

        Args:
            request: ListenToSymbolsRequest containing list of symbols
            context: gRPC context for checking connection state

        Yields:
            StreamTickResponse containing the symbol and its latest Tick
        """
        logger.info(f"ListenToSymbols request received for symbols: {request.symbols}")

        # Determine polling interval from terminal info
        terminal_info = mt5.terminal_info()
        ping_last = getattr(terminal_info, "ping_last", 0) if terminal_info is not None else 0
        if ping_last <= 0:
            ping_last = 100000  # fallback to 100ms
        
        # Determine sleep interval (min 10ms)
        interval_seconds = max(0.01, ping_last / 1000000.0)
        logger.debug(f"ListenToSymbols: ping_last={ping_last}us, using polling interval={interval_seconds}s")

        # Validate and select symbols in Market Watch
        valid_symbols = []
        for symbol in request.symbols:
            info = mt5.symbol_info(symbol)
            if info is None:
                logger.warning(f"ListenToSymbols: Symbol '{symbol}' is invalid or not found. Skipping.")
                continue
            
            # Ensure it is selected in Market Watch so tick updates are received
            if not info.select:
                if not mt5.symbol_select(symbol, True):
                    logger.warning(f"ListenToSymbols: Failed to select symbol '{symbol}' in Market Watch.")
            
            valid_symbols.append(symbol)

        if not valid_symbols:
            logger.warning("ListenToSymbols: No valid symbols specified in request.")
            return

        # Track the last seen tick for each symbol to avoid duplicates
        last_ticks_msc = {}
        last_ticks_data = {}

        import time

        while context.is_active():
            for symbol in valid_symbols:
                tick = mt5.symbol_info_tick(symbol)
                if tick is not None:
                    last_msc = last_ticks_msc.get(symbol)
                    
                    is_new = False
                    if last_msc is None:
                        is_new = True
                    elif tick.time_msc > last_msc:
                        is_new = True
                    elif tick.time_msc == last_msc:
                        # Compare critical fields for potential sub-millisecond updates
                        prev_data = last_ticks_data.get(symbol)
                        current_data = (tick.bid, tick.ask, tick.last, tick.volume_real, getattr(tick, "flags", 0))
                        if prev_data != current_data:
                            is_new = True
                    
                    if is_new:
                        last_ticks_msc[symbol] = tick.time_msc
                        last_ticks_data[symbol] = (tick.bid, tick.ask, tick.last, tick.volume_real, getattr(tick, "flags", 0))
                        
                        yield ticks_pb2.StreamTickResponse(
                            symbol=symbol,
                            ticks=convert_tick(tick)
                        )
            
            # Sleep until the next polling cycle
            time.sleep(interval_seconds)
