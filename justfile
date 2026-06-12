set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

generate:
	uv run -m grpc_tools.protoc --proto_path=protobuf/protos --python_out=src/stubs --pyi_out=src/stubs --grpc_python_out=src/stubs enums.proto types.proto account.proto market_data.proto market_depth.proto rates.proto ticks.proto trade.proto
	Get-ChildItem src/stubs/*_pb2*.py | ForEach-Object { $f = $_; (Get-Content $f) -replace '^import (\w+_pb2) as ', 'from . import $1 as ' | Set-Content $f }

compile:
	uv run --with pyinstaller pyinstaller main.spec
