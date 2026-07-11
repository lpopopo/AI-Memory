"""V8 trend core with optional inverse-volatility weights and volatility scaling."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from v81_dynamic_enhancer import TrendVote


@dataclass(frozen=True)
class V82Config:
    risk_weighting: str = "fixed"
    risk_lookback: int = 60
    target_volatility: float | None = None
    volatility_lookback: int = 60
    qqq_cap: float = 1.0

    def __post_init__(self):
        if self.risk_weighting not in {"fixed", "inverse_vol"}:
            raise ValueError("invalid risk weighting")
        if self.risk_lookback not in {60, 126}:
            raise ValueError("risk lookback must be 60 or 126")
        if self.target_volatility not in {None, 0.10, 0.12, 0.15}:
            raise ValueError("unsupported target volatility")
        if self.volatility_lookback not in {20, 60}:
            raise ValueError("volatility lookback must be 20 or 60")
        if self.qqq_cap not in {0.50, 0.60, 1.0}:
            raise ValueError("unsupported QQQ cap")


class V82Allocator:
    """Monthly allocator. Every statistic at dt uses data available by dt."""

    def __init__(self, close: pd.DataFrame, config: V82Config):
        self.close = close[["SPY", "QQQ"]]
        self.config = config
        self.ma150 = self.close.rolling(150).mean()
        self.ma200 = self.close.rolling(200).mean()
        returns = self.close.pct_change()
        self.asset_vol = returns.rolling(config.risk_lookback).std() * np.sqrt(252)
        self.covariances = returns.rolling(config.volatility_lookback).cov() * 252
        self.votes = {s: {150: TrendVote(), 200: TrendVote()} for s in self.close}
        self.audit: list[dict] = []

    def _portfolio_vol(self, dt: pd.Timestamp, weights: dict[str, float]) -> float:
        symbols = [s for s in ("SPY", "QQQ") if weights.get(s, 0) > 0]
        if not symbols:
            return 0.0
        try:
            cov = self.covariances.loc[dt].loc[symbols, symbols]
        except KeyError:
            return float("nan")
        vector = np.array([weights[s] for s in symbols])
        variance = float(vector @ cov.to_numpy() @ vector)
        return float(np.sqrt(max(variance, 0.0))) if np.isfinite(variance) else float("nan")

    def target(self, dt: pd.Timestamp) -> dict[str, float]:
        strengths = {}
        for symbol in ("SPY", "QQQ"):
            price = self.close.at[dt, symbol]
            active150 = self.votes[symbol][150].update(price, self.ma150.at[dt, symbol], 0, 1)
            active200 = self.votes[symbol][200].update(price, self.ma200.at[dt, symbol], 0, 1)
            strengths[symbol] = (int(active150) + int(active200)) / 2

        total_exposure = 0.5 * strengths["SPY"] + 0.5 * strengths["QQQ"]
        scores = {}
        for symbol, strength in strengths.items():
            if strength <= 0:
                continue
            if self.config.risk_weighting == "inverse_vol":
                vol = self.asset_vol.at[dt, symbol]
                if pd.isna(vol) or vol <= 0:
                    continue
                scores[symbol] = strength / float(vol)
            else:
                scores[symbol] = strength

        if not scores or total_exposure <= 0:
            target = {}
        else:
            score_sum = sum(scores.values())
            target = {s: total_exposure * score / score_sum for s, score in scores.items()}
            if "QQQ" in target and target["QQQ"] > self.config.qqq_cap:
                excess = target["QQQ"] - self.config.qqq_cap
                target["QQQ"] = self.config.qqq_cap
                if "SPY" in target:
                    target["SPY"] += excess

        pre_scale_vol = self._portfolio_vol(dt, target)
        scale = 1.0
        if self.config.target_volatility is not None and pd.notna(pre_scale_vol) and pre_scale_vol > 0:
            scale = min(1.0, self.config.target_volatility / pre_scale_vol)
            target = {s: w * scale for s, w in target.items()}

        total = sum(target.values())
        if total > 1.000001 or scale > 1.000001:
            raise AssertionError("V8.2 must not use leverage")
        self.audit.append({
            "date": str(dt.date()), "trend_strength": strengths,
            "pre_scale_exposure": total_exposure, "pre_scale_volatility": pre_scale_vol,
            "volatility_scale": scale, "target": target, "cash": 1 - total,
        })
        return target
