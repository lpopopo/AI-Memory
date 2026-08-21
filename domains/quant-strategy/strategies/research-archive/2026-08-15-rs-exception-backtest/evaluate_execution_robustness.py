#!/usr/bin/env python3
"""Test signal-to-open latency and next-open gap sensitivity."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
RESULTS = HERE / "results"
DELAYS = (1, 2, 3)
GAP_CAPS = (0.03, 0.05, 0.10, 1.00)
COMMON = dict(
    rs20_min=0.03,
    volume_ratio_min=1.20,
    max_extension=0.12,
    max_hold_days=20,
    stop_loss=0.08,
    normal_target_weight=0.08,
)


def config(filtered: bool, delay: int, gap_cap: float):
    return MODULE["Config"](
        **COMMON,
        max_atr_pct=0.04 if filtered else 1.00,
        min_close_location=0.50 if filtered else 0.00,
        entry_delay_sessions=delay,
        max_entry_gap=gap_cap,
    )


def evaluate(panels, symbols, last_date):
    intervals = {
        "train_2024_2025": ("2024-01-02", "2025-12-31"),
        "2026": ("2026-01-01", str(last_date.date())),
        "full": ("2024-01-02", str(last_date.date())),
    }
    rows = []
    frozen_result = None
    for period_name, interval in intervals.items():
        for delay in DELAYS:
            for gap_cap in GAP_CAPS:
                pair = {}
                for filtered in (False, True):
                    name = "risk_filter" if filtered else "matched_baseline"
                    result = MODULE["simulate"](
                        panels,
                        symbols,
                        config(filtered, delay, gap_cap),
                        "strict_veto",
                        *interval,
                        slippage=0.001,
                    )
                    pair[name] = result
                    if period_name == "full" and delay == 1 and gap_cap == 1.00 and filtered:
                        frozen_result = result
                baseline = pair["matched_baseline"]["metrics"]
                candidate = pair["risk_filter"]["metrics"]
                rows.append(
                    {
                        "period": period_name,
                        "entry_delay_sessions": delay,
                        "max_entry_gap": gap_cap,
                        "baseline_return": baseline["total_return"],
                        "candidate_return": candidate["total_return"],
                        "return_delta": candidate["total_return"] - baseline["total_return"],
                        "baseline_drawdown": baseline["max_drawdown"],
                        "candidate_drawdown": candidate["max_drawdown"],
                        "drawdown_delta": candidate["max_drawdown"] - baseline["max_drawdown"],
                        "baseline_sharpe": baseline["sharpe"],
                        "candidate_sharpe": candidate["sharpe"],
                        "sharpe_delta": candidate["sharpe"] - baseline["sharpe"],
                        "baseline_win_rate": baseline["win_rate"],
                        "candidate_win_rate": candidate["win_rate"],
                        "win_rate_delta": (
                            candidate["win_rate"] - baseline["win_rate"]
                            if candidate["win_rate"] is not None and baseline["win_rate"] is not None
                            else np.nan
                        ),
                        "baseline_trades": baseline["trade_count"],
                        "candidate_trades": candidate["trade_count"],
                        "candidate_exposure": candidate["exposure"],
                    }
                )
    return pd.DataFrame(rows), frozen_result


def gap_attribution(frozen_result: dict) -> pd.DataFrame:
    trades = pd.DataFrame(frozen_result["trades"])
    bins = [-np.inf, 0.0, 0.03, 0.05, 0.10, np.inf]
    labels = ["<=0%", "0-3%", "3-5%", "5-10%", ">10%"]
    trades["gap_bucket"] = pd.cut(trades["entry_gap"], bins=bins, labels=labels, right=True)
    return (
        trades.groupby("gap_bucket", observed=False)
        .agg(
            trades=("return", "size"),
            win_rate=("return", lambda values: (values > 0).mean() if len(values) else np.nan),
            average_return=("return", "mean"),
            net_pnl=("pnl", "sum"),
            max_gap=("entry_gap", "max"),
        )
        .reset_index()
    )


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2%}"


def num(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2f}"


def write_report(metrics: pd.DataFrame, gaps: pd.DataFrame):
    full = metrics.loc[metrics["period"] == "full"]
    paired = metrics.loc[metrics["period"].isin(["train_2024_2025", "2026"])]
    cell_summary = (
        paired.groupby(["entry_delay_sessions", "max_entry_gap"])
        .agg(
            return_better=("return_delta", lambda values: (values > 0).all()),
            drawdown_better=("drawdown_delta", lambda values: (values >= 0).all()),
            sharpe_better=("sharpe_delta", lambda values: (values > 0).all()),
            win_better=("win_rate_delta", lambda values: (values > 0).all()),
            minimum_candidate_trades=("candidate_trades", "min"),
        )
        .reset_index()
    )
    stable = cell_summary.loc[
        cell_summary["return_better"] & cell_summary["drawdown_better"] & cell_summary["sharpe_better"]
    ]
    sampled = stable.loc[stable["minimum_candidate_trades"] >= 4]
    frozen = full.loc[(full["entry_delay_sessions"] == 1) & (full["max_entry_gap"] == 1.00)].iloc[0]
    delayed = full.loc[full["max_entry_gap"] == 1.00].sort_values("entry_delay_sessions")

    lines = [
        "# Signal-to-execution robustness",
        "",
        "## Boundary",
        "",
        "Signals remain completed-close only. Delay 1 is the frozen next-open execution; delays 2 and 3 intentionally execute the original signal later without hindsight. Gap caps reject a planned order when its eventual open is too far above the original signal close. "
        "This is fixed-watchlist post-hoc research and cannot alter RSR1 or authorize a trade.",
        "",
        "## Full-period candidate grid",
        "",
        "| Delay | Gap cap | Return | Max DD | Sharpe | Win rate | Trades | Exposure | Filter return delta |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in full.sort_values(["entry_delay_sessions", "max_entry_gap"]).itertuples(index=False):
        cap = "none" if row.max_entry_gap >= 1.0 else pct(row.max_entry_gap)
        lines.append(
            f"| {row.entry_delay_sessions} | {cap} | {pct(row.candidate_return)} | {pct(row.candidate_drawdown)} | "
            f"{num(row.candidate_sharpe)} | {pct(row.candidate_win_rate)} | {row.candidate_trades} | "
            f"{pct(row.candidate_exposure)} | {row.return_delta:+.2%} |"
        )
    lines.extend(
        [
            "",
            "## Frozen-trade next-open gap attribution",
            "",
            "| Entry gap | Trades | Win rate | Average return | Net P&L | Max gap |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in gaps.itertuples(index=False):
        lines.append(
            f"| {row.gap_bucket} | {row.trades} | {pct(row.win_rate)} | {pct(row.average_return)} | "
            f"${row.net_pnl:.2f} | {pct(row.max_gap)} |"
        )
    lines.extend(
        [
            "",
            "## Robustness screen",
            "",
            f"- Cells improving paired baseline return, Sharpe and drawdown in both training and 2026: `{len(stable)}/{len(cell_summary)}`.",
            f"- Same result after requiring at least four candidate trades in each period: `{len(sampled)}/{len(cell_summary)}`.",
            f"- Frozen next-open/no-gap-cap full result: return {frozen.candidate_return:.2%}, max DD {frozen.candidate_drawdown:.2%}, Sharpe {frozen.candidate_sharpe:.2f}.",
            "- No new gap threshold is selected from this retrospective grid. A cap that looks better mainly by deleting trades is not evidence of executable alpha.",
            "",
            "## Delay-only path",
            "",
            "| Delay | Return | Max DD | Sharpe | Win rate | Trades |",
            "| ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in delayed.itertuples(index=False):
        lines.append(
            f"| {row.entry_delay_sessions} | {pct(row.candidate_return)} | {pct(row.candidate_drawdown)} | "
            f"{num(row.candidate_sharpe)} | {pct(row.candidate_win_rate)} | {row.candidate_trades} |"
        )
    (RESULTS / "execution_robustness_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, symbols = MODULE["load_panels"]()
    last_date = panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1]
    metrics, frozen_result = evaluate(panels, symbols, last_date)
    gaps = gap_attribution(frozen_result)
    metrics.to_csv(RESULTS / "execution_robustness_metrics.csv", index=False)
    gaps.to_csv(RESULTS / "execution_gap_attribution.csv", index=False)
    (RESULTS / "execution_robustness_summary.json").write_text(
        json.dumps(
            {
                "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
                "data_end": str(last_date.date()),
                "research_only": True,
                "authorizes_trade": False,
                "frozen_delay_sessions": 1,
                "frozen_max_entry_gap": 1.0,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    write_report(metrics, gaps)
    print(RESULTS / "execution_robustness_report.md")


if __name__ == "__main__":
    main()
