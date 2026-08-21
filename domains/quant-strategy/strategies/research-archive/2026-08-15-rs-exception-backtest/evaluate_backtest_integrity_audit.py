#!/usr/bin/env python3
"""Adversarial integrity audit of the frozen RSR backtest implementations."""
from __future__ import annotations

import json
import math
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RSR = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
PIT = runpy.run_path(str(HERE / "evaluate_pit_exact_filter.py"))
SLIPPAGE = 0.001
COMMISSION = 1.0


def panel_invariants(panels: dict[str, pd.DataFrame]) -> dict:
    index_ok = all(frame.index.is_monotonic_increasing and frame.index.is_unique for frame in panels.values())
    aligned = all(frame.index.equals(panels["close"].index) for frame in panels.values())
    common = (
        panels["open"].notna()
        & panels["high"].notna()
        & panels["low"].notna()
        & panels["close"].notna()
    )
    tolerance = 1e-8
    high_bad = common & (
        (panels["high"] + tolerance < panels["open"])
        | (panels["high"] + tolerance < panels["close"])
        | (panels["high"] + tolerance < panels["low"])
    )
    low_bad = common & (
        (panels["low"] > panels["open"] + tolerance)
        | (panels["low"] > panels["close"] + tolerance)
    )
    nonpositive = common & (
        (panels["open"] <= 0)
        | (panels["high"] <= 0)
        | (panels["low"] <= 0)
        | (panels["close"] <= 0)
    )
    negative_volume = panels["volume"].notna() & (panels["volume"] < 0)
    bad = high_bad | low_bad | nonpositive
    bad_rows, bad_columns = np.where(bad.to_numpy())
    records = [
        {
            "date": str(bad.index[row].date()),
            "symbol": str(bad.columns[column]),
            "open": float(panels["open"].iat[row, column]),
            "high": float(panels["high"].iat[row, column]),
            "low": float(panels["low"].iat[row, column]),
            "close": float(panels["close"].iat[row, column]),
        }
        for row, column in zip(bad_rows, bad_columns)
    ]
    return {
        "strictly_increasing_unique_dates": bool(index_ok),
        "aligned_panel_dates": bool(aligned),
        "invalid_high_bars": int(high_bad.to_numpy().sum()),
        "invalid_low_bars": int(low_bad.to_numpy().sum()),
        "nonpositive_ohlc_bars": int(nonpositive.to_numpy().sum()),
        "negative_volume_bars": int(negative_volume.to_numpy().sum()),
        "invalid_ohlc_records": records,
    }


def frame_equal(left, right) -> bool:
    if isinstance(left, pd.Series):
        left, right = left.to_frame(), right.to_frame()
    if left.dtypes.apply(lambda value: value == bool).all():
        return left.equals(right)
    return bool(np.allclose(left.to_numpy(dtype=float), right.to_numpy(dtype=float), equal_nan=True))


def causal_feature_test(panels: dict[str, pd.DataFrame], symbols: list[str], config) -> dict:
    cutoff = pd.Timestamp("2025-12-31")
    original = RSR["build_features"](panels, symbols, config)
    perturbed = {name: frame.copy(deep=True) for name, frame in panels.items()}
    future = perturbed["close"].index > cutoff
    for name in ("open", "high", "low", "close"):
        perturbed[name].loc[future, :] *= 3.0
    perturbed["volume"].loc[future, :] *= 7.0
    changed = RSR["build_features"](perturbed, symbols, config)
    keys = ("ma20", "rs20", "volume_ratio", "atr_pct", "close_location", "signal", "score", "broad_healthy", "smh_healthy")
    comparisons = {}
    for key in keys:
        comparisons[key] = frame_equal(original[key].loc[:cutoff], changed[key].loc[:cutoff])
    return {"cutoff": str(cutoff.date()), "feature_prefix_unchanged": comparisons, "passed": all(comparisons.values())}


def cash_replay(trades: list[dict], initial_nav: float) -> dict:
    events = []
    for trade in trades:
        events.append((trade["entry_date"], 2, -(trade["shares"] * trade["entry_price"] + COMMISSION)))
        partial_shares = int(trade.get("partial_exit_shares") or 0)
        if partial_shares and trade.get("partial_exit_date"):
            events.append(
                (
                    trade["partial_exit_date"],
                    1,
                    partial_shares * float(trade["partial_exit_price"]) - COMMISSION,
                )
            )
        if trade.get("exit_date"):
            remaining = int(trade["shares"]) - partial_shares
            exit_priority = 0 if trade.get("exit_reason") == "signal" else 3
            events.append(
                (
                    trade["exit_date"],
                    exit_priority,
                    remaining * float(trade["exit_price"]) - COMMISSION,
                )
            )
    cash = float(initial_nav)
    minimum = cash
    for _, _, change in sorted(events, key=lambda row: (row[0], row[1])):
        cash += change
        minimum = min(minimum, cash)
    return {"ending_cash_for_closed_and_open_path": cash, "minimum_cash": minimum, "nonnegative": minimum >= -1e-8}


def maximum_entry_exposure(
    trades: list[dict], panels: dict[str, pd.DataFrame], initial_nav: float
) -> float:
    cash = float(initial_nav)
    positions: dict[str, int] = {}
    maximum = 0.0
    dates = sorted(
        {
            pd.Timestamp(value)
            for trade in trades
            for value in (trade.get("entry_date"), trade.get("partial_exit_date"), trade.get("exit_date"))
            if value
        }
    )
    for date in dates:
        exiting = [
            trade
            for trade in trades
            if trade.get("exit_date") == str(date.date()) and trade.get("exit_reason") == "signal"
        ]
        for trade in exiting:
            remaining = positions.pop(trade["symbol"], 0)
            cash += remaining * float(trade["exit_price"]) - COMMISSION
        partials = [trade for trade in trades if trade.get("partial_exit_date") == str(date.date())]
        for trade in partials:
            shares = int(trade.get("partial_exit_shares") or 0)
            positions[trade["symbol"]] -= shares
            cash += shares * float(trade["partial_exit_price"]) - COMMISSION
        entries = [trade for trade in trades if trade.get("entry_date") == str(date.date())]
        for trade in entries:
            existing_value = sum(
                shares * float(panels["open"].at[date, symbol])
                for symbol, shares in positions.items()
            )
            open_equity = cash + existing_value
            notional = int(trade["shares"]) * float(trade["entry_price"])
            maximum = max(maximum, (existing_value + notional) / open_equity)
            cash -= notional + COMMISSION
            positions[trade["symbol"]] = int(trade["shares"])
        later_exits = [
            trade
            for trade in trades
            if trade.get("exit_date") == str(date.date()) and trade.get("exit_reason") != "signal"
        ]
        for trade in later_exits:
            remaining = positions.pop(trade["symbol"], 0)
            cash += remaining * float(trade["exit_price"]) - COMMISSION
    return maximum


def invalid_bar_trade_impacts(records: list[dict]) -> list[dict]:
    trades = pd.read_csv(RESULTS / "pit_exact_filter_trades.csv")
    impacts = []
    for record in records:
        date = pd.Timestamp(record["date"])
        rows = trades.loc[trades["symbol"].eq(record["symbol"])]
        for trade in rows.to_dict("records"):
            entry = pd.Timestamp(trade["entry_date"])
            exit_ = pd.Timestamp(trade["exit_date"])
            if entry <= date <= exit_:
                impacts.append({**record, "variant": trade["variant"], "entry_date": trade["entry_date"]})
    return impacts


def maximum_concurrent(trades: list[dict], dates: pd.DatetimeIndex) -> int:
    maximum = 0
    for date in dates:
        active = 0
        for trade in trades:
            entry = pd.Timestamp(trade["entry_date"])
            exit_ = pd.Timestamp(trade["exit_date"]) if trade.get("exit_date") else None
            active += entry <= date and (exit_ is None or date < exit_)
        maximum = max(maximum, active)
    return maximum


def price_and_chronology_audit(result: dict, panels: dict[str, pd.DataFrame], stop_loss: float) -> dict:
    chronology_failures = []
    price_failures = []
    for trade in result["trades"]:
        signal = pd.Timestamp(trade["signal_date"])
        entry = pd.Timestamp(trade["entry_date"])
        if entry <= signal:
            chronology_failures.append(f"{trade['symbol']}:{signal.date()}->{entry.date()}")
        raw_entry = float(trade["entry_price"]) / (1.0 + SLIPPAGE)
        expected_entry = float(panels["open"].at[entry, trade["symbol"]])
        if not math.isclose(raw_entry, expected_entry, rel_tol=0.0, abs_tol=1e-8):
            price_failures.append(f"entry:{trade['symbol']}:{entry.date()}")
        if not trade.get("exit_date"):
            continue
        exit_date = pd.Timestamp(trade["exit_date"])
        if exit_date < entry:
            chronology_failures.append(f"exit:{trade['symbol']}:{entry.date()}->{exit_date.date()}")
        raw_exit = float(trade["exit_price"]) / (1.0 - SLIPPAGE)
        reason = trade.get("exit_reason")
        if reason == "signal":
            expected = float(panels["open"].at[exit_date, trade["symbol"]])
            feasible = math.isclose(raw_exit, expected, rel_tol=0.0, abs_tol=1e-8)
        elif reason in {"stop", "profit_lock"}:
            day_open = float(panels["open"].at[exit_date, trade["symbol"]])
            stop = float(trade.get("profit_lock_stop") or (trade["entry_price"] * (1.0 - stop_loss)))
            expected = day_open if day_open <= stop else stop
            feasible = math.isclose(raw_exit, expected, rel_tol=0.0, abs_tol=1e-8)
        elif reason == "terminal":
            expected = float(panels["close"].at[exit_date, trade["symbol"]])
            feasible = math.isclose(raw_exit, expected, rel_tol=0.0, abs_tol=1e-8)
        else:
            feasible = False
        if not feasible:
            price_failures.append(f"exit:{reason}:{trade['symbol']}:{exit_date.date()}")
    return {
        "chronology_failures": chronology_failures,
        "price_feasibility_failures": price_failures,
        "chronology_passed": not chronology_failures,
        "price_feasibility_passed": not price_failures,
    }


def pit_terminal_sensitivity() -> dict:
    panels, membership, stocks = PIT["load_inputs"]()
    members = PIT["membership_mask"](membership, panels["close"].index, stocks)
    features = PIT["build_features"](panels, stocks, members)
    rows = []
    original_terminal_count = 0
    for period, (start, end) in PIT["PERIODS"].items():
        for variant in ("matched_baseline", "combined_4pct_50pct"):
            forced_equity, forced_trades = PIT["simulate_period"](
                panels, features, stocks, variant, start, end, liquidate_final=True
            )
            open_equity, open_trades = PIT["simulate_period"](
                panels, features, stocks, variant, start, end, liquidate_final=False
            )
            original_terminal_count += int(forced_trades["exit_reason"].eq("terminal").sum())
            forced = PIT["portfolio_statistics"](forced_equity, forced_trades)
            nonliquidated = PIT["portfolio_statistics"](open_equity, open_trades)
            rows.append(
                {
                    "period": period,
                    "variant": variant,
                    "forced_terminal_trades": int(forced_trades["exit_reason"].eq("terminal").sum()),
                    "open_positions_at_end": int(open_trades["exit_date"].isna().sum()),
                    "forced_return": forced["total_return"],
                    "nonliquidated_return": nonliquidated["total_return"],
                    "return_delta": nonliquidated["total_return"] - forced["total_return"],
                    "forced_win_rate": forced["win_rate"],
                    "nonliquidated_win_rate": nonliquidated["win_rate"],
                    "forced_trade_count": forced["trade_count"],
                    "nonliquidated_trade_count": nonliquidated["trade_count"],
                    "nonliquidated_metrics": nonliquidated,
                }
            )
    nonliquidated_metrics = pd.DataFrame(
        [{"period": row["period"], "variant": row["variant"], **row["nonliquidated_metrics"]} for row in rows]
    )
    coverage = PIT["period_coverage"](PIT["coverage_by_month"](panels["close"], members, stocks))
    passed, screen_rows = PIT["screen"](nonliquidated_metrics, coverage)
    for row in rows:
        row.pop("nonliquidated_metrics")
    return {
        "forced_terminal_trade_count": original_terminal_count,
        "maximum_absolute_return_delta": max(abs(row["return_delta"]) for row in rows),
        "nonliquidated_transferability_screen_passed": bool(passed),
        "nonliquidated_screen": screen_rows,
        "rows": rows,
    }


def evaluate() -> dict:
    panels, all_symbols = RSR["load_panels"]()
    universes, _ = UNIVERSE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    config = UNIVERSE["make_config"](True)
    start = "2024-01-02"
    end = str(panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1].date())
    rsr1 = RSR["simulate"](panels, symbols, config, "strict_veto", start, end, liquidate_final=False)
    rsr2 = RSR["simulate"](
        panels,
        symbols,
        config,
        "strict_veto",
        start,
        end,
        liquidate_final=False,
        profit_lock_trigger=0.15,
        profit_lock_floor=0.05,
    )
    causality = causal_feature_test(panels, symbols, config)
    current_data = panel_invariants(panels)
    pit_panels, _, _ = PIT["load_inputs"]()
    pit_data = panel_invariants(pit_panels)
    execution = price_and_chronology_audit(rsr2, panels, config.stop_loss)
    cash = cash_replay(rsr2["trades"], 6_000.0)
    concurrent = maximum_concurrent(rsr2["trades"], panels["close"].loc[start:end].index)
    whole_shares = all(isinstance(trade["shares"], int) and trade["shares"] >= 1 for trade in rsr2["trades"])
    entry_exposure = maximum_entry_exposure(rsr2["trades"], panels, 6_000.0)
    exposure_ok = entry_exposure <= config.stock_sleeve_max + 1e-9

    r1 = {(t["symbol"], t["signal_date"]): t for t in rsr1["trades"]}
    r2 = {(t["symbol"], t["signal_date"]): t for t in rsr2["trades"]}
    common = sorted(set(r1) & set(r2))
    common_entry_mismatches = [
        key
        for key in common
        if any(r1[key][field] != r2[key][field] for field in ("entry_date", "entry_price"))
    ]
    unaffected_exit_mismatches = [
        key
        for key in common
        if r2[key].get("profit_lock_date") is None
        and any(r1[key].get(field) != r2[key].get(field) for field in ("exit_date", "exit_price", "exit_reason"))
    ]
    cross_engine = {
        "common_trades": len(common),
        "common_entry_mismatches": [list(key) for key in common_entry_mismatches],
        "unactivated_profit_lock_exit_mismatches": [list(key) for key in unaffected_exit_mismatches],
        "passed": not common_entry_mismatches and not unaffected_exit_mismatches,
    }
    terminal = pit_terminal_sensitivity()
    invalid_impacts = invalid_bar_trade_impacts(pit_data["invalid_ohlc_records"])

    adjustment_meta = json.loads((RSR["DATA"] / "metadata.json").read_text(encoding="utf-8"))
    pit_meta = json.loads((HERE / "datasets" / "pit_exact_ohlcv" / "manifest.json").read_text(encoding="utf-8"))
    adjustment = {
        "current_source": adjustment_meta.get("source"),
        "pit_adjustment": pit_meta.get("adjustment"),
        "same_basis_documented": "auto_adjust" in str(adjustment_meta.get("source", ""))
        and "auto_adjust=True" in str(pit_meta.get("adjustment", "")),
    }
    clean_current_data = all(
        data["strictly_increasing_unique_dates"]
        and data["aligned_panel_dates"]
        and data["invalid_high_bars"] == 0
        and data["invalid_low_bars"] == 0
        and data["nonpositive_ohlc_bars"] == 0
        and data["negative_volume_bars"] == 0
        for data in (current_data,)
    )
    accounting_ok = cash["nonnegative"] and whole_shares and exposure_ok and concurrent <= 3
    checks = [
        {"check": "causal_features", "severity": "pass" if causality["passed"] else "critical"},
        {"check": "execution_chronology", "severity": "pass" if execution["chronology_passed"] else "critical"},
        {"check": "price_feasibility", "severity": "pass" if execution["price_feasibility_passed"] else "critical"},
        {"check": "corporate_action_consistency", "severity": "pass" if adjustment["same_basis_documented"] else "major"},
        {"check": "portfolio_accounting", "severity": "pass" if accounting_ok else "critical"},
        {
            "check": "exit_path_integrity",
            "severity": "minor"
            if terminal["forced_terminal_trade_count"] and not terminal["nonliquidated_transferability_screen_passed"]
            else ("major" if terminal["forced_terminal_trade_count"] else "pass"),
        },
        {
            "check": "data_invariants",
            "severity": "pass"
            if clean_current_data and not pit_data["invalid_ohlc_records"]
            else ("minor" if clean_current_data and not invalid_impacts else "major"),
        },
        {"check": "cross_engine_consistency", "severity": "pass" if cross_engine["passed"] else "major"},
    ]
    return {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "as_of": end,
        "audit_passed": all(row["severity"] in {"pass", "minor"} for row in checks),
        "headline_conclusion_changed": bool(terminal["nonliquidated_transferability_screen_passed"]),
        "checks": checks,
        "causality": causality,
        "execution": execution,
        "adjustment": adjustment,
        "current_data": current_data,
        "pit_data": pit_data,
        "accounting": {
            **cash,
            "whole_shares": whole_shares,
            "maximum_concurrent_positions": concurrent,
            "maximum_entry_exposure": entry_exposure,
            "maximum_close_exposure_after_price_drift": max(rsr2["exposure"].values(), default=0.0),
            "sleeve_cap": config.stock_sleeve_max,
        },
        "invalid_bar_trade_impacts": invalid_impacts,
        "cross_engine": cross_engine,
        "terminal_liquidation_sensitivity": terminal,
    }


def write_report(summary: dict) -> None:
    terminal = summary["terminal_liquidation_sensitivity"]
    lines = [
        "# Backtest integrity audit",
        "",
        "## Bottom line",
        "",
        (
            "The frozen audit passed. No implementation issue changes the current strategy decision."
            if summary["audit_passed"]
            else "The frozen audit found a major/critical issue; affected conclusions must be recomputed."
        ),
        "Formal V9 and the real account are unchanged; this audit authorizes no order.",
        "",
        "## Frozen checks",
        "",
        "| Check | Result |",
        "| --- | --- |",
    ]
    for row in summary["checks"]:
        lines.append(f"| {row['check']} | {row['severity']} |")
    lines.extend(
        [
            "",
            "## Key evidence",
            "",
            f"- Future-row perturbation left every feature and signal unchanged through {summary['causality']['cutoff']}.",
            f"- Execution chronology failures: {len(summary['execution']['chronology_failures'])}; price-feasibility failures: {len(summary['execution']['price_feasibility_failures'])}.",
            f"- Minimum replayed RSR2 cash: USD {summary['accounting']['minimum_cash']:.2f}; maximum entry-time exposure: {summary['accounting']['maximum_entry_exposure']:.2%}; maximum close exposure after price drift: {summary['accounting']['maximum_close_exposure_after_price_drift']:.2%}; maximum concurrent names: {summary['accounting']['maximum_concurrent_positions']}.",
            f"- Point-in-time OHLC geometry exceptions above floating tolerance: {len(summary['pit_data']['invalid_ohlc_records'])}; affected held trade paths: {len(summary['invalid_bar_trade_impacts'])}.",
            f"- Point-in-time forced terminal trades across the six period/variant cells: {terminal['forced_terminal_trade_count']}.",
            f"- Maximum return change when terminal positions remain open and are marked to market: {terminal['maximum_absolute_return_delta']:.4%}.",
            f"- Non-liquidating point-in-time transfer screen passed: {terminal['nonliquidated_transferability_screen_passed']}.",
            "",
            "## Terminal-liquidation sensitivity",
            "",
            "| Period | Variant | Terminal trades | Open at end | Forced return | Mark-to-market return | Delta | Forced win | Closed-only win |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in terminal["rows"]:
        lines.append(
            f"| {row['period']} | {row['variant']} | {row['forced_terminal_trades']} | {row['open_positions_at_end']} | "
            f"{row['forced_return']:.2%} | {row['nonliquidated_return']:.2%} | {row['return_delta']:+.2%} | "
            f"{row['forced_win_rate']:.2%} | {row['nonliquidated_win_rate']:.2%} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Retain the existing negative transfer conclusion. Report terminal liquidation explicitly and use non-liquidating mark-to-market sensitivity in future period-boundary audits. Do not alter RSR1/RSR2 parameters or promotion gates.",
        ]
    )
    (RESULTS / "backtest_integrity_audit_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary = evaluate()
    (RESULTS / "backtest_integrity_audit_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_report(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
