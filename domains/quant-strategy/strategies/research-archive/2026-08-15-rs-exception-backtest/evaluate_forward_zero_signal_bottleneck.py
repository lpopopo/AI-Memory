#!/usr/bin/env python3
"""Explain zero forward RSR1 signals with a fixed, non-optimizing funnel."""
from __future__ import annotations

import json
import runpy
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
BACKTEST = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
START = pd.Timestamp("2026-08-17")
FUNNEL = [
    "usable_ohlcv",
    "broad_gate",
    "smh_ma50",
    "above_ma20",
    "above_ma50",
    "breakout_prior_high20",
    "rs20_at_least_3pct",
    "volume_ratio_at_least_1_2",
    "extension_0_to_12pct",
    "event_cooldown_clear",
    "atr_at_most_4pct",
    "close_location_at_least_50pct",
]


def broadcast(series: pd.Series, columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame(
        np.repeat(series.fillna(False).to_numpy(dtype=bool)[:, None], len(columns), axis=1),
        index=series.index,
        columns=columns,
    )


def sequential_survivors(conditions: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    missing = [name for name in FUNNEL if name not in conditions]
    if missing:
        raise RuntimeError(f"missing funnel conditions: {missing}")
    active = pd.DataFrame(True, index=conditions[FUNNEL[0]].index, columns=conditions[FUNNEL[0]].columns)
    frames = {}
    counts = {}
    for name in FUNNEL:
        active = active & conditions[name].fillna(False)
        frames[name] = active.copy()
        counts[name] = active.sum(axis=1).astype(int)
    return pd.DataFrame(counts), frames


def first_zero_step(counts: pd.Series) -> str | None:
    previous = None
    for name in FUNNEL:
        current = int(counts[name])
        if current == 0 and (previous is None or previous > 0):
            return name
        previous = current
    return None


def binding_symbols(
    date: pd.Timestamp,
    step: str | None,
    conditions: dict[str, pd.DataFrame],
    frames: dict[str, pd.DataFrame],
) -> list[str]:
    if step is None:
        return []
    offset = FUNNEL.index(step)
    prior = (
        pd.Series(True, index=conditions[step].columns)
        if offset == 0
        else frames[FUNNEL[offset - 1]].loc[date]
    )
    failed_here = prior & ~conditions[step].loc[date]
    return sorted(failed_here.index[failed_here].tolist())


def evaluate() -> tuple[dict, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    status = json.loads((RESULTS / "forward_shadow_status.json").read_text(encoding="utf-8"))
    as_of = pd.Timestamp(status["as_of"])
    panels, all_symbols = BACKTEST["load_panels"]()
    universes, _ = UNIVERSE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    dates = panels["close"].index[(panels["close"].index >= START) & (panels["close"].index <= as_of)]
    if len(dates) != int(status.get("sessions", 0)):
        raise RuntimeError(f"status/data session mismatch: {status.get('sessions')} vs {len(dates)}")

    close, open_, high, low, volume = (panels[name] for name in ("close", "open", "high", "low", "volume"))
    stock_close = close[symbols]
    stock_open, stock_high, stock_low, stock_volume = (
        open_[symbols], high[symbols], low[symbols], volume[symbols]
    )
    ma20 = stock_close.rolling(20, min_periods=20).mean()
    ma50 = stock_close.rolling(50, min_periods=50).mean()
    prior_high20 = stock_high.rolling(20, min_periods=20).max().shift(1)
    rs20 = stock_close.pct_change(20, fill_method=None).sub(
        close["SMH"].pct_change(20, fill_method=None), axis=0
    )
    volume_ratio = stock_volume / stock_volume.rolling(20, min_periods=20).mean().shift(1)
    extension = stock_close / ma20 - 1.0
    prior_close = stock_close.shift(1)
    true_range = pd.DataFrame(
        np.maximum.reduce(
            [
                (stock_high - stock_low).to_numpy(),
                (stock_high - prior_close).abs().to_numpy(),
                (stock_low - prior_close).abs().to_numpy(),
            ]
        ),
        index=stock_close.index,
        columns=symbols,
    )
    atr_pct = true_range.rolling(14, min_periods=14).mean() / stock_close
    close_location = (stock_close - stock_low) / (stock_high - stock_low).replace(0.0, np.nan)
    positive_gap = stock_open / prior_close - 1.0 >= 0.10
    day_range = (stock_high - stock_low) / stock_open
    event_block = positive_gap | positive_gap.shift(1).fillna(False)
    event_block |= positive_gap.shift(2).fillna(False) & (day_range >= 0.03)

    spy_ma200 = close["SPY"].rolling(200, min_periods=200).mean()
    qqq_ma100 = close["QQQ"].rolling(100, min_periods=100).mean()
    smh_ma50 = close["SMH"].rolling(50, min_periods=50).mean()
    vix_ratio = close["^VIX"] / close["^VIX3M"]
    broad_gate = (
        (close["SPY"] > spy_ma200)
        & (close["QQQ"] > qqq_ma100)
        & (close["^VIX"] < 25.0)
        & (vix_ratio < 1.0)
    )
    smh_gate = close["SMH"] >= smh_ma50
    usable = stock_open.notna() & stock_high.notna() & stock_low.notna() & stock_close.notna() & stock_volume.notna()
    conditions = {
        "usable_ohlcv": usable,
        "broad_gate": broadcast(broad_gate, symbols),
        "smh_ma50": broadcast(smh_gate, symbols),
        "above_ma20": stock_close > ma20,
        "above_ma50": stock_close > ma50,
        "breakout_prior_high20": stock_close > prior_high20,
        "rs20_at_least_3pct": rs20 >= 0.03,
        "volume_ratio_at_least_1_2": volume_ratio >= 1.20,
        "extension_0_to_12pct": (extension >= 0.0) & (extension <= 0.12),
        "event_cooldown_clear": ~event_block,
        "atr_at_most_4pct": atr_pct <= 0.04,
        "close_location_at_least_50pct": close_location >= 0.50,
    }
    conditions = {name: frame.loc[dates, symbols] for name, frame in conditions.items()}
    sequential, frames = sequential_survivors(conditions)
    marginal_pass = pd.DataFrame({name: frame.sum(axis=1).astype(int) for name, frame in conditions.items()})
    marginal_fail = len(symbols) - marginal_pass

    stock_baseline = (
        conditions["usable_ohlcv"]
        & conditions["above_ma20"]
        & conditions["above_ma50"]
        & conditions["breakout_prior_high20"]
        & conditions["rs20_at_least_3pct"]
        & conditions["volume_ratio_at_least_1_2"]
        & conditions["extension_0_to_12pct"]
        & conditions["event_cooldown_clear"]
    )
    broad_without_smh = stock_baseline & conditions["broad_gate"]
    strict_pre_quality = broad_without_smh & conditions["smh_ma50"]
    final_rsr1 = strict_pre_quality & conditions["atr_at_most_4pct"] & conditions["close_location_at_least_50pct"]

    config = UNIVERSE["make_config"](True)
    built = BACKTEST["build_features"](panels, symbols, config)
    engine_final = built["signal"].loc[dates, symbols] & broadcast(built["smh_healthy"], symbols).loc[dates, symbols]
    if not final_rsr1.equals(engine_final):
        raise RuntimeError("diagnostic funnel does not reproduce frozen RSR1 final signals")

    rows = []
    bottlenecks = Counter()
    for date in dates:
        bottleneck = first_zero_step(sequential.loc[date])
        bound = binding_symbols(date, bottleneck, conditions, frames)
        bottlenecks[bottleneck or "final_candidates_present"] += 1
        rows.append(
            {
                "date": str(date.date()),
                "spy_above_ma200": bool(close.at[date, "SPY"] > spy_ma200.at[date]),
                "qqq_above_ma100": bool(close.at[date, "QQQ"] > qqq_ma100.at[date]),
                "vix_below_25": bool(close.at[date, "^VIX"] < 25.0),
                "vix_term_ratio_below_1": bool(vix_ratio.at[date] < 1.0),
                "broad_gate": bool(broad_gate.at[date]),
                "smh_close": float(close.at[date, "SMH"]),
                "smh_ma50": float(smh_ma50.at[date]),
                "smh_gate": bool(smh_gate.at[date]),
                "stock_level_baseline_before_market_gates": int(stock_baseline.loc[date].sum()),
                "baseline_with_broad_without_smh": int(broad_without_smh.loc[date].sum()),
                "strict_pre_quality": int(strict_pre_quality.loc[date].sum()),
                "final_rsr1": int(final_rsr1.loc[date].sum()),
                "first_zero_step": bottleneck,
                "binding_symbol_count": len(bound),
                "binding_symbols": bound,
            }
        )
    daily = pd.DataFrame(rows)
    aggregate_rows = []
    for name in FUNNEL:
        aggregate_rows.append(
            {
                "condition": name,
                "marginal_pass_symbol_days": int(marginal_pass[name].sum()),
                "marginal_fail_symbol_days": int(marginal_fail[name].sum()),
                "sequential_survivor_symbol_days": int(sequential[name].sum()),
            }
        )
    aggregate = pd.DataFrame(aggregate_rows)
    detail_rows = []
    for date in dates:
        for symbol in symbols:
            detail_rows.append(
                {
                    "date": str(date.date()),
                    "symbol": symbol,
                    **{name: bool(conditions[name].at[date, symbol]) for name in FUNNEL},
                    "final_rsr1": bool(final_rsr1.at[date, symbol]),
                    "extension": float(extension.at[date, symbol]),
                    "atr_pct": float(atr_pct.at[date, symbol]),
                    "close_location": float(close_location.at[date, symbol]),
                    "rs20": float(rs20.at[date, symbol]),
                    "volume_ratio": float(volume_ratio.at[date, symbol]),
                }
            )
    details = pd.DataFrame(detail_rows)
    summary = {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "changes_gate": False,
        "period": [str(dates[0].date()), str(dates[-1].date())],
        "sessions": len(dates),
        "symbols": len(symbols),
        "symbol_days": len(dates) * len(symbols),
        "fixed_funnel": FUNNEL,
        "binding_bottleneck_sessions": dict(sorted(bottlenecks.items())),
        "counterfactual_totals": {
            "stock_level_baseline_before_market_gates": int(stock_baseline.to_numpy().sum()),
            "baseline_with_broad_without_smh": int(broad_without_smh.to_numpy().sum()),
            "strict_pre_quality": int(strict_pre_quality.to_numpy().sum()),
            "final_rsr1": int(final_rsr1.to_numpy().sum()),
        },
        "daily": rows,
        "engine_reconciliation_passed": True,
        "decision": "diagnostic_only_no_rule_relaxation",
    }
    return summary, daily, aggregate, details


def write_report(summary: dict, aggregate: pd.DataFrame) -> None:
    totals = summary["counterfactual_totals"]
    lines = [
        "# Forward zero-signal bottleneck audit",
        "",
        "## Bottom line",
        "",
        "This audit explains the absence of RSR1 signals without changing any threshold. Counterfactual counts are diagnostics, not trades.",
        "",
        f"- Period: {summary['period'][0]} through {summary['period'][1]}",
        f"- Sessions / symbols / symbol-days: {summary['sessions']} / {summary['symbols']} / {summary['symbol_days']}",
        f"- Binding first-zero steps by session: {summary['binding_bottleneck_sessions']}",
        f"- Stock-level baseline candidates before broad/SMH gates: {totals['stock_level_baseline_before_market_gates']}",
        f"- With broad gate but ignoring SMH veto: {totals['baseline_with_broad_without_smh']}",
        f"- With strict SMH veto, before quality pair: {totals['strict_pre_quality']}",
        f"- Final RSR1 candidates: {totals['final_rsr1']}",
        "",
        "## Daily market gates and counterfactuals",
        "",
        "| Date | Broad | SMH>=MA50 | SMH close | SMH MA50 | Stock baseline | Broad/no-SMH | Strict pre-quality | RSR1 | First zero |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summary["daily"]:
        lines.append(
            f"| {row['date']} | {row['broad_gate']} | {row['smh_gate']} | {row['smh_close']:.2f} | "
            f"{row['smh_ma50']:.2f} | {row['stock_level_baseline_before_market_gates']} | "
            f"{row['baseline_with_broad_without_smh']} | {row['strict_pre_quality']} | {row['final_rsr1']} | "
            f"{row['first_zero_step']} ({row['binding_symbol_count']}) |"
        )
    lines.extend(["", "## Binding symbols", ""])
    for row in summary["daily"]:
        names = row["binding_symbols"]
        display = ", ".join(names) if len(names) <= 5 else f"all {len(names)} frozen shadow symbols"
        lines.append(f"- {row['date']}: {row['first_zero_step']} — {display}")
    lines.extend(
        [
            "",
            "## Fixed funnel aggregate",
            "",
            "| Condition | Marginal pass | Marginal fail | Sequential survivors |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in aggregate.to_dict("records"):
        lines.append(
            f"| {row['condition']} | {row['marginal_pass_symbol_days']} | {row['marginal_fail_symbol_days']} | {row['sequential_survivor_symbol_days']} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Do not relax the SMH veto or the quality pair to manufacture trades. Continue the frozen forward comparison; zero trades provide no win-rate evidence and no order authorization.",
        ]
    )
    (RESULTS / "forward_zero_signal_bottleneck_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary, daily, aggregate, details = evaluate()
    (RESULTS / "forward_zero_signal_bottleneck_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    daily.to_csv(RESULTS / "forward_zero_signal_bottleneck_daily.csv", index=False)
    aggregate.to_csv(RESULTS / "forward_zero_signal_bottleneck_funnel.csv", index=False)
    details.to_csv(RESULTS / "forward_zero_signal_bottleneck_details.csv", index=False)
    write_report(summary, aggregate)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
