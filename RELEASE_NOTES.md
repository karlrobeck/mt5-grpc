# Release Notes - v1.0.0

We are proud to release version `1.0.0` of **MT5 gRPC Service**. This version marks the project's transition to a production-ready, packageable, and secure gRPC interface layer for the MetaTrader 5 Python API on Windows.

Here is a summary of the key features and enhancements included in this release:

---

## Key Features

### 1. 🚀 Zero-Setup Execution (`uvx` Support)
- You can now run the gRPC server instantly on any Windows machine using `uvx` without cloning the repository or manually installing dependencies:
  ```bash
  uvx --from git+https://github.com/karlrobeck/mt5-grpc@1.0.0 mt5-grpc serve
  ```
- Restructured the project layout to place all source files under `src/` (conforming to modern Python packaging standards).
- Switched the build system to `hatchling` and registered the global `mt5-grpc` CLI script alias.

### 2. 🔑 Secure gRPC Authentication Middleware
- Added an authentication interceptor to restrict access to the gRPC server.
- Supports server-side validation of client credentials (`login` and `password` via standard HTTP Basic auth) and verification of the target MetaTrader 5 server name (`X-MT5-Server` header).
- Credentials can be configured during startup using `--login`, `--password`, and `--server` CLI flags.

### 3. 📊 Real-Time Streaming (`ListenToSymbols`)
- Introduced the `ListenToSymbols` streaming RPC in `TickService`.
- Allows clients to subscribe to and receive real-time, multiplexed tick data streams for a list of financial symbols in a single, persistent server-streaming connection.

### 4. 🧪 Robust Pytest Test Suite
- Integrated a comprehensive test suite using the `grpc-testing` framework to validate all service handlers.
- The suite contains 41 tests covering:
  - Account and terminal metadata queries.
  - Market data and depth (order book) polling.
  - Trading operations (orders, positions, deals).
  - Ticks and historical OHLCV rates.
  - Authentication middleware and header validation.
  - Custom gRPC error interceptors and conversion logic.

### 5. 📦 Standalone Executable Bundling (PyInstaller)
- Updated PyInstaller configurations (`main.spec` and `justfile`) to build a single-file executable (`dist/main.exe`) directly from the package's entry point, enabling convenient distributions for Windows systems without Python installed.

---

## How to Get Started

Refer to the [README.md](README.md) for full setup instructions. To run the server now:

```bash
# Direct execution via uvx
uvx --from git+https://github.com/karlrobeck/mt5-grpc@1.0.0 mt5-grpc serve --host 127.0.0.1 --port 8080
```
