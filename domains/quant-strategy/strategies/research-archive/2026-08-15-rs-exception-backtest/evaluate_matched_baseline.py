#!/usr/bin/env python3
"""Compare the frozen risk filter with an otherwise identical strict baseline."""
from __future__ import annotations

import json
import runpy
from dataclasses import asdict
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
RESULTS = HERE / "results"


def configs():
    common = dict(
        rs20_min=0.03,
        volume_ratio_min=1.20,
        max_extension=0.12,
        max_hold_days=20,
        stop_loss=0.08,
    )
    baseline = MODULE["Config"](**common, max_atr_pct=1.00, min_close_location=0.00)
    candidate = MODULE["Config"](**common, max_atr_pct=0.04, min_close_location=0.50)
    return baseline, candidate


def compact(result: dict) -> dict:
    return {"config": result["config"], **result["metrics"]}


def trade_group_stats(trades: list[dict]) -> dict:
    if not trades:
        return {"trades": 0, "win_rate": None, "average_return": None, "net_pnl": 0.0}
    return {
        "trades": len(trades),
        "win_rate": sum(trade["pnl"] > 0 for trade in trades) / len(trades),
        "average_return": sum(trade["return"] for trade in trades) / len(trades),
        "net_pnl": sum(trade["pnl"] for trade in trades),
    }


def compare_trade_paths(panels, symbols, baseline_result: dict, candidate_result: dict, candidate_config):
    key = lambda trade: (trade["signal_date"], trade["symbol"])
    baseline = {key(trade): trade for trade in baseline_result["trades"]}
    candidate = {key(trade): trade for trade in candidate_result["trades"]}
    candidate_features = MODULE["build_features"](panels, symbols, candidate_config)
    rows = []
    for trade_key, trade in baseline.items():
        if trade_key in candidate:
            group = "common"
            reasons = ""
        else:
            group = "baseline_only"
            date = pd.Timestamp(trade["signal_date"])
            symbol = trade["symbol"]
            atr = candidate_features["atr_pct"].at[date, symbol]
            location = candidate_features["close_location"].at[date, symbol]
            reason_parts = []
            if not pd.notna(atr) or atr > 0.04:
                reason_parts.append("atr_pct")
            if not pd.notna(location) or location < 0.50:
                reason_parts.append("close_location")
            reasons = "+".join(reason_parts) or "portfolio_path"
        rows.append({"group": group, "source_variant": "matched_baseline", "filter_reason": reasons, **trade})
    for trade_key, trade in candidate.items():
        if trade_key not in baseline:
            rows.append(
                {
                    "group": "candidate_only",
                    "source_variant": "risk_filter",
                    "filter_reason": "capacity_reallocation",
                    **trade,
                }
            )
    frame = pd.DataFrame(rows)
    summaries = {}
    for group in ("common", "baseline_only", "candidate_only"):
        sample = frame.loc[frame["group"] == group].to_dict("records")
        summaries[group] = trade_group_stats(sample)
    return frame, summaries


def pct(value) -> str:
    return "n/a" if value is None else f"{value:.2%}"


def main() -> None:
    panels, symbols = MODULE["load_panels"]()
    last_date = panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1]
    periods = {
        "2024": ("2024-01-02", "2024-12-31"),
        "2025": ("2025-01-01", "2025-12-31"),
        "2026": ("2026-01-01", str(last_date.date())),
        "train_2024_2025": ("2024-01-02", "2025-12-31"),
        "full": ("2024-01-02", str(last_date.date())),
    }
    baseline, candidate = configs()
    runs = {}
    rows = []
    full_results = {}
    for period_name, period in periods.items():
        runs[period_name] = {}
        for name, config in (("matched_baseline", baseline), ("risk_filter", candidate)):
            result = MODULE["simulate"](panels, symbols, config, "strict_veto", *period)
            runs[period_name][name] = compact(result)
            rows.append({"period": period_name, "variant": name, **result["metrics"]})
            if period_name == "full":
                full_results[name] = result
    trade_paths, path_summary = compare_trade_paths(
        panels, symbols, full_results["matched_baseline"], full_results["risk_filter"], candidate
    )
    baseline_only = trade_paths.loc[trade_paths["group"] == "baseline_only"]
    reason_summary = (
        baseline_only.groupby("filter_reason", dropna=False)
        .agg(
            trades=("return", "size"),
            win_rate=("return", lambda values: (values > 0).mean()),
            average_return=("return", "mean"),
            net_pnl=("pnl", "sum"),
        )
        .reset_index()
        .sort_values("net_pnl")
    )
    output = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_end": str(last_date.date()),
        "research_only": True,
        "authorizes_trade": False,
        "comparison_isolation": "ATR cap and close-location floor only",
        "matched_baseline": asdict(baseline),
        "risk_filter": asdict(candidate),
        "trade_path_summary": path_summary,
        "baseline_only_reason_summary": reason_summary.to_dict("records"),
        "runs": runs,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "matched_baseline.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    pd.DataFrame(rows).to_csv(RESULTS / "matched_baseline_metrics.csv", index=False)
    trade_paths.to_csv(RESULTS / "matched_baseline_trade_paths.csv", index=False)
    reason_summary.to_csv(RESULTS / "matched_baseline_filter_reasons.csv", index=False)

    lines = [
        "# Matched-baseline risk-filter comparison",
        "",
        "This corrects the earlier attribution problem: both variants use the same 3% RS20 minimum, volume, extension, hold and stop settings. "
        "They differ only in `ATR14/close <= 4%` and signal-day close location >= 50%.",
        "",
        "| Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Profit factor |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        pf = "n/a" if row["profit_factor"] is None else f"{row['profit_factor']:.2f}"
        lines.append(
            f"| {row['period']} | {row['variant']} | {pct(row['total_return'])} | {pct(row['max_drawdown'])} | "
            f"{row['sharpe']:.2f} | {pct(row['win_rate'])} | {row['trade_count']} | {pf} |"
        )
    lines.extend(
        [
            "",
            "## Full-period trade-path decomposition",
            "",
            "| Group | Trades | Win rate | Average return | Net P&L |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for group in ("common", "baseline_only", "candidate_only"):
        stats = path_summary[group]
        lines.append(
            f"| {group} | {stats['trades']} | {pct(stats['win_rate'])} | {pct(stats['average_return'])} | "
            f"${stats['net_pnl']:.2f} |"
        )
    lines.extend(
        [
            "",
            "`baseline_only` measures trades absent from the candidate path, usually because ATR/close location rejected them. "
            "`candidate_only` measures replacement opportunities made possible by the changed portfolio path; it must not be attributed solely to the filter.",
            "",
            "| Baseline-only reason | Trades | Win rate | Average return | Net P&L |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in reason_summary.itertuples(index=False):
        lines.append(
            f"| {row.filter_reason} | {row.trades} | {pct(row.win_rate)} | {pct(row.average_return)} | ${row.net_pnl:.2f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "On the fixed current watchlist, the exact filter looks materially better than its matched baseline in 2024, 2025 and 2026 YTD. "
            "This strengthens the case for the already-frozen forward shadow, but does not override the broader point-in-time proxy result, "
            "the watchlist survivorship bias, or the minimum 126-session/20-closed-trade promotion gate.",
        ]
    )
    (RESULTS / "matched_baseline_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(RESULTS / "matched_baseline_report.md")


if __name__ == "__main__":
    main()
