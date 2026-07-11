"""Read-only V9 research diagnostics.

These monitors never authorize trades, change weights, or override stops.
They power daily/shadow diagnostics and pre-registered validation experiments.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class FearSignal:
    name: str
    value: float | None
    points: int
    note: str


@dataclass(frozen=True)
class FearSnapshot:
    as_of: str
    score: int
    regime: str
    risk_multiplier: float
    max_gross_exposure: float
    max_new_buy_exposure: float
    cash_floor: float
    signals: list[FearSignal]
    action: str


def _safe(value: float | None) -> float | None:
    if value is None or pd.isna(value):
        return None
    return float(value)


def realized_vol126(close: pd.Series, window: int = 126, min_periods: int = 80) -> pd.Series:
    returns = close.pct_change()
    return returns.rolling(window, min_periods=min_periods).std() * np.sqrt(252.0)


def slow_vol_scale(
    close: pd.Series,
    target_vol: float = 0.12,
    floor: float = 0.25,
    ceiling: float = 1.00,
    window: int = 126,
) -> pd.Series:
    """Target-vol / realized-vol scaling with hard caps and no leverage."""
    vol = realized_vol126(close, window=window)
    raw = target_vol / vol
    return raw.clip(lower=floor, upper=ceiling)


def drawdown_from_high(close: pd.Series, window: int = 63) -> pd.Series:
    rolling_max = close.rolling(window, min_periods=1).max()
    return close / rolling_max - 1.0


def compute_fear_snapshot(
    close: pd.DataFrame,
    vix: pd.DataFrame | None,
    as_of: pd.Timestamp,
) -> FearSnapshot:
    """Port of the 14-point Market Fear Gate for advisory diagnostics only."""
    as_of = pd.Timestamp(as_of)
    if as_of not in close.index:
        raise KeyError(f"as_of not in close index: {as_of.date()}")

    signals: list[FearSignal] = []

    def add(name: str, value: float | None, points: int, note: str) -> None:
        signals.append(FearSignal(name=name, value=_safe(value), points=int(points), note=note))

    vix_level = None
    vix_ratio = None
    vix_5d = None
    if vix is not None and as_of in vix.index:
        if "^VIX" in vix.columns and pd.notna(vix.at[as_of, "^VIX"]):
            vix_level = float(vix.at[as_of, "^VIX"])
        if "^VIX3M" in vix.columns and pd.notna(vix.at[as_of, "^VIX3M"]) and vix_level is not None:
            denom = float(vix.at[as_of, "^VIX3M"])
            if denom > 0:
                vix_ratio = vix_level / denom
        loc = vix.index.get_loc(as_of)
        if isinstance(loc, int) and loc >= 5 and vix_level is not None and "^VIX" in vix.columns:
            prior = vix.index[loc - 5]
            prior_vix = vix.at[prior, "^VIX"]
            if pd.notna(prior_vix) and prior_vix > 0:
                vix_5d = vix_level / float(prior_vix) - 1.0

    if vix_level is None:
        add("vix_level", None, 0, "VIX unavailable")
    elif vix_level >= 35:
        add("vix_level", vix_level, 4, "panic VIX")
    elif vix_level >= 30:
        add("vix_level", vix_level, 3, "high-stress VIX")
    elif vix_level >= 22:
        add("vix_level", vix_level, 2, "stress VIX")
    elif vix_level >= 16:
        add("vix_level", vix_level, 1, "elevated VIX")
    else:
        add("vix_level", vix_level, 0, "calm VIX")

    if vix_5d is None:
        add("vix_5d_change", None, 0, "VIX 5d change unavailable")
    elif vix_5d >= 0.50:
        add("vix_5d_change", vix_5d, 3, "panic VIX spike")
    elif vix_5d >= 0.30:
        add("vix_5d_change", vix_5d, 2, "stress VIX spike")
    elif vix_5d >= 0.15:
        add("vix_5d_change", vix_5d, 1, "early VIX stress")
    else:
        add("vix_5d_change", vix_5d, 0, "VIX change normal")

    if vix_ratio is None:
        add("vix_term", None, 0, "VIX term unavailable")
    elif vix_ratio > 1.05:
        add("vix_term", vix_ratio, 3, "near-term panic inversion")
    elif vix_ratio >= 1.00:
        add("vix_term", vix_ratio, 1, "flat/mild inversion")
    else:
        add("vix_term", vix_ratio, 0, "contango")

    for ticker in ("SPY", "QQQ", "SMH"):
        if ticker not in close.columns:
            add(f"{ticker}_dd63", None, 0, f"{ticker} unavailable")
            continue
        dd = drawdown_from_high(close[ticker]).at[as_of]
        if pd.isna(dd):
            add(f"{ticker}_dd63", None, 0, f"{ticker} drawdown unavailable")
        elif dd <= -0.12:
            add(f"{ticker}_dd63", dd, 3, f"{ticker} deep drawdown")
        elif dd <= -0.08:
            add(f"{ticker}_dd63", dd, 2, f"{ticker} meaningful stress")
        elif dd <= -0.04:
            add(f"{ticker}_dd63", dd, 1, f"{ticker} mild drawdown")
        else:
            add(f"{ticker}_dd63", dd, 0, f"{ticker} drawdown normal")

    for ticker, label in (("SPY", "spy_trend"), ("QQQ", "qqq_trend")):
        if ticker not in close.columns:
            add(label, None, 0, f"{ticker} unavailable")
            continue
        ma50 = close[ticker].rolling(50, min_periods=30).mean().at[as_of]
        ma200 = close[ticker].rolling(200, min_periods=120).mean().at[as_of]
        px = close.at[as_of, ticker]
        points = 0
        note = f"{ticker} above MA50/MA200"
        if pd.notna(ma200) and px < ma200:
            points += 2
            note = f"{ticker} below MA200"
        elif pd.notna(ma50) and px < ma50:
            points += 1
            note = f"{ticker} below MA50"
        add(label, _safe(px / ma200 - 1.0) if pd.notna(ma200) and ma200 else None, points, note)

    for left, right, name in (("IWM", "SPY", "iwm_spy_21d"), ("RSP", "SPY", "rsp_spy_21d"), ("HYG", "LQD", "hyg_lqd_21d")):
        if left not in close.columns or right not in close.columns:
            add(name, None, 0, f"{name} unavailable")
            continue
        rel = close[left] / close[right]
        if as_of not in rel.index:
            add(name, None, 0, f"{name} unavailable")
            continue
        loc = rel.index.get_loc(as_of)
        if not isinstance(loc, int) or loc < 21:
            add(name, None, 0, f"{name} warm-up")
            continue
        prior = rel.index[loc - 21]
        if pd.isna(rel.at[as_of]) or pd.isna(rel.at[prior]) or rel.at[prior] == 0:
            add(name, None, 0, f"{name} unavailable")
            continue
        change = float(rel.at[as_of] / rel.at[prior] - 1.0)
        if change <= -0.05:
            add(name, change, 2, f"{name} deteriorating sharply")
        elif change <= -0.025:
            add(name, change, 1, f"{name} deteriorating")
        else:
            add(name, change, 0, f"{name} stable")

    score = int(sum(signal.points for signal in signals))
    if score >= 14:
        regime, risk_multiplier, max_gross, max_new_buy, cash_floor = "panic", 0.20, 0.35, 0.00, 0.65
        action = "Stop new buys; preserve capital; only consider hedges or forced risk reduction."
    elif score >= 9:
        regime, risk_multiplier, max_gross, max_new_buy, cash_floor = "stress", 0.40, 0.55, 0.10, 0.45
        action = "Cut position sizes, avoid weak names, and require reclaim signals before adding."
    elif score >= 5:
        regime, risk_multiplier, max_gross, max_new_buy, cash_floor = "elevated", 0.70, 0.75, 0.25, 0.25
        action = "Allow staged buys only near support; keep a meaningful cash buffer."
    else:
        regime, risk_multiplier, max_gross, max_new_buy, cash_floor = "normal", 1.00, 0.95, 0.50, 0.05
        action = "Normal staged buying is allowed when stock-level filters agree."

    return FearSnapshot(
        as_of=str(as_of.date()),
        score=score,
        regime=regime,
        risk_multiplier=risk_multiplier,
        max_gross_exposure=max_gross,
        max_new_buy_exposure=max_new_buy,
        cash_floor=cash_floor,
        signals=signals,
        action=action,
    )


def panic_to_repair_label(
    close: pd.DataFrame,
    vix: pd.DataFrame | None,
    as_of: pd.Timestamp,
    prior_drawdown_threshold: float = -0.15,
    rebound_window: int = 21,
    rebound_threshold: float = 0.08,
    high_vix: float = 25.0,
) -> dict[str, Any]:
    """Causal panic-to-repair diagnostic.

    Label is true only when:
    1. SPY experienced a lagged drawdown beyond the threshold;
    2. VIX was elevated into the rebound window;
    3. SPY has rebounded sharply over the recent rebound window.
    """
    as_of = pd.Timestamp(as_of)
    if "SPY" not in close.columns or as_of not in close.index:
        return {
            "as_of": str(as_of.date()),
            "label": "unavailable",
            "is_panic_to_repair": False,
            "reason": "SPY unavailable",
        }

    spy = close["SPY"]
    loc = spy.index.get_loc(as_of)
    if not isinstance(loc, int) or loc < max(126, rebound_window + 5):
        return {
            "as_of": str(as_of.date()),
            "label": "warmup",
            "is_panic_to_repair": False,
            "reason": "insufficient history",
        }

    dd63 = drawdown_from_high(spy, 63)
    prior_start = spy.index[max(0, loc - 252)]
    prior_end = spy.index[max(0, loc - rebound_window)]
    prior_min_dd = float(dd63.loc[prior_start:prior_end].min())

    rebound = float(spy.at[as_of] / spy.at[spy.index[loc - rebound_window]] - 1.0)
    vix_peak = None
    if vix is not None and "^VIX" in vix.columns:
        window = vix.loc[spy.index[loc - rebound_window]:as_of, "^VIX"].dropna()
        if not window.empty:
            vix_peak = float(window.max())

    is_event = (
        prior_min_dd <= prior_drawdown_threshold
        and rebound >= rebound_threshold
        and (vix_peak is None or vix_peak >= high_vix)
    )
    if is_event:
        label = "panic_to_repair"
        reason = "prior deep drawdown + elevated vol + sharp rebound"
    elif prior_min_dd <= prior_drawdown_threshold:
        label = "post_drawdown_watch"
        reason = "prior deep drawdown without confirmed rebound package"
    else:
        label = "normal"
        reason = "no panic-to-repair package"

    return {
        "as_of": str(as_of.date()),
        "label": label,
        "is_panic_to_repair": bool(is_event),
        "prior_min_dd63": prior_min_dd,
        "rebound_21d": rebound,
        "vix_peak_in_rebound_window": vix_peak,
        "reason": reason,
        "factor_family": "state_transition_monitor",
        "authorizes_trade": False,
    }


def momentum_family_snapshot(close: pd.DataFrame, as_of: pd.Timestamp) -> dict[str, Any]:
    """Keep XSMOM/TSMOM/MA/drawdown momentum definitions separated."""
    as_of = pd.Timestamp(as_of)
    out: dict[str, Any] = {"as_of": str(as_of.date()), "families": {}}
    for ticker in ("SPY", "QQQ"):
        if ticker not in close.columns or as_of not in close.index:
            continue
        series = close[ticker]
        ma150 = series.rolling(150, min_periods=100).mean().at[as_of]
        ma200 = series.rolling(200, min_periods=120).mean().at[as_of]
        px = float(series.at[as_of])
        out["families"][ticker] = {
            "ma_trend": {
                "above_ma150": bool(pd.notna(ma150) and px > ma150),
                "above_ma200": bool(pd.notna(ma200) and px > ma200),
            },
            "drawdown_momentum": {
                "dd63": _safe(drawdown_from_high(series, 63).at[as_of]),
            },
            "absolute_momentum": {
                "mom21": _safe(series.pct_change(21).at[as_of]),
                "mom63": _safe(series.pct_change(63).at[as_of]),
                "mom126": _safe(series.pct_change(126).at[as_of]),
            },
            "vol126": _safe(realized_vol126(series).at[as_of]),
            "slow_vol_scale": _safe(slow_vol_scale(series).at[as_of]),
        }
    if "SPY" in out["families"] and "QQQ" in out["families"]:
        q = out["families"]["QQQ"]["absolute_momentum"]
        s = out["families"]["SPY"]["absolute_momentum"]
        out["relative_momentum"] = {
            "qqq_minus_spy_mom63": (
                None
                if q["mom63"] is None or s["mom63"] is None
                else float(q["mom63"] - s["mom63"])
            ),
            "note": "relative momentum is monitor-only; not a chase/short signal",
        }
    out["definitions"] = {
        "XSMOM": "cross-sectional winners-minus-losers ranking; not used by V9 weights",
        "TSMOM": "own-history sign of returns; not used by V9 weights",
        "MA_trend": "SPY/QQQ vs MA150/MA200; formal V8 index-core weights",
        "drawdown_momentum": "distance from 63-day high; Fear Gate input",
        "Rule_E_RS": "event + technical relative strength; long-only sleeve",
    }
    return out


def behavioral_execution_audit(fields: dict[str, Any] | None = None) -> dict[str, Any]:
    """Checklist for detecting reference-point / loss-domain process violations."""
    fields = fields or {}
    flags = {
        "cost_basis_used_as_invalidation": bool(fields.get("cost_basis_used_as_invalidation", False)),
        "break_even_desire_overrides_stop": bool(fields.get("break_even_desire_overrides_stop", False)),
        "averaging_down_without_reclaim": bool(fields.get("averaging_down_without_reclaim", False)),
        "peak_anchor_blocks_trim": bool(fields.get("peak_anchor_blocks_trim", False)),
    }
    return {
        "authorizes_trade": False,
        "flags": flags,
        "violation_count": int(sum(flags.values())),
        "note": "Behavioral audit may expose process violations but never creates a price signal.",
    }


def build_research_diagnostics(
    close: pd.DataFrame,
    vix: pd.DataFrame | None,
    as_of: pd.Timestamp,
    behavioral_fields: dict[str, Any] | None = None,
) -> dict[str, Any]:
    fear = compute_fear_snapshot(close, vix, as_of)
    return {
        "authorizes_trade": False,
        "fear_gate_advisory": {
            **{k: v for k, v in asdict(fear).items() if k != "signals"},
            "signals": [asdict(signal) for signal in fear.signals],
        },
        "panic_to_repair": panic_to_repair_label(close, vix, as_of),
        "momentum_families": momentum_family_snapshot(close, as_of),
        "behavioral_execution_audit": behavioral_execution_audit(behavioral_fields),
    }
