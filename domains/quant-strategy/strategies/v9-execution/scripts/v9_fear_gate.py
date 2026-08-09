"""Canonical completed-close Market Fear Gate used by V9 execution and diagnostics."""
from __future__ import annotations

import pandas as pd


def compute_canonical_fear_gate(
    close: pd.DataFrame,
    vix: pd.DataFrame | None,
    as_of: pd.Timestamp,
    *,
    enabled: bool = True,
) -> dict:
    """Return the single formal Fear Gate calculation for one completed session."""
    as_of = pd.Timestamp(as_of)
    if as_of not in close.index:
        raise KeyError(f"as_of not in close index: {as_of.date()}")
    if not enabled:
        return {
            "score": 0,
            "regime": "disabled",
            "risk_multiplier": 1.0,
            "max_gross_exposure": 1.0,
            "max_new_buy_exposure": 1.0,
            "cash_floor": 0.0,
            "signals": [],
            "action": "Fear Gate disabled by explicit configuration.",
        }

    signals: list[dict] = []
    score = 0

    def add(name: str, value: float | None, points: int, note: str) -> None:
        nonlocal score
        score += int(points)
        signals.append({"name": name, "value": value, "points": int(points), "note": note})

    vix_value = None
    if vix is not None and as_of in vix.index and "^VIX" in vix.columns and pd.notna(vix.at[as_of, "^VIX"]):
        vix_value = float(vix.at[as_of, "^VIX"])
    if vix_value is None:
        add("vix_level", None, 0, "VIX unavailable")
    elif vix_value >= 35:
        add("vix_level", vix_value, 4, "panic VIX")
    elif vix_value >= 30:
        add("vix_level", vix_value, 3, "high-stress VIX")
    elif vix_value >= 22:
        add("vix_level", vix_value, 2, "stress VIX")
    elif vix_value >= 16:
        add("vix_level", vix_value, 1, "elevated VIX")
    else:
        add("vix_level", vix_value, 0, "calm VIX")

    vix_hist = vix.loc[:as_of, "^VIX"].dropna() if vix is not None and "^VIX" in vix.columns else pd.Series(dtype=float)
    if len(vix_hist) >= 6:
        change = float(vix_hist.iloc[-1] / vix_hist.iloc[-6] - 1.0)
        points = 3 if change >= .50 else 2 if change >= .30 else 1 if change >= .15 else 0
        note = "panic VIX spike" if points == 3 else "stress VIX spike" if points == 2 else "early VIX stress" if points == 1 else "VIX change normal"
        add("vix_5d_change", change, points, note)
    else:
        add("vix_5d_change", None, 0, "VIX 5d change unavailable")

    term = None
    if vix is not None and as_of in vix.index and "^VIX3M" in vix.columns and vix_value is not None:
        vix3m = vix.at[as_of, "^VIX3M"]
        if pd.notna(vix3m) and float(vix3m) > 0:
            term = vix_value / float(vix3m)
    if term is None:
        add("vix_vix3m_ratio", None, 0, "VIX term unavailable")
    elif term >= 1.05:
        add("vix_vix3m_ratio", term, 3, "near-term panic inversion")
    elif term >= 1.00:
        add("vix_vix3m_ratio", term, 2, "flat/mild inversion")
    else:
        add("vix_vix3m_ratio", term, 0, "contango")

    for symbol in ("SPY", "QQQ", "SMH"):
        if symbol not in close.columns:
            add(f"{symbol.lower()}_drawdown_63d", None, 0, f"{symbol} unavailable")
            add(f"{symbol.lower()}_trend_break", None, 0, f"{symbol} unavailable")
            continue
        history = close.loc[:as_of, symbol].dropna()
        if len(history) >= 63:
            drawdown = float(history.iloc[-1] / history.iloc[-63:].max() - 1.0)
            points = 3 if drawdown <= -.12 else 2 if drawdown <= -.08 else 1 if drawdown <= -.04 else 0
            note = f"{symbol} deep drawdown" if points == 3 else f"{symbol} meaningful stress" if points == 2 else f"{symbol} mild drawdown" if points == 1 else f"{symbol} drawdown normal"
            add(f"{symbol.lower()}_drawdown_63d", drawdown, points, note)
        else:
            add(f"{symbol.lower()}_drawdown_63d", None, 0, f"{symbol} drawdown warm-up")
        if len(history) >= 50:
            below50 = bool(history.iloc[-1] < history.rolling(50).mean().iloc[-1])
            below200 = bool(len(history) >= 200 and history.iloc[-1] < history.rolling(200).mean().iloc[-1])
            points = 3 if below200 else 1 if below50 else 0
            note = f"{symbol} below MA200" if below200 else f"{symbol} below MA50" if below50 else f"{symbol} above MA50/MA200"
            add(f"{symbol.lower()}_trend_break", float(below50 or below200), points, note)
        else:
            add(f"{symbol.lower()}_trend_break", None, 0, f"{symbol} trend warm-up")

    for numerator, denominator, name in (
        ("IWM", "SPY", "smallcap_vs_spy_21d"),
        ("RSP", "SPY", "equal_weight_vs_spy_21d"),
        ("HYG", "LQD", "credit_risk_21d"),
    ):
        if numerator not in close.columns or denominator not in close.columns:
            add(name, None, 0, f"{name} unavailable")
            continue
        relative = (close.loc[:as_of, numerator] / close.loc[:as_of, denominator]).dropna()
        if len(relative) >= 22:
            change = float(relative.iloc[-1] / relative.iloc[-22] - 1.0)
            points = 2 if change <= -.05 else 1 if change <= -.025 else 0
            note = f"{name} deteriorating sharply" if points == 2 else f"{name} deteriorating" if points == 1 else f"{name} stable"
            add(name, change, points, note)
        else:
            add(name, None, 0, f"{name} warm-up")

    if (vix_value is not None and vix_value >= 35) or score >= 14:
        regime, multiplier, max_gross, max_new_buy, cash_floor = "panic", .20, .35, 0.0, .65
        action = "Stop new buys; preserve capital; only consider forced risk reduction."
    elif score >= 9:
        regime, multiplier, max_gross, max_new_buy, cash_floor = "stress", .40, .55, .10, .45
        action = "Cut sizes, avoid weak names, and require reclaim signals before adding."
    elif score >= 5:
        regime, multiplier, max_gross, max_new_buy, cash_floor = "elevated", .70, .75, .25, .25
        action = "Allow staged buys only near support and keep a meaningful cash buffer."
    else:
        regime, multiplier, max_gross, max_new_buy, cash_floor = "normal", 1.0, .95, .50, .05
        action = "Normal staged buying is allowed only when stock-level filters agree."
    return {
        "score": int(score),
        "regime": regime,
        "risk_multiplier": multiplier,
        "max_gross_exposure": max_gross,
        "max_new_buy_exposure": max_new_buy,
        "cash_floor": cash_floor,
        "signals": signals,
        "action": action,
    }
