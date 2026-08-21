#!/usr/bin/env python3
"""Ablate ATR and close-location filters and test fixed-watchlist robustness."""
from __future__ import annotations

import json
import runpy
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
RESULTS = HERE / "results"
COMMON = dict(
    rs20_min=0.03,
    volume_ratio_min=1.20,
    max_extension=0.12,
    max_hold_days=20,
    stop_loss=0.08,
)
VARIANTS = {
    "matched_baseline": MODULE["Config"](**COMMON, max_atr_pct=1.00, min_close_location=0.00),
    "atr_only": MODULE["Config"](**COMMON, max_atr_pct=0.04, min_close_location=0.00),
    "close_location_only": MODULE["Config"](**COMMON, max_atr_pct=1.00, min_close_location=0.50),
    "combined": MODULE["Config"](**COMMON, max_atr_pct=0.04, min_close_location=0.50),
}


def periods(last_date: pd.Timestamp) -> dict[str, tuple[str, str]]:
    return {
        "2024": ("2024-01-02", "2024-12-31"),
        "2025": ("2025-01-01", "2025-12-31"),
        "2026": ("2026-01-01", str(last_date.date())),
        "train_2024_2025": ("2024-01-02", "2025-12-31"),
        "full": ("2024-01-02", str(last_date.date())),
    }


def run_ablation(panels, symbols, last_date):
    rows = []
    results = {}
    for period_name, interval in periods(last_date).items():
        results[period_name] = {}
        for cost_bps in (10, 20):
            for name, config in VARIANTS.items():
                result = MODULE["simulate"](
                    panels,
                    symbols,
                    config,
                    "strict_veto",
                    *interval,
                    slippage=cost_bps / 10_000,
                )
                results[period_name][f"{name}_{cost_bps}bps"] = result
                rows.append(
                    {
                        "period": period_name,
                        "cost_bps": cost_bps,
                        "variant": name,
                        **result["metrics"],
                    }
                )
    return pd.DataFrame(rows), results


def parameter_grid(panels, symbols, last_date) -> pd.DataFrame:
    rows = []
    grid = [
        (atr, location)
        for atr in (0.03, 0.04, 0.05, 0.06, 1.00)
        for location in (0.00, 0.25, 0.50, 0.75)
    ]
    baseline_cache = {}
    for period_name in ("train_2024_2025", "2026"):
        interval = periods(last_date)[period_name]
        baseline_cache[period_name] = MODULE["simulate"](
            panels,
            symbols,
            VARIANTS["matched_baseline"],
            "strict_veto",
            *interval,
            slippage=0.001,
        )["metrics"]
        for atr, location in grid:
            config = MODULE["Config"](
                **COMMON,
                max_atr_pct=atr,
                min_close_location=location,
            )
            metrics = MODULE["simulate"](
                panels,
                symbols,
                config,
                "strict_veto",
                *interval,
                slippage=0.001,
            )["metrics"]
            base = baseline_cache[period_name]
            rows.append(
                {
                    "period": period_name,
                    "atr_cap": atr,
                    "close_location_floor": location,
                    **metrics,
                    "return_delta": metrics["total_return"] - base["total_return"],
                    "drawdown_delta": metrics["max_drawdown"] - base["max_drawdown"],
                    "sharpe_delta": metrics["sharpe"] - base["sharpe"],
                    "win_rate_delta": (
                        metrics["win_rate"] - base["win_rate"]
                        if metrics["win_rate"] is not None and base["win_rate"] is not None
                        else np.nan
                    ),
                }
            )
    return pd.DataFrame(rows)


def leave_one_symbol_out(panels, symbols, last_date) -> pd.DataFrame:
    rows = []
    interval = periods(last_date)["full"]
    for omitted in symbols:
        reduced = [symbol for symbol in symbols if symbol != omitted]
        baseline = MODULE["simulate"](
            panels,
            reduced,
            VARIANTS["matched_baseline"],
            "strict_veto",
            *interval,
            slippage=0.001,
        )["metrics"]
        candidate = MODULE["simulate"](
            panels,
            reduced,
            VARIANTS["combined"],
            "strict_veto",
            *interval,
            slippage=0.001,
        )["metrics"]
        rows.append(
            {
                "omitted_symbol": omitted,
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
            }
        )
    return pd.DataFrame(rows)


def exit_stability(panels, symbols, last_date) -> pd.DataFrame:
    rows = []
    entry_common = dict(rs20_min=0.03, volume_ratio_min=1.20, max_extension=0.12)
    for period_name in ("train_2024_2025", "2026"):
        interval = periods(last_date)[period_name]
        for stop_loss in (0.06, 0.08, 0.10):
            for max_hold_days in (10, 20, 30):
                baseline_config = MODULE["Config"](
                    **entry_common,
                    stop_loss=stop_loss,
                    max_hold_days=max_hold_days,
                    max_atr_pct=1.00,
                    min_close_location=0.00,
                )
                candidate_config = MODULE["Config"](
                    **entry_common,
                    stop_loss=stop_loss,
                    max_hold_days=max_hold_days,
                    max_atr_pct=0.04,
                    min_close_location=0.50,
                )
                baseline = MODULE["simulate"](
                    panels, symbols, baseline_config, "strict_veto", *interval, slippage=0.001
                )["metrics"]
                candidate = MODULE["simulate"](
                    panels, symbols, candidate_config, "strict_veto", *interval, slippage=0.001
                )["metrics"]
                rows.append(
                    {
                        "period": period_name,
                        "stop_loss": stop_loss,
                        "max_hold_days": max_hold_days,
                        "baseline_return": baseline["total_return"],
                        "candidate_return": candidate["total_return"],
                        "return_delta": candidate["total_return"] - baseline["total_return"],
                        "drawdown_delta": candidate["max_drawdown"] - baseline["max_drawdown"],
                        "sharpe_delta": candidate["sharpe"] - baseline["sharpe"],
                        "win_rate_delta": (
                            candidate["win_rate"] - baseline["win_rate"]
                            if candidate["win_rate"] is not None and baseline["win_rate"] is not None
                            else np.nan
                        ),
                        "baseline_trades": baseline["trade_count"],
                        "candidate_trades": candidate["trade_count"],
                    }
                )
    return pd.DataFrame(rows)


def paired_block_bootstrap(
    baseline_equity: dict[str, float],
    candidate_equity: dict[str, float],
    samples: int = 5_000,
    block: int = 20,
    seed: int = 20260815,
) -> dict[str, float]:
    baseline = pd.Series(baseline_equity, dtype=float)
    candidate = pd.Series(candidate_equity, dtype=float)
    baseline.index = pd.to_datetime(baseline.index)
    candidate.index = pd.to_datetime(candidate.index)
    frame = pd.concat(
        [baseline.pct_change().rename("baseline"), candidate.pct_change().rename("candidate")],
        axis=1,
    ).dropna()
    values = frame.to_numpy()
    count = len(values)
    rng = np.random.default_rng(seed)
    deltas = np.empty(samples)
    drawdown_better = np.empty(samples, dtype=bool)
    for sample_id in range(samples):
        sampled = []
        while sum(len(part) for part in sampled) < count:
            start = int(rng.integers(0, max(count - block + 1, 1)))
            sampled.append(values[start : min(start + block, count)])
        path = np.concatenate(sampled, axis=0)[:count]
        base_nav = np.cumprod(1.0 + path[:, 0])
        candidate_nav = np.cumprod(1.0 + path[:, 1])
        deltas[sample_id] = candidate_nav[-1] - base_nav[-1]
        base_dd = np.min(base_nav / np.maximum.accumulate(base_nav) - 1.0)
        candidate_dd = np.min(candidate_nav / np.maximum.accumulate(candidate_nav) - 1.0)
        drawdown_better[sample_id] = candidate_dd >= base_dd
    return {
        "samples": float(samples),
        "block_sessions": float(block),
        "probability_higher_return": float((deltas > 0).mean()),
        "probability_better_drawdown": float(drawdown_better.mean()),
        "median_return_delta": float(np.median(deltas)),
        "return_delta_p05": float(np.quantile(deltas, 0.05)),
        "return_delta_p95": float(np.quantile(deltas, 0.95)),
    }


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2%}"


def num(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2f}"


def write_report(metrics, grid, leave_one_out, exits, bootstrap):
    lines = [
        "# Exact-filter ablation and robustness",
        "",
        "## Boundary",
        "",
        "All variants use the same fixed current watchlist, broad/theme gates, RS20 3%, volume, extension, cooldown, sizing, stop and hold rules. "
        "Only ATR and signal-day close-location filters change. This is post-hoc, survivorship-biased research and cannot authorize a trade.",
        "",
        "## Ten-basis-point ablation",
        "",
        "| Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Profit factor |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in metrics.loc[metrics["cost_bps"] == 10].itertuples(index=False):
        lines.append(
            f"| {row.period} | {row.variant} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
            f"{num(row.sharpe)} | {pct(row.win_rate)} | {row.trade_count} | {num(row.profit_factor)} |"
        )
    lines.extend(
        [
            "",
            "## Full-period cost sensitivity",
            "",
            "| Cost | Variant | Return | Max DD | Sharpe | Win rate |",
            "| ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in metrics.loc[metrics["period"] == "full"].itertuples(index=False):
        lines.append(
            f"| {row.cost_bps} bps | {row.variant} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
            f"{num(row.sharpe)} | {pct(row.win_rate)} |"
        )

    frozen_grid = grid.loc[(grid["atr_cap"] == 0.04) & (grid["close_location_floor"] == 0.50)]
    grid_summary = (
        grid.groupby(["atr_cap", "close_location_floor"])
        .agg(
            positive_return_delta_rate=("return_delta", lambda values: (values > 0).mean()),
            positive_sharpe_delta_rate=("sharpe_delta", lambda values: (values > 0).mean()),
            nonworse_drawdown_rate=("drawdown_delta", lambda values: (values >= 0).mean()),
            positive_win_delta_rate=("win_rate_delta", lambda values: (values > 0).mean()),
        )
        .reset_index()
    )
    trade_counts = grid.pivot_table(
        index=["atr_cap", "close_location_floor"], columns="period", values="trade_count", aggfunc="first"
    ).reset_index()
    grid_summary = grid_summary.merge(trade_counts, on=["atr_cap", "close_location_floor"], how="left")
    grid_summary["minimum_sample"] = (
        (grid_summary["train_2024_2025"] >= 10) & (grid_summary["2026"] >= 4)
    )
    robust_cells = grid_summary.loc[
        (grid_summary["positive_return_delta_rate"] == 1.0)
        & (grid_summary["positive_sharpe_delta_rate"] == 1.0)
        & (grid_summary["nonworse_drawdown_rate"] == 1.0)
    ]
    robust_sampled_cells = robust_cells.loc[robust_cells["minimum_sample"]]
    loo = {
        "runs": len(leave_one_out),
        "return_better": (leave_one_out["return_delta"] > 0).mean(),
        "drawdown_better": (leave_one_out["drawdown_delta"] >= 0).mean(),
        "sharpe_better": (leave_one_out["sharpe_delta"] > 0).mean(),
        "win_better": (leave_one_out["win_rate_delta"] > 0).mean(),
        "min_return_delta": leave_one_out["return_delta"].min(),
        "max_return_delta": leave_one_out["return_delta"].max(),
    }
    exit_summary = (
        exits.groupby(["stop_loss", "max_hold_days"])
        .agg(
            return_better=("return_delta", lambda values: (values > 0).all()),
            drawdown_better=("drawdown_delta", lambda values: (values >= 0).all()),
            sharpe_better=("sharpe_delta", lambda values: (values > 0).all()),
            win_better=("win_rate_delta", lambda values: (values > 0).all()),
            min_return_delta=("return_delta", "min"),
        )
        .reset_index()
    )
    stable_exit_cells = exit_summary.loc[
        exit_summary["return_better"] & exit_summary["drawdown_better"] & exit_summary["sharpe_better"]
    ]
    lines.extend(
        [
            "",
            "## Parameter and concentration robustness",
            "",
            f"- Frozen 4%/50% cell beats the unfiltered baseline in both 2024-2025 and 2026 on return, Sharpe and drawdown: "
            f"`{bool((frozen_grid['return_delta'] > 0).all() and (frozen_grid['sharpe_delta'] > 0).all() and (frozen_grid['drawdown_delta'] >= 0).all())}`.",
            f"- Raw grid cells beating baseline on return, Sharpe and drawdown in both periods: `{len(robust_cells)}/{len(grid_summary)}`.",
            f"- After a lenient anti-cash screen of at least 10 training and 4 test trades: `{len(robust_sampled_cells)}/{len(grid_summary)}`. "
            "This is still far below the promotion sample gate.",
            f"- Across {loo['runs']} leave-one-symbol-out runs, combined beats baseline on return in {loo['return_better']:.1%}, "
            f"drawdown in {loo['drawdown_better']:.1%}, Sharpe in {loo['sharpe_better']:.1%}, and win rate in {loo['win_better']:.1%}.",
            f"- Leave-one-symbol-out return delta range: {loo['min_return_delta']:+.2%} to {loo['max_return_delta']:+.2%}.",
            f"- Across stop-loss 6%/8%/10% and maximum-hold 10/20/30 combinations, the filter beats its paired baseline on return, "
            f"Sharpe and drawdown in both periods for `{len(stable_exit_cells)}/{len(exit_summary)}` exit cells.",
            "",
            "## Paired 20-session block bootstrap",
            "",
            "| Period | P(candidate return > baseline) | P(candidate DD better) | Median delta | 5%-95% delta |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for period_name, stats in bootstrap.items():
        lines.append(
            f"| {period_name} | {stats['probability_higher_return']:.1%} | {stats['probability_better_drawdown']:.1%} | "
            f"{stats['median_return_delta']:+.2%} | {stats['return_delta_p05']:+.2%} to {stats['return_delta_p95']:+.2%} |"
        )
    lines.extend(
        [
            "",
            "The bootstrap resamples paired realized return blocks from the same post-hoc sample. It describes path consistency; it is not an out-of-sample p-value and cannot cure watchlist selection bias.",
            "",
            "## Decision rule",
            "",
            "Ablation can identify the likely contributor but cannot promote it. The frozen combined RSR1 shadow remains unchanged. "
            "If ATR-only dominates combined across both held-out behavior and parameter neighbors, that finding may seed a separately versioned future challenger only after RSR1 has accumulated genuine forward evidence.",
            "",
            "The follow-up family-wise selection-bias audit is in `selection_bias_audit_report.md`. It finds supportive but non-decisive "
            "structure (PBO 13.1%, family-wise p=0.063) and fails the immutable 7/10 chronological-block stability gates. "
            "This supersedes any interpretation that 17/20 successful raw grid cells alone establishes an independent edge.",
        ]
    )
    (RESULTS / "risk_filter_ablation_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, symbols = MODULE["load_panels"]()
    last_date = panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1]
    metrics, results = run_ablation(panels, symbols, last_date)
    grid = parameter_grid(panels, symbols, last_date)
    leave_one_out = leave_one_symbol_out(panels, symbols, last_date)
    exits = exit_stability(panels, symbols, last_date)
    bootstrap = {}
    for period_name in ("train_2024_2025", "2026", "full"):
        base = results[period_name]["matched_baseline_10bps"]
        candidate = results[period_name]["combined_10bps"]
        bootstrap[period_name] = paired_block_bootstrap(base["equity"], candidate["equity"])
    metrics.to_csv(RESULTS / "risk_filter_ablation_metrics.csv", index=False)
    grid.to_csv(RESULTS / "risk_filter_parameter_grid.csv", index=False)
    leave_one_out.to_csv(RESULTS / "risk_filter_leave_one_symbol_out.csv", index=False)
    exits.to_csv(RESULTS / "risk_filter_exit_stability.csv", index=False)
    with (RESULTS / "risk_filter_ablation_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
                "data_end": str(last_date.date()),
                "research_only": True,
                "authorizes_trade": False,
                "variants": {name: asdict(config) for name, config in VARIANTS.items()},
                "bootstrap": bootstrap,
            },
            handle,
            indent=2,
        )
    write_report(metrics, grid, leave_one_out, exits, bootstrap)
    print(RESULTS / "risk_filter_ablation_report.md")


if __name__ == "__main__":
    main()
