import click
import MetaTrader5 as mt5 # type: ignore

# grpc definition
import stubs.ticks_pb2_grpc as ticks_grpc
from api.ticks import TickService

import grpc
from concurrent import futures

@click.command("serve")
@click.option("--path", default=None, help="Path to metatrader.exe")
@click.option("--host", default="127.0.0.1", help="host address")
@click.option("--port", default="8080", help="port number")
@click.option("--max-workers", default=10, help="Max thread pool executor workers")
def run_grpc(path: str | None, host: str, port: str, max_workers:int):
    if not mt5.initialize(): # type: ignore
        raise RuntimeError("Unable to connect to metatrader.exe")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers))

    ticks_grpc.add_TickServiceServicer_to_server(TickService(),server) # type: ignore

    print(f"Listening to {host}:{port}")

    server.add_insecure_port(f"{host}:{port}")
    server.start()
    server.wait_for_termination()
    if not mt5.shutdown(): # type: ignore
        raise RuntimeError("Unable to close connection to metatrader.exe")

@click.group()
def cli():
    pass

if __name__ == "__main__":
    cli.add_command(run_grpc)
    cli()