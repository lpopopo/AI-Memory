#!/usr/bin/env python3
"""Whole-share, shared-cash comparison of formal 70/25 and challenger 80/20."""
from __future__ import annotations

import json
import math
import runpy
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
QUANT_ROOT = HERE.parents[2]
V9 = QUANT_ROOT / "strategies" / "v9-execution"
sys.path.insert(0, str(V9 / "scripts"))

from v9_data import load_data  # noqa: E402
from v9_information_strategy import V9Backtester, V9Config  # noqa: E402


BACKTEST = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
FRONTIER = runpy.run_path(str(HERE / "evaluate_core_allocation_frontier.py"))
RESULTS = HERE / "results"
ARCHITECTURES = {
    "formal_70_25": {"core_cap": 0.70, "stock_cap": 0.25},
    "challenger_80_20": {"core_cap": 0.80, "stock_cap": 0.20},
}
NAVS = (6_000.0, 5_751.77)
PERIODS = {
    "train_2024_2025": ("2024-01-02", "2025-12-31", "2023-01-03"),
    "heldout_2026": ("2026-01-02", None, "2024-01-02"),
    "full_2024_2026": ("2024-01-02", None, "2023-01-03"),
}
SLIPPAGE = 0.001
COMMISSION = 1.0
TARGET_STOCK_WEIGHT = 0.08
STOCK_SINGLE_MAX = 0.15
MIN_NOTIONAL = 200.0


def _safe(frame: pd.DataFrame, date: pd.Timestamp, symbol: str) -> float | None:
    try:
        value = float(frame.at[date, symbol])
    except (KeyError, TypeError, ValueError):
        return None
    return value if np.isfinite(value) and value > 0 else None


def stitch_core_history(
    historical: dict[str, pd.DataFrame],
    historical_vix: pd.DataFrame,
    current: dict[str, pd.DataFrame],
    current_vix: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    current_start = current["close"].index.min()
    panels = {}
    for field in ("open", "high", "low", "close", "volume"):
        old = historical[field][["SPY", "QQQ"]].loc[
            historical[field].index < current_start
        ]
        new = current[field][["SPY", "QQQ"]]
        panels[field] = pd.concat([old, new]).sort_index()
        panels[field] = panels[field][~panels[field].index.duplicated(keep="last")]
    old_vix = historical_vix.loc[historical_vix.index < current_start]
    vix = pd.concat([old_vix, current_vix[["^VIX", "^VIX3M"]]]).sort_index()
    vix = vix[~vix.index.duplicated(keep="last")].reindex(panels["close"].index).ffill()
    return panels, vix


def core_execution_schedule(
    panels: dict[str, pd.DataFrame],
    vix: pd.DataFrame,
    core_cap: float,
    start: str,
    end: str,
    warmup: str,
) -> tuple[dict[pd.Timestamp, dict], dict]:
    engine = V9Backtester(
        panels,
        vix,
        [],
        V9Config(v8_core_weight=core_cap, info_sleeve_weight=1.0 - core_cap),
        [],
    )
    result = engine.run(warmup_start=warmup, trading_start=start, trading_end=end)
    ledger = pd.DataFrame(result.ledger)
    if ledger.empty:
        return {}, {"fractional_transactions": 0, "fractional_turnover": 0.0}
    ledger["date"] = pd.to_datetime(ledger["date"])
    core_ledger = ledger.loc[ledger["reason"] == "v8_rebalance"].copy()
    schedule = {}
    for date, block in core_ledger.groupby("date"):
        base = engine.v8_base_weights.get(pd.Timestamp(date), {})
        effective_cap, _, _ = engine._effective_sleeve_caps(pd.Timestamp(date))
        schedule[pd.Timestamp(date)] = {
            "trade_symbols": sorted(set(block["symbol"])),
            "targets": {
                symbol: float(base.get(symbol, 0.0) * effective_cap)
                for symbol in ("SPY", "QQQ")
            },
        }
    return schedule, {
        "fractional_transactions": int(len(core_ledger)),
        "fractional_turnover": float(result.diagnostics["turnover"]),
    }


def desired_whole_shares(nav: float, target_weight: float, raw_price: float) -> int:
    fill = raw_price * (1.0 + SLIPPAGE)
    return max(math.floor(max(nav * target_weight - COMMISSION, 0.0) / fill), 0)


def _period_returns(curve: pd.Series, frequency: str = "M") -> pd.Series:
    values = curve.groupby(curve.index.to_period(frequency)).last()
    returns = values.pct_change()
    if len(returns):
        returns.iloc[0] = values.iloc[0] / curve.iloc[0] - 1.0
    return returns.dropna()


def combined_metrics(curve: pd.Series, initial_nav: float) -> dict[str, float]:
    daily = curve.pct_change(fill_method=None).dropna()
    drawdown = curve / curve.cummax() - 1.0
    std = float(daily.std(ddof=0))
    monthly = _period_returns(curve)
    return {
        "final_value": float(curve.iloc[-1]),
        "total_return": float(curve.iloc[-1] / initial_nav - 1.0),
        "max_drawdown": float(drawdown.min()),
        "sharpe": float(daily.mean() / std * math.sqrt(252)) if std else 0.0,
        "monthly_win_rate": float((monthly > 0).mean()) if len(monthly) else 0.0,
        "sessions": int(len(curve)),
    }


def simulate_shared(
    panels: dict[str, pd.DataFrame],
    core_schedule: dict[pd.Timestamp, dict],
    source_stock_run: dict,
    core_cap: float,
    stock_cap: float,
    initial_nav: float,
    start: str,
    end: str,
) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    dates = panels["close"].loc[start:end].dropna(subset=["SPY", "QQQ"]).index
    if len(dates) < 2:
        raise RuntimeError(f"insufficient shared-capital dates for {start}..{end}")
    trades = [dict(trade, source_trade_id=i) for i, trade in enumerate(source_stock_run["trades"])]
    entries: dict[pd.Timestamp, list[dict]] = {}
    exits: dict[pd.Timestamp, list[dict]] = {}
    for trade in trades:
        entries.setdefault(pd.Timestamp(trade["entry_date"]), []).append(trade)
        if trade.get("exit_date"):
            exits.setdefault(pd.Timestamp(trade["exit_date"]), []).append(trade)

    cash = float(initial_nav)
    core_shares = {"SPY": 0, "QQQ": 0}
    stock_positions: dict[int, dict] = {}
    desired_targets = {"SPY": 0.0, "QQQ": 0.0}
    ledger_rows = []
    daily_rows = []
    costs = 0.0
    planned_entries = len(trades)
    filled_entries = skipped_entries = reduced_entries = 0
    core_shortfall_events = 0
    realized_stock_pnl = []

    def stock_value(date: pd.Timestamp, field: str = "close") -> float:
        value = 0.0
        for pos in stock_positions.values():
            price = _safe(panels[field], date, pos["symbol"])
            value += pos["shares"] * (price or pos["entry_fill"])
        return value

    def core_value(date: pd.Timestamp) -> float:
        return sum(
            core_shares[symbol] * (_safe(panels["close"], date, symbol) or 0.0)
            for symbol in ("SPY", "QQQ")
        )

    for date in dates:
        # Frozen stock exits release shared cash before any same-session entries.
        for trade in exits.get(date, []):
            trade_id = trade["source_trade_id"]
            if trade_id not in stock_positions:
                continue
            pos = stock_positions.pop(trade_id)
            fill = float(trade["exit_price"])
            proceeds = pos["shares"] * fill - COMMISSION
            cash += proceeds
            raw_fill = fill / (1.0 - SLIPPAGE)
            trade_cost = COMMISSION + pos["shares"] * raw_fill * SLIPPAGE
            costs += trade_cost
            pnl = proceeds - pos["cost_basis"]
            realized_stock_pnl.append(pnl)
            ledger_rows.append(
                {
                    "date": date,
                    "module": "rsr2",
                    "symbol": pos["symbol"],
                    "action": "SELL",
                    "shares": pos["shares"],
                    "fill": fill,
                    "cash_after": cash,
                    "reason": trade.get("exit_reason"),
                    "source_trade_id": trade_id,
                }
            )

        for trade in entries.get(date, []):
            fill = float(trade["entry_price"])
            nav_open = cash + stock_value(date, "open") + sum(
                core_shares[symbol] * (_safe(panels["open"], date, symbol) or 0.0)
                for symbol in ("SPY", "QQQ")
            )
            shares = math.floor(max(nav_open * TARGET_STOCK_WEIGHT - COMMISSION, 0.0) / fill)
            if shares < 1 and fill + COMMISSION <= nav_open * STOCK_SINGLE_MAX:
                shares = 1
            planned_shares = shares
            existing_stock = stock_value(date, "open")
            while shares > 0:
                notional = shares * fill
                valid = (
                    notional >= MIN_NOTIONAL
                    and 2 * COMMISSION / notional <= 0.01
                    and notional <= nav_open * STOCK_SINGLE_MAX + 1e-9
                    and existing_stock + notional <= nav_open * stock_cap + 1e-9
                    and notional + COMMISSION <= cash + 1e-9
                )
                if valid:
                    break
                shares -= 1
            if shares < planned_shares and shares > 0:
                reduced_entries += 1
            if shares < 1:
                skipped_entries += 1
                continue
            notional = shares * fill
            cash -= notional + COMMISSION
            raw_open = _safe(panels["open"], date, trade["symbol"]) or fill / (1.0 + SLIPPAGE)
            trade_cost = COMMISSION + shares * raw_open * SLIPPAGE
            costs += trade_cost
            stock_positions[trade["source_trade_id"]] = {
                "symbol": trade["symbol"],
                "shares": shares,
                "entry_fill": fill,
                "cost_basis": notional + COMMISSION,
            }
            filled_entries += 1
            ledger_rows.append(
                {
                    "date": date,
                    "module": "rsr2",
                    "symbol": trade["symbol"],
                    "action": "BUY",
                    "shares": shares,
                    "fill": fill,
                    "cash_after": cash,
                    "reason": "frozen_entry",
                    "source_trade_id": trade["source_trade_id"],
                }
            )

        if date in core_schedule:
            event = core_schedule[date]
            desired_targets = dict(event["targets"])
            prices = {
                symbol: _safe(panels["close"], date, symbol)
                for symbol in ("SPY", "QQQ")
            }
            if not all(prices.values()):
                raise RuntimeError(f"missing core close on {date.date()}")
            pre_nav = cash + stock_value(date) + core_value(date)
            desired = {
                symbol: desired_whole_shares(pre_nav, desired_targets[symbol], prices[symbol])
                for symbol in event["trade_symbols"]
            }
            # Sells first so both ETFs have equal access to released cash.
            for symbol in event["trade_symbols"]:
                current = core_shares[symbol]
                if current <= desired[symbol]:
                    continue
                shares = current - desired[symbol]
                fill = prices[symbol] * (1.0 - SLIPPAGE)
                cash += shares * fill - COMMISSION
                costs += COMMISSION + shares * prices[symbol] * SLIPPAGE
                core_shares[symbol] -= shares
                ledger_rows.append(
                    {
                        "date": date,
                        "module": "core",
                        "symbol": symbol,
                        "action": "SELL",
                        "shares": shares,
                        "fill": fill,
                        "cash_after": cash,
                        "reason": "v9_core_rebalance",
                        "source_trade_id": None,
                    }
                )
            buy_order = sorted(
                event["trade_symbols"],
                key=lambda symbol: (desired[symbol] - core_shares[symbol]) * prices[symbol],
                reverse=True,
            )
            for symbol in buy_order:
                requested = max(desired[symbol] - core_shares[symbol], 0)
                if requested < 1:
                    continue
                fill = prices[symbol] * (1.0 + SLIPPAGE)
                affordable = max(math.floor(max(cash - COMMISSION, 0.0) / fill), 0)
                shares = min(requested, affordable)
                if shares < 1:
                    continue
                cash -= shares * fill + COMMISSION
                costs += COMMISSION + shares * prices[symbol] * SLIPPAGE
                core_shares[symbol] += shares
                ledger_rows.append(
                    {
                        "date": date,
                        "module": "core",
                        "symbol": symbol,
                        "action": "BUY",
                        "shares": shares,
                        "fill": fill,
                        "cash_after": cash,
                        "reason": "v9_core_rebalance",
                        "source_trade_id": None,
                    }
                )
            post_nav = cash + stock_value(date) + core_value(date)
            actual_core = core_value(date) / post_nav if post_nav else 0.0
            target_core = sum(desired_targets.values())
            if target_core - actual_core > 0.02 + 1e-12:
                core_shortfall_events += 1

        close_stock = stock_value(date)
        close_core = core_value(date)
        equity = cash + close_stock + close_core
        if cash < -1e-8:
            raise AssertionError(f"negative shared cash on {date.date()}: {cash}")
        daily_rows.append(
            {
                "date": date,
                "equity": equity,
                "cash": cash,
                "core_value": close_core,
                "stock_value": close_stock,
                "core_exposure": close_core / equity if equity else 0.0,
                "stock_exposure": close_stock / equity if equity else 0.0,
                "gross_exposure": (close_core + close_stock) / equity if equity else 0.0,
                "target_core_exposure": sum(desired_targets.values()),
            }
        )

    daily = pd.DataFrame(daily_rows).set_index("date")
    ledger = pd.DataFrame(ledger_rows)
    metrics = combined_metrics(daily["equity"], initial_nav)
    wins = [pnl for pnl in realized_stock_pnl if pnl > 0]
    metrics.update(
        {
            "core_cap": core_cap,
            "stock_cap": stock_cap,
            "average_core_exposure": float(daily["core_exposure"].mean()),
            "max_core_exposure": float(daily["core_exposure"].max()),
            "average_stock_exposure": float(daily["stock_exposure"].mean()),
            "max_stock_exposure": float(daily["stock_exposure"].max()),
            "max_gross_exposure": float(daily["gross_exposure"].max()),
            "minimum_cash": float(daily["cash"].min()),
            "total_costs": float(costs),
            "core_shortfall_events": int(core_shortfall_events),
            "planned_stock_entries": int(planned_entries),
            "filled_stock_entries": int(filled_entries),
            "skipped_stock_entries": int(skipped_entries),
            "reduced_stock_entries": int(reduced_entries),
            "closed_stock_trades": int(len(realized_stock_pnl)),
            "stock_win_rate": (
                float(len(wins) / len(realized_stock_pnl)) if realized_stock_pnl else np.nan
            ),
            "stock_realized_pnl": float(sum(realized_stock_pnl)),
            "ledger_reconciles": bool(
                abs(
                    daily["equity"].iloc[-1]
                    - (daily["cash"].iloc[-1] + daily["core_value"].iloc[-1] + daily["stock_value"].iloc[-1])
                )
                < 1e-8
            ),
        }
    )
    return metrics, daily, ledger


def challenger_screen(metrics: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    by_key = metrics.set_index(["initial_nav", "period", "architecture"])
    rows = []
    for nav in NAVS:
        checks = {}
        for period in PERIODS:
            formal = by_key.loc[(nav, period, "formal_70_25")]
            challenger = by_key.loc[(nav, period, "challenger_80_20")]
            checks[f"{period}_return_higher"] = bool(
                challenger["total_return"] > formal["total_return"] + 1e-12
            )
            checks[f"{period}_dd_within_2pp"] = bool(
                challenger["max_drawdown"] >= formal["max_drawdown"] - 0.02 - 1e-12
            )
            checks[f"{period}_sharpe_within_005"] = bool(
                challenger["sharpe"] >= formal["sharpe"] - 0.05 - 1e-12
            )
            checks[f"{period}_monthly_win_within_1pp"] = bool(
                challenger["monthly_win_rate"] >= formal["monthly_win_rate"] - 0.01 - 1e-12
            )
        for period in ("train_2024_2025", "heldout_2026"):
            formal = by_key.loc[(nav, period, "formal_70_25")]
            challenger = by_key.loc[(nav, period, "challenger_80_20")]
            checks[f"{period}_average_core_higher"] = bool(
                challenger["average_core_exposure"]
                > formal["average_core_exposure"] + 1e-12
            )
            checks[f"{period}_stock_count_retained"] = bool(
                challenger["closed_stock_trades"]
                >= math.ceil(0.80 * formal["closed_stock_trades"] - 1e-12)
            )
            formal_win = formal["stock_win_rate"]
            challenger_win = challenger["stock_win_rate"]
            checks[f"{period}_stock_win_nonworse"] = bool(
                (pd.isna(formal_win) and pd.isna(challenger_win))
                or (not pd.isna(challenger_win) and challenger_win >= formal_win - 1e-12)
            )
        candidate_rows = metrics.loc[
            (metrics["initial_nav"] == nav)
            & (metrics["architecture"] == "challenger_80_20")
        ]
        checks["no_leverage"] = bool(
            (candidate_rows["max_gross_exposure"] <= 1.0 + 1e-9).all()
        )
        checks["nonnegative_cash"] = bool((candidate_rows["minimum_cash"] >= -1e-8).all())
        checks["ledger_reconciles"] = bool(candidate_rows["ledger_reconciles"].all())
        rows.append({"initial_nav": nav, **checks, "passes": bool(all(checks.values()))})
    screen = pd.DataFrame(rows)
    return screen, bool(screen["passes"].all())


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{float(value):.2%}"


def write_report(
    metrics: pd.DataFrame,
    screen: pd.DataFrame,
    opportunity: pd.DataFrame,
    summary: dict,
) -> None:
    lines = [
        "# Whole-share shared-capital architecture audit",
        "",
        "## Scope",
        "",
        "This audit puts the V9 index core and frozen RSR2 stock path into one cash ledger. SPY, QQQ and stocks use whole shares, USD 1 per order and 10 bps slippage. The formal comparison is 70% core plus RSR's frozen 25% internal cap; the challenger is 80% core plus 20% RSR. No signal parameter changes.",
        "",
        "## Results",
        "",
        "| NAV | Period | Architecture | Return | Max DD | Sharpe | Monthly win | Avg core | Max stock | Stock trades | Stock win | Stock PnL | Min cash |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in metrics.itertuples(index=False):
        lines.append(
            f"| ${row.initial_nav:,.2f} | {row.period} | {row.architecture} | "
            f"{pct(row.total_return)} | {pct(row.max_drawdown)} | {row.sharpe:.2f} | "
            f"{pct(row.monthly_win_rate)} | {pct(row.average_core_exposure)} | "
            f"{pct(row.max_stock_exposure)} | {row.closed_stock_trades} | "
            f"{pct(row.stock_win_rate)} | ${row.stock_realized_pnl:,.2f} | ${row.minimum_cash:,.2f} |"
        )
    lines.extend(["", "## Challenger screen", ""])
    for row in screen.itertuples(index=False):
        failed = [
            column
            for column in screen.columns
            if column not in {"initial_nav", "passes"} and not bool(getattr(row, column))
        ]
        lines.append(
            f"- NAV `${row.initial_nav:,.2f}`: `{'pass' if row.passes else 'fail'}`"
            + (f"; failed: {', '.join(failed)}" if failed else "")
        )
    lines.extend(["", "## Stock-cap opportunity difference", ""])
    for nav in NAVS:
        omitted = opportunity.loc[
            (opportunity["initial_nav"] == nav)
            & (opportunity["period"] == "train_2024_2025")
            & (opportunity["difference"] == "omitted_by_challenger")
        ]
        names = ", ".join(
            f"{row.symbol}@{row.entry_date}" for row in omitted.itertuples(index=False)
        )
        lines.append(
            f"- NAV `${nav:,.2f}`: 20% stock capacity omits `{len(omitted)}` training trades"
            f" with formal-path source PnL `{omitted['source_pnl'].sum():,.2f}`: {names or 'none'}."
        )
        if not omitted.empty:
            largest = omitted.loc[omitted["source_pnl"].idxmax()]
            lines.append(
                f"  The largest omitted contributor is `{largest['symbol']}` at"
                f" `${largest['source_pnl']:,.2f}`; the architecture difference is therefore"
                " concentrated and is not proof that a 25% stock sleeve will always win."
            )
    lines.extend(["", "## Decision", ""])
    if summary["challenger_passes"]:
        lines.extend(
            [
                "- 80/20 survives the frozen shared-capital and whole-share screen at both account sizes. It remains a forward research challenger, not a formal allocation change.",
                "- The higher index ceiling is operationally deployable without reducing RSR2's observed trade count or win rate in the tested periods. This still does not prove future RSR alpha.",
            ]
        )
    else:
        lines.extend(
            [
                "- 80/20 fails at least one frozen shared-capital requirement and is removed as an allocation challenger on this history.",
                "- Formal 70/30 governance remains; do not reopen the core-cap grid merely to find a passing threshold.",
            ]
        )
    lines.extend(
        [
            "- The 2026 held-out monitor ends at the latest completed formal local row, not the current calendar date.",
            "- Research-only. No order, live-account mutation, formal V9 change or forward-ledger write is authorized.",
            "",
            "See `shared-capital-architecture-preregistration.md` for the frozen comparison.",
        ]
    )
    (RESULTS / "shared_capital_architecture_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    current_panels, current_vix, meta = load_data()
    stock_panels, all_symbols = BACKTEST["load_panels"]()
    universes, _ = UNIVERSE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    historical_panels, historical_vix, long_meta = FRONTIER["load_long_history"]()
    core_panels, core_vix = stitch_core_history(
        historical_panels, historical_vix, current_panels, current_vix
    )
    latest = min(pd.Timestamp(meta["last_date"]), stock_panels["close"].index.max())
    latest_text = str(latest.date())
    metric_rows = []
    daily_blocks = []
    ledger_blocks = []
    core_diagnostics = []
    source_trade_rows = []
    base_config = UNIVERSE["make_config"](True)
    for period, (start, configured_end, warmup) in PERIODS.items():
        end = latest_text if configured_end is None else configured_end
        for architecture, limits in ARCHITECTURES.items():
            schedule, diagnostics = core_execution_schedule(
                core_panels,
                core_vix,
                limits["core_cap"],
                start,
                end,
                warmup,
            )
            core_diagnostics.append(
                {"period": period, "architecture": architecture, **diagnostics}
            )
            for nav in NAVS:
                config = replace(base_config, stock_sleeve_max=limits["stock_cap"])
                stock_run = BACKTEST["simulate"](
                    stock_panels,
                    symbols,
                    config,
                    "strict_veto",
                    start,
                    end,
                    slippage=SLIPPAGE,
                    commission=COMMISSION,
                    profit_lock_trigger=0.15,
                    profit_lock_floor=0.05,
                    initial_nav=nav,
                )
                for trade in stock_run["trades"]:
                    source_trade_rows.append(
                        {
                            "initial_nav": nav,
                            "period": period,
                            "architecture": architecture,
                            "symbol": trade["symbol"],
                            "entry_date": trade["entry_date"],
                            "exit_date": trade.get("exit_date"),
                            "source_pnl": trade.get("pnl"),
                            "source_return": trade.get("return"),
                        }
                    )
                metrics, daily, ledger = simulate_shared(
                    stock_panels,
                    schedule,
                    stock_run,
                    limits["core_cap"],
                    limits["stock_cap"],
                    nav,
                    start,
                    end,
                )
                metric_rows.append(
                    {
                        "initial_nav": nav,
                        "period": period,
                        "architecture": architecture,
                        "start": start,
                        "end": end,
                        **metrics,
                    }
                )
                block = daily.reset_index()
                block.insert(0, "architecture", architecture)
                block.insert(0, "period", period)
                block.insert(0, "initial_nav", nav)
                daily_blocks.append(block)
                if not ledger.empty:
                    ledger.insert(0, "architecture", architecture)
                    ledger.insert(0, "period", period)
                    ledger.insert(0, "initial_nav", nav)
                    ledger_blocks.append(ledger)
    metrics = pd.DataFrame(metric_rows)
    screen, challenger_passes = challenger_screen(metrics)
    daily = pd.concat(daily_blocks, ignore_index=True)
    ledger = pd.concat(ledger_blocks, ignore_index=True) if ledger_blocks else pd.DataFrame()
    source_trades = pd.DataFrame(source_trade_rows)
    opportunity_rows = []
    for nav in NAVS:
        for period in PERIODS:
            formal = source_trades.loc[
                (source_trades["initial_nav"] == nav)
                & (source_trades["period"] == period)
                & (source_trades["architecture"] == "formal_70_25")
            ]
            challenger = source_trades.loc[
                (source_trades["initial_nav"] == nav)
                & (source_trades["period"] == period)
                & (source_trades["architecture"] == "challenger_80_20")
            ]
            formal_keys = set(zip(formal["symbol"], formal["entry_date"]))
            challenger_keys = set(zip(challenger["symbol"], challenger["entry_date"]))
            for difference, frame, keys in (
                ("omitted_by_challenger", formal, formal_keys - challenger_keys),
                ("added_by_challenger", challenger, challenger_keys - formal_keys),
            ):
                for symbol, entry_date in sorted(keys):
                    row = frame.loc[
                        (frame["symbol"] == symbol) & (frame["entry_date"] == entry_date)
                    ].iloc[0]
                    opportunity_rows.append(
                        {
                            "initial_nav": nav,
                            "period": period,
                            "difference": difference,
                            "symbol": symbol,
                            "entry_date": entry_date,
                            "exit_date": row["exit_date"],
                            "source_pnl": row["source_pnl"],
                            "source_return": row["source_return"],
                        }
                    )
    opportunity = pd.DataFrame(opportunity_rows)
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "latest_completed_date": latest_text,
        "current_data_source": meta.get("source"),
        "long_history_data_source": long_meta,
        "research_only": True,
        "authorizes_trade": False,
        "challenger_passes": challenger_passes,
        "decision": (
            "retain_80_20_as_forward_research_challenger"
            if challenger_passes
            else "remove_80_20_challenger_keep_formal_70_30"
        ),
    }
    metrics.to_csv(RESULTS / "shared_capital_architecture_metrics.csv", index=False)
    screen.to_csv(RESULTS / "shared_capital_architecture_screen.csv", index=False)
    daily.to_csv(RESULTS / "shared_capital_architecture_daily.csv", index=False)
    ledger.to_csv(RESULTS / "shared_capital_architecture_ledger.csv", index=False)
    source_trades.to_csv(
        RESULTS / "shared_capital_architecture_source_trades.csv", index=False
    )
    opportunity.to_csv(
        RESULTS / "shared_capital_architecture_opportunity_difference.csv", index=False
    )
    pd.DataFrame(core_diagnostics).drop_duplicates().to_csv(
        RESULTS / "shared_capital_architecture_core_diagnostics.csv", index=False
    )
    (RESULTS / "shared_capital_architecture_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(metrics, screen, opportunity, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
