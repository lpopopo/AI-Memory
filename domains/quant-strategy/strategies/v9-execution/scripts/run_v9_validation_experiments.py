#!/usr/bin/env python3
"""Run the three pre-registered V9 research experiments on available data.

Experiments are diagnostic only and never change formal V9 weights.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
import sys

sys.path.insert(0, str(SCRIPTS))

from v9_research_monitors import (
    compute_fear_snapshot,
    drawdown_from_high,
    panic_to_repair_label,
    slow_vol_scale,
)

OUT_DIR = ROOT / "results" / "validation"


def load_market_panel() -> tuple[pd.DataFrame, pd.DataFrame | None]:
    preferred = ROOT / "datasets" / "data_v87_forward" / "market_adjusted_close.csv"
    if preferred.exists():
        close = pd.read_csv(preferred, index_col=0, parse_dates=True).sort_index()
        vix_cols = [c for c in close.columns if c.startswith("^VIX")]
        vix = close[vix_cols].copy() if vix_cols else None
        return close, vix

    from v9_data import load_data

    panels, vix, _ = load_data()
    return panels["close"], vix


def load_wml() -> pd.Series | None:
    path = ROOT / "datasets" / "data_factor" / "ff_wml_daily.csv"
    if not path.exists():
        path = ROOT / "datasets" / "data_factor" / "ff_mom_daily.csv"
    if not path.exists():
        return None
    frame = pd.read_csv(path, index_col=0, parse_dates=True).sort_index()
    if "WML" in frame.columns:
        return frame["WML"].dropna()
    for column in frame.columns:
        if "mom" in column.lower() or column.lower() == "umd":
            return frame[column].dropna()
    return None


def max_drawdown(equity: pd.Series) -> float:
    peak = equity.cummax()
    return float((equity / peak - 1.0).min())


def expected_shortfall(returns: pd.Series, q: float = 0.05) -> float:
    if returns.empty:
        return float("nan")
    threshold = returns.quantile(q)
    tail = returns[returns <= threshold]
    return float(tail.mean()) if not tail.empty else float("nan")


def sharpe(returns: pd.Series) -> float:
    if returns.std(ddof=0) == 0 or returns.empty:
        return float("nan")
    return float(np.sqrt(252.0) * returns.mean() / returns.std(ddof=0))


def apply_costs(weights: pd.Series, one_way_cost: float) -> pd.Series:
    turnover = weights.diff().abs().fillna(weights.abs())
    return turnover * one_way_cost


def experiment_a_panic_to_repair(close: pd.DataFrame, vix: pd.DataFrame | None) -> dict:
    labels = []
    fear_regimes = []
    for dt in close.index[252:]:
        labels.append(panic_to_repair_label(close, vix, dt))
        fear_regimes.append(compute_fear_snapshot(close, vix, dt).regime)
    label_frame = pd.DataFrame(labels).set_index(close.index[252:])
    label_frame["fear_regime"] = fear_regimes
    event_dates = label_frame.index[label_frame["is_panic_to_repair"]].tolist()

    forward = {}
    for horizon in (1, 5, 21, 63):
        spy = close["SPY"].pct_change(horizon).shift(-horizon)
        qqq = close["QQQ"].pct_change(horizon).shift(-horizon) if "QQQ" in close.columns else None
        rows = []
        for dt in event_dates:
            if dt not in spy.index or pd.isna(spy.at[dt]):
                continue
            row = {"date": str(dt.date()), "spy": float(spy.at[dt])}
            if qqq is not None and pd.notna(qqq.at[dt]):
                row["qqq"] = float(qqq.at[dt])
            rows.append(row)
        forward[str(horizon)] = {
            "n": len(rows),
            "spy_mean": float(np.mean([r["spy"] for r in rows])) if rows else None,
            "qqq_mean": float(np.mean([r["qqq"] for r in rows if "qqq" in r])) if rows else None,
        }

    return {
        "experiment": "A_panic_to_repair",
        "event_count": int(label_frame["is_panic_to_repair"].sum()),
        "label_counts": label_frame["label"].value_counts().to_dict(),
        "overlap_with_fear_stress_or_worse": int(
            ((label_frame["is_panic_to_repair"]) & (label_frame["fear_regime"].isin(["stress", "panic"]))).sum()
        ),
        "forward_returns": forward,
        "authorizes_trade": False,
    }


def experiment_b_slow_vol(close: pd.DataFrame) -> dict:
    spy = close["SPY"].dropna()
    scale = slow_vol_scale(spy).dropna()
    aligned = pd.concat({"ret": spy.pct_change(), "scale": scale}, axis=1).dropna()
    results = {}
    for cost in (0.001, 0.002, 0.005):
        gross = aligned["ret"] * aligned["scale"]
        net = gross - apply_costs(aligned["scale"], cost)
        equity = (1.0 + net).cumprod()
        baseline = (1.0 + aligned["ret"]).cumprod()
        results[str(cost)] = {
            "overlay_cagr": float(equity.iloc[-1] ** (252 / len(equity)) - 1),
            "baseline_cagr": float(baseline.iloc[-1] ** (252 / len(baseline)) - 1),
            "overlay_sharpe": sharpe(net),
            "baseline_sharpe": sharpe(aligned["ret"]),
            "overlay_max_drawdown": max_drawdown(equity),
            "baseline_max_drawdown": max_drawdown(baseline),
            "overlay_es5": expected_shortfall(net),
            "baseline_es5": expected_shortfall(aligned["ret"]),
            "avg_scale": float(aligned["scale"].mean()),
            "turnover": float(aligned["scale"].diff().abs().fillna(aligned["scale"]).mean()),
        }
    return {
        "experiment": "B_slow_vol_overlay_126d",
        "sample_start": str(aligned.index.min().date()),
        "sample_end": str(aligned.index.max().date()),
        "by_cost": results,
        "authorizes_trade": False,
        "note": "Inspected 2019-2025 is not a fresh OOS period for future parameter changes.",
    }


def load_approx_legs() -> pd.DataFrame | None:
    path = ROOT / "datasets" / "data_factor" / "approx_winner_loser_legs.csv"
    if not path.exists():
        return None
    return pd.read_csv(path, index_col=0, parse_dates=True).sort_index()


def experiment_c_wml(close: pd.DataFrame, vix: pd.DataFrame | None, wml: pd.Series | None) -> dict:
    labels = [panic_to_repair_label(close, vix, dt) for dt in close.index[252:]]
    label_frame = pd.DataFrame(labels).set_index(close.index[252:])
    event_dates = label_frame.index[label_frame["is_panic_to_repair"]]

    result = {
        "experiment": "C_wml_comparator",
        "authorizes_trade": False,
        "v9_is_not_wml": True,
        "event_count": int(label_frame["is_panic_to_repair"].sum()),
    }

    if wml is None:
        result["status"] = "blocked_missing_ff_momentum"
        result["required"] = "Run scripts/download_ff_momentum.py"
        return result

    common = event_dates.intersection(wml.index)
    forward = {}
    for horizon in (1, 5, 21, 63):
        fut = wml.rolling(horizon).sum().shift(-horizon)
        spy = close["SPY"].pct_change(horizon).shift(-horizon)
        qqq = close["QQQ"].pct_change(horizon).shift(-horizon) if "QQQ" in close.columns else None
        rows = []
        for dt in common:
            if dt not in fut.index or pd.isna(fut.at[dt]):
                continue
            row = {
                "date": str(dt.date()),
                "wml": float(fut.at[dt]),
                "spy": float(spy.at[dt]) if dt in spy.index and pd.notna(spy.at[dt]) else None,
            }
            if qqq is not None and dt in qqq.index and pd.notna(qqq.at[dt]):
                row["qqq"] = float(qqq.at[dt])
            rows.append(row)
        forward[str(horizon)] = {
            "n": len(rows),
            "wml_mean": float(np.mean([r["wml"] for r in rows])) if rows else None,
            "spy_mean": float(np.mean([r["spy"] for r in rows if r["spy"] is not None])) if rows else None,
            "qqq_mean": float(np.mean([r["qqq"] for r in rows if "qqq" in r])) if rows else None,
            "wml_skew_fullsample": float(wml.skew()),
        }

    legs = load_approx_legs()
    legs_summary = None
    if legs is not None and not legs.empty:
        # Align to nearest prior rebalance date for each panic-to-repair event.
        leg_rows = []
        for dt in event_dates:
            prior = legs.index[legs.index <= dt]
            if len(prior) == 0:
                continue
            row = legs.loc[prior[-1]]
            leg_rows.append({
                "event_date": str(dt.date()),
                "leg_date": str(prior[-1].date()),
                "winner_leg": float(row["winner_leg"]),
                "loser_leg": float(row["loser_leg"]),
                "WML_approx": float(row["WML_approx"]),
            })
        if leg_rows:
            winners = [r["winner_leg"] for r in leg_rows]
            losers = [r["loser_leg"] for r in leg_rows]
            legs_summary = {
                "n": len(leg_rows),
                "winner_leg_mean": float(np.mean(winners)),
                "loser_leg_mean": float(np.mean(losers)),
                "WML_approx_mean": float(np.mean([r["WML_approx"] for r in leg_rows])),
                "loser_outperforms_winner_share": float(np.mean(np.asarray(losers) > np.asarray(winners))),
                "note": "Approx equal-weight decile legs from cached PIT/universe prices; not CRSP.",
            }

    result.update({
        "status": "completed_with_wml_and_approx_legs" if legs_summary else "completed_with_wml_only",
        "wml_sample": {
            "start": str(wml.index.min().date()),
            "end": str(wml.index.max().date()),
            "n": int(len(wml)),
        },
        "forward_returns": forward,
        "approx_legs_in_panic_to_repair": legs_summary,
    })
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    close, vix = load_market_panel()
    wml = load_wml()
    report = {
        "as_of_generated": str(pd.Timestamp.now(tz="UTC")),
        "contract": "validation/v9-validation-data-contract-v1.md",
        "experiments": {
            "A": experiment_a_panic_to_repair(close, vix),
            "B": experiment_b_slow_vol(close),
            "C": experiment_c_wml(close, vix, wml),
        },
        "promotion": {
            "formal_v9_changed": False,
            "reason": "Research diagnostics only; promotion requires independent gates in BEHAVIORAL_MOMENTUM_SUPPLEMENT.md",
        },
    }
    path = args.output_dir / "v9_validation_report_v1.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# V9 Validation Report v1",
        "",
        f"- Generated: `{report['as_of_generated']}`",
        "- Formal V9 weights unchanged.",
        "",
        "## Experiment A: Panic-to-repair",
        "",
        "```json",
        json.dumps(report["experiments"]["A"], indent=2),
        "```",
        "",
        "## Experiment B: Slow vol overlay",
        "",
        "```json",
        json.dumps(report["experiments"]["B"], indent=2),
        "```",
        "",
        "## Experiment C: WML comparator",
        "",
        "```json",
        json.dumps(report["experiments"]["C"], indent=2),
        "```",
    ]
    md_path = args.output_dir / "v9_validation_report_v1.md"
    md_path.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({"json": str(path), "markdown": str(md_path), "summary": {
        "A_events": report["experiments"]["A"].get("event_count"),
        "B_costs": list(report["experiments"]["B"].get("by_cost", {})),
        "C_status": report["experiments"]["C"].get("status"),
    }}, indent=2))


if __name__ == "__main__":
    main()
