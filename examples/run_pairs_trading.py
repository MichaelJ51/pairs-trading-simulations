import argparse
from pathlib import Path

import matplotlib.pyplot as plt

from pairs_trading.backtest import backtest_pairs_strategy
from pairs_trading.data_loader import (
    download_price_data_yahoo,
    load_price_data_from_file,
)
from pairs_trading.plotting import (
    plot_equity_curve,
    plot_prices_with_signals,
    plot_zscore,
)
from pairs_trading.strategy import (
    StrategyParams,
    compute_spread_and_zscore,
    estimate_hedge_ratio,
    generate_signals,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a simple pairs trading backtest on historical data."
    )

    # Mode 1: use --file
    parser.add_argument(
        "--file",
        type=str,
        help="Path to CSV or Excel file with price data (optional if using --tickers).",
    )
    parser.add_argument(
        "--asset1",
        type=str,
        help="Column name for first asset (file mode).",
    )
    parser.add_argument(
        "--asset2",
        type=str,
        help="Column name for second asset (file mode).",
    )
    parser.add_argument(
        "--file-type",
        type=str,
        choices=["csv", "excel"],
        default="csv",
        help="Type of input file (csv or excel).",
    )

    # Mode 2: automatic download via yfinance
    parser.add_argument(
        "--tickers",
        type=str,
        nargs=2,
        metavar=("TICKER1", "TICKER2"),
        help="Two ticker symbols to download from Yahoo Finance (e.g., AAPL MSFT).",
    )
    parser.add_argument(
        "--start",
        type=str,
        default=None,
        help="Start date (YYYY-MM-DD) for downloaded data.",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="End date (YYYY-MM-DD) for downloaded data.",
    )
    parser.add_argument(
        "--period",
        type=str,
        default="5y",
        help="Period for downloaded data (used if start/end not provided).",
    )

    parser.add_argument(
        "--lookback",
        type=int,
        default=60,
        help="Lookback window for z-score.",
    )
    parser.add_argument(
        "--entry-z",
        type=float,
        default=2.0,
        help="Entry threshold for z-score.",
    )
    parser.add_argument(
        "--exit-z",
        type=float,
        default=0.5,
        help="Exit threshold for z-score.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.tickers:
        # yfinance mode
        prices = download_price_data_yahoo(
            tickers=args.tickers,
            start=args.start,
            end=args.end,
            period=args.period,
        )
        print(f"Downloaded data for: {args.tickers[0]} and {args.tickers[1]}")
    else:
        # file mode
        if not args.file or not args.asset1 or not args.asset2:
            raise SystemExit(
                "You must either provide --tickers T1 T2, or --file + --asset1 + --asset2."
            )
        prices = load_price_data_from_file(
            path=Path(args.file),
            asset1=args.asset1,
            asset2=args.asset2,
            file_type=args.file_type,
        )
        print(f"Loaded file data from {args.file} for {args.asset1} and {args.asset2}")

    params = StrategyParams(
        lookback=args.lookback,
        entry_z=args.entry_z,
        exit_z=args.exit_z,
    )

    beta = estimate_hedge_ratio(prices)
    print(f"Hedge ratio (beta): {beta:.4f}")

    spread_and_z = compute_spread_and_zscore(
        prices=prices,
        beta=beta,
        lookback=params.lookback,
    )

    positions = generate_signals(
        zscore=spread_and_z["zscore"],
        params=params,
    )

    result = backtest_pairs_strategy(
        prices=prices,
        positions=positions,
        beta=beta,
        params=params,
    )

    print(f"Cumulative return: {result.cumulative_return:.2%}")
    print(f"Sharpe ratio: {result.sharpe_ratio:.2f}")
    print(f"Number of trades: {result.trades}")

    # Plots
    plot_prices_with_signals(prices, positions)
    plot_zscore(spread_and_z, params.entry_z, params.exit_z)
    plot_equity_curve(result.equity_curve)

    plt.show()


if __name__ == "__main__":
    main()
