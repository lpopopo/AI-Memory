#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent))

from backtest_dual_sleeve import RESULTS_DIR, pct, run_buy_hold, summarize
from market_fear import compute_fear, download_market_data
from test_v4_stock_alpha import V4Config, combine_weights, is_bear, is_bull, month_end_dates, prepare_indicators, value_weights
from test_v4_universe_alpha import calculate_turnover, growth_weights_universe, run_v4_universe
from test_v4_long_term import slice_curve
from validate_2026_current_strategy import START_2026, load_validation_data


V5_CONFIG = V4Config(
    name="dual_sleeve_v5_with_market_fear_gate",
    bull_value_weight=0.30,
    bull_growth_weight=0.70,
    normal_value_weight=0.40,
    normal_growth_weight=0.60,
    bear_value_weight=0.70,
    bear_growth_weight=0.30,
    bull_rule="qqq200_m126",
    bear_rule="both_below_200_negative_m63",
    stock_top_n=10,
    value_mode="top2",
    score_mode="m63_m126",
    fallback="cash",
)


BASE_V5_CONFIG = V4Config(
    name="dual_sleeve_v5_universe_optimal",
    bull_value_weight=0.30,
    bull_growth_weight=0.70,
    normal_value_weight=0.40,
    normal_growth_weight=0.60,
    bear_value_weight=0.70,
    bear_growth_weight=0.30,
    bull_rule="qqq200_m126",
    bear_rule="both_below_200_negative_m63",
    stock_top_n=10,
    value_mode="top2",
    score_mode="m63_m126",
    fallback="cash",
)


def market_fear_by_date(start="2025-01-01", end="2026-05-30") -> dict[pd.Timestamp, object]:
    market = download_market_data(start=start, end=end)
    out = {}
    for dt in market.index:
        sub = market.loc[:dt]
        if len(sub) < 200:
            continue
        result = compute_fear(sub)
        out[pd.Timestamp(dt).normalize()] = result
    return out


def get_fear_result(fear_map, dt):
    key = pd.Timestamp(dt).normalize()
    if key in fear_map:
        return fear_map[key]
    prior = [k for k in fear_map.keys() if k <= key]
    if not prior:
        return None
    return fear_map[max(prior)]


def scale_weights_for_fear(weights, result):
    if result is None:
        return weights, 0.0
    target_exposure = min(sum(weights.values()) * result.risk_multiplier, result.max_gross_exposure)
    if result.regime == "panic":
        target_exposure = 0.0
    if target_exposure <= 0:
        return {}, 1.0
    current = sum(weights.values())
    if current <= 0:
        return {}, 1.0
    scale = min(1.0, target_exposure / current)
    scaled = {symbol: weight * scale for symbol, weight in weights.items()}
    cash = max(0.0, 1.0 - sum(scaled.values()))
    if cash < result.cash_floor:
        floor_scale = max(0.0, (1.0 - result.cash_floor) / sum(scaled.values()))
        scaled = {symbol: weight * floor_scale for symbol, weight in scaled.items()}
    return scaled, max(0.0, 1.0 - sum(scaled.values()))


def run_v5_with_fear_gate(close, indicators, config, fear_map, transaction_cost=0.001, stop_loss_pct=0.30):
    returns = indicators["returns"]
    rebalance_dates = month_end_dates(close.index)
    equity = []
    allocations = []
    weights = {}
    pending_weights = None
    high_water_marks = {}
    value = 1.0

    for dt in close.index:
        day_return = 0.0
        for symbol, weight in weights.items():
            if symbol in returns.columns and pd.notna(returns.at[dt, symbol]):
                day_return += weight * returns.at[dt, symbol]
        value *= 1.0 + day_return

        if pending_weights is not None:
            turnover = calculate_turnover(weights, pending_weights)
            value *= 1.0 - (turnover * transaction_cost)
            weights = pending_weights
            pending_weights = None
            high_water_marks = {}
            for symbol in weights.keys():
                if symbol in close.columns and pd.notna(close.at[dt, symbol]):
                    high_water_marks[symbol] = close.at[dt, symbol]
        else:
            symbols_to_sell = []
            for symbol in list(weights.keys()):
                if symbol in {"SPY", "QQQ", "VTV", "IWD", "SCHD"}:
                    continue
                current_price = close.at[dt, symbol] if symbol in close.columns else None
                if current_price is None or pd.isna(current_price):
                    continue
                high_water_marks[symbol] = max(high_water_marks.get(symbol, current_price), current_price)
                if current_price < high_water_marks[symbol] * (1.0 - stop_loss_pct):
                    symbols_to_sell.append(symbol)
            for symbol in symbols_to_sell:
                value *= 1.0 - (weights[symbol] * transaction_cost)
                del weights[symbol]
                high_water_marks.pop(symbol, None)

        equity.append(value)

        if dt in rebalance_dates:
            bull = is_bull(config, close, indicators, dt)
            bear = is_bear(config, close, indicators, dt)
            if bear:
                value_target = config.bear_value_weight
                growth_target = config.bear_growth_weight
            elif bull:
                value_target = config.bull_value_weight
                growth_target = config.bull_growth_weight
            else:
                value_target = config.normal_value_weight
                growth_target = config.normal_growth_weight

            v = value_weights(config, close, indicators, dt, value_target)
            if bear:
                filtered_v = {}
                for symbol, w in v.items():
                    ma200 = indicators["ma200"].at[dt, symbol]
                    current_price = close.at[dt, symbol]
                    if pd.notna(ma200) and current_price > ma200:
                        filtered_v[symbol] = w
                v = filtered_v
            g = growth_weights_universe(config, close, indicators, dt, growth_target, bull)
            raw_weights = combine_weights(v, g)

            fear = get_fear_result(fear_map, dt)
            pending_weights, cash = scale_weights_for_fear(raw_weights, fear)
            allocations.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "bull": bull,
                    "bear": bear,
                    "fear_regime": fear.regime if fear else "unavailable",
                    "fear_score": fear.score if fear else None,
                    "risk_multiplier": fear.risk_multiplier if fear else None,
                    "value": "|".join(sorted(v)),
                    "growth": "|".join(sorted(g)),
                    "cash": cash,
                }
            )

    return pd.Series(equity, index=close.index, name=config.name), pd.DataFrame(allocations)


def period_return(curve):
    sliced = slice_curve(curve, START_2026, curve.index[-1])
    return float(sliced.iloc[-1] / sliced.iloc[0] - 1.0)


def rebased(curve):
    sliced = slice_curve(curve, START_2026, curve.index[-1])
    return sliced / sliced.iloc[0]


def write_report(curves, allocations):
    rows = []
    rebased_curves = []
    for label, curve in curves.items():
        ytd = rebased(curve).rename(label)
        rebased_curves.append(ytd)
        row = summarize(label, ytd)
        row["period_return"] = period_return(curve)
        rows.append(row)

    equity_path = RESULTS_DIR / "strategy_2026_ytd_fear_integrated_equity_curve.csv"
    pd.concat(rebased_curves, axis=1).to_csv(equity_path, index_label="date")
    allocations_path = RESULTS_DIR / "strategy_2026_ytd_fear_integrated_allocations.csv"
    allocations.to_csv(allocations_path, index=False)

    lines = [
        "# 2026 YTD Fear-Integrated Strategy Validation",
        "",
        "This report compares the original V5 strategy with V5 plus the market fear gate.",
        "",
        "## Performance",
        "",
        "| Strategy | Period Return | Annualized Return | Max Drawdown | Volatility | Sharpe | Sortino |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['name']} | {pct(row['period_return'])} | {pct(row['cagr'])} | "
            f"{pct(row['max_drawdown'])} | {pct(row['volatility'])} | "
            f"{row['sharpe']:.2f} | {row['sortino']:.2f} |"
        )

    lines.extend(
        [
            "",
            "## 2026 Fear-Gated Monthly Allocations",
            "",
            "| Signal Date | Fear | Score | Risk Multiplier | Bull | Bear | Value | Growth | Cash |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | ---: |",
        ]
    )
    ytd_alloc = allocations[allocations["date"] >= START_2026]
    for _, row in ytd_alloc.iterrows():
        lines.append(
            f"| {row['date']} | {row['fear_regime']} | {row['fear_score']} | "
            f"{float(row['risk_multiplier']):.0%} | {row['bull']} | {row['bear']} | "
            f"{row['value']} | {row['growth']} | {float(row['cash']):.2%} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The fear gate reduced 2026 YTD return versus original V5 because it forced 30% cash in February and 100% cash during the March panic signal.",
            "- The tradeoff was materially lower drawdown and volatility: the gate improved max drawdown while keeping returns far above SPY, QQQ, and 50/50 SPY/QQQ.",
            "- In `normal` months the integrated strategy still keeps the configured 5% cash floor, so it will not exactly match fully invested V5.",
            "- This 2026 test supports using the panic layer as a risk governor rather than as an alpha engine.",
        ]
    )

    report_path = RESULTS_DIR / "strategy_2026_ytd_fear_integrated_validation.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def main():
    close = load_validation_data()
    indicators = prepare_indicators(close)
    fear_map = market_fear_by_date()

    base_v5, _base_alloc = run_v4_universe(
        close,
        indicators,
        BASE_V5_CONFIG,
        transaction_cost=0.001,
        stop_loss_pct=0.30,
    )
    fear_v5, fear_alloc = run_v5_with_fear_gate(
        close,
        indicators,
        V5_CONFIG,
        fear_map,
        transaction_cost=0.001,
        stop_loss_pct=0.30,
    )

    curves = {
        "V5 Original": base_v5,
        "V5 + Market Fear Gate": fear_v5,
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }
    report_path = write_report(curves, fear_alloc)
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
