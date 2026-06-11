import click
import logging
import MetaTrader5 as mt5  # type: ignore

import grpc
from concurrent import futures

# gRPC service imports
from src.api.account import AccountService
from src.api.market_data import MarketDataService
from src.api.trade import TradeService
from src.api.market_depth import MarketDepthService
from src.api.ticks import TicksService
from src.api.rates import RatesService
from src.api.middleware import ErrorHandlingInterceptor

# gRPC stub imports
from src.stubs import (
    account_pb2_grpc,
    market_data_pb2_grpc,
    trade_pb2_grpc,
    market_depth_pb2_grpc,
    ticks_pb2_grpc,
    rates_pb2_grpc
)

logger = logging.getLogger(__name__)

@click.command("serve")
@click.option("--path", default=None, help="Path to metatrader.exe")
@click.option("--host", default="127.0.0.1", help="host address")
@click.option("--port", default="8080", help="port number")
@click.option("--max-workers", default=10, help="Max thread pool executor workers")
def run_grpc(path: str | None, host: str, port: str, max_workers: int):
    """Run the MT5 gRPC service server."""
    if not mt5.initialize():  # type: ignore
        raise RuntimeError("Unable to connect to metatrader.exe")
    
    # Create gRPC server with error handling interceptor
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers),
        interceptors=[ErrorHandlingInterceptor()]
    )

    # Register all service servicers
    logger.info("Registering gRPC services...")
    account_pb2_grpc.add_AccountServiceServicer_to_server(AccountService(), server)
    market_data_pb2_grpc.add_MarketDataServiceServicer_to_server(MarketDataService(), server)
    trade_pb2_grpc.add_TradeServiceServicer_to_server(TradeService(), server)
    market_depth_pb2_grpc.add_MarketDepthServiceServicer_to_server(MarketDepthService(), server)
    ticks_pb2_grpc.add_TickServiceServicer_to_server(TicksService(),server)
    rates_pb2_grpc.add_RatesServiceServicer_to_server(RatesService(),server)
    logger.info("All services registered successfully")

    print(f"Listening to {host}:{port}")

    server.add_insecure_port(f"{host}:{port}")
    server.start()
    server.wait_for_termination()
    
    if not mt5.shutdown():  # type: ignore
        raise RuntimeError("Unable to close connection to metatrader.exe")

@click.group()
def cli():
    pass

if __name__ == "__main__":
    cli.add_command(run_grpc)
    cli()