import MetaTrader5 as mt5 # type: ignore
import src.stubs.ticks_pb2_grpc as tick_stub
from src.stubs.ticks_pb2 import LastTickRequest,Tick
from grpc import ServicerContext


class TickService(tick_stub.TickServiceServicer):
    def LastTick(self, request: LastTickRequest, context:ServicerContext) -> Tick:
      last_tick = mt5.symbol_info_tick(request.symbol) # type: ignore
      return Tick(time=last_tick.time,ask=last_tick.ask,bid=last_tick.bid,volume=last_tick.volume) # type: ignore
    