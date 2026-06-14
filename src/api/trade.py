"""
MT5 gRPC Trade Service implementation.

This module implements the TradeService gRPC servicer, providing access to
MetaTrader5 trading operations including orders, positions, and history
through gRPC endpoints.
"""

import logging
from typing import Any, Dict, Optional

import MetaTrader5 as mt5
from google.protobuf import empty_pb2

from src.api.exceptions import MT5Exception
from src.api.helpers import (
    convert_trade_deal,
    convert_trade_order,
    convert_trade_position,
)
from src.stubs import trade_pb2, types_pb2
from src.stubs.trade_pb2_grpc import TradeServiceServicer

logger = logging.getLogger(__name__)


class TradeService(TradeServiceServicer):
    """
    Implements TradeService gRPC servicer for trading operations.

    Provides methods to retrieve orders, positions, history, and perform
    trading calculations and operations through MetaTrader5 API.
    """

    def GetOrdersTotal(
        self, request: empty_pb2.Empty, context: Any
    ) -> trade_pb2.OrdersTotalResponse:
        """
        Get total count of current orders.

        Args:
            request: Empty protobuf message
            context: gRPC context

        Returns:
            OrdersTotalResponse with total order count

        Raises:
            MT5Exception: If order count retrieval fails
        """
        logger.debug("GetOrdersTotal called")
        result = mt5.orders_total()

        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to get orders total: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        logger.debug("Successfully retrieved orders total: %d", result)
        return trade_pb2.OrdersTotalResponse(total=result)

    def GetOrders(
        self, request: trade_pb2.OrdersRequest, context: Any
    ) -> trade_pb2.OrdersResponse:
        """
        Get list of current orders with optional filtering.

        Args:
            request: OrdersRequest with optional symbol, group, or ticket filters
            context: gRPC context

        Returns:
            OrdersResponse with list of TradeOrder messages

        Raises:
            MT5Exception: If order retrieval fails
        """
        logger.debug(
            "GetOrders called with symbol=%s, group=%s, ticket=%d",
            request.symbol,
            request.group,
            request.ticket,
        )

        # Convert empty strings to None for optional filters
        symbol = request.symbol if request.symbol else None
        group = request.group if request.group else None
        ticket = request.ticket if request.ticket else None

        result = mt5.orders_get(symbol=symbol, group=group, ticket=ticket)

        # Handle empty result gracefully (no orders found is not an error)
        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to get orders: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        # Convert each order to protobuf message
        orders = [convert_trade_order(order) for order in result]
        logger.debug("Successfully retrieved %d orders", len(orders))
        return trade_pb2.OrdersResponse(orders=orders)

    def GetPositionsTotal(
        self, request: empty_pb2.Empty, context: Any
    ) -> trade_pb2.PositionsTotalResponse:
        """
        Get total count of current positions.

        Args:
            request: Empty protobuf message
            context: gRPC context

        Returns:
            PositionsTotalResponse with total position count

        Raises:
            MT5Exception: If position count retrieval fails
        """
        logger.debug("GetPositionsTotal called")
        result = mt5.positions_total()

        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to get positions total: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        logger.debug("Successfully retrieved positions total: %d", result)
        return trade_pb2.PositionsTotalResponse(total=result)

    def GetPositions(
        self, request: trade_pb2.PositionsRequest, context: Any
    ) -> trade_pb2.PositionsResponse:
        """
        Get list of current positions with optional filtering.

        Args:
            request: PositionsRequest with optional symbol, group, or ticket filters
            context: gRPC context

        Returns:
            PositionsResponse with list of TradePosition messages

        Raises:
            MT5Exception: If position retrieval fails
        """
        logger.debug(
            "GetPositions called with symbol=%s, group=%s, ticket=%d",
            request.symbol,
            request.group,
            request.ticket,
        )

        # Convert empty strings to None for optional filters
        symbol = request.symbol if request.symbol else None
        group = request.group if request.group else None
        ticket = request.ticket if request.ticket else None

        result = mt5.positions_get(symbol=symbol, group=group, ticket=ticket)

        # Handle empty result gracefully (no positions found is not an error)
        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to get positions: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        # Convert each position to protobuf message
        positions = [convert_trade_position(position) for position in result]
        logger.debug("Successfully retrieved %d positions", len(positions))
        return trade_pb2.PositionsResponse(positions=positions)

    def GetHistoryOrdersTotal(
        self, request: trade_pb2.HistoryRangeRequest, context: Any
    ) -> trade_pb2.HistoryOrdersTotalResponse:
        """
        Get total count of historical orders in date range.

        Args:
            request: HistoryRangeRequest with date_from and date_to
            context: gRPC context

        Returns:
            HistoryOrdersTotalResponse with total count

        Raises:
            MT5Exception: If history orders total retrieval fails
        """
        logger.debug(
            "GetHistoryOrdersTotal called with date_from=%d, date_to=%d",
            request.date_from.seconds,
            request.date_to.seconds,
        )

        result = mt5.history_orders_total(request.date_from.seconds, request.date_to.seconds)

        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to get history orders total: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        logger.debug("Successfully retrieved history orders total: %d", result)
        return trade_pb2.HistoryOrdersTotalResponse(total=result)

    def GetHistoryOrders(
        self, request: trade_pb2.HistoryOrdersRequest, context: Any
    ) -> trade_pb2.HistoryOrdersResponse:
        """
        Get list of historical orders with optional filtering.

        Args:
            request: HistoryOrdersRequest with date range and optional filters
            context: gRPC context

        Returns:
            HistoryOrdersResponse with list of TradeOrder messages

        Raises:
            MT5Exception: If history orders retrieval fails
        """
        logger.debug(
            "GetHistoryOrders called with date_from=%d, date_to=%d, group=%s, ticket=%d, position=%d",
            request.date_from.seconds,
            request.date_to.seconds,
            request.group,
            request.ticket,
            request.position,
        )

        # Convert empty strings to None for optional filters
        group = request.group if request.group else None
        ticket = request.ticket if request.ticket else None
        position = request.position if request.position else None

        if ticket is not None or position is not None:
            # Query history globally by ticket or position
            result = mt5.history_orders_get(
                group=group,
                ticket=ticket,
                position=position,
            )
        else:
            result = mt5.history_orders_get(
                date_from=request.date_from.seconds,
                date_to=request.date_to.seconds,
                group=group,
            )

        # Handle empty result gracefully (no history found is not an error)
        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to get history orders: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        # Convert each order to protobuf message
        orders = [convert_trade_order(order) for order in result]
        logger.debug("Successfully retrieved %d history orders", len(orders))
        return trade_pb2.HistoryOrdersResponse(orders=orders)

    def GetHistoryDealsTotal(
        self, request: trade_pb2.HistoryRangeRequest, context: Any
    ) -> trade_pb2.HistoryDealsTotalResponse:
        """
        Get total count of historical deals in date range.

        Args:
            request: HistoryRangeRequest with date_from and date_to
            context: gRPC context

        Returns:
            HistoryDealsTotalResponse with total count

        Raises:
            MT5Exception: If history deals total retrieval fails
        """
        logger.debug(
            "GetHistoryDealsTotal called with date_from=%d, date_to=%d",
            request.date_from.seconds,
            request.date_to.seconds,
        )

        result = mt5.history_deals_total(request.date_from.seconds, request.date_to.seconds)

        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to get history deals total: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        logger.debug("Successfully retrieved history deals total: %d", result)
        return trade_pb2.HistoryDealsTotalResponse(total=result)

    def GetHistoryDeals(
        self, request: trade_pb2.HistoryDealsRequest, context: Any
    ) -> trade_pb2.HistoryDealsResponse:
        """
        Get list of historical deals with optional filtering.

        Args:
            request: HistoryDealsRequest with date range and optional filters
            context: gRPC context

        Returns:
            HistoryDealsResponse with list of TradeDeal messages

        Raises:
            MT5Exception: If history deals retrieval fails
        """
        logger.debug(
            "GetHistoryDeals called with date_from=%d, date_to=%d, group=%s, ticket=%d, position=%d",
            request.date_from.seconds,
            request.date_to.seconds,
            request.group,
            request.ticket,
            request.position,
        )

        # Convert empty strings to None for optional filters
        group = request.group if request.group else None
        ticket = request.ticket if request.ticket else None
        position = request.position if request.position else None

        if ticket is not None or position is not None:
            # Query history globally by ticket or position
            result = mt5.history_deals_get(
                group=group,
                ticket=ticket,
                position=position,
            )
        else:
            result = mt5.history_deals_get(
                date_from=request.date_from.seconds,
                date_to=request.date_to.seconds,
                group=group,
            )

        # Handle empty result gracefully (no history found is not an error)
        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to get history deals: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        # Convert each deal to protobuf message
        deals = [convert_trade_deal(deal) for deal in result]
        logger.debug("Successfully retrieved %d history deals", len(deals))
        return trade_pb2.HistoryDealsResponse(deals=deals)

    def CalcMargin(
        self, request: trade_pb2.CalcMarginRequest, context: Any
    ) -> trade_pb2.CalcMarginResponse:
        """
        Calculate required margin for a trade request.

        Args:
            request: CalcMarginRequest with trade request details
            context: gRPC context

        Returns:
            CalcMarginResponse with calculated margin value

        Raises:
            MT5Exception: If margin calculation fails
        """
        logger.debug("CalcMargin called")

        result = mt5.order_calc_margin(
            request.action,
            request.symbol,
            request.volume,
            request.price,
        )

        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to calculate margin: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        logger.debug("Successfully calculated margin: %f", result)
        return trade_pb2.CalcMarginResponse(margin=result)

    def CalcProfit(
        self, request: trade_pb2.CalcProfitRequest, context: Any
    ) -> trade_pb2.CalcProfitResponse:
        """
        Calculate potential profit for a trade request.

        Args:
            request: CalcProfitRequest with trade request details
            context: gRPC context

        Returns:
            CalcProfitResponse with calculated profit value

        Raises:
            MT5Exception: If profit calculation fails
        """
        logger.debug("CalcProfit called")

        result = mt5.order_calc_profit(
            request.action,
            request.symbol,
            request.volume,
            request.price_open,
            request.price_close,
        )

        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to calculate profit: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        logger.debug("Successfully calculated profit: %f", result)
        return trade_pb2.CalcProfitResponse(profit=result)

    def CheckOrder(
        self, request: trade_pb2.CheckOrderRequest, context: Any
    ) -> types_pb2.TradeCheckResult:
        """
        Check if a trade order can be executed.

        Args:
            request: CheckOrderRequest with trade request to validate
            context: gRPC context

        Returns:
            TradeCheckResult with order validation details

        Raises:
            MT5Exception: If order check fails
        """
        logger.debug("CheckOrder called")

        # Convert gRPC TradeRequest to MT5 Python dict
        trade_dict = self._convert_trade_request_to_dict(request.request)

        # Call MT5 order_check
        result = mt5.order_check(trade_dict)

        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to check order: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        # Convert result to protobuf
        check_result = types_pb2.TradeCheckResult()
        check_result.retcode = int(result.retcode) if result.retcode else 0
        check_result.balance = float(result.balance) if result.balance else 0.0
        check_result.equity = float(result.equity) if result.equity else 0.0
        check_result.profit = float(result.profit) if result.profit else 0.0
        check_result.margin = float(result.margin) if result.margin else 0.0
        check_result.margin_free = (
            float(result.margin_free) if result.margin_free else 0.0
        )
        check_result.margin_level = (
            float(result.margin_level) if result.margin_level else 0.0
        )
        check_result.comment = str(result.comment) if result.comment else ""

        # Copy the request
        check_result.request.CopyFrom(self._convert_dict_to_trade_request(trade_dict))

        logger.debug("Successfully checked order: retcode=%d", check_result.retcode)
        return check_result

    def SendOrder(
        self, request: trade_pb2.SendOrderRequest, context: Any
    ) -> types_pb2.TradeSendResult:
        """
        Send a trade order for execution.

        Args:
            request: SendOrderRequest with trade request to execute
            context: gRPC context

        Returns:
            TradeSendResult with order execution details

        Raises:
            MT5Exception: If order send fails
        """
        logger.debug("SendOrder called")

        # Convert gRPC TradeRequest to MT5 Python dict
        trade_dict = self._convert_trade_request_to_dict(request.request)

        # Call MT5 order_send
        result = mt5.order_send(trade_dict)

        if result is None:
            last_error = mt5.last_error()
            logger.error(
                "Failed to send order: %s (code: %d)",
                last_error[1],
                last_error[0],
            )
            raise MT5Exception(last_error[0], last_error[1])

        # Convert result to protobuf
        send_result = types_pb2.TradeSendResult()
        send_result.retcode = int(result.retcode) if result.retcode else 0
        send_result.deal = int(result.deal) if result.deal else 0
        send_result.order = int(result.order) if result.order else 0
        send_result.volume = float(result.volume) if result.volume else 0.0
        send_result.price = float(result.price) if result.price else 0.0
        send_result.bid = float(result.bid) if result.bid else 0.0
        send_result.ask = float(result.ask) if result.ask else 0.0
        send_result.comment = str(result.comment) if result.comment else ""
        send_result.request_id = (
            int(result.request_id) if hasattr(result, "request_id") and result.request_id else 0
        )
        send_result.retcode_external = (
            int(result.retcode_external)
            if hasattr(result, "retcode_external") and result.retcode_external
            else 0
        )

        # Copy the request
        send_result.request.CopyFrom(self._convert_dict_to_trade_request(trade_dict))

        logger.debug("Successfully sent order: retcode=%d, deal=%d", send_result.retcode, send_result.deal)
        return send_result

    @staticmethod
    def _convert_trade_request_to_dict(trade_request: types_pb2.TradeRequest) -> Dict[str, Any]:
        """
        Convert gRPC TradeRequest protobuf to MT5 dictionary format.

        Args:
            trade_request: gRPC TradeRequest message

        Returns:
            Dictionary in MT5 order_send/order_check format
        """
        request_dict: Dict[str, Any] = {}

        # Generic fields
        if trade_request.HasField("symbol"):
            request_dict["symbol"] = trade_request.symbol
        if trade_request.HasField("volume"):
            request_dict["volume"] = trade_request.volume
        if trade_request.HasField("price"):
            request_dict["price"] = trade_request.price
        if trade_request.HasField("stoplimit"):
            request_dict["stoplimit"] = trade_request.stoplimit
        if trade_request.HasField("sl"):
            request_dict["sl"] = trade_request.sl
        if trade_request.HasField("tp"):
            request_dict["tp"] = trade_request.tp
        if trade_request.HasField("deviation"):
            request_dict["deviation"] = trade_request.deviation
        if trade_request.HasField("expiration"):
            request_dict["expiration"] = trade_request.expiration.seconds
        if trade_request.HasField("comment"):
            request_dict["comment"] = trade_request.comment
        if trade_request.HasField("order"):
            request_dict["order"] = trade_request.order
        if trade_request.HasField("position"):
            request_dict["position"] = trade_request.position

        # MT5-specific nested fields
        if trade_request.HasField("mt5"):
            mt5_request = trade_request.mt5
            if mt5_request.HasField("action"):
                request_dict["action"] = mt5_request.action
            if mt5_request.HasField("magic"):
                request_dict["magic"] = mt5_request.magic
            if mt5_request.HasField("type"):
                request_dict["type"] = mt5_request.type
            if mt5_request.HasField("type_filling"):
                request_dict["type_filling"] = mt5_request.type_filling
            if mt5_request.HasField("type_time"):
                request_dict["type_time"] = mt5_request.type_time
            if mt5_request.HasField("position_by"):
                request_dict["position_by"] = mt5_request.position_by

        return request_dict

    @staticmethod
    def _convert_dict_to_trade_request(request_dict: Dict[str, Any]) -> types_pb2.TradeRequest:
        """
        Convert MT5 dictionary to gRPC TradeRequest protobuf.

        Args:
            request_dict: MT5 order dictionary

        Returns:
            gRPC TradeRequest message
        """
        trade_request = types_pb2.TradeRequest()

        # Generic fields
        if "symbol" in request_dict:
            trade_request.symbol = str(request_dict["symbol"])
        if "volume" in request_dict:
            trade_request.volume = float(request_dict["volume"])
        if "price" in request_dict:
            trade_request.price = float(request_dict["price"])
        if "stoplimit" in request_dict:
            trade_request.stoplimit = float(request_dict["stoplimit"])
        if "sl" in request_dict:
            trade_request.sl = float(request_dict["sl"])
        if "tp" in request_dict:
            trade_request.tp = float(request_dict["tp"])
        if "deviation" in request_dict:
            trade_request.deviation = int(request_dict["deviation"])
        if "expiration" in request_dict:
            trade_request.expiration.FromSeconds(int(request_dict["expiration"]))
        if "comment" in request_dict:
            trade_request.comment = str(request_dict["comment"])
        if "order" in request_dict:
            trade_request.order = int(request_dict["order"])
        if "position" in request_dict:
            trade_request.position = int(request_dict["position"])

        # MT5-specific nested fields
        mt5_request = types_pb2.Mt5TradeRequest()
        if "action" in request_dict:
            mt5_request.action = request_dict["action"]
        if "magic" in request_dict:
            mt5_request.magic = int(request_dict["magic"])
        if "type" in request_dict:
            mt5_request.type = request_dict["type"]
        if "type_filling" in request_dict:
            mt5_request.type_filling = request_dict["type_filling"]
        if "type_time" in request_dict:
            mt5_request.type_time = request_dict["type_time"]
        if "position_by" in request_dict:
            mt5_request.position_by = int(request_dict["position_by"])

        trade_request.mt5.CopyFrom(mt5_request)
        return trade_request
