#!/usr/bin/env python3
"""Research fixed target weights for the exact risk-filter candidate."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
RESULTS = HERE / "results"
WEIGHTS = (0.04, 0.06, 0.08, 0.10, 0.12, 0.15)
COMMON = dict(
    rs20_min=0.03,
    volume_ratio_min=1.20,
    max_extension=0.12,
    max_hold_days=20,
    stop_loss=0.08,
)


def make_config(weight: float, filtered: bool):
    return MODULE["Config"](
        **COMMON,
        max_atr_pct=0.04 if filtered else 1.00,
        min_close_location=0.50 if filtered else 0.00,
        normal_target_weight=weight,
    )


def peak_concurrent_positions(trades: list[dict]) -> int:
    events = []
    for trade in trades:
        events.append((pd.Timestamp(trade["entry_date"]), 1))
        if trade.get("exit_date"):
            # Exits occur before new entries at the next open in the simulator.
            events.append((pd.Timestamp(trade["exit_date"]), -1))
    active = peak = 0
    for _, delta in sorted(events, key=lambda item: (item[0], item[1])):
        active += delta
        peak = max(peak, active)
    return peak


def profit_concentration(trades: list[dict]) -> dict[str, float]:
    wins = [trade for trade in trades if trade.get("pnl") is not None and trade["pnl"] > 0]
    gross_profit = sum(trade["pnl"] for trade in wins)
    by_symbol: dict[str, float] = {}
    for trade in wins:
        by_symbol[trade["symbol"]] = by_symbol.get(trade["symbol"], 0.0) + trade["pnl"]
    return {
        "gross_profit": gross_profit,
        "winning_symbols": float(len(by_symbol)),
        "max_symbol_profit_share": max(by_symbol.values(), default=0.0) / gross_profit if gross_profit else 1.0,
    }


def evaluate(panels, symbols, last_date):
    intervals = {
        "train_2024_2025": ("2024-01-02", "2025-12-31"),
        "2026": ("2026-01-01", str(last_date.date())),
        "full": ("2024-01-02", str(last_date.date())),
    }
    rows = []
    for period_name, interval in intervals.items():
        for cost_bps in (10, 20):
            for filtered in (False, True):
                variant = "risk_filter" if filtered else "matched_baseline"
                for weight in WEIGHTS:
                    result = MODULE["simulate"](
                        panels,
                        symbols,
                        make_config(weight, filtered),
                        "strict_veto",
                        *interval,
                        slippage=cost_bps / 10_000,
                    )
                    metrics = result["metrics"]
                    concentration = profit_concentration(result["trades"])
                    rows.append(
                        {
                            "period": period_name,
                            "cost_bps": cost_bps,
                            "variant": variant,
                            "target_weight": weight,
                            **metrics,
                            "peak_concurrent_positions": peak_concurrent_positions(result["trades"]),
                            "return_per_average_exposure": (
                                metrics["total_return"] / metrics["exposure"] if metrics["exposure"] > 0 else np.nan
                            ),
                            "return_to_drawdown": (
                                metrics["total_return"] / abs(metrics["max_drawdown"])
                                if metrics["max_drawdown"] < 0
                                else np.nan
                            ),
                            **concentration,
                        }
                    )
    return pd.DataFrame(rows)


def execution_path_stability(panels, symbols, last_date) -> pd.DataFrame:
    interval = ("2024-01-02", str(last_date.date()))
    rows = []
    for weight in WEIGHTS:
        trade_sets = {}
        results = {}
        for cost_bps in (10, 20):
            result = MODULE["simulate"](
                panels,
                symbols,
                make_config(weight, True),
                "strict_veto",
                *interval,
                slippage=cost_bps / 10_000,
            )
            results[cost_bps] = result
            trade_sets[cost_bps] = {
                (trade["signal_date"], trade["symbol"]) for trade in result["trades"]
            }
        fixed_stress = MODULE["fixed_path_cost_stress"](
            results[10], source_slippage=0.001, stressed_slippage=0.002
        )
        union = trade_sets[10] | trade_sets[20]
        intersection = trade_sets[10] & trade_sets[20]
        rows.append(
            {
                "target_weight": weight,
                "trades_10bps": len(trade_sets[10]),
                "trades_20bps": len(trade_sets[20]),
                "only_10bps": len(trade_sets[10] - trade_sets[20]),
                "only_20bps": len(trade_sets[20] - trade_sets[10]),
                "jaccard": len(intersection) / len(union) if union else 1.0,
                "path_stable": trade_sets[10] == trade_sets[20],
                "rerun_10bps_return": results[10]["metrics"]["total_return"],
                "rerun_20bps_return": results[20]["metrics"]["total_return"],
                "fixed_path_20bps_return": fixed_stress["total_return"],
                "fixed_path_cost_delta": fixed_stress["total_return"] - results[10]["metrics"]["total_return"],
                "only_10bps_keys": ";".join(f"{date}|{symbol}" for date, symbol in sorted(trade_sets[10] - trade_sets[20])),
                "only_20bps_keys": ";".join(f"{date}|{symbol}" for date, symbol in sorted(trade_sets[20] - trade_sets[10])),
            }
        )
    return pd.DataFrame(rows)


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2%}"


def num(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2f}"


def write_report(metrics: pd.DataFrame, path_stability: pd.DataFrame):
    candidate = metrics.loc[(metrics["variant"] == "risk_filter") & (metrics["cost_bps"] == 10)]
    full = candidate.loc[candidate["period"] == "full"]
    frozen = full.loc[full["target_weight"] == 0.08].iloc[0]
    robust = []
    for weight in WEIGHTS:
        sample = candidate.loc[candidate["target_weight"] == weight].set_index("period")
        robust.append(
            {
                "target_weight": weight,
                "positive_both": bool(
                    (sample.loc["train_2024_2025", "total_return"] > 0)
                    and (sample.loc["2026", "total_return"] > 0)
                ),
                "beats_frozen_both": bool(
                    (sample.loc["train_2024_2025", "total_return"]
                     > candidate.loc[
                         (candidate["period"] == "train_2024_2025") & (candidate["target_weight"] == 0.08),
                         "total_return",
                     ].iloc[0])
                    and (sample.loc["2026", "total_return"]
                         > candidate.loc[
                             (candidate["period"] == "2026") & (candidate["target_weight"] == 0.08),
                             "total_return",
                         ].iloc[0])
                ),
                "max_drawdown_both_under_5pct": bool((sample["max_drawdown"] >= -0.05).all()),
            }
        )
    robust_frame = pd.DataFrame(robust)
    robust_frame = robust_frame.merge(
        path_stability[["target_weight", "path_stable"]], on="target_weight", how="left"
    )
    challengers = robust_frame.loc[
        robust_frame["beats_frozen_both"] & robust_frame["max_drawdown_both_under_5pct"]
        & robust_frame["path_stable"]
    ]

    lines = [
        "# Exact-filter position-sizing study",
        "",
        "## Boundary",
        "",
        "This changes only the normal target weight of the fixed exact-filter strategy. Initial NAV remains $6,000, whole shares and the $200 fee floor remain active, single-name max is 15%, stock-sleeve max is 25%, and maximum names is three. "
        "Weights above 8% may reduce concurrent diversification because three full targets no longer fit inside the 25% sleeve. Research-only; frozen RSR1 remains 8%.",
        "",
        "## Candidate at 10 bps",
        "",
        "| Period | Target | Return | Max DD | Sharpe | Win rate | Trades | Exposure | Peak names | Max profit share |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in candidate.itertuples(index=False):
        lines.append(
            f"| {row.period} | {pct(row.target_weight)} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
            f"{num(row.sharpe)} | {pct(row.win_rate)} | {row.trade_count} | {pct(row.exposure)} | "
            f"{row.peak_concurrent_positions} | {pct(row.max_symbol_profit_share)} |"
        )
    lines.extend(
        [
            "",
            "## Full-period 10/20 bps sensitivity",
            "",
            "| Cost | Target | Return | Max DD | Sharpe | Exposure | Return / DD |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    full_cost = metrics.loc[(metrics["variant"] == "risk_filter") & (metrics["period"] == "full")]
    for row in full_cost.itertuples(index=False):
        lines.append(
            f"| {row.cost_bps} bps | {pct(row.target_weight)} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
            f"{num(row.sharpe)} | {pct(row.exposure)} | {num(row.return_to_drawdown)} |"
        )
    lines.extend(
        [
            "",
            "## Execution-path stability between 10 and 20 bps",
            "",
            "| Target | Trades 10bps | Trades 20bps | Only at 10bps | Only at 20bps | Jaccard | Stable |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in path_stability.itertuples(index=False):
        lines.append(
            f"| {pct(row.target_weight)} | {row.trades_10bps} | {row.trades_20bps} | {row.only_10bps} | "
            f"{row.only_20bps} | {row.jaccard:.2f} | {row.path_stable} |"
        )
    lines.extend(
        [
            "",
            "| Target | 10bps return | 20bps rerun | 20bps fixed-path | Fixed-path cost drag |",
            "| ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in path_stability.itertuples(index=False):
        lines.append(
            f"| {pct(row.target_weight)} | {pct(row.rerun_10bps_return)} | {pct(row.rerun_20bps_return)} | "
            f"{pct(row.fixed_path_20bps_return)} | {row.fixed_path_cost_delta:+.2%} |"
        )
    lines.extend(
        [
            "",
            "A higher-cost result can look better when slippage pushes one whole-share order over the 15% single-name cap and removes a losing trade. "
            "That is a sizing cliff, not cost robustness; a challenger must preserve its trade set across the tested cost levels.",
            "",
            "## Decision",
            "",
            f"- Frozen 8% full-period result: return {frozen.total_return:.2%}, max DD {frozen.max_drawdown:.2%}, "
            f"Sharpe {frozen.sharpe:.2f}, peak names {int(frozen.peak_concurrent_positions)}, max symbol gross-profit share "
            f"{frozen.max_symbol_profit_share:.2%}.",
            f"- Higher/lower weights that beat 8% on return in both training and 2026 while keeping both drawdowns within 5%: "
            f"`{', '.join(f'{value:.0%}' for value in challengers['target_weight']) if not challengers.empty else 'none'}` after requiring an unchanged trade path between 10 and 20 bps.",
            "- A larger historical dollar return is not enough if it reduces diversification, breaches the profit-concentration gate, or fails one period. "
            "No sizing parameter is changed before genuine forward evidence.",
        ]
    )
    (RESULTS / "position_sizing_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, symbols = MODULE["load_panels"]()
    last_date = panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1]
    metrics = evaluate(panels, symbols, last_date)
    path_stability = execution_path_stability(panels, symbols, last_date)
    metrics.to_csv(RESULTS / "position_sizing_metrics.csv", index=False)
    path_stability.to_csv(RESULTS / "position_sizing_execution_paths.csv", index=False)
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_end": str(last_date.date()),
        "research_only": True,
        "authorizes_trade": False,
        "initial_nav": MODULE["INITIAL_NAV"],
        "weights": WEIGHTS,
        "frozen_weight": 0.08,
    }
    (RESULTS / "position_sizing_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_report(metrics, path_stability)
    print(RESULTS / "position_sizing_report.md")


if __name__ == "__main__":
    main()
