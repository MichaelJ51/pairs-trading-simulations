import matplotlib.pyplot as plt
import pandas as pd


def plot_prices_with_signals(
    prices: pd.DataFrame,
    positions: pd.Series,
    title: str = "Asset Prices with Pairs Trading Signals",
) -> None:
    prices = prices.copy()
    pos = positions.reindex(prices.index).fillna(0)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(prices.index, prices["asset1"], label="Asset 1")
    ax.plot(prices.index, prices["asset2"], label="Asset 2")

    # Mark entry/exit points
    long_entries = (pos == 1) & (pos.shift(1) == 0)
    short_entries = (pos == -1) & (pos.shift(1) == 0)
    exits = (pos == 0) & (pos.shift(1) != 0)

    ax.scatter(
        prices.index[long_entries],
        prices["asset1"][long_entries],
        marker="^",
        label="Long spread entry",
    )
    ax.scatter(
        prices.index[short_entries],
        prices["asset1"][short_entries],
        marker="v",
        label="Short spread entry",
    )
    ax.scatter(
        prices.index[exits],
        prices["asset1"][exits],
        marker="o",
        label="Exit",
    )

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()


def plot_zscore(
    spread_and_z: pd.DataFrame,
    entry_z: float,
    exit_z: float,
    title: str = "Spread Z-Score",
) -> None:
    z = spread_and_z["zscore"]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(z.index, z, label="Z-score")
    ax.axhline(entry_z, linestyle="--", label=f"+{entry_z}")
    ax.axhline(-entry_z, linestyle="--", label=f"-{entry_z}")
    ax.axhline(exit_z, linestyle=":", label=f"+{exit_z}")
    ax.axhline(-exit_z, linestyle=":", label=f"-{exit_z}")
    ax.axhline(0, linestyle="-", linewidth=0.7)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Z-score")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()


def plot_equity_curve(
    equity_curve: pd.Series,
    title: str = "Equity Curve",
) -> None:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(equity_curve.index, equity_curve, label="Equity")
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity (starting at 1.0)")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
