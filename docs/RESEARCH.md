# MT5 Python API Research — gRPC Protobuf Baseline

This document catalogs every method and data structure in the `MetaTrader5` Python package (v5.0.29+), classifies each field as **generic trading domain** or **MT5-specific**, and explains the rationale. This serves as the baseline for designing the gRPC protobuf schema.

---

## Table of Contents

1. [Connection & Lifecycle](#1-connection--lifecycle)
2. [Account & Terminal Info](#2-account--terminal-info)
3. [Symbols & Market Data](#3-symbols--market-data)
4. [Market Depth (Order Book)](#4-market-depth-order-book)
5. [Price History (Rates / OHLCV)](#5-price-history-rates--ohlcv)
6. [Tick History](#6-tick-history)
7. [Orders (Active Pending)](#7-orders-active-pending)
8. [Positions (Open Trades)](#8-positions-open-trades)
9. [History — Orders & Deals](#9-history--orders--deals)
10. [Trading Request / Result Structures](#10-trading-request--result-structures)
11. [Enum Reference](#11-enum-reference)
12. [Protobuf Design Recommendations](#12-protobuf-design-recommendations)

---

## 1. Connection & Lifecycle

### 1.1 `initialize()`

**Purpose:** Establish a connection with the MetaTrader 5 terminal. If the terminal is not running, it launches it automatically.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `path` | `string` | No | Path to `metatrader.exe` or `metatrader64.exe`. If omitted, auto-detected. | **MT5-specific** — filesystem path to a specific MT5 terminal binary |
| `login` | `uint64` | No | Trading account number. If omitted, uses last account. | **Generic** — account ID |
| `password` | `string` | No | Account password. If omitted, uses saved password. | **Generic** — credentials |
| `server` | `string` | No | Trade server name. If omitted, uses saved server. | **Generic** — broker server name |
| `timeout` | `uint64` | No | Connection timeout in milliseconds. Default: 60000 (60s). | **Generic** — connection timeout |
| `portable` | `bool` | No | Launch terminal in portable mode. Default: False. | **MT5-specific** — MT5 portable mode (self-contained folder) |

**Return Value:** `bool` — True if connection established, False otherwise.

### 1.2 `login()`

**Purpose:** Connect to a specific trading account after the terminal is already initialized.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `login` | `uint64` | Yes | Trading account number. | **Generic** |
| `password` | `string` | No | Account password. If omitted, uses saved password. | **Generic** |
| `server` | `string` | No | Trade server name. If omitted, uses last used server. | **Generic** |
| `timeout` | `uint64` | No | Connection timeout in milliseconds. Default: 60000. | **Generic** |

**Return Value:** `bool` — True if connected successfully.

### 1.3 `shutdown()`

**Purpose:** Close the connection to the MetaTrader 5 terminal.

**Parameters:** None

**Return Value:** `None`

### 1.4 `version()`

**Purpose:** Return the MetaTrader 5 terminal version, build number, and release date.

**Parameters:** None

**Return Value:** Tuple of `(int32 version, int32 build, string release_date)`

| Field | Type | Description | Classification |
|-------|------|-------------|----------------|
| `version` | `int32` | Terminal version (e.g., 500). | **MT5-specific** — MetaQuotes versioning scheme |
| `build` | `int32` | Build number (e.g., 2367). | **MT5-specific** — MetaQuotes build numbering |
| `release_date` | `string` | Build release date (e.g., "23 Mar 2020"). | **MT5-specific** — MetaQuotes release tracking |

### 1.5 `last_error()`

**Purpose:** Return the last error code and description.

**Parameters:** None

**Return Value:** Tuple of `(int32 code, string description)`

| Field | Type | Description | Classification |
|-------|------|-------------|----------------|
| `code` | `int32` | Error code. Uses MT5-specific constants (RES_S_OK=1, RES_E_FAIL=-1, etc.). | **MT5-specific** — proprietary error code enum |
| `description` | `string` | Human-readable description. | **Generic** — error message |

---

## 2. Account & Terminal Info

### 2.1 `account_info()`

**Purpose:** Get info on the current trading account. Returns all data from `AccountInfoInteger`, `AccountInfoDouble`, and `AccountInfoString` in one call.

**Parameters:** None

**Return Type:** `AccountInfo` (namedtuple)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `login` | `int64` | Account number. | **Generic** | Every trading platform has account IDs |
| 2 | `trade_mode` | `int32` | Account trade mode (0=DEMO, 1=CONTEST, 2=REAL). | **MT5-specific** | MT5 proprietary enum (`ACCOUNT_TRADE_MODE_*`) |
| 3 | `leverage` | `int64` | Account leverage (e.g., 100 = 1:100). | **Generic** | Leverage is universal across brokers |
| 4 | `limit_orders` | `int32` | Max limit orders allowed (0=unlimited). | **MT5-specific** | MT5-specific account limitation setting |
| 5 | `margin_so_mode` | `int32` | Stop-out mode (0=percent, 1=money). | **MT5-specific** | MT5 enum (`ACCOUNT_STOPOUT_MODE_*`) — how stop-out threshold is measured |
| 6 | `trade_allowed` | `bool` | Trading permission flag. | **Generic** | Trading enabled/disabled exists in all platforms |
| 7 | `trade_expert` | `bool` | Expert Advisor trading allowed. | **MT5-specific** | MQL5 EA permission flag — MT5's automated trading concept |
| 8 | `margin_mode` | `int32` | Margin calculation mode (0=retail hedging, 1=exchange, 2=retail netting). | **MT5-specific** | MT5 enum (`ACCOUNT_MARGIN_MODE_*`) — proprietary margin calc algorithm |
| 9 | `currency_digits` | `int32` | Number of decimal places in deposit currency. | **MT5-specific** | MT5-specific precision indicator tied to deposit currency |
| 10 | `fifo_close` | `bool` | FIFO rule enforced for closing positions. | **MT5-specific** | Regulatory flag specific to certain brokers/regions; MT5 exposes it as an account property |
| 11 | `balance` | `double` | Account balance. | **Generic** | Universal |
| 12 | `credit` | `double` | Credit facility amount. | **Generic** | Broker credit is a common concept |
| 13 | `profit` | `double` | Floating profit on open positions. | **Generic** | Universal |
| 14 | `equity` | `double` | Account equity (balance + credit + profit - swap - commission). | **Generic** | Universal |
| 15 | `margin` | `double` | Used margin. | **Generic** | Universal |
| 16 | `margin_free` | `double` | Free margin. | **Generic** | Universal |
| 17 | `margin_level` | `double` | Margin level percentage (equity / margin * 100). | **Generic** | Universal risk metric |
| 18 | `margin_so_call` | `double` | Margin call threshold (percent or money). | **Generic** | Margin call is a universal concept (though the mode is MT5-specific) |
| 19 | `margin_so_so` | `double` | Stop-out threshold (percent or money). | **Generic** | Stop-out is universal |
| 20 | `margin_initial` | `double` | Initial margin for all open positions. | **MT5-specific** | MT5-specific aggregated initial margin calc |
| 21 | `margin_maintenance` | `double` | Maintenance margin for all open positions. | **MT5-specific** | MT5-specific aggregated maintenance margin |
| 22 | `assets` | `double` | Net asset valuation (netting accounts). | **MT5-specific** | Netting account concept in MT5 |
| 23 | `liabilities` | `double` | Liability valuation (netting accounts). | **MT5-specific** | Netting account concept in MT5 |
| 24 | `commission_blocked` | `double` | Blocked commission amount. | **MT5-specific** | MT5-specific commission blocking mechanism |
| 25 | `name` | `string` | Account holder name. | **Generic** | Universal |
| 26 | `server` | `string` | Trade server name. | **Generic** | Broker server identification |
| 27 | `currency` | `string` | Deposit currency (e.g., "USD", "EUR"). | **Generic** | Universal |
| 28 | `company` | `string` | Broker company name. | **Generic** | Universal |

### 2.2 `terminal_info()`

**Purpose:** Get connected MetaTrader 5 terminal status and settings. Returns all data from `TerminalInfoInteger`, `TerminalInfoDouble`, and `TerminalInfoString` in one call.

**Parameters:** None

**Return Type:** `TerminalInfo` (namedtuple)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `community_account` | `bool` | MQL5 community account is logged in. | **MT5-specific** | MQL5 community ecosystem is MetaQuotes proprietary |
| 2 | `community_connection` | `bool` | MQL5 community connection active. | **MT5-specific** | MQL5 community feature |
| 3 | `connected` | `bool` | Terminal connected to trade server. | **Generic** | Connection status is universal |
| 4 | `dlls_allowed` | `bool` | DLL imports allowed for MQL5 programs. | **MT5-specific** | MQL5-specific security setting |
| 5 | `trade_allowed` | `bool` | Trading enabled in terminal. | **Generic** | Universal platform setting |
| 6 | `tradeapi_disabled` | `bool` | Trade API calls disabled. | **MT5-specific** | MT5-specific API control flag |
| 7 | `email_enabled` | `bool` | Email notifications enabled in terminal. | **MT5-specific** | MQL5 notification config |
| 8 | `ftp_enabled` | `bool` | FTP publishing enabled. | **MT5-specific** | MQL5 FTP config |
| 9 | `notifications_enabled` | `bool` | Push notifications enabled. | **MT5-specific** | MQL5 push notification config |
| 10 | `mqid` | `bool` | MQL5 community account numeric ID. | **MT5-specific** | MQL5 community feature |
| 11 | `build` | `int32` | Terminal build number. | **MT5-specific** | MetaQuotes proprietary build numbering |
| 12 | `maxbars` | `int64` | Max bars in chart (history limit). | **MT5-specific** | MT5 terminal preference |
| 13 | `codepage` | `int32` | Terminal codepage (Windows locale). | **MT5-specific** | OS-level config exposed by MT5 |
| 14 | `ping_last` | `int64` | Last known ping to trade server (milliseconds). | **Generic** | Network latency metric (exists in all trading platforms) |
| 15 | `community_balance` | `double` | MQL5 community account balance (USD). | **MT5-specific** | MQL5 community ecosystem feature |
| 16 | `retransmission` | `double` | Retransmission rate (0-100%). | **MT5-specific** | MT5-specific quality of service metric |
| 17 | `company` | `string` | Broker company name. | **Generic** | Universal |
| 18 | `name` | `string` | Terminal user name. | **Generic** | Universal |
| 19 | `language` | `string` | Terminal UI language (e.g., "Russian"). | **MT5-specific** | Terminal localization setting |
| 20 | `path` | `string` | Terminal installation path. | **MT5-specific** | Local filesystem path |
| 21 | `data_path` | `string` | Terminal data folder path. | **MT5-specific** | Local filesystem path |
| 22 | `commondata_path` | `string` | Common data folder path (shared across terminals). | **MT5-specific** | MT5 multi-terminal shared data path |

---

## 3. Symbols & Market Data

### 3.1 `symbols_total()`

**Purpose:** Get the number of all financial instruments in the terminal.

**Parameters:** None

**Return Value:** `int32` — total symbol count.

### 3.2 `symbols_get()`

**Purpose:** Get all financial instruments, optionally filtered by group name.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `group` | `string` | No | Wildcard filter (e.g., `"*EUR*"`, `"*,!*USD*"`). | **Generic** — name filtering concept (syntax is MT5-specific) |

**Return Type:** Tuple of `SymbolInfo` (see 3.3)

### 3.3 `symbol_info()`

**Purpose:** Get detailed data on a specific financial instrument.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Instrument name (e.g., "EURUSD"). | **Generic** |

**Return Type:** `SymbolInfo` (namedtuple) — 96 fields.

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `custom` | `bool` | Custom synthetic symbol. | **MT5-specific** | MT5 user-defined symbol concept |
| 2 | `chart_mode` | `int32` | Chart mode (bid/ask/last). | **MT5-specific** | MT5 enum (`SYMBOL_CHART_MODE_*`) |
| 3 | `select` | `bool` | Symbol is selected in MarketWatch. | **Generic** | Market Watch selection (common UI concept) |
| 4 | `visible` | `bool` | Symbol is visible in MarketWatch. | **Generic** | Visibility toggle (common) |
| 5 | `session_deals` | `int32` | Trading session deals count limit. | **MT5-specific** | MT5 session config struct |
| 6 | `session_buy_orders` | `int32` | Session buy orders limit. | **MT5-specific** | MT5 session config |
| 7 | `session_sell_orders` | `int32` | Session sell orders limit. | **MT5-specific** | MT5 session config |
| 8 | `volume` | `int64` | Last reported trade volume (integer lots). | **Generic** | Volume is universal |
| 9 | `volumehigh` | `int64` | Daily high volume (integer lots). | **Generic** | Universal |
| 10 | `volumelow` | `int64` | Daily low volume (integer lots). | **Generic** | Universal |
| 11 | `time` | `int64` | Last quote time (Unix seconds). | **Generic** | Timestamps are universal |
| 12 | `digits` | `int32` | Number of decimal places. | **Generic** | Price precision (known as "digits" in MT4/5, "pip location" elsewhere) |
| 13 | `spread` | `int32` | Spread in points. | **Generic** | Universal |
| 14 | `spread_float` | `bool` | Floating spread. | **Generic** | Universal concept |
| 15 | `ticks_bookdepth` | `int32` | Market depth depth (levels). | **MT5-specific** | MT5 market depth config |
| 16 | `trade_calc_mode` | `int32` | Profit calculation mode (0=Forex, 1=CFD, 2=Futures, 3=CFD#). | **MT5-specific** | MT5 enum (`SYMBOL_TRADE_CALC_MODE_*`) — proprietary profit calc |
| 17 | `trade_mode` | `int32` | Trade mode (disabled/long-only/short-only/close-only/full). | **MT5-specific** | MT5 enum (`SYMBOL_TRADE_MODE_*`) |
| 18 | `start_time` | `int64` | Contract start date (futures/options). | **Generic** | Universal contract field |
| 19 | `expiration_time` | `int64` | Contract expiration date. | **Generic** | Universal |
| 20 | `trade_stops_level` | `int32` | Distance from market to place stops (points). | **Generic** | Common broker requirement (stop distance) |
| 21 | `trade_freeze_level` | `int32` | Freeze level in points. | **Generic** | Common broker requirement |
| 22 | `trade_exemode` | `int32` | Order execution mode (request/instant/market/exchange). | **MT5-specific** | MT5 enum (`SYMBOL_TRADE_EXECUTION_*`) |
| 23 | `swap_mode` | `int32` | Swap calculation mode (points/money/interest/etc). | **MT5-specific** | MT5 enum (`SYMBOL_SWAP_MODE_*`) |
| 24 | `swap_rollover3days` | `int32` | Day of week for triple swap (e.g., Wednesday). | **MT5-specific** | MT5-specific rollover day config |
| 25 | `margin_hedged_use_leg` | `bool` | Use largest leg for hedged margin. | **MT5-specific** | MT5-specific hedging margin rule |
| 26 | `expiration_mode` | `int32` | Allowed order expiration modes (bitmask). | **MT5-specific** | MT5 enum (`SYMBOL_EXPIRATION_MODE_*`) |
| 27 | `filling_mode` | `int32` | Allowed order filling modes (bitmask). | **MT5-specific** | MT5 enum (`SYMBOL_FILLING_MODE_*`) |
| 28 | `order_mode` | `int32` | Allowed order types (bitmask). | **MT5-specific** | MT5 enum (`SYMBOL_ORDER_MODE_*`) |
| 29 | `order_gtc_mode` | `int32` | Good-til-cancelled order handling. | **MT5-specific** | MT5 enum (`SYMBOL_ORDERS_GTC_*`) |
| 30 | `option_mode` | `int32` | Option type (American/European). | **Generic** | Option style classification |
| 31 | `option_right` | `int32` | Option right (call/put). | **Generic** | Universal option classification |
| 32 | `bid` | `double` | Current bid price. | **Generic** | Universal |
| 33 | `bidhigh` | `double` | Daily high bid. | **Generic** | Universal |
| 34 | `bidlow` | `double` | Daily low bid. | **Generic** | Universal |
| 35 | `ask` | `double` | Current ask price. | **Generic** | Universal |
| 36 | `askhigh` | `double` | Daily high ask. | **Generic** | Universal |
| 37 | `asklow` | `double` | Daily low ask. | **Generic** | Universal |
| 38 | `last` | `double` | Last trade price. | **Generic** | Universal |
| 39 | `lasthigh` | `double` | Daily high last. | **Generic** | Universal |
| 40 | `lastlow` | `double` | Daily low last. | **Generic** | Universal |
| 41 | `volume_real` | `double` | Last volume (float). | **Generic** | Universal |
| 42 | `volumehigh_real` | `double` | Daily high volume (float). | **Generic** | Universal |
| 43 | `volumelow_real` | `double` | Daily low volume (float). | **Generic** | Universal |
| 44 | `option_strike` | `double` | Option strike price. | **Generic** | Universal |
| 45 | `point` | `double` | Symbol point value (smallest price change). | **Generic** | Universal tick/point value |
| 46 | `trade_tick_value` | `double` | Tick value in deposit currency. | **Generic** | Universal concept |
| 47 | `trade_tick_value_profit` | `double` | Tick value for long positions. | **Generic** | Universal (some platforms call it "tick value" for direction) |
| 48 | `trade_tick_value_loss` | `double` | Tick value for short positions. | **Generic** | Universal |
| 49 | `trade_tick_size` | `double` | Tick size (minimum price change). | **Generic** | Universal |
| 50 | `trade_contract_size` | `double` | Contract size (e.g., 100000 for forex). | **Generic** | Universal |
| 51 | `trade_accrued_interest` | `double` | Accrued interest (bond trading). | **Generic** | Standard bond concept |
| 52 | `trade_face_value` | `double` | Face value (bond trading). | **Generic** | Standard bond concept |
| 53 | `trade_liquidity_rate` | `double` | Liquidity rate. | **Generic** | Standard market metric |
| 54 | `volume_min` | `double` | Minimum trade volume (lots). | **Generic** | Universal |
| 55 | `volume_max` | `double` | Maximum trade volume (lots). | **Generic** | Universal |
| 56 | `volume_step` | `double` | Volume increment step. | **Generic** | Universal |
| 57 | `volume_limit` | `double` | Aggregate volume limit for symbol. | **MT5-specific** | MT5-specific total volume cap on a symbol |
| 58 | `swap_long` | `double` | Long position swap rate. | **Generic** | Universal |
| 59 | `swap_short` | `double` | Short position swap rate. | **Generic** | Universal |
| 60 | `margin_initial` | `double` | Initial margin per lot. | **Generic** | Universal margin requirement |
| 61 | `margin_maintenance` | `double` | Maintenance margin per lot. | **Generic** | Universal |
| 62 | `session_volume` | `double` | Current session volume. | **MT5-specific** | MT5 session statistics struct |
| 63 | `session_turnover` | `double` | Current session turnover. | **MT5-specific** | MT5 session statistics |
| 64 | `session_interest` | `double` | Current session open interest. | **MT5-specific** | MT5 session statistics |
| 65 | `session_buy_orders_volume` | `double` | Session buy limit order volume. | **MT5-specific** | MT5 session statistics |
| 66 | `session_sell_orders_volume` | `double` | Session sell limit order volume. | **MT5-specific** | MT5 session statistics |
| 67 | `session_open` | `double` | Session open price. | **MT5-specific** | MT5 session statistics |
| 68 | `session_close` | `double` | Session close price. | **MT5-specific** | MT5 session statistics |
| 69 | `session_aw` | `double` | Session adjustment (average weighted). | **MT5-specific** | MT5 session statistics |
| 70 | `session_price_settlement` | `double` | Session settlement price. | **MT5-specific** | MT5 session statistics |
| 71 | `session_price_limit_min` | `double` | Session minimum price limit. | **MT5-specific** | MT5 session statistics |
| 72 | `session_price_limit_max` | `double` | Session maximum price limit. | **MT5-specific** | MT5 session statistics |
| 73 | `margin_hedged` | `double` | Margin required for hedged positions. | **Generic** | Common concept in hedging platforms |
| 74 | `price_change` | `double` | Price change from previous close. | **Generic** | Universal |
| 75 | `price_volatility` | `double` | Price volatility measure. | **Generic** | Universal market metric |
| 76 | `price_theoretical` | `double` | Theoretical option price. | **Generic** | Standard option pricing |
| 77 | `price_greeks_delta` | `double` | Option delta. | **Generic** | Standard option greek |
| 78 | `price_greeks_theta` | `double` | Option theta. | **Generic** | Standard option greek |
| 79 | `price_greeks_gamma` | `double` | Option gamma. | **Generic** | Standard option greek |
| 80 | `price_greeks_vega` | `double` | Option vega. | **Generic** | Standard option greek |
| 81 | `price_greeks_rho` | `double` | Option rho. | **Generic** | Standard option greek |
| 82 | `price_greeks_omega` | `double` | Option omega (lambda). | **Generic** | Standard option greek |
| 83 | `price_sensitivity` | `double` | Price sensitivity measure. | **Generic** | Standard metric |
| 84 | `basis` | `string` | Futures basis (cash vs futures price diff). | **Generic** | Standard futures concept |
| 85 | `category` | `string` | Symbol category. | **MT5-specific** | MT5-specific grouping taxonomy |
| 86 | `currency_base` | `string` | Base currency (e.g., "EUR" in EURUSD). | **Generic** | Universal |
| 87 | `currency_profit` | `string` | Profit currency. | **Generic** | Universal |
| 88 | `currency_margin` | `string` | Margin currency. | **Generic** | Universal (though named differently in some platforms) |
| 89 | `bank` | `string` | Liquidity provider / desk name. | **MT5-specific** | MT5-specific symbol metadata |
| 90 | `description` | `string` | Instrument description. | **Generic** | Universal |
| 91 | `exchange` | `string` | Exchange name. | **Generic** | Universal |
| 92 | `formula` | `string` | Custom symbol pricing formula. | **MT5-specific** | MT5 user-defined symbol formula |
| 93 | `isin` | `string` | ISIN identifier. | **Generic** | Universal financial identifier |
| 94 | `name` | `string` | Symbol name. | **Generic** | Universal |
| 95 | `page` | `string` | Symbol info web page URL. | **MT5-specific** | MT5-specific metadata (default Google Finance URL) |
| 96 | `path` | `string` | Symbol tree path in MarketWatch (e.g., "Forex\\EURJPY"). | **MT5-specific** | MT5-specific UI grouping |

### 3.4 `symbol_info_tick()`

**Purpose:** Get the last tick for the specified financial instrument.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Instrument name. | **Generic** |

**Return Type:** `Tick` (namedtuple)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `time` | `int64` | Tick timestamp (Unix seconds). | **Generic** | Universal |
| 2 | `bid` | `double` | Bid price. | **Generic** | Universal |
| 3 | `ask` | `double` | Ask price. | **Generic** | Universal |
| 4 | `last` | `double` | Last trade price. | **Generic** | Universal |
| 5 | `volume` | `int64` | Tick volume (integer lots). | **Generic** | Universal |
| 6 | `time_msc` | `int64` | Tick timestamp with milliseconds (Unix ms). | **Generic** | High-precision timestamp (field name `_msc` is MT5 convention) |
| 7 | `flags` | `int32` | Tick flags bitmask (TICK_FLAG_BID, ASK, LAST, VOLUME, BUY, SELL). | **MT5-specific** | MT5 enum (`TICK_FLAG_*`) — proprietary flag definitions |
| 8 | `volume_real` | `double` | Tick volume (float). | **Generic** | Universal |

### 3.5 `symbol_select()`

**Purpose:** Add or remove a symbol from the MarketWatch window.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Instrument name. | **Generic** |
| `enable` | `bool` | No | True=select in MarketWatch, False=remove. | **Generic** (though "MarketWatch" is MT5's UI name) |

**Return Value:** `bool` — True if successful.

---

## 4. Market Depth (Order Book)

### 4.1 `market_book_add()`

**Purpose:** Subscribe to Market Depth change events for a symbol.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Financial instrument name. | **Generic** |

**Return Value:** `bool`

### 4.2 `market_book_get()`

**Purpose:** Get current Market Depth entries (order book) for a symbol. Must call `market_book_add()` first.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Financial instrument name. | **Generic** |

**Return Type:** Tuple of `BookInfo` (namedtuple)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `type` | `int32` | Order type (1=SELL, 2=BUY, 3=SELL_MARKET, 4=BUY_MARKET). | **MT5-specific** | MT5 enum (`BOOK_TYPE_*`) — proprietary order book side classification |
| 2 | `price` | `double` | Order price. | **Generic** | Universal |
| 3 | `volume` | `int64` | Volume in lots (integer). | **Generic** | Universal |
| 4 | `volume_dbl` | `double` | Volume in lots (float). | **Generic** | Universal |

### 4.3 `market_book_release()`

**Purpose:** Cancel subscription to Market Depth change events.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Financial instrument name. | **Generic** |

**Return Value:** `bool`

---

## 5. Price History (Rates / OHLCV)

### 5.1 `copy_rates_from()`

**Purpose:** Get bars starting from a specific date.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Instrument name. | **Generic** |
| `timeframe` | `int32` | Yes | TIMEFRAME enum value (1M, 5M, 1H, D1, etc.). | **Generic** (standard timeframes) |
| `date_from` | `int64` / `datetime` | Yes | Start date (Unix seconds or Python datetime). | **Generic** |
| `count` | `int32` | Yes | Number of bars to retrieve. | **Generic** |

**Return Type:** NumPy array of `Rate` records

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `time` | `int64` | Bar open time (Unix seconds, UTC). | **Generic** | Universal |
| 2 | `open` | `double` | Open price. | **Generic** | Universal |
| 3 | `high` | `double` | High price. | **Generic** | Universal |
| 4 | `low` | `double` | Low price. | **Generic** | Universal |
| 5 | `close` | `double` | Close price. | **Generic** | Universal |
| 6 | `tick_volume` | `int64` | Tick count volume. | **Generic** | Universal (though some platforms use actual volume) |
| 7 | `spread` | `int32` | Spread in points at bar open. | **Generic** | Universal |
| 8 | `real_volume` | `int64` | Exchange-reported volume. | **Generic** | Universal |

### 5.2 `copy_rates_from_pos()`

**Purpose:** Get bars starting from a specific index (0 = current/forming bar, counting from present to past).

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Instrument name. | **Generic** |
| `timeframe` | `int32` | Yes | TIMEFRAME enum. | **Generic** |
| `start_pos` | `int32` | Yes | Starting bar index (0 = current). | **Generic** |
| `count` | `int32` | Yes | Number of bars. | **Generic** |

**Return Type:** Same as `copy_rates_from()` — `Rate` array.

### 5.3 `copy_rates_range()`

**Purpose:** Get bars within a date range.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Instrument name. | **Generic** |
| `timeframe` | `int32` | Yes | TIMEFRAME enum. | **Generic** |
| `date_from` | `int64` / `datetime` | Yes | Range start (inclusive). | **Generic** |
| `date_to` | `int64` / `datetime` | Yes | Range end (inclusive). | **Generic** |

**Return Type:** Same as above — `Rate` array.

---

## 6. Tick History

### 6.1 `copy_ticks_from()`

**Purpose:** Get ticks starting from a specified date.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Instrument name. | **Generic** |
| `date_from` | `int64` / `datetime` | Yes | Start date. | **Generic** |
| `count` | `int32` | Yes | Number of ticks. | **Generic** |
| `flags` | `int32` | Yes | COPY_TICKS_ALL, COPY_TICKS_INFO, or COPY_TICKS_TRADE. | **MT5-specific** (proprietary flag enum) |

**Return Type:** NumPy array of `Tick` records (same fields as 3.4 but with all tick data).

### 6.2 `copy_ticks_range()`

**Purpose:** Get ticks within a date range.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | Yes | Instrument name. | **Generic** |
| `date_from` | `int64` / `datetime` | Yes | Range start. | **Generic** |
| `date_to` | `int64` / `datetime` | Yes | Range end. | **Generic** |
| `flags` | `int32` | Yes | COPY_TICKS flag. | **MT5-specific** |

**Return Type:** Same as 6.1 — `Tick` array.

---

## 7. Orders (Active Pending)

### 7.1 `orders_total()`

**Purpose:** Get the number of active (pending) orders.

**Parameters:** None

**Return Value:** `int32`

### 7.2 `orders_get()`

**Purpose:** Get active orders with optional filtering by symbol, group, or ticket.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | No | Filter by symbol name. | **Generic** |
| `group` | `string` | No | Wildcard filter for symbols. | **MT5-specific** (wildcard syntax is MT5's convention) |
| `ticket` | `int64` | No | Filter by specific order ticket. | **Generic** |

**Return Type:** Tuple of `TradeOrder` (namedtuple)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `ticket` | `int64` | Order ticket (unique ID). | **Generic** | Universal order ID |
| 2 | `time_setup` | `int64` | Order creation time (Unix seconds). | **Generic** | Universal |
| 3 | `time_setup_msc` | `int64` | Order creation time with ms. | **Generic** | High-precision timestamp |
| 4 | `time_done` | `int64` | Order execution/cancellation time. | **Generic** | Universal |
| 5 | `time_done_msc` | `int64` | Execution time with ms. | **Generic** | High-precision timestamp |
| 6 | `time_expiration` | `int64` | Order expiration time. | **Generic** | Universal |
| 7 | `type` | `int32` | Order type (BUY/SELL/BUY_LIMIT/SELL_LIMIT/BUY_STOP/SELL_STOP/BUY_STOP_LIMIT/SELL_STOP_LIMIT/CLOSE_BY). | **MT5-specific** | MT5 enum (`ORDER_TYPE_*`) — includes MT5-specific types like CLOSE_BY |
| 8 | `type_time` | `int32` | Order expiration type (GTC/DAY/SPECIFIED/SPECIFIED_DAY). | **MT5-specific** | MT5 enum (`ORDER_TYPE_TIME_*`) |
| 9 | `type_filling` | `int32` | Order filling type (FOK/IOC/RETURN). | **MT5-specific** | MT5 enum (`ORDER_TYPE_FILLING_*`) — proprietary execution policy |
| 10 | `state` | `int32` | Order state (STARTED/PLACED/CANCELED/PARTIAL/FILLED/REJECTED/EXPIRED). | **MT5-specific** | MT5 enum (`ORDER_STATE_*`) |
| 11 | `magic` | `int64` | Expert Advisor ID. | **MT5-specific** | MQL5 concept for identifying which EA created the order |
| 12 | `volume_current` | `double` | Remaining volume to fill. | **Generic** | Universal (remaining open quantity) |
| 13 | `volume_initial` | `double` | Original volume when placed. | **Generic** | Universal |
| 14 | `price_open` | `double` | Order price. | **Generic** | Universal |
| 15 | `sl` | `double` | Stop Loss price. | **Generic** | Universal |
| 16 | `tp` | `double` | Take Profit price. | **Generic** | Universal |
| 17 | `price_current` | `double` | Current market price for the symbol. | **Generic** | Universal |
| 18 | `price_stoplimit` | `double` | Stop Limit trigger price. | **Generic** | Universal for Stop Limit orders |
| 19 | `symbol` | `string` | Symbol name. | **Generic** | Universal |
| 20 | `comment` | `string` | Order comment. | **Generic** | Universal |
| 21 | `external_id` | `string` | External (broker/exchange) order ID. | **Generic** | Universal |
| 22 | `position_id` | `int64` | ID of the position the order is associated with. | **Generic** | Common position linkage concept |
| 23 | `position_by_id` | `int64` | Opposite position ID (MT5 hedging). | **MT5-specific** | MT5 hedge-close mechanism — opposite position reference |
| 24 | `reason` | `int32` | Order creation reason (CLIENT/MOBILE/WEB/EXPERT/etc). | **MT5-specific** | MT5 enum (`ORDER_REASON_*`) — proprietary origin tracking |

### 7.3 `order_calc_margin()`

**Purpose:** Calculate margin required for a specific trading operation.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `action` | `int32` | Yes | ORDER_TYPE (BUY or SELL). | **Generic** |
| `symbol` | `string` | Yes | Instrument name. | **Generic** |
| `volume` | `double` | Yes | Trade volume in lots. | **Generic** |
| `price` | `double` | Yes | Open price. | **Generic** |

**Return Value:** `double` — margin in account currency.

**Note:** The margin calculation itself uses MT5's `OrderCalcMargin()` internally, but the concept is universal.

### 7.4 `order_calc_profit()`

**Purpose:** Calculate profit for a specific trading operation.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `action` | `int32` | Yes | ORDER_TYPE (BUY or SELL). | **Generic** |
| `symbol` | `string` | Yes | Instrument name. | **Generic** |
| `volume` | `double` | Yes | Trade volume. | **Generic** |
| `price_open` | `double` | Yes | Open price. | **Generic** |
| `price_close` | `double` | Yes | Close price. | **Generic** |

**Return Value:** `double` — profit in account currency.

### 7.5 `order_check()`

**Purpose:** Check funds sufficiency for a trading operation before sending it.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `request` | `dict` (TradeRequest) | Yes | Trading request structure. | See [Section 10](#10-trading-request--result-structures) |

**Return Type:** `TradeCheckResult` (see 10.2)

### 7.6 `order_send()`

**Purpose:** Send a trading request to the trade server for execution.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `request` | `dict` (TradeRequest) | Yes | Trading request structure. | See [Section 10](#10-trading-request--result-structures) |

**Return Type:** `TradeSendResult` (see 10.3)

---

## 8. Positions (Open Trades)

### 8.1 `positions_total()`

**Purpose:** Get the number of open positions.

**Parameters:** None

**Return Value:** `int32`

### 8.2 `positions_get()`

**Purpose:** Get open positions with optional filtering.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `symbol` | `string` | No | Filter by symbol. | **Generic** |
| `group` | `string` | No | Wildcard filter for symbols. | **MT5-specific** |
| `ticket` | `int64` | No | Filter by position ticket. | **Generic** |

**Return Type:** Tuple of `TradePosition` (namedtuple)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `ticket` | `int64` | Position ticket (unique ID). | **Generic** | Universal |
| 2 | `time` | `int64` | Position open time (Unix seconds). | **Generic** | Universal |
| 3 | `time_msc` | `int64` | Open time with milliseconds. | **Generic** | High-precision timestamp |
| 4 | `time_update` | `int64` | Last update time (Unix seconds). | **Generic** | Universal |
| 5 | `time_update_msc` | `int64` | Update time with milliseconds. | **Generic** | High-precision timestamp |
| 6 | `type` | `int32` | Position type (0=BUY, 1=SELL). | **MT5-specific** | MT5 enum (`POSITION_TYPE_*`); other platforms may use different enum values |
| 7 | `magic` | `int64` | Expert Advisor ID. | **MT5-specific** | MQL5 concept |
| 8 | `identifier` | `int64` | Position identifier (distinct from ticket in netting mode). | **MT5-specific** | MT5 netting system identifier; ticket != identifier in netting mode |
| 9 | `reason` | `int32` | Position open reason. | **MT5-specific** | MT5 enum (`POSITION_REASON_*`) |
| 10 | `volume` | `double` | Position volume (lots). | **Generic** | Universal |
| 11 | `price_open` | `double` | Open price. | **Generic** | Universal |
| 12 | `sl` | `double` | Stop Loss price. | **Generic** | Universal |
| 13 | `tp` | `double` | Take Profit price. | **Generic** | Universal |
| 14 | `price_current` | `double` | Current market price. | **Generic** | Universal |
| 15 | `swap` | `double` | Accumulated swap (rollover interest). | **Generic** | Universal |
| 16 | `profit` | `double` | Floating profit/loss. | **Generic** | Universal |
| 17 | `symbol` | `string` | Symbol name. | **Generic** | Universal |
| 18 | `comment` | `string` | Position comment. | **Generic** | Universal |
| 19 | `external_id` | `string` | External ID (broker/exchange). | **Generic** | Universal |

---

## 9. History — Orders & Deals

### 9.1 `history_orders_total()`

**Purpose:** Get the number of orders in trading history within a time interval.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `date_from` | `int64` / `datetime` | Yes | Start of interval. | **Generic** |
| `date_to` | `int64` / `datetime` | Yes | End of interval. | **Generic** |

**Return Value:** `int32`

### 9.2 `history_orders_get()`

**Purpose:** Get orders from trading history with optional filtering.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `date_from` | `int64` / `datetime` | Yes* | Start of interval (*required for time-based query). | **Generic** |
| `date_to` | `int64` / `datetime` | Yes* | End of interval (*required for time-based query). | **Generic** |
| `group` | `string` | No | Wildcard filter for symbols. | **MT5-specific** |
| `ticket` | `int64` | No | Filter by order ticket (alternative query mode). | **Generic** |
| `position` | `int64` | No | Filter by position ticket (alternative query mode). | **Generic** |

**Return Type:** Tuple of `TradeOrder` (same fields as 7.2)

### 9.3 `history_deals_total()`

**Purpose:** Get the number of deals in trading history within a time interval.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `date_from` | `int64` / `datetime` | Yes | Start of interval. | **Generic** |
| `date_to` | `int64` / `datetime` | Yes | End of interval. | **Generic** |

**Return Value:** `int32`

### 9.4 `history_deals_get()`

**Purpose:** Get deals from trading history with optional filtering.

**Parameters:**

| Parameter | Type | Required | Description | Classification |
|-----------|------|----------|-------------|----------------|
| `date_from` | `int64` / `datetime` | Yes* | Start of interval (*required for time-based query). | **Generic** |
| `date_to` | `int64` / `datetime` | Yes* | End of interval (*required for time-based query). | **Generic** |
| `group` | `string` | No | Wildcard filter for symbols. | **MT5-specific** |
| `ticket` | `int64` | No | Filter by order ticket (all deals for an order). | **Generic** |
| `position` | `int64` | No | Filter by position ticket (all deals for a position). | **Generic** |

**Return Type:** Tuple of `TradeDeal` (namedtuple)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `ticket` | `int64` | Deal ticket (unique ID). | **Generic** | Universal |
| 2 | `order` | `int64` | Order ticket that generated the deal. | **Generic** | Universal order link |
| 3 | `time` | `int64` | Deal time (Unix seconds). | **Generic** | Universal |
| 4 | `time_msc` | `int64` | Deal time with milliseconds. | **Generic** | High-precision timestamp |
| 5 | `type` | `int32` | Deal type (BUY/SELL/BALANCE/CREDIT/CHARGE/CORRECTION/BONUS/COMMISSION/COMMISSION_DAILY/etc). | **MT5-specific** | MT5 enum (`DEAL_TYPE_*`) — includes MT5-specific types like COMMISSION_DAILY, COMMISSION_AGENT_MONTHLY |
| 6 | `entry` | `int32` | Deal entry (IN/OUT/INOUT/OUT_BY). | **MT5-specific** | MT5 enum (`DEAL_ENTRY_*`) — proprietary position entry/exit classification |
| 7 | `magic` | `int64` | Expert Advisor ID. | **MT5-specific** | MQL5 concept |
| 8 | `position_id` | `int64` | Position ID the deal belongs to. | **Generic** | Position link (common concept) |
| 9 | `reason` | `int32` | Deal reason (CLIENT/MOBILE/WEB/EXPERT/etc). | **MT5-specific** | MT5 enum (`DEAL_REASON_*`) |
| 10 | `volume` | `double` | Deal volume (lots). | **Generic** | Universal |
| 11 | `price` | `double` | Deal price. | **Generic** | Universal |
| 12 | `commission` | `double` | Commission charged. | **Generic** | Universal |
| 13 | `swap` | `double` | Swap charged. | **Generic** | Universal |
| 14 | `profit` | `double` | Deal profit/loss. | **Generic** | Universal |
| 15 | `fee` | `double` | Service fee. | **Generic** | Universal |
| 16 | `symbol` | `string` | Symbol name. | **Generic** | Universal |
| 17 | `comment` | `string` | Deal comment. | **Generic** | Universal |
| 18 | `external_id` | `string` | External ID. | **Generic** | Universal |

---

## 10. Trading Request / Result Structures

### 10.1 `TradeRequest` (dict used in `order_check()` and `order_send()`)

| # | Field | Type | Required | Description | Classification | Rationale |
|---|-------|------|----------|-------------|----------------|----------|
| 1 | `action` | `int32` | Yes | TRADE_ACTION enum (DEAL/PENDING/SLTP/MODIFY/REMOVE/CLOSE_BY). | **MT5-specific** | MT5 enum (`TRADE_REQUEST_ACTIONS_*`) |
| 2 | `magic` | `int64` | No | EA ID. | **MT5-specific** | MQL5 concept |
| 3 | `order` | `int64` | Cond. | Order ticket (required for MODIFY/REMOVE). | **Generic** | Order reference |
| 4 | `symbol` | `string` | Cond. | Symbol name (not required for MODIFY/REMOVE). | **Generic** | Universal |
| 5 | `volume` | `double` | Cond. | Deal volume (required for DEAL/PENDING). | **Generic** | Universal |
| 6 | `price` | `double` | Cond. | Order price (not required for market orders with Market Execution). | **Generic** | Universal |
| 7 | `stoplimit` | `double` | No | Stop Limit trigger price. | **Generic** | Universal |
| 8 | `sl` | `double` | No | Stop Loss price. | **Generic** | Universal |
| 9 | `tp` | `double` | No | Take Profit price. | **Generic** | Universal |
| 10 | `deviation` | `int32` | No | Max price deviation (slippage) in points. | **Generic** | Universal slippage control |
| 11 | `type` | `int32` | Cond. | ORDER_TYPE (required for DEAL/PENDING). | **MT5-specific** | MT5 enum |
| 12 | `type_filling` | `int32` | No | ORDER_FILLING type. | **MT5-specific** | MT5 enum |
| 13 | `type_time` | `int32` | No | ORDER_TIME type. | **MT5-specific** | MT5 enum |
| 14 | `expiration` | `int64` | No | Order expiration time (for SPECIFIED/SPECIFIED_DAY). | **Generic** | Universal |
| 15 | `comment` | `string` | No | Order comment. | **Generic** | Universal |
| 16 | `position` | `int64` | Cond. | Position ticket (required for closing/modifying positions). | **Generic** | Position reference (naming is MT5-style) |
| 17 | `position_by` | `int64` | No | Opposite position ticket (for CLOSE_BY). | **MT5-specific** | MT5 hedge-close concept |

### 10.2 `TradeCheckResult` (from `order_check()`)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `retcode` | `int32` | Return code (0 = success). | **MT5-specific** | MT5 enum (`TRADE_RETCODE_*`) |
| 2 | `balance` | `double` | Account balance after check. | **Generic** | Universal |
| 3 | `equity` | `double` | Account equity after check. | **Generic** | Universal |
| 4 | `profit` | `double` | Account profit after check. | **Generic** | Universal |
| 5 | `margin` | `double` | Margin required. | **Generic** | Universal |
| 6 | `margin_free` | `double` | Free margin after check. | **Generic** | Universal |
| 7 | `margin_level` | `double` | Margin level after check. | **Generic** | Universal |
| 8 | `comment` | `string` | Result description. | **Generic** | Universal |
| 9 | `request` | `TradeRequest` | Copy of the original request. | **Generic** | Echo of input |

### 10.3 `TradeSendResult` (from `order_send()`)

| # | Field | Type | Description | Classification | Rationale |
|---|-------|------|-------------|----------------|----------|
| 1 | `retcode` | `int32` | Return code (10009 = DONE). | **MT5-specific** | MT5 enum |
| 2 | `deal` | `int64` | Deal ticket (if a deal was made). | **Generic** | Universal |
| 3 | `order` | `int64` | Order ticket (if an order was placed). | **Generic** | Universal |
| 4 | `volume` | `double` | Executed volume. | **Generic** | Universal |
| 5 | `price` | `double` | Executed price. | **Generic** | Universal |
| 6 | `bid` | `double` | Bid price after execution. | **Generic** | Universal |
| 7 | `ask` | `double` | Ask price after execution. | **Generic** | Universal |
| 8 | `comment` | `string` | Result description. | **Generic** | Universal |
| 9 | `request_id` | `int32` | Internal MT5 request tracking ID. | **MT5-specific** | MT5 internal routing |
| 10 | `retcode_external` | `int32` | External (gateway/broker) return code. | **MT5-specific** | Broker/exchange gateway return code |
| 11 | `request` | `TradeRequest` | Copy of the original request. | **Generic** | Echo of input |

---

## 11. Enum Reference

The following enums are used by the MT5 Python API. All values are sourced from the `MetaTrader5` Python module source (`MetaTrader5/__init__.py` v5.0.5735). Each corresponds to a protobuf enum definition.

> **Protobuf note:** Enums with raw values are designed for `int32` mapping in proto3. Non-contiguous values (e.g. `TRADE_REQUEST_ACTIONS`) require explicit `option allow_alias = false` or numbered entries. Bitmask fields (`TICK_FLAG`, `SYMBOL_EXPIRATION_MODE`, `SYMBOL_FILLING_MODE`, `SYMBOL_ORDER_MODE`) should use `int32` in protobuf rather than enum, since multiple bits can be set simultaneously.

---

### 11.1 `TIMEFRAME` (shared with MQL5 standard)

| Name | Value |
|------|-------|
| `TIMEFRAME_M1` | 1 |
| `TIMEFRAME_M2` | 2 |
| `TIMEFRAME_M3` | 3 |
| `TIMEFRAME_M4` | 4 |
| `TIMEFRAME_M5` | 5 |
| `TIMEFRAME_M6` | 6 |
| `TIMEFRAME_M10` | 10 |
| `TIMEFRAME_M12` | 12 |
| `TIMEFRAME_M15` | 15 |
| `TIMEFRAME_M20` | 20 |
| `TIMEFRAME_M30` | 30 |
| `TIMEFRAME_H1` | 1 \| 0x4000 = 16385 |
| `TIMEFRAME_H2` | 2 \| 0x4000 = 16386 |
| `TIMEFRAME_H3` | 3 \| 0x4000 = 16387 |
| `TIMEFRAME_H4` | 4 \| 0x4000 = 16388 |
| `TIMEFRAME_H6` | 6 \| 0x4000 = 16390 |
| `TIMEFRAME_H8` | 8 \| 0x4000 = 16392 |
| `TIMEFRAME_H12` | 12 \| 0x4000 = 16396 |
| `TIMEFRAME_D1` | 24 \| 0x4000 = 16408 |
| `TIMEFRAME_W1` | 1 \| 0x8000 = 32769 |
| `TIMEFRAME_MN1` | 1 \| 0xC000 = 49153 |

---

### 11.2 `ORDER_TYPE` (`ENUM_ORDER_TYPE`)

| Name | Value | Description |
|------|-------|-------------|
| `ORDER_TYPE_BUY` | 0 | Market Buy order |
| `ORDER_TYPE_SELL` | 1 | Market Sell order |
| `ORDER_TYPE_BUY_LIMIT` | 2 | Buy Limit pending order |
| `ORDER_TYPE_SELL_LIMIT` | 3 | Sell Limit pending order |
| `ORDER_TYPE_BUY_STOP` | 4 | Buy Stop pending order |
| `ORDER_TYPE_SELL_STOP` | 5 | Sell Stop pending order |
| `ORDER_TYPE_BUY_STOP_LIMIT` | 6 | Upon reaching the order price, a pending Buy Limit order is placed at the StopLimit price |
| `ORDER_TYPE_SELL_STOP_LIMIT` | 7 | Upon reaching the order price, a pending Sell Limit order is placed at the StopLimit price |
| `ORDER_TYPE_CLOSE_BY` | 8 | Order to close a position by an opposite one |

---

### 11.3 `ORDER_TYPE_FILLING` (`ENUM_ORDER_TYPE_FILLING`)

| Name | Value | Description |
|------|-------|-------------|
| `ORDER_FILLING_FOK` | 0 | Fill Or Kill — execute entirely or cancel |
| `ORDER_FILLING_IOC` | 1 | Immediate Or Cancel — execute max available volume |
| `ORDER_FILLING_RETURN` | 2 | Return — remaining volume stays as an active order |
| `ORDER_FILLING_BOC` | 3 | Book Or Cancel — placed in Depth of Market only, not immediately executed |

---

### 11.4 `ORDER_TYPE_TIME` (`ENUM_ORDER_TYPE_TIME`)

| Name | Value | Description |
|------|-------|-------------|
| `ORDER_TIME_GTC` | 0 | Good till cancelled |
| `ORDER_TIME_DAY` | 1 | Good till current trading day |
| `ORDER_TIME_SPECIFIED` | 2 | Good till specified expiration date |
| `ORDER_TIME_SPECIFIED_DAY` | 3 | Good till 23:59:59 of specified day |

---

### 11.5 `ORDER_STATE` (`ENUM_ORDER_STATE`)

| Name | Value | Description |
|------|-------|-------------|
| `ORDER_STATE_STARTED` | 0 | Checked but not yet accepted by broker |
| `ORDER_STATE_PLACED` | 1 | Accepted |
| `ORDER_STATE_CANCELED` | 2 | Cancelled by client |
| `ORDER_STATE_PARTIAL` | 3 | Partially executed |
| `ORDER_STATE_FILLED` | 4 | Fully executed |
| `ORDER_STATE_REJECTED` | 5 | Rejected |
| `ORDER_STATE_EXPIRED` | 6 | Expired |
| `ORDER_STATE_REQUEST_ADD` | 7 | Being registered (placing to trading system) |
| `ORDER_STATE_REQUEST_MODIFY` | 8 | Being modified (changing parameters) |
| `ORDER_STATE_REQUEST_CANCEL` | 9 | Being deleted (deleting from trading system) |

---

### 11.6 `TRADE_REQUEST_ACTIONS` (`ENUM_TRADE_REQUEST_ACTIONS`)

| Name | Value | Description |
|------|-------|-------------|
| `TRADE_ACTION_DEAL` | 1 | Market order (immediate execution) |
| `TRADE_ACTION_PENDING` | 5 | Place a pending order |
| `TRADE_ACTION_SLTP` | 6 | Modify Stop Loss and Take Profit |
| `TRADE_ACTION_MODIFY` | 7 | Modify order parameters |
| `TRADE_ACTION_REMOVE` | 8 | Delete a pending order |
| `TRADE_ACTION_CLOSE_BY` | 10 | Close a position by an opposite one |

> **Note:** Values are non-contiguous (gaps at 2,3,4,9). Protobuf enum numbering should preserve these raw values.

---

### 11.7 `DEAL_TYPE` (`ENUM_DEAL_TYPE`)

| Name | Value | Description |
|------|-------|-------------|
| `DEAL_TYPE_BUY` | 0 | Buy |
| `DEAL_TYPE_SELL` | 1 | Sell |
| `DEAL_TYPE_BALANCE` | 2 | Balance |
| `DEAL_TYPE_CREDIT` | 3 | Credit |
| `DEAL_TYPE_CHARGE` | 4 | Additional charge |
| `DEAL_TYPE_CORRECTION` | 5 | Correction |
| `DEAL_TYPE_BONUS` | 6 | Bonus |
| `DEAL_TYPE_COMMISSION` | 7 | Additional commission |
| `DEAL_TYPE_COMMISSION_DAILY` | 8 | Daily commission |
| `DEAL_TYPE_COMMISSION_MONTHLY` | 9 | Monthly commission |
| `DEAL_TYPE_COMMISSION_AGENT_DAILY` | 10 | Daily agent commission |
| `DEAL_TYPE_COMMISSION_AGENT_MONTHLY` | 11 | Monthly agent commission |
| `DEAL_TYPE_INTEREST` | 12 | Interest rate |
| `DEAL_TYPE_BUY_CANCELED` | 13 | Canceled buy deal |
| `DEAL_TYPE_SELL_CANCELED` | 14 | Canceled sell deal |
| `DEAL_DIVIDEND` | 15 | Dividend operations |
| `DEAL_DIVIDEND_FRANKED` | 16 | Franked (non-taxable) dividend operations |
| `DEAL_TAX` | 17 | Tax charges |

---

### 11.8 `DEAL_ENTRY` (`ENUM_DEAL_ENTRY`)

| Name | Value | Description |
|------|-------|-------------|
| `DEAL_ENTRY_IN` | 0 | Entry in (position open) |
| `DEAL_ENTRY_OUT` | 1 | Entry out (position close) |
| `DEAL_ENTRY_INOUT` | 2 | Reverse |
| `DEAL_ENTRY_OUT_BY` | 3 | Close by an opposite position |

---

### 11.9 `COPY_TICKS`

| Name | Value | Description |
|------|-------|-------------|
| `COPY_TICKS_ALL` | -1 | All ticks |
| `COPY_TICKS_INFO` | 1 | Ticks with Bid and/or Ask changes |
| `COPY_TICKS_TRADE` | 2 | Ticks with Last and/or Volume changes |

> **Note:** `COPY_TICKS_ALL = -1` is a signed int, not a bitmask. Use `int32` in protobuf.

---

### 11.10 `TICK_FLAG` (bitmask)

| Name | Value | Bit | Description |
|------|-------|-----|-------------|
| `TICK_FLAG_BID` | `0x02` | 1 | Bid price changed |
| `TICK_FLAG_ASK` | `0x04` | 2 | Ask price changed |
| `TICK_FLAG_LAST` | `0x08` | 3 | Last price changed |
| `TICK_FLAG_VOLUME` | `0x10` | 4 | Volume changed |
| `TICK_FLAG_BUY` | `0x20` | 5 | Last Buy price changed |
| `TICK_FLAG_SELL` | `0x40` | 6 | Last Sell price changed |

> **Note:** A reserved internal flag (`0x80`, bit 7) may appear in real tick data. Multiple flags can be combined (e.g. `0x86` = ASK \| BID \| VOLUME).

---

### 11.11 `BOOK_TYPE` (`ENUM_BOOK_TYPE`)

| Name | Value | Description |
|------|-------|-------------|
| `BOOK_TYPE_SELL` | 1 | Sell order |
| `BOOK_TYPE_BUY` | 2 | Buy order |
| `BOOK_TYPE_SELL_MARKET` | 3 | Sell market order |
| `BOOK_TYPE_BUY_MARKET` | 4 | Buy market order |

---

### 11.12 `TRADE_RETCODE` (trade server return codes)

| Name | Value | Description |
|------|-------|-------------|
| `TRADE_RETCODE_REQUOTE` | 10004 | Requote |
| `TRADE_RETCODE_REJECT` | 10006 | Request rejected |
| `TRADE_RETCODE_CANCEL` | 10007 | Request cancelled by trader |
| `TRADE_RETCODE_PLACED` | 10008 | Order placed |
| `TRADE_RETCODE_DONE` | 10009 | Request completed |
| `TRADE_RETCODE_DONE_PARTIAL` | 10010 | Request partially completed |
| `TRADE_RETCODE_ERROR` | 10011 | Request processing error |
| `TRADE_RETCODE_TIMEOUT` | 10012 | Request cancelled by timeout |
| `TRADE_RETCODE_INVALID` | 10013 | Invalid request |
| `TRADE_RETCODE_INVALID_VOLUME` | 10014 | Invalid volume |
| `TRADE_RETCODE_INVALID_PRICE` | 10015 | Invalid price |
| `TRADE_RETCODE_INVALID_STOPS` | 10016 | Invalid stops |
| `TRADE_RETCODE_TRADE_DISABLED` | 10017 | Trade disabled |
| `TRADE_RETCODE_MARKET_CLOSED` | 10018 | Market closed |
| `TRADE_RETCODE_NO_MONEY` | 10019 | Insufficient funds |
| `TRADE_RETCODE_PRICE_CHANGED` | 10020 | Price changed |
| `TRADE_RETCODE_PRICE_OFF` | 10021 | Price out of offset |
| `TRADE_RETCODE_INVALID_EXPIRATION` | 10022 | Invalid expiration |
| `TRADE_RETCODE_ORDER_CHANGED` | 10023 | Order changed |
| `TRADE_RETCODE_TOO_MANY_REQUESTS` | 10024 | Too many requests |
| `TRADE_RETCODE_NO_CHANGES` | 10025 | No changes |
| `TRADE_RETCODE_SERVER_DISABLES_AT` | 10026 | Auto-trading disabled by server |
| `TRADE_RETCODE_CLIENT_DISABLES_AT` | 10027 | Auto-trading disabled by client |
| `TRADE_RETCODE_LOCKED` | 10028 | Request locked |
| `TRADE_RETCODE_FROZEN` | 10029 | Request frozen |
| `TRADE_RETCODE_INVALID_FILL` | 10030 | Invalid fill |
| `TRADE_RETCODE_CONNECTION` | 10031 | No connection |
| `TRADE_RETCODE_ONLY_REAL` | 10032 | Allowed only for real accounts |
| `TRADE_RETCODE_LIMIT_ORDERS` | 10033 | Limit orders exceeded |
| `TRADE_RETCODE_LIMIT_VOLUME` | 10034 | Limit volume exceeded |
| `TRADE_RETCODE_INVALID_ORDER` | 10035 | Invalid order |
| `TRADE_RETCODE_POSITION_CLOSED` | 10036 | Position already closed |
| `TRADE_RETCODE_INVALID_CLOSE_VOLUME` | 10038 | Invalid close volume |
| `TRADE_RETCODE_CLOSE_ORDER_EXIST` | 10039 | Close order already exists |
| `TRADE_RETCODE_LIMIT_POSITIONS` | 10040 | Limit positions exceeded |
| `TRADE_RETCODE_REJECT_CANCEL` | 10041 | Cancel of pending order rejected |
| `TRADE_RETCODE_LONG_ONLY` | 10042 | Long positions only allowed |
| `TRADE_RETCODE_SHORT_ONLY` | 10043 | Short positions only allowed |
| `TRADE_RETCODE_CLOSE_ONLY` | 10044 | Close only allowed |
| `TRADE_RETCODE_FIFO_CLOSE` | 10045 | FIFO close required |

> **Note:** The range is 10004–10045, not starting at 0. Protobuf enum numbering should preserve these raw values.

---

### 11.13 `POSITION_TYPE` (`ENUM_POSITION_TYPE`)

| Name | Value | Description |
|------|-------|-------------|
| `POSITION_TYPE_BUY` | 0 | Buy |
| `POSITION_TYPE_SELL` | 1 | Sell |

---

### 11.14 `POSITION_REASON` (`ENUM_POSITION_REASON`)

| Name | Value | Description |
|------|-------|-------------|
| `POSITION_REASON_CLIENT` | 0 | Opened from a desktop terminal |
| `POSITION_REASON_MOBILE` | 1 | Opened from a mobile application |
| `POSITION_REASON_WEB` | 2 | Opened from a web platform |
| `POSITION_REASON_EXPERT` | 3 | Opened from an MQL5 program (EA / script) |

---

### 11.15 `ORDER_REASON` (`ENUM_ORDER_REASON`)

| Name | Value | Description |
|------|-------|-------------|
| `ORDER_REASON_CLIENT` | 0 | Placed from a desktop terminal |
| `ORDER_REASON_MOBILE` | 1 | Placed from a mobile application |
| `ORDER_REASON_WEB` | 2 | Placed from a web platform |
| `ORDER_REASON_EXPERT` | 3 | Placed from an MQL5 program |
| `ORDER_REASON_SL` | 4 | Stop Loss activation |
| `ORDER_REASON_TP` | 5 | Take Profit activation |
| `ORDER_REASON_SO` | 6 | Stop Out event |

---

### 11.16 `DEAL_REASON` (`ENUM_DEAL_REASON`)

| Name | Value | Description |
|------|-------|-------------|
| `DEAL_REASON_CLIENT` | 0 | Desktop terminal |
| `DEAL_REASON_MOBILE` | 1 | Mobile application |
| `DEAL_REASON_WEB` | 2 | Web platform |
| `DEAL_REASON_EXPERT` | 3 | MQL5 program |
| `DEAL_REASON_SL` | 4 | Stop Loss activation |
| `DEAL_REASON_TP` | 5 | Take Profit activation |
| `DEAL_REASON_SO` | 6 | Stop Out event |
| `DEAL_REASON_ROLLOVER` | 7 | Rollover |
| `DEAL_REASON_VMARGIN` | 8 | Variation margin |
| `DEAL_REASON_SPLIT` | 9 | Split (price reduction) |

---

### 11.17 `SYMBOL_CALC_MODE` (`ENUM_SYMBOL_CALC_MODE`)

Used by `SymbolInfo.trade_calc_mode` field.

| Name | Value | Description |
|------|-------|-------------|
| `SYMBOL_CALC_MODE_FOREX` | 0 | Forex |
| `SYMBOL_CALC_MODE_FUTURES` | 1 | Futures |
| `SYMBOL_CALC_MODE_CFD` | 2 | CFD |
| `SYMBOL_CALC_MODE_CFDINDEX` | 3 | CFD Index |
| `SYMBOL_CALC_MODE_CFDLEVERAGE` | 4 | CFD Leverage |
| `SYMBOL_CALC_MODE_FOREX_NO_LEVERAGE` | 5 | Forex no leverage |
| `SYMBOL_CALC_MODE_EXCH_STOCKS` | 32 | Exchange stocks |
| `SYMBOL_CALC_MODE_EXCH_FUTURES` | 33 | Exchange futures |
| `SYMBOL_CALC_MODE_EXCH_OPTIONS` | 34 | Exchange options |
| `SYMBOL_CALC_MODE_EXCH_OPTIONS_MARGIN` | 36 | Exchange options (margin) |
| `SYMBOL_CALC_MODE_EXCH_BONDS` | 37 | Exchange bonds |
| `SYMBOL_CALC_MODE_EXCH_STOCKS_MOEX` | 38 | Exchange stocks (MOEX) |
| `SYMBOL_CALC_MODE_EXCH_BONDS_MOEX` | 39 | Exchange bonds (MOEX) |
| `SYMBOL_CALC_MODE_SERV_COLLATERAL` | 64 | Service collateral |

---

### 11.18 `SYMBOL_TRADE_MODE` (`ENUM_SYMBOL_TRADE_MODE`)

Used by `SymbolInfo.trade_mode` field.

| Name | Value | Description |
|------|-------|-------------|
| `SYMBOL_TRADE_MODE_DISABLED` | 0 | Trading disabled |
| `SYMBOL_TRADE_MODE_LONGONLY` | 1 | Long positions only |
| `SYMBOL_TRADE_MODE_SHORTONLY` | 2 | Short positions only |
| `SYMBOL_TRADE_MODE_CLOSEONLY` | 3 | Close only |
| `SYMBOL_TRADE_MODE_FULL` | 4 | Full trading |

---

### 11.19 `SYMBOL_TRADE_EXECUTION` (`ENUM_SYMBOL_TRADE_EXECUTION`)

Used by `SymbolInfo.trade_exemode` field.

| Name | Value | Description |
|------|-------|-------------|
| `SYMBOL_TRADE_EXECUTION_REQUEST` | 0 | Request execution |
| `SYMBOL_TRADE_EXECUTION_INSTANT` | 1 | Instant execution |
| `SYMBOL_TRADE_EXECUTION_MARKET` | 2 | Market execution |
| `SYMBOL_TRADE_EXECUTION_EXCHANGE` | 3 | Exchange execution |

---

### 11.20 `SYMBOL_SWAP_MODE` (`ENUM_SYMBOL_SWAP_MODE`)

Used by `SymbolInfo.swap_mode` field.

| Name | Value | Description |
|------|-------|-------------|
| `SYMBOL_SWAP_MODE_DISABLED` | 0 | Swaps disabled |
| `SYMBOL_SWAP_MODE_POINTS` | 1 | Points |
| `SYMBOL_SWAP_MODE_CURRENCY_SYMBOL` | 2 | Currency (symbol deposit) |
| `SYMBOL_SWAP_MODE_CURRENCY_MARGIN` | 3 | Currency (margin deposit) |
| `SYMBOL_SWAP_MODE_CURRENCY_DEPOSIT` | 4 | Currency (deposit) |
| `SYMBOL_SWAP_MODE_INTEREST_CURRENT` | 5 | Interest (current) |
| `SYMBOL_SWAP_MODE_INTEREST_OPEN` | 6 | Interest (open) |
| `SYMBOL_SWAP_MODE_REOPEN_CURRENT` | 7 | Reopen (current) |
| `SYMBOL_SWAP_MODE_REOPEN_BID` | 8 | Reopen (bid) |

---

### 11.21 `SYMBOL_CHART_MODE` (`ENUM_SYMBOL_CHART_MODE`)

Used by `SymbolInfo.chart_mode` field.

| Name | Value |
|------|-------|
| `SYMBOL_CHART_MODE_BID` | 0 |
| `SYMBOL_CHART_MODE_LAST` | 1 |

---

### 11.22 `SYMBOL_ORDER_GTC_MODE` (`ENUM_SYMBOL_ORDER_GTC_MODE`)

Used by `SymbolInfo.order_gtc_mode` field.

| Name | Value | Description |
|------|-------|-------------|
| `SYMBOL_ORDERS_GTC` | 0 | Good-till-cancelled orders allowed |
| `SYMBOL_ORDERS_DAILY` | 1 | Daily orders only |
| `SYMBOL_ORDERS_DAILY_NO_STOPS` | 2 | Daily orders, no stops |

---

### 11.23 `SYMBOL_OPTION_RIGHT` (`ENUM_SYMBOL_OPTION_RIGHT`)

Used by `SymbolInfo.option_right` field.

| Name | Value |
|------|-------|
| `SYMBOL_OPTION_RIGHT_CALL` | 0 |
| `SYMBOL_OPTION_RIGHT_PUT` | 1 |

---

### 11.24 `SYMBOL_OPTION_MODE` (`ENUM_SYMBOL_OPTION_MODE`)

Used by `SymbolInfo.option_mode` field.

| Name | Value |
|------|-------|
| `SYMBOL_OPTION_MODE_EUROPEAN` | 0 |
| `SYMBOL_OPTION_MODE_AMERICAN` | 1 |

---

### 11.25 `DAY_OF_WEEK` (`ENUM_DAY_OF_WEEK`)

Used by `SymbolInfo.swap_rollover3days` field (day of triple swap).

| Name | Value |
|------|-------|
| `DAY_OF_WEEK_SUNDAY` | 0 |
| `DAY_OF_WEEK_MONDAY` | 1 |
| `DAY_OF_WEEK_TUESDAY` | 2 |
| `DAY_OF_WEEK_WEDNESDAY` | 3 |
| `DAY_OF_WEEK_THURSDAY` | 4 |
| `DAY_OF_WEEK_FRIDAY` | 5 |
| `DAY_OF_WEEK_SATURDAY` | 6 |

---

### 11.26 `ACCOUNT_TRADE_MODE` (`ENUM_ACCOUNT_TRADE_MODE`)

Used by `AccountInfo.trade_mode` field.

| Name | Value | Description |
|------|-------|-------------|
| `ACCOUNT_TRADE_MODE_DEMO` | 0 | Demo account |
| `ACCOUNT_TRADE_MODE_CONTEST` | 1 | Contest account |
| `ACCOUNT_TRADE_MODE_REAL` | 2 | Real account |

---

### 11.27 `ACCOUNT_STOPOUT_MODE` (`ENUM_ACCOUNT_STOPOUT_MODE`)

Used by `AccountInfo.margin_so_mode` field.

| Name | Value | Description |
|------|-------|-------------|
| `ACCOUNT_STOPOUT_MODE_PERCENT` | 0 | Stop-out as percentage |
| `ACCOUNT_STOPOUT_MODE_MONEY` | 1 | Stop-out as absolute money |

---

### 11.28 `ACCOUNT_MARGIN_MODE` (`ENUM_ACCOUNT_MARGIN_MODE`)

Used by `AccountInfo.margin_mode` field.

| Name | Value | Description |
|------|-------|-------------|
| `ACCOUNT_MARGIN_MODE_RETAIL_NETTING` | 0 | Retail netting |
| `ACCOUNT_MARGIN_MODE_EXCHANGE` | 1 | Exchange |
| `ACCOUNT_MARGIN_MODE_RETAIL_HEDGING` | 2 | Retail hedging |

---

### 11.29 `RES_E_*` (function error codes — `last_error()`)

| Name | Value | Description |
|------|-------|-------------|
| `RES_S_OK` | 1 | Generic success |
| `RES_E_FAIL` | -1 | Generic failure |
| `RES_E_INVALID_PARAMS` | -2 | Invalid arguments/parameters |
| `RES_E_NO_MEMORY` | -3 | No memory condition |
| `RES_E_NOT_FOUND` | -4 | No history / not found |
| `RES_E_INVALID_VERSION` | -5 | Invalid version |
| `RES_E_AUTH_FAILED` | -6 | Authorization failed |
| `RES_E_UNSUPPORTED` | -7 | Unsupported method |
| `RES_E_AUTO_TRADING_DISABLED` | -8 | Auto-trading disabled |
| `RES_E_INTERNAL_FAIL` | -10000 | Internal IPC general error |
| `RES_E_INTERNAL_FAIL_SEND` | -10001 | Internal IPC send failed |
| `RES_E_INTERNAL_FAIL_RECEIVE` | -10002 | Internal IPC receive failed |
| `RES_E_INTERNAL_FAIL_INIT` | -10003 | Internal IPC initialization fail |
| `RES_E_INTERNAL_FAIL_CONNECT` | -10004 | Internal IPC no connection |
| `RES_E_INTERNAL_FAIL_TIMEOUT` | -10005 | Internal timeout |

---

### 11.30 Bitmask Fields (no Python constants — raw integers from MQL5)

These `SymbolInfo` fields use bitmask values. The Python package does not expose named constants for them.

**`SYMBOL_EXPIRATION_MODE`** (used by `expiration_mode` field):  
Bitmask allowing order expiration types: `ORDER_TIME_GTC` (1), `ORDER_TIME_DAY` (2), `ORDER_TIME_SPECIFIED` (4), `ORDER_TIME_SPECIFIED_DAY` (8).

**`SYMBOL_FILLING_MODE`** (used by `filling_mode` field):  
Bitmask allowing order filling types: `ORDER_FILLING_FOK` (1), `ORDER_FILLING_IOC` (2), `ORDER_FILLING_BOC` (4), `ORDER_FILLING_RETURN` (8).

**`SYMBOL_ORDER_MODE`** (used by `order_mode` field):  
Bitmask allowing order types: `ORDER_TYPE_BUY` (1), `ORDER_TYPE_SELL` (2), `ORDER_TYPE_BUY_LIMIT` (4), `ORDER_TYPE_SELL_LIMIT` (8), `ORDER_TYPE_BUY_STOP` (16), `ORDER_TYPE_SELL_STOP` (32), `ORDER_TYPE_BUY_STOP_LIMIT` (64), `ORDER_TYPE_SELL_STOP_LIMIT` (128).

---

## 12. Protobuf Design Recommendations

### 12.1 Field Classification Summary

Across all data structures:

| Category | Count | Examples |
|----------|-------|---------|
| **Generic fields** | ~80+ | price, volume, balance, equity, profit, ticket, time, SL, TP, symbol, comment |
| **MT5-specific fields** | ~70+ | magic, trade_mode, margin_mode, fifo_close, custom, spread_float, session_*, type_time, type_filling, state, entry, reason, flags, retcode |

### 12.2 Design Approaches

**Option A — Single flat message with all MT5 fields:**
```
message AccountInfo {
  int64 login = 1;
  double balance = 2;
  ...
  int32 trade_mode = 20;       // MT5-specific
  bool fifo_close = 21;        // MT5-specific
}
```
- Pros: Simple, 1:1 mapping, no nesting
- Cons: Tight coupling to MT5, confusing for multi-broker support

**Option B — Generic base + MT5 extension message:**
```
message AccountInfo {
  int64 login = 1;
  double balance = 2;
  ...
  Mt5AccountInfo mt5 = 15;     // optional, MT5-only fields
}

message Mt5AccountInfo {
  int32 trade_mode = 1;
  bool fifo_close = 2;
  ...
}
```
- Pros: Clean separation, portable core model, easy to swap broker
- Cons: More messages, nested access

**Option C — `oneof` per MT5-specific field group:**
```
message AccountInfo {
  int64 login = 1;
  double balance = 2;
  ...
  oneof broker_ext {
    Mt5AccountInfo mt5 = 15;
    // OtherBrokerInfo other = 16;
  }
}
```
- Pros: Forward-compatible for multi-broker, explicit typing
- Cons: More complex, `oneof` has limitations

### 12.3 Recommended Split

For each major message type, these fields are the **core generic subset** that should be in the base message:

| Message | Generic Fields |
|---------|---------------|
| **AccountInfo** | login, leverage, trade_allowed, balance, credit, profit, equity, margin, margin_free, margin_level, margin_so_call, margin_so_so, name, server, currency, company |
| **TerminalInfo** | connected, trade_allowed, ping_last, company, name |
| **SymbolInfo** | digits, spread, bid, ask, last, point, trade_tick_size, trade_contract_size, volume_min/max/step, swap_long/short, margin_initial/maintenance, margin_hedged, price_change, price_volatility, option_*, currency_base, currency_profit, currency_margin, description, exchange, isin, name, start_time, expiration_time, trade_stops_level, trade_freeze_level |
| **Tick** | time, bid, ask, last, volume, time_msc, volume_real |
| **Rate** | time, open, high, low, close, tick_volume, spread, real_volume |
| **TradeOrder** | ticket, time_setup, time_done, time_expiration, volume_initial, volume_current, price_open, sl, tp, price_current, price_stoplimit, symbol, comment, external_id, position_id |
| **TradePosition** | ticket, time, type (buy/sell), volume, price_open, sl, tp, price_current, swap, profit, symbol, comment, external_id |
| **TradeDeal** | ticket, order, time, volume, price, commission, swap, profit, fee, symbol, comment, external_id, position_id |
| **BookInfo** | price, volume, volume_dbl |
| **TradeRequest** | symbol, volume, price, stoplimit, sl, tp, deviation, expiration, comment, order, position |
| **TradeCheckResult** | balance, equity, profit, margin, margin_free, margin_level, comment |
| **TradeSendResult** | deal, order, volume, price, bid, ask, comment |
