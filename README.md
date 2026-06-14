# MT5 gRPC Service

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.14+](https://img.shields.io/badge/Python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![gRPC](https://img.shields.io/badge/gRPC-1.81.0+-brightgreen.svg)](https://grpc.io/)
[![MetaTrader5](https://img.shields.io/badge/MetaTrader5-5.0.5735+-orange.svg)](https://www.metatrader5.com/)

A production-ready gRPC service layer for MetaTrader5 Python API, providing remote access to MT5 trading functionality over gRPC with comprehensive error handling and proper type safety.

## Features

- 🚀 **Full MT5 API Coverage**: All major MT5 Python API methods exposed via gRPC
  - Account & terminal management
  - Symbol & market data queries
  - Trading operations (orders, positions, deals)
  - Market depth (order book)
  - Price history (OHLCV rates)
  - Tick history

- 🛡️ **Comprehensive Error Handling**
  - Custom `MT5Exception` with structured error codes
  - gRPC middleware for automatic error → status code conversion
  - Graceful error propagation to clients

- 📊 **Type-Safe Architecture**
  - Full type hints (PEP 484 compliant)
  - Protobuf message definitions for all MT5 data structures
  - Automatic conversion from MT5 namedtuples to protobuf messages

- 🔌 **Production Ready**
  - Comprehensive logging throughout
  - Proper async I/O with thread pooling
  - Defensive programming patterns
  - Well-documented codebase

## Quick Start

### Prerequisites

- Python 3.14+
- MetaTrader5 terminal running (Windows)
- pip or uv package manager

### Installation

#### Method 1: Clone & Install (For Development)

1. Clone the repository:
```bash
git clone https://github.com/karlrobeck/mt5-grpc.git
cd mt5-grpc
```

2. Install dependencies:
```bash
# Using pip
pip install -e .

# Or using uv
uv sync
```

#### Method 2: Install directly via `uv tool`

If you want to install `mt5-grpc` as a standalone CLI tool on your system without cloning the repository:
```bash
uv tool install git+https://github.com/karlrobeck/mt5-grpc
```

### Running the Server

You can run the MT5 gRPC server directly using `uvx` (without cloning the repository), or run it locally as a package or module.

#### Option A: Run directly from the Git repository (using `uvx`)
You can run the tool directly from git without cloning it first. To run the latest code from the default branch:
```bash
uvx --from git+https://github.com/karlrobeck/mt5-grpc mt5-grpc serve --host 127.0.0.1 --port 8080 --max-workers 10
```

To run a specific release (such as `1.3.0`), pin the version by appending `@1.3.0` to the Git URL:
```bash
uvx --from git+https://github.com/karlrobeck/mt5-grpc@1.3.0 mt5-grpc serve --host 127.0.0.1 --port 8080 --max-workers 10
```

#### Option B: Run locally after installing the package
```bash
# Install the package in editable mode
pip install -e . # or: uv pip install -e .

# Run the CLI tool
mt5-grpc serve --host 127.0.0.1 --port 8080 --max-workers 10
```

#### Option C: Run using the Python module path
```bash
python -m src.main serve --host 127.0.0.1 --port 8080 --max-workers 10
```

**Options:**
- `--path`: Path to metatrader.exe (auto-detected if omitted)
- `--login`: MT5 account login number (requires `--password` to enable Basic auth)
- `--password`: MT5 account password (requires `--login` to enable Basic auth)
- `--server`: MT5 account server (enables case-insensitive `X-MT5-Server` validation)
- `--host`: Server host address (default: 127.0.0.1)
- `--port`: Server port (default: 8080)
- `--max-workers`: Max thread pool executor workers (default: 10)

### Authentication (Optional)

You can secure the gRPC server by configuring authentication credentials. 

#### Enabling Authentication on the Server
Pass `--login`, `--password`, and/or `--server` parameters to the `serve` command:

```bash
mt5-grpc serve \
  --login 123456 \
  --password my_password \
  --server MetaQuotes-Demo
```

*Note: If only one of `--login` or `--password` is provided, the server will raise an error and fail to start.*

#### Authenticating Client Requests
When authentication is enabled, clients must supply the following metadata headers with every request:

1. **`Authorization`**: Using the standard Basic authentication scheme: `Basic <base64(login:password)>`
   - Example: `Basic MTIzNDU2Om15X3Bhc3N3b3Jk`
2. **`X-MT5-Server`**: The exact configured MT5 server name (compared case-insensitively).
   - Example: `MetaQuotes-Demo`

If a client fails to provide the required headers, or if the credentials/server do not match, the request will immediately return a `StatusCode.UNAUTHENTICATED` error.

### Connecting a Client

Example Python gRPC client:

```python
import grpc
from src.stubs import account_pb2_grpc, market_data_pb2_grpc
from google.protobuf import empty_pb2

# Create channel
channel = grpc.aio.secure_channel('127.0.0.1:8080', grpc.ssl_channel_credentials())

# Account Service
account_stub = account_pb2_grpc.AccountServiceStub(channel)

# If authentication is enabled, pass metadata with the request
metadata = (
    ('authorization', 'Basic MTIzNDU2Om15X3Bhc3N3b3Jk'),
    ('x-mt5-server', 'MetaQuotes-Demo')
)
account_info = await account_stub.GetAccountInfo(empty_pb2.Empty(), metadata=metadata)
print(f"Account: {account_info.login}")

# Market Data Service
market_stub = market_data_pb2_grpc.MarketDataServiceStub(channel)
symbol_info = await market_stub.GetSymbolInfo(
    market_data_pb2.SymbolRequest(symbol='EURUSD')
)
print(f"Symbol: {symbol_info.name}, Bid: {symbol_info.bid}, Ask: {symbol_info.ask}")

await channel.close()
```

## Architecture

### Service Layer Structure

```
src/api/
├── exceptions.py       # MT5Exception, error mapping
├── middleware.py       # gRPC error handling interceptor
├── helpers.py          # MT5 → Protobuf conversion utilities
├── account.py          # AccountService (2 methods)
├── market_data.py      # MarketDataService (5 methods)
├── trade.py            # TradeService (12 methods)
├── market_depth.py     # MarketDepthService (3 methods)
├── rates.py            # RatesService (3 methods)
└── ticks.py            # TicksService (2 methods)
```

### Error Handling Pattern

All service methods follow this error handling pattern:

```python
result = mt5.account_info()
if not result:
    last_error = mt5.last_error()
    raise MT5Exception(last_error[0], last_error[1])
return convert_to_proto(result)
```

The gRPC middleware automatically catches `MT5Exception` and converts it to appropriate gRPC status codes:

- `UNAUTHENTICATED`: Login/auth errors
- `NOT_FOUND`: Invalid symbol or resource not found
- `FAILED_PRECONDITION`: Insufficient margin/funds
- `UNAVAILABLE`: Terminal disconnected
- `INTERNAL`: Other errors

### Data Flow

```
MT5 Terminal
    ↓
MT5 Python API (namedtuples)
    ↓
helpers.py (conversion)
    ↓
Protobuf messages
    ↓
gRPC Service
    ↓
Error Handling Middleware
    ↓
gRPC Client Response
```

## Available Services

### AccountService
- `GetAccountInfo()` - Get current trading account information
- `GetTerminalInfo()` - Get MetaTrader5 terminal status

### MarketDataService
- `GetSymbolsTotal()` - Get total count of available symbols
- `GetSymbols()` - Get list of symbols (with optional filtering)
- `GetSymbolInfo()` - Get detailed information for a specific symbol
- `GetSymbolInfoTick()` - Get the last tick for a specific symbol
- `SelectSymbol()` - Add/remove symbol from MarketWatch

### TradeService
- `GetOrdersTotal()` - Get count of active orders
- `GetOrders()` - Get list of active orders (with filtering)
- `GetPositionsTotal()` - Get count of open positions
- `GetPositions()` - Get list of open positions (with filtering)
- `GetHistoryOrdersTotal()` - Get count of historical orders
- `GetHistoryOrders()` - Get list of historical orders (with filtering)
- `GetHistoryDealsTotal()` - Get count of historical deals
- `GetHistoryDeals()` - Get list of historical deals (with filtering)
- `CalcMargin()` - Calculate margin required for a trade
- `CalcProfit()` - Calculate profit for a trade
- `CheckOrder()` - Validate order before execution
- `SendOrder()` - Send order to the broker

### MarketDepthService
- `Subscribe()` - Subscribe to market depth updates for a symbol
- `GetDepth()` - Get current market depth (order book)
- `Unsubscribe()` - Unsubscribe from market depth updates

### RatesService
- `CopyRatesFrom()` - Get bars starting from a specific date
- `CopyRatesFromPos()` - Get bars starting from a specific index
- `CopyRatesRange()` - Get bars within a date range

### TicksService
- `CopyTicksFrom()` - Get ticks starting from a specific date
- `CopyTicksRange()` - Get ticks within a date range
- `ListenToSymbols()` - Stream real-time tick updates for a list of symbols (Server Streaming API)

## Development

### Project Structure

```
mt5-grpc/
├── src/                  # Source code
│   ├── api/             # Service implementations
│   ├── stubs/           # Generated protobuf code
│   └── main.py          # Entry point
├── protobuf/            # Protobuf definitions (.proto files)
├── tests/               # Test suite
├── docs/                # Documentation
├── pyproject.toml       # Project configuration
├── justfile             # Task automation
└── README.md            # This file
```

### Building Protobuf Messages

Generate protobuf stubs from .proto definitions:

```bash
python -m grpc_tools.protoc -I./protobuf/protos --python_out=./src/stubs --grpc_python_out=./src/stubs ./protobuf/protos/*.proto
```

### Running Tests

```bash
pytest tests/
```

### Type Checking

```bash
mypy src/
```

## Requirements

See `pyproject.toml` for full list:

- **click** >= 8.4.1 - CLI framework
- **grpcio** >= 1.81.0 - gRPC runtime
- **grpcio-tools** >= 1.81.0 - Protobuf compiler
- **metatrader5** >= 5.0.5735 - MT5 Python API

### Dev Requirements

- **grpcio-testing** >= 1.81.0 - gRPC testing utilities
- **pytest** >= 9.0.3 - Testing framework

## Configuration

### MT5 Connection

The server automatically handles MT5 connection initialization on startup. Ensure:

1. MetaTrader5 terminal is installed and running
2. Your account is logged in and ready
3. No other applications are using the MT5 Python API

### gRPC Server

Configure server parameters via command-line options:

```bash
python -m src.main serve \
  --host 0.0.0.0 \           # Listen on all interfaces
  --port 50051 \              # Use standard gRPC port
  --max-workers 20            # Increase thread pool
```

## Performance Considerations

- **Thread Pool**: Default 10 workers, adjust via `--max-workers` based on load
- **Market Data**: Subscription-based services (market depth) require `Subscribe()` before `GetDepth()`
- **Rate Limits**: MT5 API rate limits apply (typically no hard limits for local connections)
- **Data Size**: Bulk queries (history, symbols) return full results - consider pagination for large datasets

## Logging

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

All service methods and middleware log their operations at INFO/DEBUG levels.

## Common Issues

### "Unable to connect to metatrader.exe"
- Ensure MetaTrader5 terminal is running
- Check that the terminal is fully initialized (charts loaded)
- Verify MT5 version is compatible (>= 5.0.5735)

### "Symbol not found" errors
- Verify the symbol is available in your broker's symbol list
- Use `GetSymbols()` to list available symbols
- Some symbols may require `SelectSymbol()` first

### Connection timeouts
- Check firewall settings
- Ensure `--host` and `--port` are accessible
- Increase `--max-workers` if under heavy load

### gRPC errors
- Check middleware logs for MT5 error details
- Verify protobuf message structure matches proto definitions
- Ensure client and server use compatible gRPC versions

## API Compliance

This implementation follows:
- ✅ gRPC Python best practices
- ✅ Protobuf3 specifications
- ✅ PEP 484 type hints
- ✅ PEP 8 code style
- ✅ Python 3.14+ compatibility

## Design Patterns

### Error Handling
- All MT5 API calls check for falsy returns
- Failed calls raise `MT5Exception` with error code and description
- Middleware converts exceptions to gRPC status codes
- Clients receive proper gRPC error responses

### Type Safety
- Full type hints on all functions/methods
- Automatic conversion from MT5 namedtuples to protobuf
- Protobuf definitions for all data structures

### Resource Management
- Thread pool executor for concurrent requests
- Proper MT5 initialization/shutdown
- Graceful error handling and cleanup

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Add type hints to all new code
- Include docstrings for public functions/classes
- Follow PEP 8 style guide
- Add tests for new functionality
- Update README if adding new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Author**: Karl Robeck Alferez

## Acknowledgments

- MetaTrader5 Python API documentation
- gRPC Python documentation
- The Python trading community

## Contact & Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing documentation in `/docs`
- Review the protobuf definitions in `/protobuf/protos`

## Roadmap

Future enhancements:

- [ ] Client library for common languages (Python, Go, Node.js)

## Version History

### 1.3.0 (Current)
- Migrated date, time, and duration fields in protobuf schemas to standard gRPC `google.protobuf.Timestamp` and `google.protobuf.Duration` types.
- Consolidated split time/milliseconds fields (e.g. `time` and `time_msc`), removing redundant `_msc` fields.
- Updated python service classes and test suites to fully support and validate the new datetime-like objects.

### 1.2.0
- Added SSL/TLS support for secure gRPC communication (`--ssl-key` and `--ssl-cert` CLI flags).
- Added explicit file existence and readability validation for key/certificate paths.
- Automatically falls back to insecure communication if SSL flags are omitted.

### 1.0.1
- Added `-v` / `--verbose` command-line flag to configure logging level dynamically (enables `DEBUG` mode).
- Improved CLI startup logging to output server listening address via standard logging instead of plain standard output.
- Updated protobuf generation scripts in `justfile` to dynamically glob all proto files.

### 1.0.0
- Transitioned to production-ready packageable architecture with modern `src/` layout.
- Switched build backend to `hatchling` and added support for direct `uvx` execution from Git repository.
- Added comprehensive authentication middleware with server-side validation (`login`, `password`, and custom `X-MT5-Server` header).
- Added real-time streaming support (`ListenToSymbols` method).
- Integrated unit tests for CLI and authentication using `grpc-testing` framework.
- Standardized PyInstaller standalone executable building pipeline.

### 0.2.0
- Added `ListenToSymbols` gRPC method in `ticks.proto` for streaming tick data of multiple symbols.
- Implemented authentication middleware support validating requests against CLI credentials and MT5 configuration.

### 0.1.0
- Initial release
- Full MT5 API coverage
- Complete error handling
- Production-ready implementation

---

**Made with ❤️ for the trading community**
