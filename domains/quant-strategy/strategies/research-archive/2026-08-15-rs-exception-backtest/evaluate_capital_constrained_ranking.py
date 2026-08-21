#!/usr/bin/env python3
"""Audit frozen ranking policies for capacity-constrained RSR2 entries."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
BACKTEST = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
RESULTS = HERE / "results"
POLICIES = ("formal_composite", "rs_only", "low_atr_first", "balanced_rank")
CHALLENGERS = POLICIES[1:]
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
    gross_profit = sum(by_symbol.values())
    return {
        "profitable_symbols": len(by_symbol),
        "top_symbol_profit_share": (
            max(by_symbol.values(), default=0.0) / gross_profit if gross_profit else 1.0
        ),
        "gross_profit": gross_profit,
    }


def _cell(metrics: pd.DataFrame, policy: str, nav: float, period: str, slippage: float) -> pd.Series:
    match = metrics.loc[
        (metrics["policy"] == policy)
        & (metrics["initial_nav"] == nav)
        & (metrics["period"] == period)
        & (metrics["slippage"] == slippage)
    ]
    if len(match) != 1:
        raise RuntimeError(f"missing or duplicate ranking cell: {policy}/{nav}/{period}/{slippage}")
    return match.iloc[0]


def challenger_screen(metrics: pd.DataFrame) -> tuple[pd.DataFrame, str | None]:
    rows = []
    for policy in CHALLENGERS:
        return_deltas_10 = []
        return_deltas_20 = []
        sharpe_ok = []
        drawdown_ok = []
        win_rate_ok = []
        contention_ok = []
        concentration_ok = []
        for nav in NAVS:
            for period in ("development_2024_2025", "heldout_2026"):
                baseline10 = _cell(metrics, "formal_composite", nav, period, 0.001)
                candidate10 = _cell(metrics, policy, nav, period, 0.001)
                baseline20 = _cell(metrics, "formal_composite", nav, period, 0.002)
                candidate20 = _cell(metrics, policy, nav, period, 0.002)
                return_deltas_10.append(candidate10.total_return - baseline10.total_return)
                return_deltas_20.append(candidate20.total_return - baseline20.total_return)
                sharpe_ok.append(candidate10.sharpe + 1e-12 >= baseline10.sharpe)
                drawdown_ok.append(candidate10.max_drawdown + 0.01 + 1e-12 >= baseline10.max_drawdown)
                win_rate_ok.append(candidate10.win_rate + 0.05 + 1e-12 >= baseline10.win_rate)
                minimum = 5 if period == "development_2024_2025" else 2
                contention_ok.append(int(candidate10.ranking_contention_decisions) >= minimum)
            full = _cell(metrics, policy, nav, "full", 0.001)
            concentration_ok.append(
                int(full.profitable_symbols) >= 3
                and float(full.top_symbol_profit_share) <= 0.35 + 1e-12
            )
        checks = {
            "sufficient_contention": all(contention_ok),
            "return_improves_10bps": all(delta > 1e-12 for delta in return_deltas_10),
            "sharpe_nonworse": all(sharpe_ok),
            "drawdown_within_1pp": all(drawdown_ok),
            "win_rate_within_5pp": all(win_rate_ok),
            "return_improves_20bps": all(delta > 1e-12 for delta in return_deltas_20),
            "profit_diversified": all(concentration_ok),
        }
        rows.append(
            {
                "policy": policy,
                **checks,
                "min_return_delta_10bps": min(return_deltas_10),
                "min_return_delta_20bps": min(return_deltas_20),
                "passes": all(checks.values()),
                "status": (
                    "insufficient"
                    if not checks["sufficient_contention"]
                    else "pass" if all(checks.values()) else "fail"
                ),
            }
        )
    screen = pd.DataFrame(rows)
    passed = screen.loc[screen["passes"]].sort_values(
        ["min_return_delta_10bps", "policy"], ascending=[False, True]
    )
    winner = str(passed.iloc[0]["policy"]) if not passed.empty else None
    return screen, winner


def pct(value: float) -> str:
    return f"{value:.2%}"


def write_report(metrics: pd.DataFrame, screen: pd.DataFrame, summary: dict) -> None:
    lines = [
        "# Capital-constrained RSR2 ranking audit",
        "",
        "## Decision",
        "",
        f"- Result: `{summary['decision']}`.",
        f"- Selected forward challenger: `{summary['selected_challenger'] or 'none'}`.",
        "- Every policy uses identical frozen RSR1 entries and RSR2 exits; only ordering among simultaneously eligible names changes.",
        "- This retrospective current-list audit cannot modify formal V9 or the already-frozen RSR1/RSR2 forward ledgers.",
        "",
        "## Advancement screen",
        "",
        "| Policy | Status | Min return delta 10bps | Min return delta 20bps | Contention | Sharpe | DD | Win rate | Diversified |",
        "| --- | --- | ---: | ---: | --- | --- | --- | --- | --- |",
    ]
    for row in screen.itertuples(index=False):
        lines.append(
            f"| {row.policy} | {row.status} | {pct(row.min_return_delta_10bps)} | "
            f"{pct(row.min_return_delta_20bps)} | {row.sufficient_contention} | "
            f"{row.sharpe_nonworse} | {row.drawdown_within_1pp} | "
            f"{row.win_rate_within_5pp} | {row.profit_diversified} |"
        )
    lines.extend(
        [
            "",
            "## Ten-basis-point results",
            "",
            "| NAV | Period | Policy | Return | Max DD | Sharpe | Win rate | Trades | Contention | Top profit share |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    subset = metrics.loc[metrics["slippage"] == 0.001]
    for row in subset.itertuples(index=False):
        lines.append(
            f"| ${row.initial_nav:,.2f} | {row.period} | {row.policy} | "
            f"{pct(row.total_return)} | {pct(row.max_drawdown)} | {row.sharpe:.2f} | "
            f"{pct(row.win_rate)} | {row.trade_count} | {row.ranking_contention_decisions} | "
            f"{pct(row.top_symbol_profit_share)} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "- A higher retrospective return is not enough: the preregistered gate requires cross-period, two-NAV and two-cost consistency plus adequate contention and profit diversification.",
            "- The 2026 segment has been seen in prior studies. It is a consistency monitor, not genuine out-of-sample evidence.",
            "- See `capital-constrained-ranking-preregistration.md` for the frozen rules and gate.",
        ]
    )
    (RESULTS / "capital_constrained_ranking_report.md").write_text(
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
    event_rows = []
    for nav in NAVS:
        for slippage in SLIPPAGES:
            for period, (start, configured_end) in PERIODS.items():
                end = configured_end or str(last_date.date())
                for policy in POLICIES:
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
                        ranking_mode=policy,
                    )
                    concentration = profit_concentration(result["trades"])
                    rows.append(
                        {
                            "initial_nav": nav,
                            "slippage": slippage,
                            "period": period,
                            "policy": policy,
                            **result["metrics"],
                            "ranking_contention_decisions": result["ranking_contention_decisions"],
                            **concentration,
                        }
                    )
                    for trade in result["trades"]:
                        trade_rows.append(
                            {
                                "initial_nav": nav,
                                "slippage": slippage,
                                "period": period,
                                "policy": policy,
                                **trade,
                            }
                        )
                    for event in result["ranking_events"]:
                        event_rows.append(
                            {
                                "initial_nav": nav,
                                "slippage": slippage,
                                "period": period,
                                "policy": policy,
                                **event,
                            }
                        )
    metrics = pd.DataFrame(rows)
    trades = pd.DataFrame(trade_rows)
    events = pd.DataFrame(event_rows)
    screen, winner = challenger_screen(metrics)
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_end": str(last_date.date()),
        "universe": "ai_capex_broad",
        "universe_size": len(symbols),
        "research_only": True,
        "authorizes_trade": False,
        "selected_challenger": winner,
        "decision": "advance_separate_forward_ranking_shadow" if winner else "retain_formal_composite",
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(RESULTS / "capital_constrained_ranking_metrics.csv", index=False)
    trades.to_csv(RESULTS / "capital_constrained_ranking_trades.csv", index=False)
    events.to_csv(RESULTS / "capital_constrained_ranking_events.csv", index=False)
    screen.to_csv(RESULTS / "capital_constrained_ranking_screen.csv", index=False)
    (RESULTS / "capital_constrained_ranking_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(metrics, screen, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
