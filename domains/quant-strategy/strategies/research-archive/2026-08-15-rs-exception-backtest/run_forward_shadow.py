#!/usr/bin/env python3
"""Deterministic, research-only runner for the frozen RSR1 forward shadow."""
from __future__ import annotations

import json
import runpy
from datetime import time
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import yfinance as yf


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
RESULTS = HERE / "results"
WATCHLIST = HERE.parents[2] / "references" / "user-selected-watchlist.json"
START = pd.Timestamp("2026-08-17")
VERSION = "RSR1-shadow"
PROFIT_VERSION = "RSR2-profit-lock-shadow"
PROFIT_LOCK_TRIGGER = 0.15
PROFIT_LOCK_FLOOR = 0.05
FIELDS = ("Open", "High", "Low", "Close", "Volume")
CBOE = {
    "^VIX": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv",
    "^VIX3M": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv",
}
LEDGER_COLUMNS = [
    "as_of",
    "version",
    "symbol",
    "signal_status",
    "signal_date",
    "planned_execution_date",
    "entry_price",
    "entry_gap",
    "shares",
    "exit_date",
    "exit_price",
    "exit_reason",
    "net_pnl",
    "return",
    "baseline_action",
    "source_complete",
    "notes",
]
SIGNAL_COLUMNS = [
    "date",
    "symbol",
    "matched_baseline_signal",
    "risk_filter_signal",
    "reject_reason",
    "smh_healthy",
    "rs20",
    "volume_ratio",
    "atr_pct",
    "close_location",
]
PROFIT_LEDGER_COLUMNS = [
    "as_of",
    "version",
    "symbol",
    "signal_status",
    "signal_date",
    "planned_execution_date",
    "entry_price",
    "entry_gap",
    "shares",
    "profit_lock_date",
    "profit_lock_stop",
    "exit_date",
    "exit_price",
    "exit_reason",
    "net_pnl",
    "return",
    "rsr1_action",
    "source_complete",
    "notes",
]
BASELINE_TRADE_COLUMNS = [
    "symbol",
    "signal_date",
    "entry_date",
    "entry_price",
    "shares",
    "entry_type",
    "smh_healthy_on_signal",
    "rs20_on_signal",
    "volume_ratio_on_signal",
    "ranking_mode",
    "ranking_score",
    "entry_gap",
    "exit_date",
    "exit_price",
    "exit_reason",
    "pnl",
    "return",
]
NON_COMMON_FACTOR_THEMES = {"consumer_defensive_beverages", "space_satellite"}


def watchlist_theme_map() -> dict[str, str]:
    raw = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    return {item["symbol"]: item["theme"] for item in raw["tickers"]}


def baseline_trade_frame(trades: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(trades).reindex(columns=BASELINE_TRADE_COLUMNS)


def shadow_universe(all_symbols: list[str]) -> list[str]:
    themes = watchlist_theme_map()
    return [symbol for symbol in all_symbols if themes[symbol] not in NON_COMMON_FACTOR_THEMES]


def frozen_configs():
    common = dict(
        rs20_min=0.03,
        volume_ratio_min=1.20,
        max_extension=0.12,
        max_hold_days=20,
        stop_loss=0.08,
    )
    matched_baseline = MODULE["Config"](**common, max_atr_pct=1.00, min_close_location=0.00)
    candidate = MODULE["Config"](**common, max_atr_pct=0.04, min_close_location=0.50)
    return matched_baseline, candidate


def completed_cutoff(now: pd.Timestamp | None = None) -> pd.Timestamp:
    if now is None:
        now = pd.Timestamp.now(tz="UTC")
    elif now.tzinfo is None:
        now = now.tz_localize("UTC")
    eastern = now.tz_convert(ZoneInfo("America/New_York"))
    cutoff = pd.Timestamp(eastern.date())
    if eastern.weekday() < 5 and eastern.time() >= time(18, 0):
        return cutoff
    cutoff -= pd.Timedelta(days=1)
    while cutoff.weekday() >= 5:
        cutoff -= pd.Timedelta(days=1)
    return cutoff


def extract_series(data: pd.DataFrame, field: str) -> pd.Series:
    selected = data[field]
    if isinstance(selected, pd.DataFrame):
        selected = selected.iloc[:, 0]
    selected.index = pd.to_datetime(selected.index).tz_localize(None)
    return pd.to_numeric(selected, errors="coerce").dropna()


def extend_panels(now: pd.Timestamp | None = None):
    panels, symbols = MODULE["load_panels"]()
    cutoff = completed_cutoff(now)
    cached_end = panels["close"]["SPY"].dropna().index[-1]
    request_start = cached_end - pd.Timedelta(days=7)
    request_end = cutoff + pd.Timedelta(days=2)
    required = sorted(set(symbols) | {"SPY", "QQQ", "SMH", "^VIX", "^VIX3M"})
    source_status: dict[str, dict] = {}
    for symbol in required:
        if symbol in CBOE:
            continue
        try:
            data = yf.download(
                symbol,
                start=str(request_start.date()),
                end=str(request_end.date()),
                auto_adjust=True,
                progress=False,
                threads=False,
            )
            if data.empty:
                raise RuntimeError("empty download")
            last_values = None
            for field in FIELDS:
                values = extract_series(data, field)
                last_values = values
                key = field.lower()
                index = panels[key].index.union(values.index)
                panels[key] = panels[key].reindex(index)
                panels[key].loc[values.index, symbol] = values
            source_status[symbol] = {
                "source": "Yahoo Finance via yfinance",
                "last_date": str(last_values.index[-1].date()),
                "error": None,
            }
        except Exception as error:
            source_status[symbol] = {"source": None, "last_date": None, "error": str(error)}
    for symbol, url in CBOE.items():
        try:
            data = pd.read_csv(url)
            data.columns = [str(column).strip().upper() for column in data.columns]
            data.index = pd.to_datetime(data.pop("DATE"), errors="coerce")
            last_values = None
            for field in ("OPEN", "HIGH", "LOW", "CLOSE"):
                values = pd.to_numeric(data[field], errors="coerce").dropna().loc[:cutoff]
                last_values = values
                key = field.lower()
                index = panels[key].index.union(values.index)
                panels[key] = panels[key].reindex(index)
                panels[key].loc[values.index, symbol] = values
            source_status[symbol] = {
                "source": "Cboe official daily history",
                "last_date": str(last_values.index[-1].date()),
                "error": None,
            }
        except Exception as error:
            source_status[symbol] = {"source": None, "last_date": None, "error": str(error)}
    equity_dates = panels["close"]["SPY"].dropna().index
    equity_dates = equity_dates[equity_dates <= cutoff]
    panels = {field: frame.reindex(equity_dates).sort_index() for field, frame in panels.items()}
    core = ["SPY", "QQQ", "SMH", "^VIX", "^VIX3M"]
    common_dates = panels["close"][core].dropna().index
    as_of = common_dates[-1]
    required_fields = {
        symbol: ("open", "high", "low", "close") if symbol in CBOE else ("open", "high", "low", "close", "volume")
        for symbol in required
    }
    missing_latest = []
    for symbol, fields in required_fields.items():
        if any(symbol not in panels[field] or pd.isna(panels[field].at[as_of, symbol]) for field in fields):
            missing_latest.append(symbol)
    source_complete = not missing_latest and as_of >= cutoff
    return panels, symbols, source_status, as_of, cutoff, source_complete, missing_latest


def signal_rows(panels, symbols, start: pd.Timestamp, as_of: pd.Timestamp) -> pd.DataFrame:
    baseline_config, candidate_config = frozen_configs()
    baseline = MODULE["build_features"](panels, symbols, baseline_config)
    candidate = MODULE["build_features"](panels, symbols, candidate_config)
    rows = []
    dates = panels["close"].loc[start:as_of].index
    for date in dates:
        smh_healthy = bool(baseline["smh_healthy"].at[date])
        for symbol in symbols:
            baseline_signal = smh_healthy and bool(baseline["signal"].at[date, symbol])
            candidate_signal = smh_healthy and bool(candidate["signal"].at[date, symbol])
            if not baseline_signal and not candidate_signal:
                continue
            reasons = []
            atr = float(candidate["atr_pct"].at[date, symbol])
            close_location = float(candidate["close_location"].at[date, symbol])
            if baseline_signal and not candidate_signal:
                if not np.isfinite(atr) or atr > 0.04:
                    reasons.append("atr_pct")
                if not np.isfinite(close_location) or close_location < 0.50:
                    reasons.append("close_location")
            rows.append(
                {
                    "date": str(date.date()),
                    "symbol": symbol,
                    "matched_baseline_signal": baseline_signal,
                    "risk_filter_signal": candidate_signal,
                    "reject_reason": "+".join(reasons),
                    "smh_healthy": smh_healthy,
                    "rs20": float(candidate["rs20"].at[date, symbol]),
                    "volume_ratio": float(candidate["volume_ratio"].at[date, symbol]),
                    "atr_pct": atr,
                    "close_location": close_location,
                }
            )
    return pd.DataFrame(rows, columns=SIGNAL_COLUMNS)


def run_pair(panels, symbols, start: pd.Timestamp, as_of: pd.Timestamp, slippage: float) -> dict[str, dict]:
    baseline_config, candidate_config = frozen_configs()
    return {
        "matched_baseline": MODULE["simulate"](
            panels,
            symbols,
            baseline_config,
            "strict_veto",
            str(start.date()),
            str(as_of.date()),
            liquidate_final=False,
            slippage=slippage,
        ),
        "risk_filter": MODULE["simulate"](
            panels,
            symbols,
            candidate_config,
            "strict_veto",
            str(start.date()),
            str(as_of.date()),
            liquidate_final=False,
            slippage=slippage,
        ),
    }


def next_session(signal_date: str, dates: pd.DatetimeIndex) -> str:
    later = dates[dates > pd.Timestamp(signal_date)]
    return str(later[0].date()) if len(later) else "next_session"


def trade_ledger(candidate: dict, baseline: dict, as_of: pd.Timestamp, dates: pd.DatetimeIndex) -> pd.DataFrame:
    baseline_keys = {(trade["signal_date"], trade["symbol"]) for trade in baseline["trades"]}
    baseline_pending_keys = {
        (order["signal_date"], order["symbol"]) for order in baseline["pending_entries"]
    }
    rows = []
    for trade in candidate["trades"]:
        closed = trade.get("exit_date") is not None
        rows.append(
            {
                "as_of": str(as_of.date()),
                "version": VERSION,
                "symbol": trade["symbol"],
                "signal_status": "closed" if closed else "open",
                "signal_date": trade["signal_date"],
                "planned_execution_date": trade["entry_date"],
                "entry_price": trade["entry_price"],
                "entry_gap": trade.get("entry_gap"),
                "shares": trade["shares"],
                "exit_date": trade.get("exit_date"),
                "exit_price": trade.get("exit_price"),
                "exit_reason": trade.get("exit_reason"),
                "net_pnl": trade.get("pnl"),
                "return": trade.get("return"),
                "baseline_action": "entered" if (trade["signal_date"], trade["symbol"]) in baseline_keys else "not_entered",
                "source_complete": True,
                "notes": "research-only; no order authorization",
            }
        )
    traded_keys = {(row["signal_date"], row["symbol"]) for row in rows}
    for order in candidate["pending_entries"]:
        key = (order["signal_date"], order["symbol"])
        if key in traded_keys:
            continue
        rows.append(
            {
                "as_of": str(as_of.date()),
                "version": VERSION,
                "symbol": order["symbol"],
                "signal_status": "pending",
                "signal_date": order["signal_date"],
                "planned_execution_date": next_session(order["signal_date"], dates),
                "entry_price": None,
                "entry_gap": None,
                "shares": None,
                "exit_date": None,
                "exit_price": None,
                "exit_reason": None,
                "net_pnl": None,
                "return": None,
                "baseline_action": (
                    "entered" if key in baseline_keys else "pending" if key in baseline_pending_keys else "not_entered"
                ),
                "source_complete": True,
                "notes": "research-only; no order authorization",
            }
        )
    return pd.DataFrame(rows, columns=LEDGER_COLUMNS)


def profit_lock_ledger(challenger: dict, rsr1: dict, as_of: pd.Timestamp, dates: pd.DatetimeIndex) -> pd.DataFrame:
    rsr1_keys = {(trade["signal_date"], trade["symbol"]) for trade in rsr1["trades"]}
    rsr1_pending = {(order["signal_date"], order["symbol"]) for order in rsr1["pending_entries"]}
    rows = []
    for trade in challenger["trades"]:
        key = (trade["signal_date"], trade["symbol"])
        closed = trade.get("exit_date") is not None
        rows.append(
            {
                "as_of": str(as_of.date()),
                "version": PROFIT_VERSION,
                "symbol": trade["symbol"],
                "signal_status": "closed" if closed else "open",
                "signal_date": trade["signal_date"],
                "planned_execution_date": trade["entry_date"],
                "entry_price": trade["entry_price"],
                "entry_gap": trade.get("entry_gap"),
                "shares": trade["shares"],
                "profit_lock_date": trade.get("profit_lock_date"),
                "profit_lock_stop": trade.get("profit_lock_stop"),
                "exit_date": trade.get("exit_date"),
                "exit_price": trade.get("exit_price"),
                "exit_reason": trade.get("exit_reason"),
                "net_pnl": trade.get("pnl"),
                "return": trade.get("return"),
                "rsr1_action": "entered" if key in rsr1_keys else "not_entered",
                "source_complete": True,
                "notes": "research-only; separate RSR2 exit challenger; no order authorization",
            }
        )
    traded_keys = {(row["signal_date"], row["symbol"]) for row in rows}
    for order in challenger["pending_entries"]:
        key = (order["signal_date"], order["symbol"])
        if key in traded_keys:
            continue
        rows.append(
            {
                "as_of": str(as_of.date()),
                "version": PROFIT_VERSION,
                "symbol": order["symbol"],
                "signal_status": "pending",
                "signal_date": order["signal_date"],
                "planned_execution_date": next_session(order["signal_date"], dates),
                "entry_price": None,
                "entry_gap": None,
                "shares": None,
                "profit_lock_date": None,
                "profit_lock_stop": None,
                "exit_date": None,
                "exit_price": None,
                "exit_reason": None,
                "net_pnl": None,
                "return": None,
                "rsr1_action": "entered" if key in rsr1_keys else "pending" if key in rsr1_pending else "not_entered",
                "source_complete": True,
                "notes": "research-only; separate RSR2 exit challenger; no order authorization",
            }
        )
    return pd.DataFrame(rows, columns=PROFIT_LEDGER_COLUMNS)


def theme_for(symbol: str) -> str:
    return watchlist_theme_map().get(symbol, "unknown")


def symbol_profit_concentration(trades: list[dict]) -> dict:
    profit_by_symbol: dict[str, float] = {}
    for trade in trades:
        pnl = trade.get("pnl")
        if pnl is None or pnl <= 0:
            continue
        symbol = trade["symbol"]
        profit_by_symbol[symbol] = profit_by_symbol.get(symbol, 0.0) + float(pnl)
    gross_profit = sum(profit_by_symbol.values())
    max_share = max(profit_by_symbol.values(), default=0.0) / gross_profit if gross_profit else 1.0
    return {
        "gross_profit": gross_profit,
        "profit_by_symbol": dict(sorted(profit_by_symbol.items())),
        "max_symbol_profit_share": max_share,
    }


def promotion_gate(pair_10: dict[str, dict], pair_20: dict[str, dict], sessions: int) -> dict:
    baseline = pair_10["matched_baseline"]
    candidate = pair_10["risk_filter"]
    candidate_metrics = candidate["metrics"]
    baseline_metrics = baseline["metrics"]
    closed = [trade for trade in candidate["trades"] if trade.get("pnl") is not None]
    profit_concentration = symbol_profit_concentration(closed)
    max_profit_share = profit_concentration["max_symbol_profit_share"]
    themes = {theme_for(trade["symbol"]) for trade in closed}
    sample_ready = sessions >= 126 and len(closed) >= 20
    win_delta = None
    if candidate_metrics["win_rate"] is not None and baseline_metrics["win_rate"] is not None:
        win_delta = candidate_metrics["win_rate"] - baseline_metrics["win_rate"]
    baseline_fixed_20 = MODULE["fixed_path_cost_stress"](
        baseline, source_slippage=0.001, stressed_slippage=0.002
    )
    candidate_fixed_20 = MODULE["fixed_path_cost_stress"](
        candidate, source_slippage=0.001, stressed_slippage=0.002
    )
    checks = {
        "sessions_at_least_126": sessions >= 126,
        "closed_trades_at_least_20": len(closed) >= 20,
        "themes_at_least_3": len(themes) >= 3,
        "max_symbol_profit_share_at_most_35pct": max_profit_share <= 0.35,
        "net_return_not_below_baseline": candidate_metrics["total_return"] >= baseline_metrics["total_return"],
        "win_rate_delta_at_least_5pp": win_delta is not None and win_delta >= 0.05,
        "profit_factor_at_least_1_30": candidate_metrics["profit_factor"] is not None
        and candidate_metrics["profit_factor"] >= 1.30,
        "sharpe_not_below_baseline": candidate_metrics["sharpe"] >= baseline_metrics["sharpe"],
        "max_drawdown_not_worse_by_1pp": candidate_metrics["max_drawdown"]
        >= baseline_metrics["max_drawdown"] - 0.01,
        "survives_20bps": pair_20["risk_filter"]["metrics"]["total_return"]
        >= pair_20["matched_baseline"]["metrics"]["total_return"],
        "survives_fixed_path_20bps": candidate_fixed_20["total_return"]
        >= baseline_fixed_20["total_return"],
    }
    return {
        "sample_ready": sample_ready,
        "eligible_for_review": sample_ready and all(checks.values()),
        "sessions": sessions,
        "closed_trades": len(closed),
        "themes": sorted(themes),
        "max_symbol_profit_share": max_profit_share,
        "gross_profit": profit_concentration["gross_profit"],
        "profit_by_symbol": profit_concentration["profit_by_symbol"],
        "win_rate_delta": win_delta,
        "fixed_path_20bps": {
            "matched_baseline": baseline_fixed_20,
            "risk_filter": candidate_fixed_20,
        },
        "checks": checks,
    }


def profit_lock_promotion_gate(
    rsr1_10: dict,
    challenger_10: dict,
    rsr1_20: dict,
    challenger_20: dict,
    sessions: int,
) -> dict:
    rsr1_metrics = rsr1_10["metrics"]
    challenger_metrics = challenger_10["metrics"]
    closed = [trade for trade in challenger_10["trades"] if trade.get("pnl") is not None]
    concentration = symbol_profit_concentration(closed)
    themes = {theme_for(trade["symbol"]) for trade in closed}
    win_delta = None
    if challenger_metrics["win_rate"] is not None and rsr1_metrics["win_rate"] is not None:
        win_delta = challenger_metrics["win_rate"] - rsr1_metrics["win_rate"]
    rsr1_fixed_20 = MODULE["fixed_path_cost_stress"](rsr1_10, 0.001, 0.002)
    challenger_fixed_20 = MODULE["fixed_path_cost_stress"](challenger_10, 0.001, 0.002)
    checks = {
        "sessions_at_least_126": sessions >= 126,
        "closed_trades_at_least_20": len(closed) >= 20,
        "themes_at_least_3": len(themes) >= 3,
        "max_symbol_profit_share_at_most_35pct": concentration["max_symbol_profit_share"] <= 0.35,
        "net_return_not_below_rsr1": challenger_metrics["total_return"] >= rsr1_metrics["total_return"],
        "win_rate_not_below_rsr1": win_delta is not None and win_delta >= 0.0,
        "profit_factor_at_least_1_30": challenger_metrics["profit_factor"] is not None
        and challenger_metrics["profit_factor"] >= 1.30,
        "sharpe_not_below_rsr1": challenger_metrics["sharpe"] >= rsr1_metrics["sharpe"],
        "max_drawdown_not_worse_by_1pp": challenger_metrics["max_drawdown"]
        >= rsr1_metrics["max_drawdown"] - 0.01,
        "survives_20bps_vs_rsr1": challenger_20["metrics"]["total_return"]
        >= rsr1_20["metrics"]["total_return"],
        "survives_fixed_path_20bps_vs_rsr1": challenger_fixed_20["total_return"]
        >= rsr1_fixed_20["total_return"],
    }
    sample_ready = sessions >= 126 and len(closed) >= 20
    return {
        "sample_ready": sample_ready,
        "eligible_for_review": sample_ready and all(checks.values()),
        "sessions": sessions,
        "closed_trades": len(closed),
        "themes": sorted(themes),
        "max_symbol_profit_share": concentration["max_symbol_profit_share"],
        "gross_profit": concentration["gross_profit"],
        "profit_by_symbol": concentration["profit_by_symbol"],
        "win_rate_delta_vs_rsr1": win_delta,
        "fixed_path_20bps": {"rsr1": rsr1_fixed_20, "challenger": challenger_fixed_20},
        "checks": checks,
    }


def write_status(output: dict) -> None:
    lines = [
        "# RSR1 forward-shadow status",
        "",
        f"- Status: `{output['status']}`",
        f"- Completed data through: `{output['as_of']}`",
        f"- Required start: `{START.date()}`",
        f"- Shadow universe: `{output['shadow_universe']}` ({output['shadow_symbol_count']} symbols)",
        "- Excluded from shadow but retained in full-watchlist analysis: `"
        + ", ".join(output["excluded_from_shadow_but_retained_in_full_watchlist_analysis"])
        + "`",
        f"- Source complete: `{output['source_complete']}`",
        f"- Full-watchlist source complete: `{output['full_watchlist_source_complete']}`",
        "- Formal V9 modified: `false`",
        "- Live-order authorization: `false`",
        f"- Separate exit challenger: `{PROFIT_VERSION}` (close +{PROFIT_LOCK_TRIGGER:.0%} -> next-session stop +{PROFIT_LOCK_FLOOR:.0%})",
        "",
    ]
    if output.get("message"):
        lines.append(output["message"])
        lines.append("")
    if output.get("pair_10bps"):
        lines.extend(
            [
                "| Variant | MTM return | Max DD | Sharpe | Closed trades | Win rate | Open positions |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
            ]
        )
        for name, result in output["pair_10bps"].items():
            metrics = result["metrics"]
            win = "n/a" if metrics["win_rate"] is None else f"{metrics['win_rate']:.2%}"
            lines.append(
                f"| {name} | {metrics['total_return']:.2%} | {metrics['max_drawdown']:.2%} | "
                f"{metrics['sharpe']:.2f} | {metrics['trade_count']} | {win} | {len(result['open_positions'])} |"
            )
    (RESULTS / "forward_shadow_status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, symbols, sources, as_of, cutoff, source_complete, missing_latest = extend_panels()
    forward_symbols = shadow_universe(symbols)
    core_symbols = {"SPY", "QQQ", "SMH", "^VIX", "^VIX3M"}
    forward_missing = sorted(set(missing_latest) & (set(forward_symbols) | core_symbols))
    forward_source_complete = not forward_missing and as_of >= cutoff
    output = {
        "version": VERSION,
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "as_of": str(as_of.date()),
        "expected_completed_cutoff": str(cutoff.date()),
        "status": "awaiting_start",
        "research_only": True,
        "formal_v9_modified": False,
        "live_order_authorization": False,
        "source_complete": forward_source_complete,
        "missing_latest": forward_missing,
        "full_watchlist_source_complete": source_complete,
        "full_watchlist_missing_latest": missing_latest,
        "shadow_universe": "ai_capex_broad",
        "shadow_symbol_count": len(forward_symbols),
        "shadow_symbols": forward_symbols,
        "excluded_from_shadow_but_retained_in_full_watchlist_analysis": sorted(set(symbols) - set(forward_symbols)),
        "profit_protection_shadow": {
            "version": PROFIT_VERSION,
            "status": "awaiting_start",
            "trigger": PROFIT_LOCK_TRIGGER,
            "floor": PROFIT_LOCK_FLOOR,
            "activation_basis": "completed_close_effective_next_session",
            "benchmark": VERSION,
            "separate_ledger": "forward_profit_protection_ledger.csv",
        },
        "sources": sources,
        "message": "No completed U.S. session at or after the preregistered start; the ledgers were not changed.",
    }
    if as_of >= START and not forward_source_complete:
        output["status"] = "data_incomplete"
        output["profit_protection_shadow"]["status"] = "data_incomplete"
        output["message"] = "Forward data are incomplete. The existing ledgers were preserved and no observation was recorded."
    elif as_of >= START:
        signals = signal_rows(panels, forward_symbols, START, as_of)
        sessions = len(panels["close"].loc[START:as_of].index)
        output["status"] = "observing"
        output["profit_protection_shadow"]["status"] = "observing"
        output["message"] = "Forward observations recorded; they do not authorize an order."
        output["sessions"] = sessions
        output["signal_counts"] = {
            "matched_baseline": int(signals.get("matched_baseline_signal", pd.Series(dtype=bool)).sum()),
            "risk_filter": int(signals.get("risk_filter_signal", pd.Series(dtype=bool)).sum()),
        }
        signals.to_csv(RESULTS / "forward_shadow_signals.csv", index=False)
        if sessions >= 2:
            pair_10 = run_pair(panels, forward_symbols, START, as_of, 0.001)
            pair_20 = run_pair(panels, forward_symbols, START, as_of, 0.002)
            _, candidate_config = frozen_configs()
            profit_challenger_10 = MODULE["simulate"](
                panels,
                forward_symbols,
                candidate_config,
                "strict_veto",
                str(START.date()),
                str(as_of.date()),
                liquidate_final=False,
                slippage=0.001,
                profit_lock_trigger=PROFIT_LOCK_TRIGGER,
                profit_lock_floor=PROFIT_LOCK_FLOOR,
            )
            profit_challenger_20 = MODULE["simulate"](
                panels,
                forward_symbols,
                candidate_config,
                "strict_veto",
                str(START.date()),
                str(as_of.date()),
                liquidate_final=False,
                slippage=0.002,
                profit_lock_trigger=PROFIT_LOCK_TRIGGER,
                profit_lock_floor=PROFIT_LOCK_FLOOR,
            )
            ledger = trade_ledger(
                pair_10["risk_filter"], pair_10["matched_baseline"], as_of, panels["close"].index
            )
            ledger.to_csv(RESULTS / "forward_shadow_ledger.csv", index=False)
            profit_ledger = profit_lock_ledger(
                profit_challenger_10,
                pair_10["risk_filter"],
                as_of,
                panels["close"].index,
            )
            profit_ledger.to_csv(RESULTS / "forward_profit_protection_ledger.csv", index=False)
            baseline_trade_frame(pair_10["matched_baseline"]["trades"]).to_csv(
                RESULTS / "forward_shadow_baseline_trades.csv", index=False
            )
            output["pair_10bps"] = pair_10
            output["pair_20bps"] = pair_20
            output["promotion_gate"] = promotion_gate(pair_10, pair_20, sessions)
            output["profit_protection_10bps"] = {
                "rsr1": pair_10["risk_filter"],
                "challenger": profit_challenger_10,
            }
            output["profit_protection_20bps"] = {
                "rsr1": pair_20["risk_filter"],
                "challenger": profit_challenger_20,
            }
            output["profit_protection_promotion_gate"] = profit_lock_promotion_gate(
                pair_10["risk_filter"],
                profit_challenger_10,
                pair_20["risk_filter"],
                profit_challenger_20,
                sessions,
            )
        else:
            output["message"] = "First completed shadow session recorded; no next-open execution is possible yet."
    (RESULTS / "forward_shadow_status.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_status(output)
    print(json.dumps({key: output[key] for key in ("status", "as_of", "source_complete", "message")}, indent=2))


if __name__ == "__main__":
    main()
