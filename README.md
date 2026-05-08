# Binance Futures Testnet Trading Bot

A simplified Python trading bot to place orders on the Binance Futures Testnet (USDT-M). This bot provides a clean CLI interface using `click` and `rich`, with robust input validation, error handling, and structured logging.

## Features
- Place **MARKET**, **LIMIT**, and **STOP_MARKET** orders.
- Buy or Sell sides supported.
- Robust input validation.
- Clear and beautiful CLI output with tables and rich formatting.
- Comprehensive logging to both a file (`trading_bot.log`) and the console.

## Setup Instructions

1. **Clone the repository** (if you haven't already).
2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure your API keys**:
   - The `.env` file must be present in the root directory.
   - It should contain your testnet API keys like so:
     ```env
     BINANCE_API_KEY=your_testnet_api_key
     BINANCE_API_SECRET=your_testnet_api_secret
     ```

## How to Run Examples

Use the `cli.py` entry point. The main command is `place`.

### 1. Place a MARKET Order
Places a market order to buy 0.01 BTC.
```bash
python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### 2. Place a LIMIT Order
Places a limit order to sell 0.01 BTC at $60,000.
```bash
python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

### 3. Place a STOP_MARKET Order (Bonus Feature)
Places a stop-market order to sell 0.01 BTC if the price hits $50,000.
```bash
python cli.py place --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.01 --stop-price 50000
```

## Logs

All API requests, responses, and errors are logged to `trading_bot.log` in the root directory.

## Assumptions
- The bot exclusively uses the Binance Futures Testnet (`https://testnet.binancefuture.com`).
- The user has already generated testnet API credentials.
- Error handling primarily focuses on network and API exceptions specific to Binance, providing user-friendly output and detailed logs.
