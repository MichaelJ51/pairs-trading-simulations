# Pairs Trading simulations

An educational algorithmic trading project that implements a basic **pairs trading** strategy with:

- Cointegration-style hedge ratio estimation (OLS on log prices)
- Z-score based entry/exit rules
- Simple backtest engine
- Matplotlib plots for:
  - Asset prices + trade markers
  - Spread z-score + thresholds
  - Equity curve

It supports **two ways** to get historical data:

1. From your own CSV/Excel file, or
2. Automatically from **Yahoo Finance** using `yfinance` (free).

## Installation

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Option 1: Automatic download (recommended)

Run a backtest on two tickers, e.g., AAPL vs MSFT over the last 5 years:

```bash
python examples/run_pairs_trading.py \
  --tickers AAPL MSFT \
  --period 5y
```

You can also specify a date range:

```bash
python examples/run_pairs_trading.py \
  --tickers XOM CVX \
  --start 2018-01-01 \
  --end 2024-01-01
```

The script will:

1. Download adjusted close prices from Yahoo Finance.
2. Estimate the hedge ratio between the two assets.
3. Compute the spread and rolling z-score.
4. Generate trading signals based on z-score thresholds.
5. Backtest the strategy and print:
   - Hedge ratio
   - Cumulative return
   - Sharpe ratio
   - Number of trades
6. Show plots with:
   - Price series and trade markers
   - Z-score over time
   - Equity curve

## Option 2: Use your own CSV/Excel file

1. Prepare a file (CSV or Excel) with columns like:

```text
Date,AAPL,MSFT
2023-01-02,130.03,239.82
2023-01-03,125.07,234.53
...
```

2. Place it under the `data/` folder, e.g. `data/my_pair.csv`.

3. Run:

```bash
python examples/run_pairs_trading.py \
  --file data/my_pair.csv \
  --asset1 AAPL \
  --asset2 MSFT \
  --file-type csv
```

## Strategy Parameters

You can tune the strategy directly from the command line:

- `--lookback` (default: 60) – rolling window for spread z-score.
- `--entry-z` (default: 2.0) – enter trade when |z-score| crosses this.
- `--exit-z` (default: 0.5) – exit when |z-score| falls below this.
- `--period` (default: 5y) – period for Yahoo Finance download.

Example with custom parameters:

```bash
python examples/run_pairs_trading.py \
  --tickers AAPL MSFT \
  --period 3y \
  --lookback 30 \
  --entry-z 1.5 \
  --exit-z 0.3
```

## Notes

- This project is **for educational purposes only** and not financial advice.
- Real trading would require transaction costs, slippage modeling, risk limits, etc.
