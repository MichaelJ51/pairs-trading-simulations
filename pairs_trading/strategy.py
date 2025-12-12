from dataclasses import dataclass

import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant


@dataclass
class StrategyParams:
    lookback: int = 60       # rolling window for z-score
    entry_z: float = 2.0     # enter trade threshold
    exit_z: float = 0.5      # exit threshold
    max_leverage: float = 1.0  # notional per leg (simplified)


def estimate_hedge_ratio(prices: pd.DataFrame) -> float:
    """Estimate hedge ratio (beta) via OLS on log prices:

    log(asset1) = alpha + beta * log(asset2) + e
    """
    y = np.log(prices["asset1"])
    x = np.log(prices["asset2"])

    x_const = add_constant(x)
    model = OLS(y, x_const).fit()
    beta = model.params["asset2"]
    return float(beta)


def compute_spread_and_zscore(
    prices: pd.DataFrame,
    beta: float,
    lookback: int,
) -> pd.DataFrame:
    """Compute spread and rolling z-score of the spread."""
    log_a1 = np.log(prices["asset1"])
    log_a2 = np.log(prices["asset2"])

    spread = log_a1 - beta * log_a2
    rolling_mean = spread.rolling(lookback).mean()
    rolling_std = spread.rolling(lookback).std()

    zscore = (spread - rolling_mean) / rolling_std

    return pd.DataFrame(
        {
            "spread": spread,
            "zscore": zscore,
        },
        index=prices.index,
    )


def generate_signals(
    zscore: pd.Series,
    params: StrategyParams,
) -> pd.Series:
    """Generate trading signals based on z-score.

    Signal meaning:
      +1 = long spread (long asset1, short asset2)
      -1 = short spread (short asset1, long asset2)
       0 = flat
    """
    position = 0
    positions = []

    for val in zscore:
        if np.isnan(val):
            positions.append(0)
            continue

        # Entry rules
        if position == 0:
            if val > params.entry_z:
                # spread is high: short spread
                position = -1
            elif val < -params.entry_z:
                # spread is low: long spread
                position = 1

        # Exit rules
        elif abs(val) < params.exit_z:
            position = 0

        positions.append(position)

    return pd.Series(positions, index=zscore.index, name="position")
