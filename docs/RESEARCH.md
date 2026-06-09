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
| 5 | `type` | `int32` | Deal type (BUY/SELL/BALANCE/CREDIT/CHARGE/CORRECTION/BONUS/COMMISSION/COMMISSION_DAILY/etc). | **MT5-specific** | MT5 enum (`DEAL_TYPE_*`) — includes MT5-specific types like COMMISSION_DAILY, AGENCY_MONTHLY |
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

The following enums are **MT5-specific** and would need corresponding protobuf enum definitions:

### 11.1 `TIMEFRAME` (shared with MQL5 standard)
M1, M2, M3, M4, M5, M6, M10, M12, M15, M20, M30, H1, H2, H3, H4, H6, H8, H12, D1, W1, MN1

### 11.2 `ORDER_TYPE`
BUY, SELL, BUY_LIMIT, SELL_LIMIT, BUY_STOP, SELL_STOP, BUY_STOP_LIMIT, SELL_STOP_LIMIT, CLOSE_BY

### 11.3 `ORDER_TYPE_FILLING`
FOK, IOC, RETURN

### 11.4 `ORDER_TYPE_TIME`
GTC, DAY, SPECIFIED, SPECIFIED_DAY

### 11.5 `ORDER_STATE`
STARTED, PLACED, CANCELED, PARTIAL, FILLED, REJECTED, EXPIRED, REQUEST_ADD, REQUEST_MODIFY

### 11.6 `TRADE_REQUEST_ACTIONS`
DEAL, PENDING, SLTP, MODIFY, REMOVE, CLOSE_BY

### 11.7 `DEAL_TYPE`
BUY, SELL, BALANCE, CREDIT, CHARGE, CORRECTION, BONUS, COMMISSION, COMMISSION_DAILY, COMMISSION_MONTHLY, AGENCY_DAILY, AGENCY_MONTHLY

### 11.8 `DEAL_ENTRY`
IN, OUT, INOUT, OUT_BY

### 11.9 `COPY_TICKS`
ALL, INFO, TRADE

### 11.10 `TICK_FLAG` (bitmask)
BID, ASK, LAST, VOLUME, BUY, SELL

### 11.11 `BOOK_TYPE`
SELL, BUY, SELL_MARKET, BUY_MARKET

### 11.12 `TRADE_RETCODE`
DONE (10009), and many others.

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
