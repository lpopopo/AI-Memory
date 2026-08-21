#!/usr/bin/env python3
"""Evaluate a close-confirmed profit-stop ratchet without changing frozen RSR1."""
from __future__ import annotations

import itertools
import json
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE_MODULE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
RESULTS = HERE / "results"
CENTRAL = "lock_15_to_5"
OVERLAYS = {"frozen": (None, 0.0)}
OVERLAYS.update(
    {
        f"lock_{int(trigger * 100)}_to_{int(floor * 100)}": (trigger, floor)
        for trigger, floor in itertools.product((0.12, 0.15, 0.18), (0.00, 0.03, 0.05))
    }
)


def trade_excursions(result: dict, panels: dict[str, pd.DataFrame], slippage: float) -> pd.DataFrame:
    rows = []
    dates = panels["close"].index
    for trade in result["trades"]:
        entry_date = pd.Timestamp(trade["entry_date"])
        exit_date = pd.Timestamp(trade["exit_date"])
        symbol = trade["symbol"]
        entry_price = trade["entry_price"]
        # The exit day is excluded because an opening or intraday exit occurs
        # before its full daily high/low is knowable. Raw exit fill is retained.
        pre_exit = dates[(dates >= entry_date) & (dates < exit_date)]
        highs = panels["high"].loc[pre_exit, symbol].dropna()
        lows = panels["low"].loc[pre_exit, symbol].dropna()
        closes = panels["close"].loc[pre_exit, symbol].dropna()
        raw_exit = trade["exit_price"] / (1.0 - slippage)
        mfe = max([0.0, *((highs / entry_price - 1.0).tolist()), raw_exit / entry_price - 1.0])
        mae = min([0.0, *((lows / entry_price - 1.0).tolist()), raw_exit / entry_price - 1.0])
        peak_close = max([0.0, *((closes / entry_price - 1.0).tolist())])
        rows.append(
            {
                **trade,
                "holding_sessions": int(dates.get_loc(exit_date) - dates.get_loc(entry_date)),
                "pre_exit_mfe": float(mfe),
                "pre_exit_mae": float(mae),
                "pre_exit_peak_close": float(peak_close),
                "mfe_giveback": float(mfe - trade["return"]),
            }
        )
    return pd.DataFrame(rows)


def path_signature(result: dict) -> list[tuple]:
    return [
        (
            trade["signal_date"],
            trade["symbol"],
            trade["entry_date"],
            trade.get("exit_date"),
            trade.get("exit_reason"),
        )
        for trade in result["trades"]
    ]


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2%}"


def num(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2f}"


def evaluate(panels, symbols, end: str):
    periods = {
        "train_2024_2025": ("2024-01-02", "2025-12-31"),
        "2026": ("2026-01-01", end),
        "full": ("2024-01-02", end),
    }
    rows = []
    runs = {}
    for overlay, (trigger, floor) in OVERLAYS.items():
        for period, interval in periods.items():
            for filtered in (False, True):
                filter_name = "risk_filter" if filtered else "matched_baseline"
                result = MODULE["simulate"](
                    panels,
                    symbols,
                    UNIVERSE_MODULE["make_config"](filtered),
                    "strict_veto",
                    *interval,
                    slippage=0.001,
                    profit_lock_trigger=trigger,
                    profit_lock_floor=floor,
                )
                runs[(overlay, period, filter_name, 0.001)] = result
                metrics = result["metrics"]
                rows.append(
                    {
                        "overlay": overlay,
                        "trigger": trigger,
                        "floor": floor,
                        "period": period,
                        "filter": filter_name,
                        "slippage": 0.001,
                        **metrics,
                        "lock_activations": sum(
                            trade.get("profit_lock_date") is not None for trade in result["trades"]
                        ),
                        "profit_lock_exits": sum(
                            trade.get("exit_reason") == "profit_lock" for trade in result["trades"]
                        ),
                    }
                )
        for filtered in (False, True):
            filter_name = "risk_filter" if filtered else "matched_baseline"
            result = MODULE["simulate"](
                panels,
                symbols,
                UNIVERSE_MODULE["make_config"](filtered),
                "strict_veto",
                "2024-01-02",
                end,
                slippage=0.002,
                profit_lock_trigger=trigger,
                profit_lock_floor=floor,
            )
            runs[(overlay, "full", filter_name, 0.002)] = result
            metrics = result["metrics"]
            rows.append(
                {
                    "overlay": overlay,
                    "trigger": trigger,
                    "floor": floor,
                    "period": "full",
                    "filter": filter_name,
                    "slippage": 0.002,
                    **metrics,
                    "lock_activations": sum(
                        trade.get("profit_lock_date") is not None for trade in result["trades"]
                    ),
                    "profit_lock_exits": sum(
                        trade.get("exit_reason") == "profit_lock" for trade in result["trades"]
                    ),
                }
            )
    metrics = pd.DataFrame(rows)
    frozen = metrics.loc[
        metrics["overlay"].eq("frozen")
        & metrics["filter"].eq("risk_filter")
        & metrics["slippage"].eq(0.001)
    ].set_index("period")
    candidate_rows = metrics.loc[
        metrics["filter"].eq("risk_filter") & metrics["slippage"].eq(0.001)
    ].copy()
    for field in ("total_return", "max_drawdown", "sharpe", "win_rate"):
        candidate_rows[f"{field}_delta_vs_frozen"] = candidate_rows.apply(
            lambda row: row[field] - frozen.at[row["period"], field], axis=1
        )
    screen_rows = []
    for overlay in OVERLAYS:
        if overlay == "frozen":
            continue
        group = candidate_rows.loc[candidate_rows["overlay"].eq(overlay)].set_index("period")
        paired = metrics.loc[
            metrics["overlay"].eq(overlay) & metrics["slippage"].eq(0.001)
        ].pivot(index="period", columns="filter", values="total_return")
        checks = {
            "return_nonworse_train_and_2026": all(
                group.at[period, "total_return_delta_vs_frozen"] >= -1e-12
                for period in ("train_2024_2025", "2026")
            ),
            "drawdown_nonworse_train_and_2026": all(
                group.at[period, "max_drawdown_delta_vs_frozen"] >= -1e-12
                for period in ("train_2024_2025", "2026")
            ),
            "sharpe_nonworse_train_and_2026": all(
                group.at[period, "sharpe_delta_vs_frozen"] >= -1e-12
                for period in ("train_2024_2025", "2026")
            ),
            "win_rate_nonworse_train_and_2026": all(
                group.at[period, "win_rate_delta_vs_frozen"] >= -1e-12
                for period in ("train_2024_2025", "2026")
            ),
            "filter_still_beats_paired_baseline": all(
                paired.at[period, "risk_filter"] > paired.at[period, "matched_baseline"]
                for period in ("train_2024_2025", "2026")
            ),
        }
        screen_rows.append({"overlay": overlay, **checks, "passes_all": all(checks.values())})
    return metrics, candidate_rows, pd.DataFrame(screen_rows), runs


def write_report(metrics, screen, excursions, summary) -> None:
    central = metrics.loc[
        metrics["overlay"].isin(["frozen", CENTRAL])
        & metrics["filter"].eq("risk_filter")
        & metrics["slippage"].eq(0.001)
    ]
    lines = [
        "# Close-confirmed profit-protection audit",
        "",
        "## What the trade paths say",
        "",
        f"The frozen 32-name candidate has `{summary['frozen_trades']}` trades, `{summary['frozen_winners']}` winners and `{summary['frozen_losses']}` losses. Only `{summary['losers_reaching_8pct_mfe']}` loss reached +8% pre-exit MFE, and only `{summary['losers_reaching_8pct_close']}` loss closed at least 8% above entry before later losing. `{summary['winners_reaching_8pct_mfe']}/{summary['frozen_winners']}` eventual winners reached +8% MFE.",
        "",
        "A fixed profit target would therefore cap nearly every winner to repair one historical giveback. The tested alternative waits for a completed close to confirm a gain, then raises the stop for the following session. Daily-bar ambiguity is avoided by never activating from the same day's intraday high.",
        "",
        "## Frozen versus central 15% -> 5% challenger at 10 bps",
        "",
        "| Period | Variant | Return | Max DD | Sharpe | Win rate | Profit factor | Trades | Lock exits |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for period in ("train_2024_2025", "2026", "full"):
        for overlay in ("frozen", CENTRAL):
            row = central.loc[central["period"].eq(period) & central["overlay"].eq(overlay)].iloc[0]
            lines.append(
                f"| {period} | {overlay} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
                f"{num(row.sharpe)} | {pct(row.win_rate)} | {num(row.profit_factor)} | "
                f"{row.trade_count} | {row.profit_lock_exits} |"
            )
    lines.extend(
        [
            "",
            "## Robustness checks",
            "",
            f"- `{summary['neighbor_passes']}/{summary['neighbor_total']}` trigger/floor neighbors pass the non-worse return, drawdown, Sharpe and win-rate screen in both training and 2026 while preserving the paired-filter advantage.",
            f"- At 20 bps, the central candidate returns `{pct(summary['central_20bps_return'])}` versus `{pct(summary['central_20bps_baseline_return'])}` for its paired baseline and `{pct(summary['frozen_20bps_return'])}` for frozen RSR1.",
            f"- Fixed-path repricing of the unchanged 10-bps trades to 20 bps gives `{pct(summary['central_fixed_path_20bps_return'])}` for the central challenger versus `{pct(summary['frozen_fixed_path_20bps_return'])}` for frozen RSR1.",
            f"- Full-rerun trade paths at 10/20 bps are not identical (`{summary['central_10bps_trades']}` versus `{summary['central_20bps_trades']}` trades), so the fixed-path check remains necessary.",
            "",
            "## Decision",
            "",
            "The 15% close-confirmed trigger with a +5% entry-price floor is a reasonable separate forward challenger, not a replacement for RSR1. Its apparent improvement is driven by only two protected exits (INTC in training and KLAC in 2026), uses the same hindsight-selected watchlist, and was examined after the base strategy. Keep RSR1 frozen; any forward test must use a new version and separate ledger.",
            "",
            "Research-only. No live order or formal V9 change is authorized.",
        ]
    )
    (RESULTS / "profit_protection_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, all_symbols = MODULE["load_panels"]()
    universes, _ = UNIVERSE_MODULE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    end = str(panels["close"][["SPY", "QQQ", "SMH"]].dropna().index[-1].date())
    metrics, candidate_rows, screen, runs = evaluate(panels, symbols, end)
    frozen_full = runs[("frozen", "full", "risk_filter", 0.001)]
    central_full = runs[(CENTRAL, "full", "risk_filter", 0.001)]
    excursions = trade_excursions(frozen_full, panels, 0.001)
    losses = excursions.loc[excursions["pnl"] <= 0]
    wins = excursions.loc[excursions["pnl"] > 0]
    central_20 = runs[(CENTRAL, "full", "risk_filter", 0.002)]
    frozen_20 = runs[("frozen", "full", "risk_filter", 0.002)]
    central_baseline_20 = runs[(CENTRAL, "full", "matched_baseline", 0.002)]
    central_fixed = MODULE["fixed_path_cost_stress"](central_full, 0.001, 0.002)
    frozen_fixed = MODULE["fixed_path_cost_stress"](frozen_full, 0.001, 0.002)
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_end": end,
        "universe": "ai_capex_broad",
        "universe_size": len(symbols),
        "research_only": True,
        "authorizes_trade": False,
        "frozen_trades": len(excursions),
        "frozen_winners": len(wins),
        "frozen_losses": len(losses),
        "losers_reaching_8pct_mfe": int((losses["pre_exit_mfe"] >= 0.08).sum()),
        "losers_reaching_8pct_close": int((losses["pre_exit_peak_close"] >= 0.08).sum()),
        "winners_reaching_8pct_mfe": int((wins["pre_exit_mfe"] >= 0.08).sum()),
        "neighbor_passes": int(screen["passes_all"].sum()),
        "neighbor_total": len(screen),
        "central_10bps_trades": central_full["metrics"]["trade_count"],
        "central_20bps_trades": central_20["metrics"]["trade_count"],
        "central_20bps_return": central_20["metrics"]["total_return"],
        "central_20bps_baseline_return": central_baseline_20["metrics"]["total_return"],
        "frozen_20bps_return": frozen_20["metrics"]["total_return"],
        "central_fixed_path_20bps_return": central_fixed["total_return"],
        "frozen_fixed_path_20bps_return": frozen_fixed["total_return"],
        "central_profit_lock_exits": [
            {
                "symbol": trade["symbol"],
                "signal_date": trade["signal_date"],
                "profit_lock_date": trade["profit_lock_date"],
                "exit_date": trade["exit_date"],
                "return": trade["return"],
            }
            for trade in central_full["trades"]
            if trade.get("exit_reason") == "profit_lock"
        ],
        "decision": "nominate_separate_forward_challenger_do_not_modify_rsr1",
    }
    metrics.to_csv(RESULTS / "profit_protection_metrics.csv", index=False)
    candidate_rows.to_csv(RESULTS / "profit_protection_candidate_deltas.csv", index=False)
    screen.to_csv(RESULTS / "profit_protection_neighbor_screen.csv", index=False)
    excursions.to_csv(RESULTS / "profit_protection_excursions.csv", index=False)
    (RESULTS / "profit_protection_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    write_report(metrics, screen, excursions, summary)
    print(RESULTS / "profit_protection_report.md")


if __name__ == "__main__":
    main()
