from grpc_testing import Server # type: ignore
from src.stubs.ticks_pb2 import LastTickRequest
from src.stubs.ticks_pb2 import DESCRIPTOR
import grpc

def test_last_tick(grpc_server: Server):
  request = LastTickRequest(symbol="EURUSD")
  
  method = grpc_server.invoke_unary_unary( # type: ignore
    method_descriptor=DESCRIPTOR
      .services_by_name['TickService']
      .methods_by_name['LastTick'],
    invocation_metadata={},
    request=request,
    timeout=1
  )

  response, _, code, _ = method.termination() # type: ignore

  assert response is not None
  assert code == grpc.StatusCode.OK