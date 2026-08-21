#!/usr/bin/env python3
"""Audit the universe implied by the SMH/common-factor hypothesis."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
WATCHLIST = ROOT / "references" / "user-selected-watchlist.json"
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
RESULTS = HERE / "results"
DIRECT_THEMES = {
    "memory_storage",
    "interconnect_custom_silicon",
    "optical_interconnect",
    "interconnect_transmission",
    "ai_server_rack",
    "semiconductor_test",
    "semiconductor_equipment",
    "edge_inference",
    "ai_compute",
    "ai_compute_foundry",
    "optical_network",
    "network_infrastructure",
    "pcb_electronics_manufacturing",
}
NON_COMMON_FACTOR_THEMES = {
    "consumer_defensive_beverages",
    "space_satellite",
}
COMMON = dict(
    rs20_min=0.03,
    volume_ratio_min=1.20,
    max_extension=0.12,
    max_hold_days=20,
    stop_loss=0.08,
    normal_target_weight=0.08,
)


def universe_definitions(all_symbols: list[str]) -> tuple[dict[str, list[str]], dict[str, str]]:
    raw = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    theme = {item["symbol"]: item["theme"] for item in raw["tickers"]}
    mapped = set().union(*MODULE["SUPER_GROUPS"].values())
    universes = {
        "all_35": list(all_symbols),
        "ai_capex_broad": [
            symbol for symbol in all_symbols if theme[symbol] not in NON_COMMON_FACTOR_THEMES
        ],
        "direct_semiconductor_chain": [
            symbol for symbol in all_symbols if theme[symbol] in DIRECT_THEMES
        ],
        "legacy_supergroup_mapped": [symbol for symbol in all_symbols if symbol in mapped],
    }
    return universes, theme


def make_config(filtered: bool):
    return MODULE["Config"](
        **COMMON,
        max_atr_pct=0.04 if filtered else 1.00,
        min_close_location=0.50 if filtered else 0.00,
    )


def theme_for(symbol: str, theme_map: dict[str, str]) -> str:
    return theme_map.get(symbol, "unknown")


def concentration(trades: list[dict], theme_map: dict[str, str]) -> dict:
    wins = [trade for trade in trades if trade.get("pnl") is not None and trade["pnl"] > 0]
    gross = sum(trade["pnl"] for trade in wins)
    by_symbol = {}
    by_theme = {}
    for trade in wins:
        by_symbol[trade["symbol"]] = by_symbol.get(trade["symbol"], 0.0) + trade["pnl"]
        theme = theme_for(trade["symbol"], theme_map)
        by_theme[theme] = by_theme.get(theme, 0.0) + trade["pnl"]
    return {
        "winning_symbols": len(by_symbol),
        "winning_themes": len(by_theme),
        "max_symbol_profit_share": max(by_symbol.values(), default=0.0) / gross if gross else 1.0,
        "max_theme_profit_share": max(by_theme.values(), default=0.0) / gross if gross else 1.0,
    }


def evaluate(panels, universes, theme_map, last_date):
    intervals = {
        "train_2024_2025": ("2024-01-02", "2025-12-31"),
        "2026": ("2026-01-01", str(last_date.date())),
        "full": ("2024-01-02", str(last_date.date())),
    }
    rows = []
    trade_rows = []
    for universe_name, symbols in universes.items():
        for period_name, interval in intervals.items():
            pair = {}
            for filtered in (False, True):
                name = "risk_filter" if filtered else "matched_baseline"
                result = MODULE["simulate"](
                    panels,
                    symbols,
                    make_config(filtered),
                    "strict_veto",
                    *interval,
                    slippage=0.001,
                )
                pair[name] = result
                if filtered and period_name == "full":
                    for trade in result["trades"]:
                        trade_rows.append(
                            {
                                "universe": universe_name,
                                "theme": theme_for(trade["symbol"], theme_map),
                                **trade,
                            }
                        )
            baseline = pair["matched_baseline"]["metrics"]
            candidate = pair["risk_filter"]["metrics"]
            conc = concentration(pair["risk_filter"]["trades"], theme_map)
            rows.append(
                {
                    "universe": universe_name,
                    "universe_size": len(symbols),
                    "period": period_name,
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
                    "win_rate_delta": candidate["win_rate"] - baseline["win_rate"],
                    "baseline_trades": baseline["trade_count"],
                    "candidate_trades": candidate["trade_count"],
                    **conc,
                }
            )
    return pd.DataFrame(rows), pd.DataFrame(trade_rows)


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2%}"


def num(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2f}"


def write_report(metrics: pd.DataFrame, universes: dict[str, list[str]], theme_map: dict[str, str]):
    lines = [
        "# SMH/common-factor universe-scope audit",
        "",
        "## Why this audit exists",
        "",
        "The user list has 36 symbols, of which QQQM is excluded as an index duplicate. The prior simulator applied the SMH gate to all remaining 35, while the preregistered hypothesis says semiconductor/common-factor entries. The following scopes are fixed from existing watchlist theme labels, not from trade outcomes.",
        "",
    ]
    for name, symbols in universes.items():
        lines.append(f"- `{name}` ({len(symbols)}): {', '.join(symbols)}")
    lines.extend(
        [
            "",
            "## Paired results at 10 bps",
            "",
            "| Universe | Period | Baseline return | Candidate return | Delta | Candidate DD | Sharpe | Win rate | Trades | Winning themes | Max symbol profit share |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in metrics.itertuples(index=False):
        lines.append(
            f"| {row.universe} | {row.period} | {pct(row.baseline_return)} | {pct(row.candidate_return)} | "
            f"{row.return_delta:+.2%} | {pct(row.candidate_drawdown)} | {num(row.candidate_sharpe)} | "
            f"{pct(row.candidate_win_rate)} | {row.candidate_trades} | {row.winning_themes} | "
            f"{pct(row.max_symbol_profit_share)} |"
        )
    scope_summary = (
        metrics.loc[metrics["period"].isin(["train_2024_2025", "2026"])]
        .groupby("universe")
        .agg(
            return_better=("return_delta", lambda values: (values > 0).all()),
            drawdown_better=("drawdown_delta", lambda values: (values >= 0).all()),
            sharpe_better=("sharpe_delta", lambda values: (values > 0).all()),
            win_better=("win_rate_delta", lambda values: (values > 0).all()),
            minimum_trades=("candidate_trades", "min"),
        )
        .reset_index()
    )
    robust = scope_summary.loc[
        scope_summary["return_better"] & scope_summary["drawdown_better"] & scope_summary["sharpe_better"]
    ]
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- Candidate improves return, drawdown and Sharpe in both training and 2026 for `{len(robust)}/{len(scope_summary)}` predefined scopes.",
            "- Scope must be resolved from strategy intent before forward accumulation; selecting the best historical scope would be another form of overfitting.",
            "- Full-watchlist analysis may still discuss every symbol, but an SMH-gated shadow ledger should not silently treat a defensive beverage or unrelated space exposure as a semiconductor/common-factor trade.",
            "",
            "Research-only. This report does not authorize exclusion, inclusion or an order by itself.",
        ]
    )
    (RESULTS / "universe_scope_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, all_symbols = MODULE["load_panels"]()
    universes, theme_map = universe_definitions(all_symbols)
    last_date = panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1]
    metrics, trades = evaluate(panels, universes, theme_map, last_date)
    metrics.to_csv(RESULTS / "universe_scope_metrics.csv", index=False)
    trades.to_csv(RESULTS / "universe_scope_trades.csv", index=False)
    (RESULTS / "universe_scope_summary.json").write_text(
        json.dumps(
            {
                "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
                "data_end": str(last_date.date()),
                "research_only": True,
                "authorizes_trade": False,
                "universes": universes,
                "theme_map": theme_map,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    write_report(metrics, universes, theme_map)
    print(RESULTS / "universe_scope_report.md")


if __name__ == "__main__":
    main()
