#!/usr/bin/env python3
"""Portfolio simulation for the preregistered hv_central signal."""
from __future__ import annotations

import json
import math
import runpy
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
EVENT = runpy.run_path(str(HERE / "evaluate_high_vol_trend.py"))
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE_MODULE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
RESULTS = HERE / "results"
INITIAL_NAV = 6_000.0
COMMISSION = 1.0
MAX_NAMES = 2
SLEEVE_CAP = 0.15
SINGLE_CAP = 0.15
RISK_BUDGET = 0.0075
MAX_TARGET = 0.08
MAX_GAP = 0.05
MAX_HOLD = 20
REENTRY_COOLDOWN = 10


def _price(frame: pd.DataFrame, date: pd.Timestamp, symbol: str) -> float | None:
    value = frame.at[date, symbol]
    return float(value) if pd.notna(value) and float(value) > 0 else None


def metrics(equity: pd.Series, trades: list[dict], exposure: pd.Series, costs: float) -> dict:
    returns = equity.pct_change().fillna(0.0)
    drawdown = equity / equity.cummax() - 1.0
    std = float(returns.std(ddof=0))
    closed = [trade for trade in trades if trade.get("pnl") is not None]
    wins = [trade for trade in closed if trade["pnl"] > 0]
    losses = [trade for trade in closed if trade["pnl"] <= 0]
    gross_profit = sum(trade["pnl"] for trade in wins)
    gross_loss = -sum(trade["pnl"] for trade in losses)
    return {
        "final_value": float(equity.iloc[-1]),
        "total_return": float(equity.iloc[-1] / equity.iloc[0] - 1.0),
        "max_drawdown": float(drawdown.min()),
        "sharpe": float(returns.mean() / std * math.sqrt(252)) if std else 0.0,
        "trade_count": len(closed),
        "win_rate": float(len(wins) / len(closed)) if closed else np.nan,
        "profit_factor": float(gross_profit / gross_loss) if gross_loss else (999.0 if gross_profit else np.nan),
        "average_trade": float(np.mean([trade["return"] for trade in closed])) if closed else np.nan,
        "max_exposure": float(exposure.max()),
        "average_exposure": float(exposure.mean()),
        "costs": float(costs),
    }


def simulate(
    panels: dict[str, pd.DataFrame],
    symbols: list[str],
    signal: pd.DataFrame,
    components: dict,
    start: str,
    end: str,
    slippage: float,
) -> dict:
    close, open_, high, low = (panels[name] for name in ("close", "open", "high", "low"))
    ma10 = close[symbols].rolling(10, min_periods=10).mean()
    dates = close.loc[start:end].dropna(subset=["SPY", "QQQ", "SMH"]).index
    cash = INITIAL_NAV
    positions: dict[str, dict] = {}
    pending_entries: list[dict] = []
    pending_exits: set[str] = set()
    last_exit_location: dict[str, int] = {}
    trades: list[dict] = []
    equity_rows = []
    exposure_rows = []
    costs = 0.0

    def open_nav(date: pd.Timestamp) -> float:
        return cash + sum(
            position["shares"] * (_price(open_, date, symbol) or position["entry_price"])
            for symbol, position in positions.items()
        )

    def sell(symbol: str, date: pd.Timestamp, raw_price: float, reason: str) -> None:
        nonlocal cash, costs
        position = positions.pop(symbol)
        fill = raw_price * (1.0 - slippage)
        proceeds = position["shares"] * fill - COMMISSION
        cash += proceeds
        costs += COMMISSION + position["shares"] * raw_price * slippage
        trade = trades[position["trade_index"]]
        pnl = proceeds - position["cost_basis"]
        trade.update(
            {
                "exit_date": str(date.date()),
                "exit_price": fill,
                "exit_reason": reason,
                "pnl": pnl,
                "return": pnl / position["cost_basis"],
            }
        )
        last_exit_location[symbol] = close.index.get_loc(date)

    for date in dates:
        location = close.index.get_loc(date)

        for symbol in sorted(pending_exits):
            if symbol in positions:
                price = _price(open_, date, symbol)
                if price is not None:
                    sell(symbol, date, price, "signal_exit")
        pending_exits.clear()

        pending_entries.sort(key=lambda order: (-order["rs20"], -order["volume_ratio"], order["symbol"]))
        for order in pending_entries:
            symbol = order["symbol"]
            if symbol in positions or len(positions) >= MAX_NAMES:
                continue
            price = _price(open_, date, symbol)
            if price is None:
                continue
            gap = price / order["signal_close"] - 1.0
            if gap > MAX_GAP:
                continue
            nav = open_nav(date)
            current_value = sum(
                position["shares"] * (_price(open_, date, held) or position["entry_price"])
                for held, position in positions.items()
            )
            stop_distance = min(0.15, max(0.08, 1.25 * order["atr_pct"]))
            target_weight = min(MAX_TARGET, RISK_BUDGET / stop_distance)
            fill = price * (1.0 + slippage)
            shares = math.floor(max(nav * target_weight - COMMISSION, 0.0) / fill)
            if shares < 1 and fill + COMMISSION <= nav * SINGLE_CAP:
                shares = 1
            notional = shares * fill
            if shares < 1 or notional + COMMISSION > cash:
                continue
            if notional > nav * SINGLE_CAP + 1e-9 or current_value + notional > nav * SLEEVE_CAP + 1e-9:
                continue
            cash -= notional + COMMISSION
            costs += COMMISSION + shares * price * slippage
            trade = {
                "symbol": symbol,
                "signal_date": order["signal_date"],
                "entry_date": str(date.date()),
                "entry_price": fill,
                "shares": shares,
                "signal_atr_pct": order["atr_pct"],
                "stop_distance": stop_distance,
                "target_weight": target_weight,
                "entry_gap": gap,
                "exit_date": None,
                "exit_price": None,
                "exit_reason": None,
                "pnl": None,
                "return": None,
            }
            trades.append(trade)
            positions[symbol] = {
                "shares": shares,
                "entry_price": fill,
                "cost_basis": notional + COMMISSION,
                "stop": fill * (1.0 - stop_distance),
                "days": 0,
                "trade_index": len(trades) - 1,
            }
        pending_entries = []

        for symbol in list(positions):
            position = positions[symbol]
            low_price = _price(low, date, symbol)
            open_price = _price(open_, date, symbol)
            if low_price is not None and open_price is not None and low_price <= position["stop"]:
                sell(symbol, date, min(open_price, position["stop"]), "stop")

        close_value = sum(
            position["shares"] * (_price(close, date, symbol) or position["entry_price"])
            for symbol, position in positions.items()
        )
        nav = cash + close_value
        equity_rows.append(nav)
        exposure_rows.append(close_value / nav if nav > 0 else 0.0)

        for symbol, position in list(positions.items()):
            position["days"] += 1
            price = _price(close, date, symbol)
            if price is None:
                continue
            if price >= position["entry_price"] * 1.15:
                position["stop"] = max(position["stop"], position["entry_price"] * 1.05)
            if position["days"] >= MAX_HOLD or price < ma10.at[date, symbol]:
                pending_exits.add(symbol)

        candidates = []
        for symbol in symbols:
            if not bool(signal.at[date, symbol]) or symbol in positions:
                continue
            if any(order["symbol"] == symbol for order in pending_entries):
                continue
            prior_exit = last_exit_location.get(symbol)
            if prior_exit is not None and location - prior_exit <= REENTRY_COOLDOWN:
                continue
            candidates.append(
                {
                    "symbol": symbol,
                    "signal_date": str(date.date()),
                    "signal_close": float(close.at[date, symbol]),
                    "rs20": float(components["rs20"].at[date, symbol]),
                    "volume_ratio": float(components["volume_ratio"].at[date, symbol]),
                    "atr_pct": float(components["atr_pct"].at[date, symbol]),
                }
            )
        pending_entries = candidates

    final_date = dates[-1]
    for symbol in list(positions):
        price = _price(close, final_date, symbol)
        if price is not None:
            sell(symbol, final_date, price, "end_of_period")
    equity = pd.Series(equity_rows, index=dates, dtype=float)
    if positions:
        raise RuntimeError("final liquidation failed")
    equity.iloc[-1] = cash
    exposure = pd.Series(exposure_rows, index=dates, dtype=float)
    exposure.iloc[-1] = 0.0
    return {
        "metrics": metrics(equity, trades, exposure, costs),
        "trades": trades,
        "equity": equity,
        "exposure": exposure,
    }


def entry_path(result: dict) -> list[tuple[str, str, str]]:
    return [(trade["signal_date"], trade["entry_date"], trade["symbol"]) for trade in result["trades"]]


def gross_profit_concentration(results: dict) -> float:
    rows = []
    for result in results.values():
        rows.extend(trade for trade in result["trades"] if trade.get("pnl") is not None and trade["pnl"] > 0)
    by_symbol = pd.DataFrame(rows).groupby("symbol")["pnl"].sum() if rows else pd.Series(dtype=float)
    return float(by_symbol.max() / by_symbol.sum()) if not by_symbol.empty and by_symbol.sum() > 0 else np.nan


def write_report(rows: pd.DataFrame, gate: dict) -> None:
    lines = [
        "# High-volatility trend portfolio simulation",
        "",
        "## Scope",
        "",
        "Only the preregistered `hv_central` signal is used. The simulation applies whole shares, next-open entry, gap rejection, volatility-linked stops, a 0.75% NAV risk budget, a 15% sleeve cap, commissions and slippage. It remains current-list and post-2026-definition research.",
        "",
        "## Results",
        "",
        "| Period | Cost/side | Return | Max DD | Sharpe | Trades | Win rate | Profit factor | Avg exposure | Max exposure |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows.itertuples(index=False):
        lines.append(
            f"| {row.period} | {row.cost_bps:.0f} bps | {row.total_return:.2%} | {row.max_drawdown:.2%} | "
            f"{row.sharpe:.2f} | {row.trade_count} | {row.win_rate:.2%} | {row.profit_factor:.2f} | "
            f"{row.average_exposure:.2%} | {row.max_exposure:.2%} |"
        )
    lines.extend(["", "## Continuation gate", ""])
    for key, value in gate.items():
        if key == "gross_profit_concentration":
            lines.append(f"- `{key}`: `{value:.2%}`")
        else:
            lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Decision", ""])
    if gate["passes_portfolio_gate"]:
        lines.append("The small sleeve passes its preregistered portfolio gate and may proceed to a shared-capital V9/RSR combination audit. It remains unpromoted until genuine forward evidence exists.")
    else:
        lines.append("Stop the sleeve branch. Retain only the non-trading high-volatility missed-opportunity diagnostic; do not optimize position or exit parameters on this history.")
    (RESULTS / "high_vol_portfolio_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, all_symbols = MODULE["load_panels"]()
    universes, _ = UNIVERSE_MODULE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    components = EVENT["signal_components"](panels, symbols)
    signal = EVENT["definition_signal"](components, EVENT["DEFINITIONS"]["hv_central"])
    runs = {}
    rows = []
    for period, (start, end) in EVENT["PERIODS"].items():
        for bps in (10, 20):
            result = simulate(panels, symbols, signal, components, str(start.date()), str(end.date()), bps / 10_000)
            runs[(period, bps)] = result
            rows.append({"period": period, "cost_bps": bps, **result["metrics"]})
    table = pd.DataFrame(rows)
    ten = table.loc[table["cost_bps"].eq(10)].set_index("period")
    twenty = table.loc[table["cost_bps"].eq(20)].set_index("period")
    paths_stable = all(entry_path(runs[(period, 10)]) == entry_path(runs[(period, 20)]) for period in EVENT["PERIODS"])
    concentration = gross_profit_concentration({period: runs[(period, 10)] for period in EVENT["PERIODS"]})
    gate = {
        "minimum_trade_count": bool(ten.at["development_2024_2025", "trade_count"] >= 10 and ten.at["retrospective_2026", "trade_count"] >= 5),
        "positive_return_both": bool((ten["total_return"] > 0).all()),
        "sharpe_ge_0_50_both": bool((ten["sharpe"] >= 0.50).all()),
        "win_rate_ge_50_both": bool((ten["win_rate"] >= 0.50).all()),
        "profit_factor_ge_1_20_both": bool((ten["profit_factor"] >= 1.20).all()),
        "max_drawdown_no_worse_10pct_both": bool((ten["max_drawdown"] >= -0.10).all()),
        "positive_at_20bps_both": bool((twenty["total_return"] > 0).all()),
        "entry_path_stable_10_to_20bps": paths_stable,
        "gross_profit_concentration": concentration,
        "gross_profit_concentration_le_35": bool(np.isfinite(concentration) and concentration <= 0.35),
    }
    gate["passes_portfolio_gate"] = all(value for key, value in gate.items() if key != "gross_profit_concentration")
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "research_only": True,
        "authorizes_trade": False,
        **gate,
        "decision": "proceed_to_shared_capital_audit" if gate["passes_portfolio_gate"] else "stop_sleeve_keep_diagnostic_only",
    }
    table.to_csv(RESULTS / "high_vol_portfolio_metrics.csv", index=False)
    trade_rows = []
    equity = {}
    exposure = {}
    for (period, bps), result in runs.items():
        for trade in result["trades"]:
            trade_rows.append({"period": period, "cost_bps": bps, **trade})
        equity[f"{period}_{bps}bps"] = result["equity"]
        exposure[f"{period}_{bps}bps"] = result["exposure"]
    pd.DataFrame(trade_rows).to_csv(RESULTS / "high_vol_portfolio_trades.csv", index=False)
    pd.DataFrame(equity).to_csv(RESULTS / "high_vol_portfolio_equity.csv")
    pd.DataFrame(exposure).to_csv(RESULTS / "high_vol_portfolio_exposure.csv")
    (RESULTS / "high_vol_portfolio_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(table, gate)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
