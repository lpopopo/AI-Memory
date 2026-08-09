"""Whole-share, fee-aware reconciliation for a manual V9 real account.

This module produces an auditable proposal only. It never connects to a broker
and never converts a stale or missed signal into authorization.
"""
from __future__ import annotations

from itertools import product
import math


def _candidate_quantities(target_shares: float, current_shares: int, max_shares: int) -> list[int]:
    if max_shares <= 200:
        return list(range(max_shares + 1))
    center = int(math.floor(target_shares))
    values = {0, current_shares, max_shares}
    values.update(range(max(0, center - 5), min(max_shares, center + 5) + 1))
    return sorted(values)


def reconcile_whole_share_account(
    *,
    cash: float,
    positions: dict[str, int],
    prices: dict[str, float],
    desired_core_weights: dict[str, float],
    stock_symbols: set[str],
    cash_floor: float,
    stock_cap: float,
    fee_per_order: float = 1.0,
    order_authorized: bool = False,
    authorization_reason: str = "signal_not_authorized",
) -> dict:
    """Reconcile model weights with actual holdings without fractional shares."""
    if cash < 0 or fee_per_order < 0:
        raise ValueError("cash and fees must be non-negative")
    if not 0 <= cash_floor < 1 or not 0 <= stock_cap <= 1:
        raise ValueError("cash floor and stock cap must be valid weights")
    if not desired_core_weights or any(weight < 0 for weight in desired_core_weights.values()):
        raise ValueError("desired core weights must be non-empty and non-negative")

    all_symbols = set(positions) | set(desired_core_weights)
    missing_prices = sorted(symbol for symbol in all_symbols if symbol not in prices or prices[symbol] <= 0)
    if missing_prices:
        raise ValueError(f"missing or invalid prices: {missing_prices}")

    market_values = {symbol: int(shares) * float(prices[symbol]) for symbol, shares in positions.items()}
    nav = float(cash) + sum(market_values.values())
    if nav <= 0:
        raise ValueError("account NAV must be positive")

    core_symbols = tuple(sorted(desired_core_weights))
    non_core_value = sum(value for symbol, value in market_values.items() if symbol not in core_symbols)
    stock_value = sum(market_values.get(symbol, 0.0) for symbol in stock_symbols)
    stock_weight = stock_value / nav
    max_gross_value = nav * (1.0 - cash_floor)
    max_core_value = max(0.0, max_gross_value - non_core_value)
    requested_core_weight = sum(desired_core_weights.values())
    feasible_core_weight = min(requested_core_weight, max_core_value / nav)
    scale = feasible_core_weight / requested_core_weight if requested_core_weight > 0 else 0.0
    effective_targets = {symbol: desired_core_weights[symbol] * scale for symbol in core_symbols}

    candidate_sets = []
    for symbol in core_symbols:
        price = float(prices[symbol])
        max_shares = int(math.floor(max_core_value / price))
        target_shares = effective_targets[symbol] * nav / price
        candidate_sets.append(_candidate_quantities(target_shares, int(positions.get(symbol, 0)), max_shares))

    best = None
    for quantities in product(*candidate_sets):
        target_shares = dict(zip(core_symbols, quantities))
        deltas = {symbol: target_shares[symbol] - int(positions.get(symbol, 0)) for symbol in core_symbols}
        order_count = sum(delta != 0 for delta in deltas.values())
        ending_cash = float(cash) - sum(delta * float(prices[symbol]) for symbol, delta in deltas.items()) - order_count * fee_per_order
        core_value = sum(target_shares[symbol] * float(prices[symbol]) for symbol in core_symbols)
        gross_value = non_core_value + core_value
        if ending_cash < nav * cash_floor - 1e-9 or gross_value > max_gross_value + 1e-9:
            continue
        tracking_error = sum((core_value_symbol / nav - effective_targets[symbol]) ** 2 for symbol, core_value_symbol in ((s, target_shares[s] * float(prices[s])) for s in core_symbols))
        turnover = sum(abs(delta) * float(prices[symbol]) for symbol, delta in deltas.items())
        key = (tracking_error, turnover, -ending_cash)
        if best is None or key < best[0]:
            best = (key, target_shares, deltas, ending_cash, core_value, order_count)

    if best is None:
        raise RuntimeError("no whole-share allocation satisfies the cash floor")

    _, target_shares, deltas, ending_cash, core_value, order_count = best
    proposed_orders = []
    for symbol in core_symbols:
        delta = deltas[symbol]
        if delta == 0:
            continue
        proposed_orders.append({
            "symbol": symbol,
            "action": "BUY" if delta > 0 else "SELL",
            "shares": abs(int(delta)),
            "reference_price": float(prices[symbol]),
            "notional": abs(float(delta)) * float(prices[symbol]),
            "estimated_fee": fee_per_order,
        })

    unknown_positions = sorted(set(positions) - stock_symbols - set(core_symbols))
    alerts = []
    if stock_weight > stock_cap + 1e-9:
        alerts.append("stock_sleeve_over_cap_no_new_stock_risk")
    if unknown_positions:
        alerts.append("unclassified_positions_require_review")
    if feasible_core_weight + 1e-9 < requested_core_weight:
        alerts.append("core_target_reduced_by_cash_floor_and_existing_positions")
    if not order_authorized and proposed_orders:
        alerts.append("proposal_only_signal_authorization_missing")

    return {
        "nav": nav,
        "starting_cash": float(cash),
        "starting_stock_weight": stock_weight,
        "stock_cap": stock_cap,
        "stock_overage": max(0.0, stock_weight - stock_cap),
        "cash_floor": cash_floor,
        "requested_core_weights": {symbol: float(desired_core_weights[symbol]) for symbol in core_symbols},
        "effective_core_weights": effective_targets,
        "target_core_shares": target_shares,
        "ending_core_weight": core_value / nav,
        "ending_cash": ending_cash,
        "ending_cash_weight": ending_cash / nav,
        "estimated_fees": order_count * fee_per_order,
        "proposed_orders": proposed_orders,
        "executable_orders": proposed_orders if order_authorized else [],
        "order_authorized": bool(order_authorized),
        "authorization_reason": authorization_reason,
        "alerts": alerts,
        "unknown_positions": unknown_positions,
    }
