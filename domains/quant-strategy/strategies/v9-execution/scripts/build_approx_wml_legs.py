#!/usr/bin/env python3
"""Approximate long-winner / short-loser legs from the PIT/universe panel.

This is a research comparator only. It is not Ken French CRSP WML and must not
validate formal V9 weights.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PIT_CLOSE = ROOT / "datasets" / "data_point_in_time" / "adjusted_close.csv"
PIT_MEMBERSHIP = ROOT / "datasets" / "data_point_in_time" / "membership_history.csv"
FALLBACK_CLOSE = ROOT / "datasets" / "data_universe" / "us_stock_universe_2000_2025.csv"
OUT_DIR = ROOT / "datasets" / "data_factor"


def normalize(symbol: str) -> str:
    return str(symbol).strip().upper().replace(".", "-")


def active_members(history: pd.DataFrame, date: pd.Timestamp) -> set[str]:
    mask = (history["opt-in"] <= date) & (history["opt-out"].isna() | (history["opt-out"] > date))
    return set(history.loc[mask, "symbol"].map(normalize))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formation", type=int, default=252, help="formation window in trading days")
    parser.add_argument("--skip", type=int, default=21, help="skip most recent days")
    parser.add_argument("--hold", type=int, default=21, help="holding period in trading days")
    args = parser.parse_args()

    close_path = PIT_CLOSE if PIT_CLOSE.exists() else FALLBACK_CLOSE
    close = pd.read_csv(close_path, index_col=0, parse_dates=True).sort_index()
    close.columns = [normalize(c) for c in close.columns]
    history = None
    if PIT_MEMBERSHIP.exists():
        history = pd.read_csv(PIT_MEMBERSHIP, parse_dates=["opt-in", "opt-out"])
        history["symbol"] = history["symbol"].map(normalize)

    formation_end = args.formation
    start_loc = formation_end + args.skip
    dates = close.index[start_loc::args.hold]
    rows = []
    for dt in dates:
        loc = close.index.get_loc(dt)
        if not isinstance(loc, int) or loc < formation_end + args.skip:
            continue
        form_end = close.index[loc - args.skip]
        form_start = close.index[loc - args.skip - args.formation]
        hold_end_loc = min(loc + args.hold, len(close.index) - 1)
        hold_end = close.index[hold_end_loc]

        members = None
        if history is not None:
            members = active_members(history, form_end)
        cols = [c for c in close.columns if members is None or c in members]
        window = close.loc[form_start:form_end, cols]
        valid = window.columns[window.notna().sum() >= max(60, int(0.6 * len(window)))]
        if len(valid) < 40:
            continue
        start_px = window[valid].apply(lambda s: s.dropna().iloc[0])
        end_px = window[valid].apply(lambda s: s.dropna().iloc[-1])
        formation_ret = (end_px / start_px - 1.0).replace([np.inf, -np.inf], np.nan).dropna()
        if len(formation_ret) < 40:
            continue
        ranked = formation_ret.sort_values()
        n = max(5, len(ranked) // 10)
        losers = ranked.index[:n]
        winners = ranked.index[-n:]
        hold = close.loc[dt:hold_end, list(set(winners) | set(losers))]
        if hold.shape[0] < 2:
            continue
        hold_ret = hold.iloc[-1] / hold.iloc[0] - 1.0
        winner_ret = float(hold_ret[winners].mean())
        loser_ret = float(hold_ret[losers].mean())
        rows.append({
            "date": dt,
            "hold_end": hold_end,
            "winner_leg": winner_ret,
            "loser_leg": loser_ret,
            "WML_approx": winner_ret - loser_ret,
            "n_winners": int(len(winners)),
            "n_losers": int(len(losers)),
        })

    if not rows:
        raise RuntimeError("failed to build approximate winner/loser legs")
    frame = pd.DataFrame(rows).set_index("date").sort_index()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / "approx_winner_loser_legs.csv"
    frame.to_csv(path)
    summary = {
        "path": str(path.relative_to(ROOT)),
        "rows": int(len(frame)),
        "start": str(frame.index.min().date()),
        "end": str(frame.index.max().date()),
        "mean_WML_approx": float(frame["WML_approx"].mean()),
        "mean_winner_leg": float(frame["winner_leg"].mean()),
        "mean_loser_leg": float(frame["loser_leg"].mean()),
        "source_close": str(close_path.relative_to(ROOT)),
        "decision_grade": False,
        "note": "Equal-weight decile approximation from cached prices; not Ken French CRSP WML.",
    }
    (OUT_DIR / "approx_winner_loser_legs_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
