"""V8.1 SPY/QQQ core with a dynamic QQQ/VT enhancement sleeve."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


CORE_BASE = {"SPY": 0.50, "QQQ": 0.50}
ENHANCER_MAX = 0.50


@dataclass(frozen=True)
class V81Config:
    frequency: str = "monthly"
    hysteresis: float = 0.0
    confirmation: int = 1
    floor_fraction: float = 0.0

    def __post_init__(self):
        if self.frequency not in {"monthly", "weekly"}:
            raise ValueError("frequency must be monthly or weekly")
        if self.hysteresis not in {0.0, 0.01, 0.02}:
            raise ValueError("hysteresis must be 0%, 1%, or 2%")
        if self.confirmation not in {1, 2}:
            raise ValueError("confirmation must be 1 or 2")
        if self.floor_fraction not in {0.0, 0.25}:
            raise ValueError("floor_fraction must be 0% or 25%")


def rebalance_dates(index: pd.DatetimeIndex, frequency: str) -> set[pd.Timestamp]:
    if frequency == "monthly":
        periods = index.to_period("M")
    elif frequency == "weekly":
        periods = index.to_period("W-FRI")
    else:
        raise ValueError(f"unsupported frequency: {frequency}")
    return {
        dt for i, dt in enumerate(index)
        if i == len(index) - 1 or periods[i + 1] != periods[i]
    }


class TrendVote:
    def __init__(self):
        self.active = False
        self.enter_count = 0
        self.exit_count = 0

    def update(self, price: float, moving_average: float, band: float, confirmation: int) -> bool:
        if pd.isna(price) or pd.isna(moving_average):
            self.active = False
            self.enter_count = self.exit_count = 0
            return False
        enter = price > moving_average * (1 + band)
        exit_ = price < moving_average * (1 - band)
        if self.active:
            self.exit_count = self.exit_count + 1 if exit_ else 0
            self.enter_count = 0
            if self.exit_count >= confirmation:
                self.active = False
                self.exit_count = 0
        else:
            self.enter_count = self.enter_count + 1 if enter else 0
            self.exit_count = 0
            if self.enter_count >= confirmation:
                self.active = True
                self.enter_count = 0
        return self.active


class V81Allocator:
    def __init__(self, close: pd.DataFrame, config: V81Config, enhancer: bool = True):
        self.close = close
        self.config = config
        self.enhancer = enhancer
        self.ma150 = close[["SPY", "QQQ"]].rolling(150).mean()
        self.ma200_core = close[["SPY", "QQQ"]].rolling(200).mean()
        self.ma200_enhancer = close[["QQQ", "VT"]].rolling(200).mean()
        self.mom63 = close[["QQQ", "VT"]].pct_change(63)
        self.mom126 = close[["QQQ", "VT"]].pct_change(126)
        self.votes = {
            symbol: {150: TrendVote(), 200: TrendVote()} for symbol in CORE_BASE
        }
        self.audit: list[dict] = []

    def target(self, dt: pd.Timestamp) -> dict[str, float]:
        core = {}
        vote_counts = {}
        for symbol, base in CORE_BASE.items():
            price = self.close.at[dt, symbol]
            active150 = self.votes[symbol][150].update(
                price, self.ma150.at[dt, symbol], self.config.hysteresis,
                self.config.confirmation,
            )
            active200 = self.votes[symbol][200].update(
                price, self.ma200_core.at[dt, symbol], self.config.hysteresis,
                self.config.confirmation,
            )
            count = int(active150) + int(active200)
            vote_counts[symbol] = count
            exposure_fraction = self.config.floor_fraction + (
                1 - self.config.floor_fraction
            ) * count / 2
            core[symbol] = base * exposure_fraction

        unused = max(0.0, 1.0 - sum(core.values()))
        enhancer_budget = min(unused, ENHANCER_MAX) if self.enhancer else 0.0
        eligibility = {}
        scores = {}
        for symbol in ("QQQ", "VT"):
            price = self.close.at[dt, symbol]
            ma200 = self.ma200_enhancer.at[dt, symbol]
            m63 = self.mom63.at[dt, symbol]
            m126 = self.mom126.at[dt, symbol]
            eligible = bool(
                pd.notna(price) and pd.notna(ma200) and pd.notna(m126)
                and price > ma200 and m126 > 0
            )
            eligibility[symbol] = eligible
            scores[symbol] = float(m63 + m126) if eligible and pd.notna(m63) else None

        selected = None
        if enhancer_budget > 0:
            candidates = [(score, symbol) for symbol, score in scores.items() if score is not None]
            if candidates:
                selected = max(candidates)[1]

        final = dict(core)
        if selected:
            final[selected] = final.get(selected, 0.0) + enhancer_budget
        final = {s: float(w) for s, w in final.items() if w > 1e-12}
        total = sum(final.values())
        if enhancer_budget > ENHANCER_MAX + 1e-12:
            raise AssertionError("enhancer budget exceeded 50%")
        if total > 1.000001:
            raise AssertionError("target weights exceeded 100%")
        self.audit.append({
            "date": str(pd.Timestamp(dt).date()), "votes": vote_counts,
            "core": core, "unused_before_enhancer": unused,
            "enhancer_budget": enhancer_budget, "eligible": eligibility,
            "scores": scores, "enhancer_selected": selected,
            "target": final, "cash": 1 - total,
        })
        return final


def run_signal_history(
    close: pd.DataFrame, config: V81Config, enhancer: bool = True,
    include_incomplete_final: bool = True,
):
    allocator = V81Allocator(close, config, enhancer=enhancer)
    dates = sorted(rebalance_dates(close.index, config.frequency))
    if not include_incomplete_final and dates and dates[-1] == close.index[-1]:
        dates = dates[:-1]
    latest = None
    for dt in dates:
        latest = allocator.target(dt)
    if latest is None:
        raise ValueError("no rebalance date available")
    return allocator.audit[-1], allocator
