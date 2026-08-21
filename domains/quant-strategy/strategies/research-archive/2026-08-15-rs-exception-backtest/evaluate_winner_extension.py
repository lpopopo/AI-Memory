#!/usr/bin/env python3
"""Evaluate conditional winner extensions on top of frozen RSR2."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE_MODULE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
RESULTS = HERE / "results"
VARIANTS = {
    "rsr2_frozen": (None, 0.0),
    "extend30_any_winner": (30, 0.0),
    "extend30_gain8": (30, 0.08),
    "extend40_gain8": (40, 0.08),
}
PERIODS = {
    "train_2024_2025": ("2024-01-02", "2025-12-31"),
    "retrospective_2026": ("2026-01-02", "2026-08-07"),
    "full": ("2024-01-02", "2026-08-07"),
}


def concentration(trades: list[dict]) -> float:
    wins = [trade for trade in trades if trade.get("pnl") is not None and trade["pnl"] > 0]
    if not wins:
        return np.nan
    by_symbol = pd.DataFrame(wins).groupby("symbol")["pnl"].sum()
    return float(by_symbol.max() / by_symbol.sum())


def evaluate(panels, symbols):
    rows = []
    runs = {}
    for name, (days, minimum_return) in VARIANTS.items():
        for period, (start, end) in PERIODS.items():
            for bps in ((10, 20) if period == "full" else (10,)):
                result = MODULE["simulate"](
                    panels,
                    symbols,
                    UNIVERSE_MODULE["make_config"](True),
                    "strict_veto",
                    start,
                    end,
                    slippage=bps / 10_000,
                    profit_lock_trigger=0.15,
                    profit_lock_floor=0.05,
                    winner_extension_days=days,
                    winner_extension_min_return=minimum_return,
                )
                runs[(name, period, bps)] = result
                rows.append(
                    {
                        "variant": name,
                        "extension_days": days,
                        "minimum_return": minimum_return,
                        "period": period,
                        "cost_bps": bps,
                        **result["metrics"],
                        "gross_profit_concentration": concentration(result["trades"]),
                    }
                )
    return pd.DataFrame(rows), runs


def screen(metrics: pd.DataFrame) -> pd.DataFrame:
    base = metrics.loc[metrics["variant"].eq("rsr2_frozen")].set_index(["period", "cost_bps"])
    rows = []
    return_improvers = 0
    for variant in VARIANTS:
        if variant == "rsr2_frozen":
            continue
        sample = metrics.loc[metrics["variant"].eq(variant)].set_index(["period", "cost_bps"])
        checks = {}
        for period in ("train_2024_2025", "retrospective_2026"):
            for field in ("total_return", "max_drawdown", "sharpe", "win_rate"):
                checks[f"{period}_{field}_nonworse"] = bool(
                    sample.at[(period, 10), field] >= base.at[(period, 10), field] - 1e-12
                )
        checks["full_20bps_return_nonworse"] = bool(
            sample.at[("full", 20), "total_return"] >= base.at[("full", 20), "total_return"] - 1e-12
        )
        checks["concentration_le_35"] = bool(
            sample.at[("full", 10), "gross_profit_concentration"] <= 0.35
        )
        improves_both = all(
            sample.at[(period, 10), "total_return"] > base.at[(period, 10), "total_return"] + 1e-12
            for period in ("train_2024_2025", "retrospective_2026")
        )
        return_improvers += int(improves_both)
        rows.append({"variant": variant, **checks, "return_improves_both": improves_both})
    result = pd.DataFrame(rows)
    result["two_of_three_return_improve_both"] = return_improvers >= 2
    result["passes_all"] = result.apply(
        lambda row: all(bool(row[column]) for column in result.columns if column != "variant"), axis=1
    )
    return result


def pct(value) -> str:
    return "n/a" if pd.isna(value) else f"{value:.2%}"


def write_report(metrics: pd.DataFrame, screened: pd.DataFrame, summary: dict) -> None:
    central = metrics.loc[metrics["variant"].isin(["rsr2_frozen", "extend30_gain8"]) & metrics["cost_bps"].eq(10)]
    lines = [
        "# RSR2 conditional winner-extension audit",
        "",
        "## Scope",
        "",
        "This post-hoc study changes only the maximum holding period for positions that remain profitable, above MA20 and non-negative in RS20 at the frozen 20-session deadline. RSR2 profit protection and every entry, sizing, cost and risk rule remain unchanged.",
        "",
        "## Frozen versus central",
        "",
        "| Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Profit concentration |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in central.itertuples(index=False):
        lines.append(
            f"| {row.period} | {row.variant} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
            f"{row.sharpe:.2f} | {pct(row.win_rate)} | {row.trade_count} | {pct(row.gross_profit_concentration)} |"
        )
    lines.extend(["", "## Screen", "", screened.to_markdown(index=False), "", "## Decision", ""])
    lines.append(summary["decision_explanation"])
    (RESULTS / "winner_extension_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, all_symbols = MODULE["load_panels"]()
    universes, _ = UNIVERSE_MODULE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    metrics, runs = evaluate(panels, symbols)
    screened = screen(metrics)
    central_passes = bool(screened.loc[screened["variant"].eq("extend30_gain8"), "passes_all"].iloc[0])
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "research_only": True,
        "authorizes_trade": False,
        "central_passes": central_passes,
        "passing_variants": screened.loc[screened["passes_all"], "variant"].tolist(),
        "decision": "forward_shadow_candidate_only" if central_passes else "reject_conditional_extension_keep_rsr2_frozen",
        "decision_explanation": (
            "The central extension passes the retrospective screen but remains a separately versioned forward-shadow candidate; frozen RSR2 is unchanged."
            if central_passes
            else "The central extension fails the preregistered cross-period screen. Keep frozen RSR2 and do not optimize further on this history."
        ),
    }
    metrics.to_csv(RESULTS / "winner_extension_metrics.csv", index=False)
    screened.to_csv(RESULTS / "winner_extension_screen.csv", index=False)
    trade_rows = []
    for (variant, period, bps), result in runs.items():
        for trade in result["trades"]:
            trade_rows.append({"variant": variant, "period": period, "cost_bps": bps, **trade})
    pd.DataFrame(trade_rows).to_csv(RESULTS / "winner_extension_trades.csv", index=False)
    (RESULTS / "winner_extension_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(metrics, screened, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
