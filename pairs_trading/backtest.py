from dataclasses import dataclass

import numpy as np
import pandas as pd

from .strategy import StrategyParams


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    daily_returns: pd.Series
    sharpe_ratio: float
    cumulative_return: float
    trades: int


def backtest_pairs_strategy(
    prices: pd.DataFrame,
    positions: pd.Series,
    beta: float,
    params: StrategyParams,
    risk_free_rate: float = 0.0,
) -> BacktestResult:
    """Backtest a simple pairs trading strategy.

    We assume each day we hold:
      position * 1 notional of asset1
      and position * (-beta) notional of asset2

    Daily return ~= position(t-1) * (r1 - beta * r2).
    """
    prices = prices.copy()
    positions = positions.reindex(prices.index).fillna(0)

    # % returns of each asset
    r1 = prices["asset1"].pct_change().fillna(0.0)
    r2 = prices["asset2"].pct_change().fillna(0.0)

    # Use previous day's position to avoid look-ahead bias
    pos_lag = positions.shift(1).fillna(0.0)

    daily_ret = pos_lag * (r1 - beta * r2) * params.max_leverage

    equity_curve = (1.0 + daily_ret).cumprod()

    # Strategy metrics
    excess_ret = daily_ret - risk_free_rate / 252.0
    if excess_ret.std() > 0:
        sharpe = float(np.sqrt(252.0) * excess_ret.mean() / excess_ret.std())
    else:
        sharpe = 0.0

    cumulative_return = float(equity_curve.iloc[-1] - 1.0)

    trade_changes = positions.diff().fillna(0.0)
    trades = int((trade_changes != 0).sum())

    return BacktestResult(
        equity_curve=equity_curve,
        daily_returns=daily_ret,
        sharpe_ratio=sharpe,
        cumulative_return=cumulative_return,
        trades=trades,
    )
