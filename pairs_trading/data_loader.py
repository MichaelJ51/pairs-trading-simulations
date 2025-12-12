from pathlib import Path
from typing import Literal, Sequence

import pandas as pd


def load_price_data_from_file(
    path: str | Path,
    asset1: str,
    asset2: str,
    file_type: Literal["csv", "excel"] = "csv",
    date_col: str = "Date",
) -> pd.DataFrame:
    """Load historical prices for two assets from a CSV or Excel file.

    Expected columns: date_col, asset1, asset2
    Example: Date, AAPL, MSFT
    """
    path = Path(path)

    if file_type == "csv":
        df = pd.read_csv(path, parse_dates=[date_col])
    else:
        df = pd.read_excel(path, parse_dates=[date_col])

    df = df.set_index(date_col).sort_index()
    df = df[[asset1, asset2]].dropna()

    df.columns = ["asset1", "asset2"]  # normalize names internally
    return df


def download_price_data_yahoo(
    tickers: Sequence[str],
    start: str | None = None,
    end: str | None = None,
    period: str | None = "5y",
) -> pd.DataFrame:
    """Download adjusted close prices from Yahoo Finance using yfinance.

    Returns a DataFrame with columns: asset1, asset2
    """
    import yfinance as yf  # imported here so library is optional if not used

    if len(tickers) != 2:
        raise ValueError("Exactly two tickers must be provided for pairs trading.")

    data = yf.download(list(tickers), start=start, end=end, period=period)["Adj Close"]
    # For a single ticker, yfinance returns a Series; for multiple it's a DataFrame.
    if isinstance(data, pd.Series):
        raise ValueError("Expected two tickers, but got one series from yfinance.")

    data = data.dropna()
    data = data.rename(columns={tickers[0]: "asset1", tickers[1]: "asset2"})
    return data
