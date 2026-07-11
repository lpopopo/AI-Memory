"""V8 core with causal moving-average slope confirmation."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class V83Config:
    slope_lookback: int | None = None
    minimum_slope: float = 0.0
    apply_to: str = "both"

    def __post_init__(self):
        if self.slope_lookback not in {None, 21, 63, 126}:
            raise ValueError("unsupported slope lookback")
        if self.minimum_slope not in {0.0, 0.005, 0.01}:
            raise ValueError("unsupported minimum slope")
        if self.apply_to not in {"ma200", "both"}:
            raise ValueError("apply_to must be ma200 or both")
        if self.slope_lookback is None and self.minimum_slope != 0:
            raise ValueError("baseline cannot have a slope threshold")


class V83Allocator:
    def __init__(self, close: pd.DataFrame, config: V83Config):
        self.close = close[["SPY", "QQQ"]]
        self.config = config
        self.mas = {days: self.close.rolling(days).mean() for days in (150, 200)}
        self.slopes = {}
        if config.slope_lookback is not None:
            self.slopes = {
                days: ma.pct_change(config.slope_lookback, fill_method=None)
                for days, ma in self.mas.items()
            }
        self.audit: list[dict] = []

    def target(self, dt: pd.Timestamp) -> dict[str, float]:
        target = {}
        audit_votes = {}
        audit_slopes = {}
        for symbol in ("SPY", "QQQ"):
            votes = 0
            audit_votes[symbol] = {}
            audit_slopes[symbol] = {}
            for days in (150, 200):
                price = self.close.at[dt, symbol]
                ma = self.mas[days].at[dt, symbol]
                above = bool(pd.notna(ma) and price > ma)
                use_slope = self.config.slope_lookback is not None and (
                    self.config.apply_to == "both" or days == 200
                )
                slope = self.slopes[days].at[dt, symbol] if use_slope else None
                confirmed = above and (not use_slope or (
                    pd.notna(slope) and slope > self.config.minimum_slope
                ))
                votes += int(confirmed)
                audit_votes[symbol][str(days)] = confirmed
                audit_slopes[symbol][str(days)] = None if slope is None or pd.isna(slope) else float(slope)
            weight = 0.25 * votes
            if weight:
                target[symbol] = weight
        total = sum(target.values())
        if total > 1.000001:
            raise AssertionError("V8.3 must not use leverage")
        self.audit.append({"date": str(dt.date()), "votes": audit_votes,
                           "slopes": audit_slopes, "target": target, "cash": 1-total})
        return target
