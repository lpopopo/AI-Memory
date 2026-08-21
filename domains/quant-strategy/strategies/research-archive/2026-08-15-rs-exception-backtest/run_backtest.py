#!/usr/bin/env python3
"""Whole-share backtest for a tightly bounded SMH-relative-strength exception."""
from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
V9 = ROOT / "strategies" / "v9-execution"
DATA = V9 / "datasets" / "data_v9"
WATCHLIST = ROOT / "references" / "user-selected-watchlist.json"
RESULTS = Path(__file__).resolve().parent / "results"

INITIAL_NAV = 6_000.0
COMMISSION = 1.0
SLIPPAGE = 0.001
NORMAL_TARGET_WEIGHT = 0.08
EXCEPTION_SINGLE_MAX = 0.08
NORMAL_SINGLE_MAX = 0.15
STOCK_SLEEVE_MAX = 0.25
MAX_NORMAL_NAMES = 3
MIN_NOTIONAL = 200.0
RANKING_MODES = {
    "formal_composite",
    "rs_only",
    "low_atr_first",
    "balanced_rank",
}


@dataclass(frozen=True)
class Config:
    rs20_min: float = 0.05
    volume_ratio_min: float = 1.20
    max_extension: float = 0.12
    max_hold_days: int = 20
    exception_target_weight: float = 0.05
    stop_loss: float = 0.08
    repair_rs10_min: float = 0.03
    breadth_min: float = 0.50
    breadth_count_min: int = 2
    max_atr_pct: float = 1.00
    min_close_location: float = 0.00
    normal_target_weight: float = NORMAL_TARGET_WEIGHT
    stock_sleeve_max: float = STOCK_SLEEVE_MAX
    entry_delay_sessions: int = 1
    max_entry_gap: float = 1.00


SUPER_GROUPS = {
    "memory_storage": {"DRAM", "MU", "WDC", "STX", "SNDK", "SKHY"},
    "optical_networking": {"MRVL", "AVGO", "ALAB", "COHR", "LITE", "AAOI", "MXL", "AXTI", "CRDO", "GLW", "NOK"},
    "equipment_test": {"TER", "ASML", "AMAT", "KLAC", "LRCX"},
    "compute_server": {"NVDA", "AMD", "INTC", "SMCI", "QCOM"},
    "space": {"RKLB", "RDW"},
    "cloud_infrastructure": {"ORCL", "META"},
}


def load_panels() -> tuple[dict[str, pd.DataFrame], list[str]]:
    panels = {}
    for field in ("open", "high", "low", "close", "volume"):
        panels[field] = pd.read_csv(DATA / f"{field}.csv", index_col=0, parse_dates=True).sort_index()
        panels[field].index = pd.to_datetime(panels[field].index).tz_localize(None)
    # Cboe volatility files can contribute dates that are not U.S. equity
    # sessions. Rolling equity indicators must therefore use SPY trading rows,
    # not the union of every provider's calendar.
    equity_dates = panels["close"]["SPY"].dropna().index
    panels = {field: frame.reindex(equity_dates) for field, frame in panels.items()}
    raw = json.loads(WATCHLIST.read_text(encoding="utf-8"))
    symbols = [item["symbol"] for item in raw["tickers"] if item["symbol"] != "QQQM"]
    required = set(symbols) | {"SPY", "QQQ", "SMH", "^VIX", "^VIX3M"}
    missing = sorted(required - set(panels["close"].columns))
    if missing:
        raise RuntimeError(f"missing required symbols: {missing}")
    return panels, symbols


def build_features(panels: dict[str, pd.DataFrame], symbols: list[str], config: Config) -> dict:
    close, high, low = panels["close"], panels["high"], panels["low"]
    open_, volume = panels["open"], panels["volume"]
    stock_close = close[symbols]
    ma20 = stock_close.rolling(20, min_periods=20).mean()
    ma50 = stock_close.rolling(50, min_periods=50).mean()
    previous_high20 = high[symbols].rolling(20, min_periods=20).max().shift(1)
    stock_ret20 = stock_close / stock_close.shift(20) - 1.0
    smh_ret20 = close["SMH"] / close["SMH"].shift(20) - 1.0
    rs20 = stock_ret20.sub(smh_ret20, axis=0)
    stock_ret10 = stock_close / stock_close.shift(10) - 1.0
    smh_ret10 = close["SMH"] / close["SMH"].shift(10) - 1.0
    rs10 = stock_ret10.sub(smh_ret10, axis=0)
    volume_ratio = volume[symbols] / volume[symbols].rolling(20, min_periods=20).mean().shift(1)
    extension = stock_close / ma20 - 1.0
    prior_stock_close = stock_close.shift(1)
    true_range = pd.DataFrame(
        np.maximum.reduce([
            (high[symbols] - low[symbols]).to_numpy(),
            (high[symbols] - prior_stock_close).abs().to_numpy(),
            (low[symbols] - prior_stock_close).abs().to_numpy(),
        ]),
        index=stock_close.index,
        columns=symbols,
    )
    atr_pct = true_range.rolling(14, min_periods=14).mean() / stock_close
    close_location = (stock_close - low[symbols]) / (high[symbols] - low[symbols]).replace(0.0, np.nan)

    prior_close = stock_close.shift(1)
    positive_gap = open_[symbols] / prior_close - 1.0 >= 0.10
    day_range = (high[symbols] - low[symbols]) / open_[symbols]
    event_block = positive_gap | positive_gap.shift(1).fillna(False)
    event_block |= positive_gap.shift(2).fillna(False) & (day_range >= 0.03)

    spy_ma200 = close["SPY"].rolling(200, min_periods=200).mean()
    qqq_ma100 = close["QQQ"].rolling(100, min_periods=100).mean()
    smh_ma50 = close["SMH"].rolling(50, min_periods=50).mean()
    vix_ratio = close["^VIX"] / close["^VIX3M"]
    broad_healthy = (
        (close["SPY"] > spy_ma200)
        & (close["QQQ"] > qqq_ma100)
        & (close["^VIX"] < 25.0)
        & (vix_ratio < 1.0)
    )
    smh_healthy = close["SMH"] >= smh_ma50
    signal = (
        stock_close.notna()
        & (stock_close > ma20)
        & (stock_close > ma50)
        & (stock_close > previous_high20)
        & (rs20 >= config.rs20_min)
        & (volume_ratio >= config.volume_ratio_min)
        & (extension >= 0.0)
        & (extension <= config.max_extension)
        & (atr_pct <= config.max_atr_pct)
        & (close_location >= config.min_close_location)
        & ~event_block
    )
    signal = signal.mul(broad_healthy, axis=0).fillna(False)
    score = rs20 * 100.0 + volume_ratio.clip(upper=5.0)

    previous_high10 = high[symbols].rolling(10, min_periods=10).max().shift(1)
    repair_trigger = (stock_close.shift(1) <= ma20.shift(1)) | (stock_close > previous_high10)
    breadth_confirmed = pd.DataFrame(False, index=stock_close.index, columns=symbols)
    breadth_score = pd.DataFrame(0.0, index=stock_close.index, columns=symbols)
    above_ma20_with_rs = (stock_close > ma20) & (rs10 > 0.0)
    for members in SUPER_GROUPS.values():
        active = sorted(set(symbols) & members)
        if len(active) < 2:
            continue
        count = above_ma20_with_rs[active].sum(axis=1)
        fraction = count / len(active)
        confirmed = (count >= config.breadth_count_min) & (fraction >= config.breadth_min)
        breadth_confirmed.loc[:, active] = np.repeat(confirmed.to_numpy()[:, None], len(active), axis=1)
        breadth_score.loc[:, active] = np.repeat(fraction.to_numpy()[:, None], len(active), axis=1)
    repair_signal = (
        stock_close.notna()
        & (stock_close > ma20)
        & repair_trigger
        & (rs10 >= config.repair_rs10_min)
        & (volume_ratio >= config.volume_ratio_min)
        & (extension >= 0.0)
        & (extension <= config.max_extension)
        & (atr_pct <= config.max_atr_pct)
        & (close_location >= config.min_close_location)
        & breadth_confirmed
        & ~event_block
    )
    repair_signal = repair_signal.mul(broad_healthy, axis=0).fillna(False)
    repair_score = rs10 * 100.0 + breadth_score * 5.0 + volume_ratio.clip(upper=5.0)
    return {
        "ma20": ma20,
        "rs20": rs20,
        "rs10": rs10,
        "volume_ratio": volume_ratio,
        "atr_pct": atr_pct,
        "close_location": close_location,
        "signal": signal,
        "score": score,
        "repair_signal": repair_signal,
        "repair_score": repair_score,
        "breadth_score": breadth_score,
        "broad_healthy": broad_healthy.fillna(False),
        "smh_healthy": smh_healthy.fillna(False),
    }


def rank_entry_candidates(
    features: dict[str, pd.DataFrame],
    date: pd.Timestamp,
    symbols: list[str],
    ranking_mode: str = "formal_composite",
) -> list[dict]:
    """Rank same-close eligible symbols using completed-close information only."""
    if ranking_mode not in RANKING_MODES:
        raise ValueError(f"unknown ranking mode: {ranking_mode}")
    if not symbols:
        return []
    rows = []
    for symbol in symbols:
        rows.append(
            {
                "symbol": symbol,
                "formal_composite": float(features["score"].at[date, symbol]),
                "rs20": float(features["rs20"].at[date, symbol]),
                "volume_ratio": float(features["volume_ratio"].at[date, symbol]),
                "close_location": float(features["close_location"].at[date, symbol]),
                "atr_pct": float(features["atr_pct"].at[date, symbol]),
            }
        )
    frame = pd.DataFrame(rows).set_index("symbol")
    if ranking_mode == "formal_composite":
        score = frame["formal_composite"]
    elif ranking_mode == "rs_only":
        score = frame["rs20"]
    elif ranking_mode == "low_atr_first":
        score = -frame["atr_pct"]
    else:
        score = pd.concat(
            [
                frame["rs20"].rank(pct=True, method="average"),
                frame["volume_ratio"].rank(pct=True, method="average"),
                frame["close_location"].rank(pct=True, method="average"),
                (-frame["atr_pct"]).rank(pct=True, method="average"),
            ],
            axis=1,
        ).mean(axis=1)
    ranked = []
    for symbol, value in score.items():
        row = frame.loc[symbol].to_dict()
        ranked.append({"symbol": symbol, "ranking_score": float(value), **row})
    return sorted(ranked, key=lambda row: (row["ranking_score"], row["symbol"]), reverse=True)


def partial_exit_order(
    shares: int,
    raw_price: float,
    slippage: float,
    fraction: float,
    minimum_notional: float,
) -> tuple[dict | None, str]:
    """Return deterministic whole-share scale-out terms or an ineligibility reason."""
    trim_shares = math.floor(shares * fraction)
    if trim_shares < 1 or trim_shares >= shares:
        return None, "ineligible_whole_shares"
    fill = raw_price * (1.0 - slippage)
    gross_proceeds = trim_shares * fill
    if gross_proceeds < minimum_notional:
        return None, "ineligible_min_notional"
    return {
        "shares": trim_shares,
        "fill": fill,
        "gross_proceeds": gross_proceeds,
    }, "executed"


def aggregate_position_pnl(position: dict, final_proceeds: float) -> tuple[float, float]:
    """Aggregate prior partial realization and the final remaining-share exit."""
    total_pnl = position.get("realized_pnl", 0.0) + final_proceeds - position["cost_basis"]
    original_cost_basis = position.get("original_cost_basis", position["cost_basis"])
    return total_pnl, total_pnl / original_cost_basis


def _safe(frame: pd.DataFrame, date: pd.Timestamp, symbol: str) -> float | None:
    try:
        value = float(frame.at[date, symbol])
    except (KeyError, TypeError, ValueError):
        return None
    return value if np.isfinite(value) and value > 0 else None


def partition_pending_exit_fills(
    pending_exits: set[str],
    positions: dict[str, dict],
    open_frame: pd.DataFrame,
    date: pd.Timestamp,
    slippage: float,
) -> tuple[dict[str, tuple[float, float]], set[str]]:
    """Keep a valid exit order pending when the next session has no open."""
    executable: dict[str, tuple[float, float]] = {}
    deferred: set[str] = set()
    for symbol in sorted(pending_exits):
        if symbol not in positions:
            continue
        price = _safe(open_frame, date, symbol)
        if price is None:
            deferred.add(symbol)
        else:
            executable[symbol] = (price, price * (1.0 - slippage))
    return executable, deferred


def ratcheted_profit_stop(
    entry_price: float,
    current_stop: float,
    completed_close: float,
    trigger: float | None,
    floor: float,
) -> tuple[float, bool]:
    """Raise a stop only after a completed close confirms the profit trigger."""
    if trigger is None or completed_close + 1e-12 < entry_price * (1.0 + trigger):
        return current_stop, False
    raised = max(current_stop, entry_price * (1.0 + floor))
    return raised, raised > current_stop + 1e-12


def winner_extension_active(
    entry_price: float,
    completed_close: float,
    ma20: float,
    rs20: float,
    held_sessions: int,
    base_hold_days: int,
    extension_days: int | None,
    minimum_return: float,
) -> bool:
    """Extend only a completed-close winner whose price and RS trends remain intact."""
    if extension_days is None:
        return False
    if extension_days <= base_hold_days:
        raise ValueError("winner extension must exceed the base holding period")
    return bool(
        held_sessions >= base_hold_days
        and held_sessions < extension_days
        and completed_close >= entry_price * (1.0 + minimum_return)
        and completed_close >= ma20
        and rs20 >= 0.0
    )


def _metrics(
    equity: pd.Series,
    trades: list[dict],
    exposure: pd.Series,
    turnover: float,
    costs: float,
    initial_nav: float = INITIAL_NAV,
) -> dict:
    returns = equity.pct_change().fillna(0.0)
    years = max((equity.index[-1] - equity.index[0]).days / 365.25, 1 / 252)
    total_return = float(equity.iloc[-1] / equity.iloc[0] - 1.0)
    cagr = float((equity.iloc[-1] / equity.iloc[0]) ** (1.0 / years) - 1.0)
    drawdown = equity / equity.cummax() - 1.0
    volatility = float(returns.std(ddof=0) * math.sqrt(252))
    sharpe = float(returns.mean() / returns.std(ddof=0) * math.sqrt(252)) if returns.std(ddof=0) else 0.0
    downside = returns[returns < 0].std(ddof=0)
    sortino = float(returns.mean() / downside * math.sqrt(252)) if downside and np.isfinite(downside) else 0.0
    closed = [trade for trade in trades if trade.get("pnl") is not None]
    wins = [trade for trade in closed if trade["pnl"] > 0]
    losses = [trade for trade in closed if trade["pnl"] <= 0]
    gross_profit = sum(trade["pnl"] for trade in wins)
    gross_loss = -sum(trade["pnl"] for trade in losses)
    exception = [trade for trade in closed if trade["entry_type"] != "normal"]
    return {
        "final_value": float(equity.iloc[-1]),
        "total_return": total_return,
        "cagr": cagr,
        "max_drawdown": float(drawdown.min()),
        "volatility": volatility,
        "sharpe": sharpe,
        "sortino": sortino,
        "trade_count": len(closed),
        "win_rate": float(len(wins) / len(closed)) if closed else None,
        "average_win": float(np.mean([trade["return"] for trade in wins])) if wins else None,
        "average_loss": float(np.mean([trade["return"] for trade in losses])) if losses else None,
        "profit_factor": float(gross_profit / gross_loss) if gross_loss else (None if not gross_profit else 999.0),
        "exception_trade_count": len(exception),
        "exception_win_rate": float(sum(t["pnl"] > 0 for t in exception) / len(exception)) if exception else None,
        "exception_average_return": float(np.mean([t["return"] for t in exception])) if exception else None,
        "exposure": float(exposure.mean()),
        "turnover": float(turnover / initial_nav),
        "costs": float(costs),
    }


def simulate(
    panels: dict[str, pd.DataFrame],
    symbols: list[str],
    config: Config,
    variant: str,
    start: str,
    end: str,
    liquidate_final: bool = True,
    slippage: float = SLIPPAGE,
    commission: float = COMMISSION,
    profit_lock_trigger: float | None = None,
    profit_lock_floor: float = 0.0,
    cash_returns: pd.Series | None = None,
    winner_extension_days: int | None = None,
    winner_extension_min_return: float = 0.0,
    initial_nav: float = INITIAL_NAV,
    ranking_mode: str = "formal_composite",
    partial_profit_trigger: float | None = None,
    partial_profit_fraction: float = 0.50,
    partial_profit_min_notional: float = MIN_NOTIONAL,
) -> dict:
    if variant not in {"strict_veto", "rs_exception", "breadth_exception", "unrestricted"}:
        raise ValueError(variant)
    if config.entry_delay_sessions < 1:
        raise ValueError("entry_delay_sessions must be at least 1")
    if not 0 < config.stock_sleeve_max <= 0.30:
        raise ValueError("stock_sleeve_max must be within (0, 0.30]")
    if initial_nav <= 0:
        raise ValueError("initial_nav must be positive")
    if ranking_mode not in RANKING_MODES:
        raise ValueError(f"unknown ranking mode: {ranking_mode}")
    if profit_lock_trigger is not None and (
        profit_lock_trigger <= 0.0 or profit_lock_floor < 0.0 or profit_lock_floor >= profit_lock_trigger
    ):
        raise ValueError("profit lock requires 0 <= floor < trigger")
    if winner_extension_days is not None and winner_extension_days <= config.max_hold_days:
        raise ValueError("winner extension must exceed max_hold_days")
    if winner_extension_min_return < 0.0:
        raise ValueError("winner extension minimum return cannot be negative")
    if partial_profit_trigger is not None and partial_profit_trigger <= 0.0:
        raise ValueError("partial-profit trigger must be positive")
    if not 0.0 < partial_profit_fraction < 1.0:
        raise ValueError("partial-profit fraction must be within (0, 1)")
    if partial_profit_min_notional <= 0.0:
        raise ValueError("partial-profit minimum notional must be positive")
    features = build_features(panels, symbols, config)
    close, open_, high, low = (panels[name] for name in ("close", "open", "high", "low"))
    dates = close.loc[start:end].dropna(subset=["SPY", "QQQ", "SMH"]).index
    if len(dates) < 2:
        raise RuntimeError(f"insufficient dates for {start}..{end}")

    cash = initial_nav
    positions: dict[str, dict] = {}
    pending_entries: list[dict] = []
    pending_exits: set[str] = set()
    pending_partial_exits: set[str] = set()
    trades: list[dict] = []
    last_exit: dict[str, pd.Timestamp] = {}
    equity_rows, exposure_rows = [], []
    turnover = costs = 0.0
    cash_yield_earned = 0.0
    cash_return_days = 0
    cash_return_missing_days = 0
    ranking_events: list[dict] = []

    for date in dates:
        # Ordinary signals are from the prior completed close and execute now.
        executable_exits, deferred_exits = partition_pending_exit_fills(
            pending_exits, positions, open_, date, slippage
        )
        for symbol, (price, fill) in executable_exits.items():
            pos = positions.pop(symbol)
            proceeds = pos["shares"] * fill - commission
            cash += proceeds
            turnover += pos["shares"] * fill
            costs += commission + pos["shares"] * price * slippage
            trade = trades[pos["trade_index"]]
            total_pnl, total_return = aggregate_position_pnl(pos, proceeds)
            trade.update({
                "exit_date": str(date.date()), "exit_price": fill, "exit_reason": "signal",
                "pnl": total_pnl,
                "return": total_return,
            })
            last_exit[symbol] = date
        pending_exits = deferred_exits

        # A partial sale is a single next-open action. A simultaneous full exit
        # above has precedence and removes the position before this loop.
        for symbol in sorted(pending_partial_exits):
            if symbol not in positions:
                continue
            pos = positions[symbol]
            trade = trades[pos["trade_index"]]
            price = _safe(open_, date, symbol)
            if price is None:
                trade["partial_exit_status"] = "missing_next_open"
                continue
            order, status = partial_exit_order(
                pos["shares"],
                price,
                slippage,
                partial_profit_fraction,
                partial_profit_min_notional,
            )
            if order is None:
                trade["partial_exit_status"] = status
                continue
            trim_shares = order["shares"]
            fill = order["fill"]
            gross_proceeds = order["gross_proceeds"]
            shares_before = pos["shares"]
            allocated_basis = pos["cost_basis"] * trim_shares / shares_before
            proceeds = gross_proceeds - commission
            partial_pnl = proceeds - allocated_basis
            cash += proceeds
            turnover += gross_proceeds
            costs += commission + trim_shares * price * slippage
            pos["shares"] -= trim_shares
            pos["cost_basis"] -= allocated_basis
            pos["realized_pnl"] = pos.get("realized_pnl", 0.0) + partial_pnl
            trade.update(
                {
                    "partial_exit_status": "executed",
                    "partial_exit_date": str(date.date()),
                    "partial_exit_price": fill,
                    "partial_exit_shares": trim_shares,
                    "partial_exit_pnl": partial_pnl,
                }
            )
        pending_partial_exits.clear()

        open_equity = cash + sum(
            pos["shares"] * (_safe(open_, date, symbol) or pos["entry_price"])
            for symbol, pos in positions.items()
        )
        stock_value = sum(
            pos["shares"] * (_safe(open_, date, symbol) or pos["entry_price"])
            for symbol, pos in positions.items()
        )
        ready_entries = []
        waiting_entries = []
        for order in pending_entries:
            order["sessions_waited"] = order.get("sessions_waited", 0) + 1
            if order["sessions_waited"] >= config.entry_delay_sessions:
                ready_entries.append(order)
            else:
                waiting_entries.append(order)
        execution_capacity_symbols = []
        for order in ready_entries:
            symbol = order["symbol"]
            if symbol in positions:
                continue
            if len(positions) >= MAX_NORMAL_NAMES:
                execution_capacity_symbols.append(symbol)
                continue
            price = _safe(open_, date, symbol)
            if price is None:
                continue
            signal_close = order.get("signal_close")
            entry_gap = price / signal_close - 1.0 if signal_close else np.nan
            if np.isfinite(entry_gap) and entry_gap > config.max_entry_gap:
                continue
            entry_type = order["entry_type"]
            is_exception = entry_type != "normal"
            target_weight = config.exception_target_weight if is_exception else config.normal_target_weight
            single_max = EXCEPTION_SINGLE_MAX if is_exception else NORMAL_SINGLE_MAX
            if is_exception and any(pos["entry_type"] != "normal" for pos in positions.values()):
                continue
            fill = price * (1.0 + slippage)
            shares = math.floor(max(open_equity * target_weight - commission, 0.0) / fill)
            if shares < 1 and fill + commission <= open_equity * single_max:
                shares = 1
            if shares < 1:
                continue
            notional = shares * fill
            if notional < MIN_NOTIONAL or 2 * commission / notional > 0.01:
                continue
            if notional + commission > cash:
                execution_capacity_symbols.append(symbol)
                continue
            if notional > open_equity * single_max + 1e-9:
                continue
            if stock_value + notional > open_equity * config.stock_sleeve_max + 1e-9:
                execution_capacity_symbols.append(symbol)
                continue
            cash -= notional + commission
            turnover += notional
            costs += commission + shares * price * slippage
            trade = {
                "symbol": symbol,
                "signal_date": order["signal_date"],
                "entry_date": str(date.date()),
                "entry_price": fill,
                "shares": shares,
                "entry_type": entry_type,
                "smh_healthy_on_signal": order["smh_healthy"],
                "rs20_on_signal": order["rs20"],
                "volume_ratio_on_signal": order["volume_ratio"],
                "ranking_mode": ranking_mode,
                "ranking_score": order.get("ranking_score"),
                "entry_gap": entry_gap,
                "profit_lock_date": None,
                "profit_lock_stop": None,
                "partial_exit_status": None,
                "partial_exit_date": None,
                "partial_exit_price": None,
                "partial_exit_shares": 0,
                "partial_exit_pnl": 0.0,
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
                "cost_basis": notional + commission,
                "original_cost_basis": notional + commission,
                "realized_pnl": 0.0,
                "partial_exit_checked": False,
                "stop": fill * (1.0 - config.stop_loss),
                "initial_stop": fill * (1.0 - config.stop_loss),
                "entry_date": date,
                "entry_type": entry_type,
                "trade_index": len(trades) - 1,
            }
            stock_value += notional
        if execution_capacity_symbols:
            ranking_events.append(
                {
                    "date": str(date.date()),
                    "event_type": "execution_capacity",
                    "available_slots": max(MAX_NORMAL_NAMES - len(positions), 0),
                    "candidates": [order["symbol"] for order in ready_entries],
                    "selected": [
                        order["symbol"]
                        for order in ready_entries
                        if order["symbol"] not in execution_capacity_symbols
                    ],
                    "rejected": execution_capacity_symbols,
                }
            )
        pending_entries = waiting_entries

        # Resting stop orders may execute intraday without using a future close.
        for symbol in list(positions):
            pos = positions[symbol]
            day_open, day_low = _safe(open_, date, symbol), _safe(low, date, symbol)
            if day_open is None or day_low is None or day_low > pos["stop"]:
                continue
            raw_fill = day_open if day_open <= pos["stop"] else pos["stop"]
            fill = raw_fill * (1.0 - slippage)
            proceeds = pos["shares"] * fill - commission
            cash += proceeds
            turnover += pos["shares"] * fill
            costs += commission + pos["shares"] * raw_fill * slippage
            trade = trades[pos["trade_index"]]
            exit_reason = "profit_lock" if pos["stop"] > pos["initial_stop"] + 1e-12 else "stop"
            total_pnl, total_return = aggregate_position_pnl(pos, proceeds)
            trade.update({
                "exit_date": str(date.date()), "exit_price": fill, "exit_reason": "stop",
                "pnl": total_pnl,
                "return": total_return,
            })
            trade["exit_reason"] = exit_reason
            positions.pop(symbol)
            last_exit[symbol] = date

        # Optional cash-sweep return accrues at the close on cash remaining
        # after that session's executions. The first backtest date earns no
        # pre-start return. The default remains zero-yield cash.
        if cash_returns is not None and date != dates[0]:
            cash_return = cash_returns.get(date, np.nan)
            if np.isfinite(cash_return):
                earned = cash * float(cash_return)
                cash += earned
                cash_yield_earned += earned
                cash_return_days += 1
            else:
                cash_return_missing_days += 1

        close_equity = cash + sum(
            pos["shares"] * (_safe(close, date, symbol) or pos["entry_price"])
            for symbol, pos in positions.items()
        )
        close_stock_value = close_equity - cash
        equity_rows.append((date, close_equity))
        exposure_rows.append((date, close_stock_value / close_equity if close_equity else 0.0))

        # Generate orders only after the completed close.
        for symbol, pos in positions.items():
            close_price = _safe(close, date, symbol)
            ma20 = _safe(features["ma20"], date, symbol)
            rs20 = features["rs20"].at[date, symbol] if date in features["rs20"].index else np.nan
            held = close.index.get_loc(date) - close.index.get_loc(pos["entry_date"])
            if close_price is not None:
                new_stop, raised = ratcheted_profit_stop(
                    pos["entry_price"],
                    pos["stop"],
                    close_price,
                    profit_lock_trigger,
                    profit_lock_floor,
                )
                if raised:
                    pos["stop"] = new_stop
                    trade = trades[pos["trade_index"]]
                    trade["profit_lock_date"] = str(date.date())
                    trade["profit_lock_stop"] = new_stop
                if (
                    partial_profit_trigger is not None
                    and not pos.get("partial_exit_checked", False)
                    and close_price >= pos["entry_price"] * (1.0 + partial_profit_trigger)
                ):
                    pos["partial_exit_checked"] = True
                    pending_partial_exits.add(symbol)
            extension_active = (
                close_price is not None
                and ma20 is not None
                and np.isfinite(rs20)
                and winner_extension_active(
                    pos["entry_price"],
                    close_price,
                    ma20,
                    float(rs20),
                    held,
                    config.max_hold_days,
                    winner_extension_days,
                    winner_extension_min_return,
                )
            )
            time_exit = held >= config.max_hold_days and not extension_active
            if close_price is not None and ma20 is not None and (
                close_price < ma20 or (np.isfinite(rs20) and rs20 < 0.0) or time_exit
            ):
                pending_exits.add(symbol)

        if not bool(features["broad_healthy"].get(date, False)):
            continue
        smh_healthy = bool(features["smh_healthy"].get(date, False))
        if variant == "strict_veto" and not smh_healthy:
            continue
        entry_type = "normal" if smh_healthy or variant == "unrestricted" else (
            "breadth_exception" if variant == "breadth_exception" else "exception"
        )
        if entry_type == "exception" and variant != "rs_exception":
            continue
        if entry_type == "breadth_exception" and variant != "breadth_exception":
            continue
        if entry_type != "normal" and any(pos["entry_type"] != "normal" for pos in positions.values()):
            continue
        available_slots = MAX_NORMAL_NAMES - len(positions)
        if entry_type != "normal":
            available_slots = min(available_slots, 1)
        if available_slots <= 0:
            continue
        candidate_signal = features["repair_signal"] if entry_type == "breadth_exception" else features["signal"]
        candidate_score = features["repair_score"] if entry_type == "breadth_exception" else features["score"]
        candidates = []
        for symbol in symbols:
            if symbol in positions or not bool(candidate_signal.at[date, symbol]):
                continue
            if symbol in last_exit and (date - last_exit[symbol]).days <= 3:
                continue
            candidates.append(symbol)
        ranked_candidates = rank_entry_candidates(features, date, candidates, ranking_mode)
        selected_candidates = ranked_candidates[:available_slots]
        if len(ranked_candidates) > available_slots:
            ranking_events.append(
                {
                    "date": str(date.date()),
                    "event_type": "signal_slot_contention",
                    "available_slots": available_slots,
                    "candidates": [row["symbol"] for row in ranked_candidates],
                    "selected": [row["symbol"] for row in selected_candidates],
                    "rejected": [row["symbol"] for row in ranked_candidates[available_slots:]],
                }
            )
        for ranked_row in selected_candidates:
            symbol = ranked_row["symbol"]
            pending_entries.append({
                "symbol": symbol,
                "signal_date": str(date.date()),
                "entry_type": entry_type,
                "smh_healthy": smh_healthy,
                "rs20": float(features["rs20"].at[date, symbol]),
                "rs10": float(features["rs10"].at[date, symbol]),
                "volume_ratio": float(features["volume_ratio"].at[date, symbol]),
                "breadth_score": float(features["breadth_score"].at[date, symbol]),
                "signal_close": float(close.at[date, symbol]),
                "ranking_score": ranked_row["ranking_score"],
                "sessions_waited": 0,
            })

    # Historical comparisons liquidate for complete trade statistics. Forward
    # shadow runs disable this so repeated snapshots do not fabricate a sale at
    # each observation cutoff.
    final_date = dates[-1]
    if liquidate_final:
        for symbol, pos in list(positions.items()):
            price = _safe(close, final_date, symbol)
            if price is None:
                continue
            fill = price * (1.0 - slippage)
            proceeds = pos["shares"] * fill - commission
            cash += proceeds
            turnover += pos["shares"] * fill
            costs += commission + pos["shares"] * price * slippage
            trade = trades[pos["trade_index"]]
            total_pnl, total_return = aggregate_position_pnl(pos, proceeds)
            trade.update({
                "exit_date": str(final_date.date()), "exit_price": fill, "exit_reason": "terminal",
                "pnl": total_pnl,
                "return": total_return,
            })
            positions.pop(symbol)
    equity = pd.Series(dict(equity_rows), dtype=float)
    if liquidate_final:
        equity.iloc[-1] = cash
    exposure = pd.Series(dict(exposure_rows), dtype=float)
    open_positions = []
    for symbol, pos in positions.items():
        last_close = _safe(close, final_date, symbol) or pos["entry_price"]
        open_positions.append({
            "symbol": symbol,
            "shares": pos["shares"],
            "entry_price": pos["entry_price"],
            "entry_date": str(pos["entry_date"].date()),
            "stop": pos["stop"],
            "entry_type": pos["entry_type"],
            "last_close": last_close,
            "unrealized_pnl": pos["shares"] * last_close - pos["cost_basis"],
            "realized_pnl": pos.get("realized_pnl", 0.0),
        })
    metrics = _metrics(equity, trades, exposure, turnover, costs, initial_nav)
    metrics.update(
        {
            "cash_yield_earned": float(cash_yield_earned),
            "cash_return_days": cash_return_days,
            "cash_return_missing_days": cash_return_missing_days,
        }
    )
    result = {
        "variant": variant,
        "period": [str(dates[0].date()), str(dates[-1].date())],
        "config": asdict(config),
        "metrics": metrics,
        "trades": trades,
        "open_positions": open_positions,
        "pending_entries": pending_entries,
        "pending_exits": sorted(pending_exits),
        "pending_partial_exits": sorted(pending_partial_exits),
        "ranking_mode": ranking_mode,
        "ranking_events": ranking_events,
        "ranking_contention_decisions": len({event["date"] for event in ranking_events}),
        "liquidated_at_end": liquidate_final,
        "profit_lock_overlay": {
            "trigger": profit_lock_trigger,
            "floor": profit_lock_floor,
            "activation_basis": "completed_close_effective_next_session",
        },
        "partial_profit_overlay": {
            "trigger": partial_profit_trigger,
            "fraction": partial_profit_fraction,
            "minimum_notional": partial_profit_min_notional,
            "executed": sum(trade.get("partial_exit_status") == "executed" for trade in trades),
            "ineligible": sum(
                str(trade.get("partial_exit_status", "")).startswith("ineligible")
                for trade in trades
            ),
            "activation_basis": "completed_close_next_session_open_once",
        },
        "cash_return_overlay": {
            "enabled": cash_returns is not None,
            "timing": "session_close_on_post_execution_cash",
        },
        "equity": {str(k.date()): float(v) for k, v in equity.items()},
        "exposure": {str(k.date()): float(v) for k, v in exposure.items()},
    }
    return result


def fixed_path_cost_stress(
    result: dict,
    source_slippage: float = SLIPPAGE,
    stressed_slippage: float = 0.002,
    commission: float = COMMISSION,
) -> dict:
    """Reprice the same shares and trade path at a different slippage level.

    This isolates execution cost from whole-share and exposure-cap path changes.
    It intentionally does not estimate a stressed daily Sharpe or drawdown.
    """
    closed_pnl = 0.0
    closed_trades = 0
    for trade in result["trades"]:
        if trade.get("exit_price") is None:
            continue
        raw_entry = trade["entry_price"] / (1.0 + source_slippage)
        raw_exit = trade["exit_price"] / (1.0 - source_slippage)
        cost_basis = trade["shares"] * raw_entry * (1.0 + stressed_slippage) + commission
        proceeds = trade["shares"] * raw_exit * (1.0 - stressed_slippage) - commission
        closed_pnl += proceeds - cost_basis
        closed_trades += 1
    open_unrealized = 0.0
    for position in result.get("open_positions", []):
        raw_entry = position["entry_price"] / (1.0 + source_slippage)
        cost_basis = position["shares"] * raw_entry * (1.0 + stressed_slippage) + commission
        open_unrealized += position["shares"] * position["last_close"] - cost_basis
    final_value = INITIAL_NAV + closed_pnl + open_unrealized
    return {
        "source_slippage": source_slippage,
        "stressed_slippage": stressed_slippage,
        "closed_trades": closed_trades,
        "open_positions": len(result.get("open_positions", [])),
        "closed_pnl": closed_pnl,
        "open_unrealized": open_unrealized,
        "final_value": final_value,
        "total_return": final_value / INITIAL_NAV - 1.0,
    }


def quality_score(metrics: dict) -> float:
    if metrics["trade_count"] < 8 or metrics["win_rate"] is None:
        return -999.0
    return (
        metrics["cagr"]
        + 0.10 * metrics["sharpe"]
        - 0.50 * abs(metrics["max_drawdown"])
        + 0.05 * (metrics["win_rate"] - 0.50)
    )


def compact(result: dict) -> dict:
    return {"variant": result["variant"], "period": result["period"], "config": result["config"], **result["metrics"]}


def format_percent(value) -> str:
    return "n/a" if value is None else f"{value:.2%}"


def main() -> None:
    panels, symbols = load_panels()
    last_date = panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1]
    train = ("2024-01-02", "2025-12-31")
    test = ("2026-01-01", str(last_date.date()))
    full = ("2024-01-02", str(last_date.date()))
    default = Config()

    default_runs = {}
    for label, period in (("train", train), ("test", test), ("full", full)):
        for variant in ("strict_veto", "rs_exception", "breadth_exception", "unrestricted"):
            default_runs[f"{label}_{variant}"] = simulate(panels, symbols, default, variant, *period)

    grid_rows = []
    configs = [
        Config(rs, vol, ext, hold, weight)
        for rs, vol, ext, hold, weight in itertools.product(
            (0.03, 0.05, 0.08),
            (1.0, 1.2, 1.5),
            (0.08, 0.12, 0.15),
            (10, 20, 30),
            (0.03, 0.05),
        )
    ]
    for cfg in configs:
        result = simulate(panels, symbols, cfg, "rs_exception", *train)
        row = {**asdict(cfg), **result["metrics"]}
        row["quality_score"] = quality_score(result["metrics"])
        grid_rows.append(row)
    grid = pd.DataFrame(grid_rows).sort_values("quality_score", ascending=False)
    best_cfg = Config(**{name: grid.iloc[0][name].item() for name in asdict(default)})

    selected_runs = {}
    for label, period in (("train", train), ("test", test), ("full", full)):
        for variant in ("strict_veto", "rs_exception"):
            selected_runs[f"{label}_{variant}"] = simulate(panels, symbols, best_cfg, variant, *period)

    breadth_grid_rows = []
    breadth_configs = [
        Config(
            volume_ratio_min=vol,
            max_hold_days=hold,
            exception_target_weight=weight,
            repair_rs10_min=rs10,
            breadth_min=breadth,
            breadth_count_min=count,
        )
        for rs10, breadth, count, vol, hold, weight in itertools.product(
            (0.02, 0.04), (0.40, 0.60), (2, 3), (1.0, 1.2), (10, 20), (0.03, 0.05)
        )
    ]
    for cfg in breadth_configs:
        result = simulate(panels, symbols, cfg, "breadth_exception", *train)
        row = {**asdict(cfg), **result["metrics"]}
        row["quality_score"] = quality_score(result["metrics"])
        breadth_grid_rows.append(row)
    breadth_grid = pd.DataFrame(breadth_grid_rows).sort_values("quality_score", ascending=False)
    best_breadth_cfg = Config(**{name: breadth_grid.iloc[0][name].item() for name in asdict(default)})
    selected_breadth_runs = {}
    for label, period in (("train", train), ("test", test), ("full", full)):
        for variant in ("strict_veto", "breadth_exception"):
            selected_breadth_runs[f"{label}_{variant}"] = simulate(
                panels, symbols, best_breadth_cfg, variant, *period
            )

    risk_grid_rows = []
    risk_configs = [
        Config(
            rs20_min=rs20,
            volume_ratio_min=vol,
            max_extension=ext,
            max_hold_days=hold,
            stop_loss=stop,
            max_atr_pct=atr,
            min_close_location=location,
        )
        for rs20, vol, ext, hold, stop, atr, location in itertools.product(
            (0.03, 0.05), (1.0, 1.2), (0.08, 0.12), (10, 20, 30),
            (0.06, 0.08), (0.04, 0.06, 0.08), (0.50, 0.70)
        )
    ]
    for cfg in risk_configs:
        result = simulate(panels, symbols, cfg, "strict_veto", *train)
        row = {**asdict(cfg), **result["metrics"]}
        row["quality_score"] = quality_score(result["metrics"])
        risk_grid_rows.append(row)
    risk_grid = pd.DataFrame(risk_grid_rows).sort_values("quality_score", ascending=False)
    best_risk_cfg = Config(**{name: risk_grid.iloc[0][name].item() for name in asdict(default)})
    risk_periods = {
        "2024": ("2024-01-02", "2024-12-31"),
        "2025": ("2025-01-01", "2025-12-31"),
        "2026": test,
        "train": train,
        "full": full,
    }
    selected_risk_runs = {
        label: simulate(panels, symbols, best_risk_cfg, "strict_veto", *period)
        for label, period in risk_periods.items()
    }

    test_strict = selected_runs["test_strict_veto"]["metrics"]
    test_exception = selected_runs["test_rs_exception"]["metrics"]
    improvement = {
        "total_return_delta": test_exception["total_return"] - test_strict["total_return"],
        "cagr_delta": test_exception["cagr"] - test_strict["cagr"],
        "max_drawdown_delta": test_exception["max_drawdown"] - test_strict["max_drawdown"],
        "sharpe_delta": test_exception["sharpe"] - test_strict["sharpe"],
        "win_rate_delta": (
            test_exception["win_rate"] - test_strict["win_rate"]
            if test_exception["win_rate"] is not None and test_strict["win_rate"] is not None else None
        ),
    }
    breadth_test_strict = selected_breadth_runs["test_strict_veto"]["metrics"]
    breadth_test_exception = selected_breadth_runs["test_breadth_exception"]["metrics"]
    breadth_improvement = {
        "total_return_delta": breadth_test_exception["total_return"] - breadth_test_strict["total_return"],
        "cagr_delta": breadth_test_exception["cagr"] - breadth_test_strict["cagr"],
        "max_drawdown_delta": breadth_test_exception["max_drawdown"] - breadth_test_strict["max_drawdown"],
        "sharpe_delta": breadth_test_exception["sharpe"] - breadth_test_strict["sharpe"],
        "win_rate_delta": (
            breadth_test_exception["win_rate"] - breadth_test_strict["win_rate"]
            if breadth_test_exception["win_rate"] is not None and breadth_test_strict["win_rate"] is not None else None
        ),
    }
    default_test_strict = default_runs["test_strict_veto"]["metrics"]
    risk_test = selected_risk_runs["2026"]["metrics"]
    risk_improvement = {
        "total_return_delta": risk_test["total_return"] - default_test_strict["total_return"],
        "cagr_delta": risk_test["cagr"] - default_test_strict["cagr"],
        "max_drawdown_delta": risk_test["max_drawdown"] - default_test_strict["max_drawdown"],
        "sharpe_delta": risk_test["sharpe"] - default_test_strict["sharpe"],
        "win_rate_delta": (
            risk_test["win_rate"] - default_test_strict["win_rate"]
            if risk_test["win_rate"] is not None and default_test_strict["win_rate"] is not None else None
        ),
    }
    passes = (
        breadth_improvement["total_return_delta"] > 0
        and breadth_improvement["sharpe_delta"] >= 0
        and breadth_improvement["max_drawdown_delta"] >= -0.01
        and (breadth_improvement["win_rate_delta"] is None or breadth_improvement["win_rate_delta"] >= 0)
        and breadth_test_exception["exception_trade_count"] >= 5
    )
    output = {
        "experiment": "smh_relative_strength_exception",
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_end": str(last_date.date()),
        "research_only": True,
        "authorizes_trade": False,
        "fixed_current_watchlist_bias": True,
        "cost_model": {"initial_nav": INITIAL_NAV, "commission_per_order": COMMISSION, "slippage_per_side": SLIPPAGE},
        "default_config": asdict(default),
        "selected_on_train_config": asdict(best_cfg),
        "selected_breadth_on_train_config": asdict(best_breadth_cfg),
        "selected_risk_on_train_config": asdict(best_risk_cfg),
        "default_runs": {key: compact(value) for key, value in default_runs.items()},
        "selected_runs": {key: compact(value) for key, value in selected_runs.items()},
        "selected_breadth_runs": {key: compact(value) for key, value in selected_breadth_runs.items()},
        "selected_risk_runs": {key: compact(value) for key, value in selected_risk_runs.items()},
        "selected_test_delta": improvement,
        "selected_breadth_test_delta": breadth_improvement,
        "selected_risk_test_delta": risk_improvement,
        "risk_filter_status": "post_hoc_candidate_requires_fresh_forward_evidence",
        "promotion_gate_passed": bool(passes),
        "decision": "eligible_for_forward_shadow" if passes else "not_promoted; retain_strict_veto_and_continue_research",
        "limitations": [
            "Current watchlist is applied retrospectively and is not a point-in-time universe.",
            "Earnings are approximated by a >=10% positive opening-gap cooldown because a PIT earnings calendar is unavailable.",
            "The cached OHLCV dataset ends before the 2026-08-14 review week completed.",
            "A research pass can only start a forward shadow; it cannot change formal V9 or authorize an order.",
        ],
    }

    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "summary.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    grid.to_csv(RESULTS / "train_parameter_grid.csv", index=False)
    breadth_grid.to_csv(RESULTS / "train_breadth_parameter_grid.csv", index=False)
    risk_grid.to_csv(RESULTS / "train_risk_parameter_grid.csv", index=False)
    trade_outputs = {
        **default_runs,
        **{f"selected_{k}": v for k, v in selected_runs.items()},
        **{f"selected_breadth_{k}": v for k, v in selected_breadth_runs.items()},
        **{f"selected_risk_{k}": v for k, v in selected_risk_runs.items()},
    }
    for key, value in trade_outputs.items():
        pd.DataFrame(value["trades"]).to_csv(RESULTS / f"{key}_trades.csv", index=False)

    rows = [
        "# SMH Relative-Strength Exception Backtest",
        "",
        f"- Data: `2024-01-02` to `{last_date.date()}`",
        "- Training: `2024-2025`; held-out test: `2026 YTD`",
        "- Research-only; formal V9 weights changed: `false`",
        f"- Promotion gate: `{'pass for forward shadow only' if passes else 'fail'}`",
        f"- Decision: `{output['decision']}`",
        "",
        "## Default pre-specified configuration",
        "",
        "| Period | Variant | Return | CAGR | Max DD | Sharpe | Win rate | Trades | Exception trades | Exposure |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label in ("train", "test", "full"):
        for variant in ("strict_veto", "rs_exception", "breadth_exception", "unrestricted"):
            m = default_runs[f"{label}_{variant}"]["metrics"]
            rows.append(
                f"| {label} | {variant} | {format_percent(m['total_return'])} | {format_percent(m['cagr'])} | "
                f"{format_percent(m['max_drawdown'])} | {m['sharpe']:.2f} | {format_percent(m['win_rate'])} | "
                f"{m['trade_count']} | {m['exception_trade_count']} | {format_percent(m['exposure'])} |"
            )
    rows += [
        "",
        "## Train-selected configuration and held-out result",
        "",
        f"Selected parameters: `{json.dumps(asdict(best_cfg), sort_keys=True)}`",
        "",
        "| Test variant | Return | Max DD | Sharpe | Win rate | Trades | Exception win rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant in ("strict_veto", "rs_exception"):
        m = selected_runs[f"test_{variant}"]["metrics"]
        rows.append(
            f"| {variant} | {format_percent(m['total_return'])} | {format_percent(m['max_drawdown'])} | "
            f"{m['sharpe']:.2f} | {format_percent(m['win_rate'])} | {m['trade_count']} | "
            f"{format_percent(m['exception_win_rate'])} |"
        )
    rows += [
        "",
        "## Held-out delta: exception minus strict veto",
        "",
        f"- Return: `{improvement['total_return_delta']:+.2%}`",
        f"- CAGR: `{improvement['cagr_delta']:+.2%}`",
        f"- Max drawdown: `{improvement['max_drawdown_delta']:+.2%}` (positive is better)",
        f"- Sharpe: `{improvement['sharpe_delta']:+.2f}`",
        f"- Trade win rate: `{format_percent(improvement['win_rate_delta'])}`",
        "",
        "## Breadth-confirmed repair exception",
        "",
        f"Selected parameters: `{json.dumps(asdict(best_breadth_cfg), sort_keys=True)}`",
        "",
        "| Test variant | Return | Max DD | Sharpe | Win rate | Trades | Exception trades | Exception win rate |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant in ("strict_veto", "breadth_exception"):
        m = selected_breadth_runs[f"test_{variant}"]["metrics"]
        rows.append(
            f"| {variant} | {format_percent(m['total_return'])} | {format_percent(m['max_drawdown'])} | "
            f"{m['sharpe']:.2f} | {format_percent(m['win_rate'])} | {m['trade_count']} | "
            f"{m['exception_trade_count']} | {format_percent(m['exception_win_rate'])} |"
        )
    rows += [
        "",
        f"Breadth test return delta: `{breadth_improvement['total_return_delta']:+.2%}`; "
        f"Sharpe delta: `{breadth_improvement['sharpe_delta']:+.2f}`; "
        f"win-rate delta: `{format_percent(breadth_improvement['win_rate_delta'])}`.",
        "",
        "## Volatility-adapted strict entry",
        "",
        f"Selected parameters: `{json.dumps(asdict(best_risk_cfg), sort_keys=True)}`",
        "",
        "| Period | Return | Max DD | Sharpe | Win rate | Trades | Profit factor |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for label in ("2024", "2025", "2026", "full"):
        m = selected_risk_runs[label]["metrics"]
        profit_factor = "n/a" if m["profit_factor"] is None else f"{m['profit_factor']:.2f}"
        rows.append(
            f"| {label} | {format_percent(m['total_return'])} | {format_percent(m['max_drawdown'])} | "
            f"{m['sharpe']:.2f} | {format_percent(m['win_rate'])} | {m['trade_count']} | "
            f"{profit_factor} |"
        )
    rows += [
        "",
        f"2026 delta versus default strict: return `{risk_improvement['total_return_delta']:+.2%}`, "
        f"Sharpe `{risk_improvement['sharpe_delta']:+.2f}`, "
        f"win rate `{format_percent(risk_improvement['win_rate_delta'])}`.",
        "",
        "This filter is post-hoc because the 2026 loss pattern was inspected before defining it; it requires fresh forward evidence.",
        "",
        "## Limitations",
        "",
    ]
    rows += [f"- {item}" for item in output["limitations"]]
    (RESULTS / "report.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
