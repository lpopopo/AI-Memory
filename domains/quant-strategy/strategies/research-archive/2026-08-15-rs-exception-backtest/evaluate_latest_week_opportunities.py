#!/usr/bin/env python3
"""Explain latest-week watchlist moves and rejected RSR1 signals."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
REPLAY = runpy.run_path(str(HERE / "replay_latest_week.py"))
RESULTS = HERE / "results"
PRIOR_CLOSE = pd.Timestamp("2026-08-07")
WEEK_START = pd.Timestamp("2026-08-10")
WEEK_END = pd.Timestamp("2026-08-14")


def build_diagnostics(panels: dict[str, pd.DataFrame], symbols: list[str]) -> pd.DataFrame:
    config = MODULE["Config"](
        rs20_min=0.03,
        volume_ratio_min=1.2,
        max_extension=0.12,
        max_hold_days=20,
        stop_loss=0.08,
        max_atr_pct=0.04,
        min_close_location=0.50,
    )
    features = MODULE["build_features"](panels, symbols, config)
    close, high, low, open_, volume = (
        panels[name] for name in ("close", "high", "low", "open", "volume")
    )
    stock_close = close[symbols]
    ma20 = stock_close.rolling(20, min_periods=20).mean()
    ma50 = stock_close.rolling(50, min_periods=50).mean()
    prior_high20 = high[symbols].rolling(20, min_periods=20).max().shift(1)
    extension = stock_close / ma20 - 1.0
    positive_gap = open_[symbols] / stock_close.shift(1) - 1.0 >= 0.10
    day_range = (high[symbols] - low[symbols]) / open_[symbols]
    event_block = positive_gap | positive_gap.shift(1).fillna(False)
    event_block |= positive_gap.shift(2).fillna(False) & (day_range >= 0.03)
    rows = []
    for date in close.loc[WEEK_START:WEEK_END].index:
        for symbol in symbols:
            conditions = {
                "broad_healthy": bool(features["broad_healthy"].at[date]),
                "above_ma20": bool(stock_close.at[date, symbol] > ma20.at[date, symbol]),
                "above_ma50": bool(stock_close.at[date, symbol] > ma50.at[date, symbol]),
                "breakout_20d": bool(stock_close.at[date, symbol] > prior_high20.at[date, symbol]),
                "rs20_ge_3pct": bool(features["rs20"].at[date, symbol] >= 0.03),
                "volume_ge_1_2x": bool(features["volume_ratio"].at[date, symbol] >= 1.2),
                "extension_le_12pct": bool(0.0 <= extension.at[date, symbol] <= 0.12),
                "atr_le_4pct": bool(features["atr_pct"].at[date, symbol] <= 0.04),
                "close_location_ge_50pct": bool(features["close_location"].at[date, symbol] >= 0.50),
                "event_gap_clear": not bool(event_block.at[date, symbol]),
                "smh_healthy": bool(features["smh_healthy"].at[date]),
            }
            entry_conditions = {key: value for key, value in conditions.items() if key != "smh_healthy"}
            failures = [key for key, value in entry_conditions.items() if not value]
            rows.append(
                {
                    "date": date,
                    "symbol": symbol,
                    "close": float(stock_close.at[date, symbol]),
                    "daily_return": float(stock_close[symbol].pct_change().at[date]),
                    "week_return_from_aug7": float(
                        stock_close.at[date, symbol] / stock_close.at[PRIOR_CLOSE, symbol] - 1.0
                    ),
                    "rs20": float(features["rs20"].at[date, symbol]),
                    "volume_ratio": float(features["volume_ratio"].at[date, symbol]),
                    "extension": float(extension.at[date, symbol]),
                    "atr_pct": float(features["atr_pct"].at[date, symbol]),
                    "close_location": float(features["close_location"].at[date, symbol]),
                    "strict_signal": bool(features["signal"].at[date, symbol] and conditions["smh_healthy"]),
                    "pre_smh_signal": bool(features["signal"].at[date, symbol]),
                    "failure_count": len(failures),
                    "failure_reasons": ";".join(failures),
                    **conditions,
                }
            )
    return pd.DataFrame(rows)


def write_report(diagnostics: pd.DataFrame, movers: pd.DataFrame, summary: dict) -> None:
    aaoi = diagnostics.loc[diagnostics["symbol"] == "AAOI"]
    lines = [
        "# Latest-week missed-opportunity audit",
        "",
        "## Boundary",
        "",
        "This is a retrospective explanation of completed sessions from 2026-08-10 through 2026-08-14. The RSR1 rules were not yet in genuine forward observation, so no row can authorize or reconstruct a live order.",
        "",
        "## Largest watchlist moves",
        "",
        "| Rank | Symbol | Aug 7 close | Aug 14 close | Weekly return | RSR1 signal this week |",
        "| ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for rank, row in enumerate(movers.head(10).itertuples(index=False), 1):
        lines.append(
            f"| {rank} | {row.symbol} | {row.prior_close:.2f} | {row.week_end_close:.2f} | "
            f"{row.week_return:.2%} | {bool(row.any_strict_signal)} |"
        )
    lines.extend(
        [
            "",
            "## AAOI decision trace",
            "",
            "| Date | Close | Daily | From Aug 7 | RS20 | Volume | ATR | Close location | Failed exact conditions |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in aaoi.itertuples(index=False):
        lines.append(
            f"| {row.date.date()} | {row.close:.2f} | {row.daily_return:.2%} | "
            f"{row.week_return_from_aug7:.2%} | {row.rs20:.2%} | {row.volume_ratio:.2f}x | "
            f"{row.atr_pct:.2%} | {row.close_location:.0%} | {row.failure_reasons or 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- AAOI returned `{summary['aaoi_week_return']:.2%}` over the week, but produced `{summary['aaoi_strict_signal_days']}` exact RSR1 signal days. Its recurring blockers were `{summary['aaoi_recurring_failures']}`.",
            f"- Across all `{summary['symbols']}` tradable watchlist names there were `{summary['all_strict_signal_days']}` exact strict-veto signal rows this week. A strong realized return alone is therefore not evidence that the strategy should have bought before the move.",
            "- Classification: AAOI was a missed outcome, not yet a demonstrated rule error. The repair is better ex-ante trigger labeling and forward capture measurement, not retroactively weakening volatility, breakout, volume or market-health gates after seeing the rally.",
        ]
    )
    (RESULTS / "latest_week_opportunity_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    panels, symbols, source_status = REPLAY["extend_panels"]()
    diagnostics = build_diagnostics(panels, symbols)
    week_end = diagnostics.loc[diagnostics["date"] == WEEK_END].copy()
    movers = week_end[["symbol", "close", "week_return_from_aug7"]].rename(
        columns={"close": "week_end_close", "week_return_from_aug7": "week_return"}
    )
    movers["prior_close"] = [float(panels["close"].at[PRIOR_CLOSE, symbol]) for symbol in movers["symbol"]]
    signal_counts = diagnostics.groupby("symbol")["strict_signal"].sum()
    movers["any_strict_signal"] = movers["symbol"].map(signal_counts).fillna(0).astype(int) > 0
    movers = movers.sort_values("week_return", ascending=False).reset_index(drop=True)
    aaoi = diagnostics.loc[diagnostics["symbol"] == "AAOI"]
    recurring = (
        aaoi.assign(reason=aaoi["failure_reasons"].str.split(";"))
        .explode("reason")["reason"]
        .loc[lambda values: values.ne("")]
        .value_counts()
    )
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "period": [str(WEEK_START.date()), str(WEEK_END.date())],
        "research_only": True,
        "authorizes_trade": False,
        "symbols": len(symbols),
        "all_strict_signal_days": int(diagnostics["strict_signal"].sum()),
        "aaoi_week_return": float(aaoi.iloc[-1]["week_return_from_aug7"]),
        "aaoi_strict_signal_days": int(aaoi["strict_signal"].sum()),
        "aaoi_recurring_failures": ", ".join(f"{name} ({count}/5)" for name, count in recurring.items()),
        "source_complete_through": str(WEEK_END.date()),
        "all_equity_sources_complete": all(
            item.get("last_date") == str(WEEK_END.date())
            for symbol, item in source_status.items()
            if not symbol.startswith("^")
        ),
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    diagnostics.to_csv(RESULTS / "latest_week_signal_diagnostics.csv", index=False)
    movers.to_csv(RESULTS / "latest_week_watchlist_movers.csv", index=False)
    (RESULTS / "latest_week_opportunity_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(diagnostics, movers, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
