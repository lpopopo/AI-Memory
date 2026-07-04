"""Causal close-to-close portfolio engine with drifting holdings.

Signals formed at today's close execute at the next session's close because the
legacy dataset contains adjusted closes only. Target weights drift naturally
between executions; no uncharged daily rebalancing is assumed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import numpy as np
import pandas as pd


TargetFunction = Callable[[pd.Timestamp], dict[str, float]]


@dataclass
class EngineResult:
    equity: pd.Series
    weights: pd.DataFrame
    executions: pd.DataFrame
    diagnostics: dict = field(default_factory=dict)


def drift_weights(
    weights: dict[str, float], returns: pd.Series
) -> tuple[float, dict[str, float]]:
    """Apply one close-to-close return and return portfolio factor/new weights."""
    invested = sum(weights.values())
    cash = max(0.0, 1.0 - invested)
    grown = {}
    for symbol, weight in weights.items():
        ret = returns.get(symbol, np.nan)
        # Missing return means the position is marked unchanged, never silently lost.
        grown[symbol] = weight * (1.0 + (0.0 if pd.isna(ret) else float(ret)))
    factor = cash + sum(grown.values())
    if factor <= 0:
        raise RuntimeError("portfolio equity became non-positive")
    return factor, {symbol: value / factor for symbol, value in grown.items() if value > 0}


def turnover(current: dict[str, float], target: dict[str, float]) -> float:
    return float(sum(abs(current.get(s, 0.0) - target.get(s, 0.0))
                     for s in set(current) | set(target)))


def validate_target(target: dict[str, float]) -> dict[str, float]:
    cleaned = {s: float(w) for s, w in target.items() if float(w) > 1e-12}
    if any(not np.isfinite(w) for w in cleaned.values()):
        raise ValueError("target contains non-finite weight")
    if sum(cleaned.values()) > 1.000001:
        raise ValueError(f"target weights exceed 100%: {sum(cleaned.values()):.6f}")
    return cleaned


def run_engine(
    close: pd.DataFrame,
    rebalance_dates: set[pd.Timestamp],
    target_function: TargetFunction,
    transaction_cost: float = 0.001,
    stop_loss_pct: float | None = None,
    stop_exempt: set[str] | None = None,
) -> EngineResult:
    """Run a target-weight strategy without look-ahead or free rebalancing."""
    returns = close.pct_change()
    stop_exempt = stop_exempt or set()
    weights: dict[str, float] = {}
    pending_target: dict[str, float] | None = None
    high_water: dict[str, float] = {}
    value = 1.0
    equity_rows = []
    weight_rows = []
    executions = []
    total_turnover = 0.0

    for dt in close.index:
        # Positions held after the prior close earn today's close-to-close return.
        factor, weights = drift_weights(weights, returns.loc[dt])
        value *= factor

        # Yesterday's close-confirmed instructions execute at today's close.
        if pending_target is not None:
            target = validate_target(pending_target)
            traded = turnover(weights, target)
            value *= max(0.0, 1.0 - traded * transaction_cost)
            prior_symbols = set(weights)
            weights = target
            total_turnover += traded
            for symbol in set(high_water) - set(weights):
                del high_water[symbol]
            for symbol in set(weights) - prior_symbols:
                px = close.at[dt, symbol] if symbol in close else np.nan
                if pd.notna(px):
                    high_water[symbol] = float(px)
            executions.append({
                "date": dt, "turnover": traded, "cost_fraction": traded * transaction_cost,
                "symbols": "|".join(sorted(weights)),
            })
            pending_target = None

        # Update close-based high-water marks and form a next-close stop instruction.
        stopped = set()
        if stop_loss_pct is not None:
            for symbol in list(weights):
                if symbol in stop_exempt or symbol not in close:
                    continue
                px = close.at[dt, symbol]
                if pd.isna(px):
                    continue
                high_water[symbol] = max(high_water.get(symbol, float(px)), float(px))
                if float(px) < high_water[symbol] * (1.0 - stop_loss_pct):
                    stopped.add(symbol)

        # Rebalance signals have priority, but a same-day stop cannot be re-added.
        if dt in rebalance_dates:
            pending_target = validate_target(target_function(dt))
            for symbol in stopped:
                pending_target.pop(symbol, None)
        elif stopped:
            pending_target = dict(weights)
            for symbol in stopped:
                pending_target.pop(symbol, None)

        equity_rows.append(value)
        weight_rows.append({"date": dt, **weights, "cash": max(0.0, 1.0 - sum(weights.values()))})

    equity = pd.Series(equity_rows, index=close.index, name="robust_equity")
    weight_frame = pd.DataFrame(weight_rows).set_index("date").fillna(0.0)
    execution_frame = pd.DataFrame(executions)
    return EngineResult(
        equity=equity, weights=weight_frame, executions=execution_frame,
        diagnostics={
            "total_turnover": total_turnover,
            "transaction_cost": transaction_cost,
            "execution": "signal close -> next session close",
            "weight_drift": True,
        },
    )
