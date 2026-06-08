set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

generate:
  uv run -m grpc_tools.protoc \
    --proto_path=protobuf \
    --python_out=src/stubs \
    --pyi_out=src/stubs \
    --grpc_python_out=src/stubs \
    ticks.proto
  
  Get-ChildItem src/stubs/*_pb2*.py | ForEach-Object { $f = $_; (Get-Content $f) -replace '^import ticks_pb2 as', 'from . import ticks_pb2 as' | Set-Content $f }

compile:
  uvx pyinstaller --onefile main.py
