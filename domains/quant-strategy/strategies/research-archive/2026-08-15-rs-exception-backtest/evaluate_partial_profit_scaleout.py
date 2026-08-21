#!/usr/bin/env python3
"""Evaluate one preregistered whole-share partial-profit overlay on RSR2."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
BACKTEST = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
RESULTS = HERE / "results"
VARIANTS = ("RSR2", "partial_half_at_15")
NAVS = (6_000.0, 5_751.77)
SLIPPAGES = (0.001, 0.002)
PERIODS = {
    "development_2024_2025": ("2024-01-02", "2025-12-31"),
    "heldout_2026": ("2026-01-02", None),
    "full": ("2024-01-02", None),
}


def profit_concentration(trades: list[dict]) -> dict:
    by_symbol: dict[str, float] = {}
    for trade in trades:
        pnl = trade.get("pnl")
        if pnl is not None and pnl > 0:
            by_symbol[trade["symbol"]] = by_symbol.get(trade["symbol"], 0.0) + float(pnl)
    gross = sum(by_symbol.values())
    return {
        "profitable_symbols": len(by_symbol),
        "top_symbol_profit_share": max(by_symbol.values(), default=0.0) / gross if gross else 1.0,
    }


def _cell(metrics: pd.DataFrame, variant: str, nav: float, period: str, slippage: float) -> pd.Series:
    match = metrics.loc[
        (metrics["variant_name"] == variant)
        & (metrics["initial_nav"] == nav)
        & (metrics["period_name"] == period)
        & (metrics["slippage"] == slippage)
    ]
    if len(match) != 1:
        raise RuntimeError(f"missing or duplicate partial-profit cell: {variant}/{nav}/{period}/{slippage}")
    return match.iloc[0]


def advancement_screen(metrics: pd.DataFrame) -> dict:
    return_deltas_10 = []
    return_deltas_20 = []
    sharpe_ok = []
    drawdown_ok = []
    win_rate_ok = []
    execution_ok = []
    diversification_ok = []
    for nav in NAVS:
        for period in ("development_2024_2025", "heldout_2026"):
            baseline10 = _cell(metrics, "RSR2", nav, period, 0.001)
            candidate10 = _cell(metrics, "partial_half_at_15", nav, period, 0.001)
            baseline20 = _cell(metrics, "RSR2", nav, period, 0.002)
            candidate20 = _cell(metrics, "partial_half_at_15", nav, period, 0.002)
            return_deltas_10.append(candidate10.total_return - baseline10.total_return)
            return_deltas_20.append(candidate20.total_return - baseline20.total_return)
            sharpe_ok.append(candidate10.sharpe + 1e-12 >= baseline10.sharpe)
            drawdown_ok.append(candidate10.max_drawdown + 0.01 + 1e-12 >= baseline10.max_drawdown)
            win_rate_ok.append(candidate10.win_rate + 1e-12 >= baseline10.win_rate)
            minimum = 5 if period == "development_2024_2025" else 2
            execution_ok.append(int(candidate10.partial_exits) >= minimum)
        full = _cell(metrics, "partial_half_at_15", nav, "full", 0.001)
        diversification_ok.append(
            int(full.profitable_symbols) >= 3
            and float(full.top_symbol_profit_share) <= 0.35 + 1e-12
        )
    checks = {
        "sufficient_partial_exits": all(execution_ok),
        "return_improves_10bps": all(delta > 1e-12 for delta in return_deltas_10),
        "sharpe_nonworse": all(sharpe_ok),
        "drawdown_within_1pp": all(drawdown_ok),
        "win_rate_nonworse": all(win_rate_ok),
        "return_improves_20bps": all(delta > 1e-12 for delta in return_deltas_20),
        "profit_diversified": all(diversification_ok),
    }
    passes = all(checks.values())
    return {
        **checks,
        "min_return_delta_10bps": min(return_deltas_10),
        "min_return_delta_20bps": min(return_deltas_20),
        "passes": passes,
        "status": "insufficient" if not checks["sufficient_partial_exits"] else "pass" if passes else "fail",
    }


def decompose_trade_paths(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    group_columns = ["initial_nav", "slippage", "period_name"]
    for keys, block in trades.groupby(group_columns, sort=True):
        baseline = block.loc[block["variant_name"] == "RSR2"].set_index(["symbol", "signal_date"])
        candidate = block.loc[block["variant_name"] == "partial_half_at_15"].set_index(
            ["symbol", "signal_date"]
        )
        all_keys = sorted(set(baseline.index) | set(candidate.index))
        for symbol, signal_date in all_keys:
            in_baseline = (symbol, signal_date) in baseline.index
            in_candidate = (symbol, signal_date) in candidate.index
            baseline_pnl = float(baseline.loc[(symbol, signal_date), "pnl"]) if in_baseline else 0.0
            candidate_pnl = float(candidate.loc[(symbol, signal_date), "pnl"]) if in_candidate else 0.0
            candidate_row = candidate.loc[(symbol, signal_date)] if in_candidate else None
            rows.append(
                {
                    **dict(zip(group_columns, keys)),
                    "symbol": symbol,
                    "signal_date": signal_date,
                    "group": "common" if in_baseline and in_candidate else "baseline_only" if in_baseline else "candidate_only",
                    "baseline_pnl": baseline_pnl,
                    "candidate_pnl": candidate_pnl,
                    "pnl_delta": candidate_pnl - baseline_pnl,
                    "partial_exit_status": (
                        candidate_row.get("partial_exit_status") if candidate_row is not None else None
                    ),
                }
            )
    return pd.DataFrame(rows)


def pct(value: float) -> str:
    return f"{value:.2%}"


def write_report(
    metrics: pd.DataFrame, decomposition: pd.DataFrame, screen: dict, summary: dict
) -> None:
    lines = [
        "# RSR2 whole-share partial-profit audit",
        "",
        "## Decision",
        "",
        f"- Result: `{summary['decision']}`.",
        f"- Advancement status: `{screen['status']}`.",
        "- One closed trade remains one trade after partial and final exits; partial sales cannot inflate hit rate.",
        "- Research only. No formal rule, order or existing forward ledger is changed.",
        "",
        "## Advancement screen",
        "",
        "| Check | Result |",
        "| --- | --- |",
    ]
    for key in (
        "sufficient_partial_exits",
        "return_improves_10bps",
        "sharpe_nonworse",
        "drawdown_within_1pp",
        "win_rate_nonworse",
        "return_improves_20bps",
        "profit_diversified",
    ):
        lines.append(f"| {key} | {screen[key]} |")
    lines.extend(
        [
            f"| minimum return delta at 10 bps | {pct(screen['min_return_delta_10bps'])} |",
            f"| minimum return delta at 20 bps | {pct(screen['min_return_delta_20bps'])} |",
            "",
            "## Ten-basis-point results",
            "",
            "| NAV | Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Partial exits | Ineligible | Top profit share |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in metrics.loc[metrics["slippage"] == 0.001].itertuples(index=False):
        lines.append(
            f"| ${row.initial_nav:,.2f} | {row.period_name} | {row.variant_name} | "
            f"{pct(row.total_return)} | {pct(row.max_drawdown)} | {row.sharpe:.2f} | "
            f"{pct(row.win_rate)} | {row.trade_count} | {row.partial_exits} | "
            f"{row.partial_ineligible} | {pct(row.top_symbol_profit_share)} |"
        )
    focus = decomposition.loc[
        (decomposition["initial_nav"] == 6_000.0)
        & (decomposition["slippage"] == 0.001)
        & (decomposition["period_name"] == "full")
    ].sort_values("pnl_delta")
    lines.extend(
        [
            "",
            "## Full-period P&L attribution at USD 6,000 / 10 bps",
            "",
            "| Symbol | Signal | Path | Baseline P&L | Partial P&L | Delta |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in focus.head(6).itertuples(index=False):
        lines.append(
            f"| {row.symbol} | {row.signal_date} | {row.group} | ${row.baseline_pnl:.2f} | "
            f"${row.candidate_pnl:.2f} | ${row.pnl_delta:.2f} |"
        )
    lines.extend(
        [
            "",
            f"- Common-trade P&L delta: `${focus.loc[focus['group'] == 'common', 'pnl_delta'].sum():.2f}`.",
            f"- Candidate-only P&L delta: `${focus.loc[focus['group'] == 'candidate_only', 'pnl_delta'].sum():.2f}`.",
            "- The largest losses come from trimming persistent right-tail winners; released capacity also admitted an additional losing trade.",
        ]
    )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "- The comparison uses the hindsight-selected current watchlist and previously observed periods. It can reject an operationally weak mechanism but cannot prove a live edge.",
            "- Whole-share feasibility and the extra commission are part of the mechanism, not implementation noise to remove after seeing the result.",
            "- See `../partial-profit-scaleout-preregistration.md` for the frozen design.",
        ]
    )
    (RESULTS / "partial_profit_scaleout_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    panels, all_symbols = BACKTEST["load_panels"]()
    universes, _ = UNIVERSE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    config = UNIVERSE["make_config"](True)
    last_date = panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1]
    rows = []
    trade_rows = []
    for nav in NAVS:
        for slippage in SLIPPAGES:
            for period_name, (start, configured_end) in PERIODS.items():
                end = configured_end or str(last_date.date())
                for variant_name in VARIANTS:
                    partial = variant_name == "partial_half_at_15"
                    result = BACKTEST["simulate"](
                        panels,
                        symbols,
                        config,
                        "strict_veto",
                        start,
                        end,
                        slippage=slippage,
                        commission=1.0,
                        profit_lock_trigger=0.15,
                        profit_lock_floor=0.05,
                        initial_nav=nav,
                        ranking_mode="formal_composite",
                        partial_profit_trigger=0.15 if partial else None,
                        partial_profit_fraction=0.50,
                        partial_profit_min_notional=200.0,
                    )
                    overlay = result["partial_profit_overlay"]
                    concentration = profit_concentration(result["trades"])
                    rows.append(
                        {
                            "initial_nav": nav,
                            "slippage": slippage,
                            "period_name": period_name,
                            "variant_name": variant_name,
                            **result["metrics"],
                            "partial_exits": overlay["executed"],
                            "partial_ineligible": overlay["ineligible"],
                            **concentration,
                        }
                    )
                    for trade in result["trades"]:
                        trade_rows.append(
                            {
                                "initial_nav": nav,
                                "slippage": slippage,
                                "period_name": period_name,
                                "variant_name": variant_name,
                                **trade,
                            }
                        )
    metrics = pd.DataFrame(rows)
    trades = pd.DataFrame(trade_rows)
    decomposition = decompose_trade_paths(trades)
    screen = advancement_screen(metrics)
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_end": str(last_date.date()),
        "universe": "ai_capex_broad",
        "universe_size": len(symbols),
        "research_only": True,
        "authorizes_trade": False,
        "decision": "advance_new_partial_profit_shadow" if screen["passes"] else "retain_RSR2_without_partial_exit",
        "screen": screen,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(RESULTS / "partial_profit_scaleout_metrics.csv", index=False)
    trades.to_csv(RESULTS / "partial_profit_scaleout_trades.csv", index=False)
    decomposition.to_csv(RESULTS / "partial_profit_scaleout_decomposition.csv", index=False)
    pd.DataFrame([screen]).to_csv(RESULTS / "partial_profit_scaleout_screen.csv", index=False)
    (RESULTS / "partial_profit_scaleout_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(metrics, decomposition, screen, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
