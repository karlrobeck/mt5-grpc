import pytest
import grpc
from google.protobuf import empty_pb2
from src.stubs import trade_pb2, types_pb2

class MockObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_get_orders_total_success(grpc_server, mt5_mock):
    mt5_mock.orders_total.return_value = 5

    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetOrdersTotal'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.total == 5

def test_get_orders_success(grpc_server, mt5_mock):
    mock_order = MockObject(
        ticket=11111,
        time_setup=1600000000,
        time_setup_msc=1600000000123,
        time_done=0,
        time_done_msc=0,
        time_expiration=0,
        type=0, # ORDER_TYPE_BUY
        type_time=0,
        type_filling=0,
        state=1, # ORDER_STATE_PLACED
        magic=9999,
        position_id=0,
        position_by_id=0,
        reason=0,
        volume_initial=1.0,
        volume_current=1.0,
        price_open=1.1200,
        sl=1.1100,
        tp=1.1300,
        price_current=1.1205,
        price_stoplimit=0.0,
        symbol="EURUSD",
        comment="test order",
        external_id=""
    )
    mt5_mock.orders_get.return_value = (mock_order,)

    req = trade_pb2.OrdersRequest(symbol="EURUSD")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetOrders'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.orders) == 1
    assert response.orders[0].ticket == 11111
    mt5_mock.orders_get.assert_called_once_with(symbol="EURUSD", group=None, ticket=None)

def test_get_positions_total_success(grpc_server, mt5_mock):
    mt5_mock.positions_total.return_value = 2

    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetPositionsTotal'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=empty_pb2.Empty(),
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.total == 2

def test_get_positions_success(grpc_server, mt5_mock):
    mock_pos = MockObject(
        ticket=22222,
        time=1600000000,
        time_msc=1600000000123,
        time_update=1600000000,
        time_update_msc=1600000000123,
        type=0, # POSITION_TYPE_BUY
        magic=1000,
        identifier=22222,
        reason=0,
        volume=0.5,
        price_open=1.1200,
        sl=1.1100,
        tp=1.1300,
        price_current=1.1210,
        swap=0.0,
        profit=50.0,
        symbol="EURUSD",
        comment="test pos",
        external_id=""
    )
    mt5_mock.positions_get.return_value = (mock_pos,)

    req = trade_pb2.PositionsRequest(symbol="EURUSD")
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetPositions'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.positions) == 1
    assert response.positions[0].ticket == 22222

def test_get_history_orders_total_success(grpc_server, mt5_mock):
    mt5_mock.history_orders_total.return_value = 10

    req = trade_pb2.HistoryRangeRequest(date_from=1600000000, date_to=1600010000)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetHistoryOrdersTotal'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.total == 10
    mt5_mock.history_orders_total.assert_called_once_with(1600000000, 1600010000)

def test_get_history_orders_success(grpc_server, mt5_mock):
    mock_order = MockObject(
        ticket=33333,
        time_setup=1600000000,
        time_setup_msc=1600000000123,
        time_done=1600000050,
        time_done_msc=1600000050123,
        time_expiration=0,
        type=0,
        type_time=0,
        type_filling=0,
        state=3, # ORDER_STATE_FILLED
        magic=1000,
        position_id=22222,
        position_by_id=0,
        reason=0,
        volume_initial=1.0,
        volume_current=0.0,
        price_open=1.1200,
        sl=0.0,
        tp=0.0,
        price_current=1.1200,
        price_stoplimit=0.0,
        symbol="EURUSD",
        comment="history",
        external_id=""
    )
    mt5_mock.history_orders_get.return_value = (mock_order,)

    req = trade_pb2.HistoryOrdersRequest(date_from=1600000000, date_to=1600010000)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetHistoryOrders'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.orders) == 1
    assert response.orders[0].ticket == 33333

def test_get_history_deals_total_success(grpc_server, mt5_mock):
    mt5_mock.history_deals_total.return_value = 8

    req = trade_pb2.HistoryRangeRequest(date_from=1600000000, date_to=1600010000)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetHistoryDealsTotal'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.total == 8
    mt5_mock.history_deals_total.assert_called_once_with(1600000000, 1600010000)

def test_get_history_deals_success(grpc_server, mt5_mock):
    mock_deal = MockObject(
        ticket=44444,
        order=33333,
        time=1600000050,
        time_msc=1600000050123,
        type=0, # DEAL_TYPE_BUY
        entry=0, # DEAL_ENTRY_IN
        magic=1000,
        position_id=22222,
        reason=0,
        volume=1.0,
        price=1.1200,
        commission=-1.5,
        swap=0.0,
        profit=0.0,
        fee=0.0,
        symbol="EURUSD",
        comment="history deal",
        external_id=""
    )
    mt5_mock.history_deals_get.return_value = (mock_deal,)

    req = trade_pb2.HistoryDealsRequest(date_from=1600000000, date_to=1600010000)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetHistoryDeals'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.deals) == 1
    assert response.deals[0].ticket == 44444

def test_calc_margin_success(grpc_server, mt5_mock):
    mt5_mock.order_calc_margin.return_value = 1200.0

    req = trade_pb2.CalcMarginRequest(
        action=0, # ORDER_TYPE_BUY
        symbol="EURUSD",
        volume=1.0,
        price=1.1200
    )
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['CalcMargin'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.margin == 1200.0
    mt5_mock.order_calc_margin.assert_called_once_with(0, "EURUSD", 1.0, 1.1200)

def test_calc_profit_success(grpc_server, mt5_mock):
    mt5_mock.order_calc_profit.return_value = 150.0

    req = trade_pb2.CalcProfitRequest(
        action=0, # ORDER_TYPE_BUY
        symbol="EURUSD",
        volume=1.0,
        price_open=1.1200,
        price_close=1.1300
    )
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['CalcProfit'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.profit == 150.0
    mt5_mock.order_calc_profit.assert_called_once_with(0, "EURUSD", 1.0, 1.1200, 1.1300)

def test_check_order_success(grpc_server, mt5_mock):
    mock_check = MockObject(
        retcode=10009, # TRADE_RETCODE_DONE
        balance=10000.0,
        equity=10000.0,
        profit=0.0,
        margin=1000.0,
        margin_free=9000.0,
        margin_level=1000.0,
        comment="Check OK"
    )
    mt5_mock.order_check.return_value = mock_check

    # Test with explicitly set falsy/default values (0/0.0)
    trade_req = types_pb2.TradeRequest(
        symbol="EURUSD", 
        volume=1.0, 
        price=1.1200,
        deviation=0
    )
    trade_req.mt5.action = 1 # TRADE_ACTION_DEAL
    trade_req.mt5.magic = 0
    trade_req.mt5.type = 0 # ORDER_TYPE_BUY
    trade_req.mt5.type_filling = 0 # ORDER_FILLING_FOK
    trade_req.mt5.type_time = 0 # ORDER_TIME_GTC
    
    req = trade_pb2.CheckOrderRequest(request=trade_req)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['CheckOrder'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.retcode == 10009
    assert response.comment == "Check OK"
    mt5_mock.order_check.assert_called_once_with({
        "symbol": "EURUSD",
        "volume": 1.0,
        "price": 1.1200,
        "deviation": 0,
        "magic": 0,
        "action": 1,
        "type": 0,
        "type_filling": 0,
        "type_time": 0
    })

def test_send_order_success(grpc_server, mt5_mock):
    mock_result = MockObject(
        retcode=10009,
        deal=55555,
        order=66666,
        volume=1.0,
        price=1.1200,
        bid=1.1199,
        ask=1.1201,
        comment="Done",
        request_id=1,
        retcode_external=0
    )
    mt5_mock.order_send.return_value = mock_result

    trade_req = types_pb2.TradeRequest(symbol="EURUSD", volume=1.0, price=1.1200)
    
    req = trade_pb2.SendOrderRequest(request=trade_req)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['SendOrder'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert response.retcode == 10009
    assert response.deal == 55555
    assert response.comment == "Done"

def test_get_history_orders_by_ticket_success(grpc_server, mt5_mock):
    mock_order = MockObject(
        ticket=33333,
        symbol="EURUSD",
        volume_initial=1.0,
        price_open=1.1200,
        comment="history",
        external_id=""
    )
    mt5_mock.history_orders_get.return_value = (mock_order,)

    req = trade_pb2.HistoryOrdersRequest(ticket=33333)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetHistoryOrders'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.orders) == 1
    assert response.orders[0].ticket == 33333
    mt5_mock.history_orders_get.assert_called_once_with(
        group=None,
        ticket=33333,
        position=None
    )

def test_get_history_deals_by_position_success(grpc_server, mt5_mock):
    mock_deal = MockObject(
        ticket=44444,
        order=33333,
        symbol="EURUSD",
        volume=1.0,
        price=1.1200,
        comment="deal",
        external_id="",
        position_id=22222
    )
    mt5_mock.history_deals_get.return_value = (mock_deal,)

    req = trade_pb2.HistoryDealsRequest(position=22222)
    rpc = grpc_server.invoke_unary_unary(
        method_descriptor=trade_pb2.DESCRIPTOR.services_by_name['TradeService'].methods_by_name['GetHistoryDeals'],
        invocation_metadata=[
            ('authorization', 'Basic MTIzNDU2OnBhc3N3b3JkMTIz'),
            ('x-mt5-server', 'MT5-Server')
        ],
        request=req,
        timeout=1.0
    )

    response, initial_metadata, code, details = rpc.termination()
    assert code == grpc.StatusCode.OK
    assert len(response.deals) == 1
    assert response.deals[0].ticket == 44444
    mt5_mock.history_deals_get.assert_called_once_with(
        group=None,
        ticket=None,
        position=22222
    )
