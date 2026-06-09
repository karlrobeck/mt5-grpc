import pytest
import MetaTrader5 as mt5 # type: ignore
from grpc_testing import server_from_dictionary, strict_real_time # type: ignore
import src.stubs.ticks_pb2 as ticks_pb2
from src.api.ticks import TickService


@pytest.fixture(scope='module')
def grpc_server():
    mt5.initialize() # type: ignore
    
    servicers = {
      ticks_pb2.DESCRIPTOR.services_by_name['TickService']: TickService()
    }
   
    return server_from_dictionary(servicers, strict_real_time())
