import click
import logging
import numpy
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
from src.api.middleware import ErrorHandlingInterceptor, AuthenticationInterceptor

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
@click.option("--login", default=None, help="Account login number")
@click.option("--password", default=None, help="Account password")
@click.option("--server", default=None, help="Account server")
@click.option("--timeout", default=60_000, help="Terminal connection timeout")
@click.option("--portable", default=False, help="Run in portable mode")
@click.option("--host", default="127.0.0.1", help="host address")
@click.option("--port", default="8080", help="port number")
@click.option("--max-workers", default=10, help="Max thread pool executor workers")
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging (DEBUG level)")
def run_grpc(
    path: str | None, 
    login: int | None,
    password: str | None,
    server: str | None,
    timeout: int,
    portable: bool,
    host: str, 
    port: str, 
    max_workers: int,
    verbose: bool
):
    """Run the MT5 gRPC service server."""
    # Configure logging
    log_level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


    # Validate login/password
    if (login is not None) != (password is not None):
        raise click.UsageError("Both --login and --password must be provided, or neither.")

    init_args = {}

    if login:
        init_args['login'] = login
    
    if password:
        init_args['password'] = password
    
    if server:
        init_args['server'] = server
    
    if timeout:
        init_args['timeout'] = timeout
    
    if portable:
        init_args['portable'] = portable

    if path:
        if not mt5.initialize(path,**init_args): # type: ignore
            raise RuntimeError("Unablt to connect to metatrader.exe")
    else:
        if not mt5.initialize(**init_args):  # type: ignore
            raise RuntimeError("Unable to connect to metatrader.exe")
    
    # Create gRPC server with interceptors
    interceptors = []
    if (login is not None and password is not None) or server is not None:
        interceptors.append(
            AuthenticationInterceptor(
                expected_login=str(login) if login is not None else None,
                expected_password=password,
                expected_server=server
            )
        )
    interceptors.append(ErrorHandlingInterceptor())

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers),
        interceptors=interceptors
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

cli.add_command(run_grpc)

if __name__ == "__main__":
    cli()
