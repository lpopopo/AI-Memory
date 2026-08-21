#!/usr/bin/env python3
"""Combine the formal V9 index-core path with research-only RSR sleeves."""
from __future__ import annotations

import json
import math
import runpy
import sys
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
QUANT_ROOT = HERE.parents[2]
V9 = QUANT_ROOT / "strategies" / "v9-execution"
sys.path.insert(0, str(V9 / "scripts"))

from v9_data import load_data  # noqa: E402
from v9_information_strategy import V9Backtester, V9Config  # noqa: E402


MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE_MODULE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
CASH_MODULE = runpy.run_path(str(HERE / "evaluate_cash_efficiency.py"))
RESULTS = HERE / "results"
START = "2026-01-02"
WARMUP = "2024-01-02"


def curve_metrics(curve: pd.Series) -> dict:
    returns = curve.pct_change().fillna(0.0)
    drawdown = curve / curve.cummax() - 1.0
    years = max((curve.index[-1] - curve.index[0]).days / 365.25, 1 / 252)
    total_return = float(curve.iloc[-1] / curve.iloc[0] - 1.0)
    volatility = float(returns.std(ddof=0) * math.sqrt(252))
    sharpe = float(returns.mean() / returns.std(ddof=0) * math.sqrt(252)) if returns.std(ddof=0) else 0.0
    return {
        "final_value": float(curve.iloc[-1]),
        "total_return": total_return,
        "cagr": float((curve.iloc[-1] / curve.iloc[0]) ** (1.0 / years) - 1.0),
        "max_drawdown": float(drawdown.min()),
        "volatility": volatility,
        "sharpe": sharpe,
        "sessions": len(curve),
    }


def combine_curves(core_curve: pd.Series, stock_curve: pd.Series, initial_nav: float = 6_000.0) -> pd.Series:
    index = core_curve.index.intersection(stock_curve.index)
    core = core_curve.loc[index] / core_curve.loc[index].iloc[0]
    stock = stock_curve.loc[index]
    return initial_nav + initial_nav * (core - 1.0) + (stock - stock.iloc[0])


def add_fixed_cash_sweep(
    combined_zero: pd.Series,
    core_curve: pd.Series,
    core_weights: pd.DataFrame,
    stock_curve: pd.Series,
    stock_exposure: pd.Series,
    cash_returns: pd.Series,
    initial_nav: float = 6_000.0,
) -> tuple[pd.Series, pd.Series]:
    index = combined_zero.index
    core = core_curve.reindex(index) / core_curve.reindex(index).iloc[0]
    weights = core_weights.reindex(index).ffill().fillna(0.0)
    stock = stock_curve.reindex(index)
    stock_weight = stock_exposure.reindex(index).fillna(0.0)
    values = [float(combined_zero.iloc[0])]
    gross = []
    first_core_risky = initial_nav * core.iloc[0] * float(weights.iloc[0].get("SPY", 0.0) + weights.iloc[0].get("QQQ", 0.0))
    first_stock_risky = float(stock.iloc[0] * stock_weight.iloc[0])
    gross.append((first_core_risky + first_stock_risky) / values[0])
    for position in range(1, len(index)):
        date = index[position]
        value = values[-1] + float(combined_zero.iloc[position] - combined_zero.iloc[position - 1])
        core_risky = initial_nav * float(core.iloc[position]) * float(
            weights.iloc[position].get("SPY", 0.0) + weights.iloc[position].get("QQQ", 0.0)
        )
        stock_risky = float(stock.iloc[position] * stock_weight.iloc[position])
        residual_cash = value - core_risky - stock_risky
        if residual_cash < -1e-8:
            raise RuntimeError(f"combined modules exceed portfolio value on {date.date()}")
        cash_return = cash_returns.get(date, np.nan)
        if not np.isfinite(cash_return):
            raise RuntimeError(f"missing cash return for {date.date()}")
        value += max(residual_cash, 0.0) * float(cash_return)
        values.append(value)
        gross.append((core_risky + stock_risky) / value)
    return pd.Series(values, index=index), pd.Series(gross, index=index)


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2%}"


def num(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2f}"


def write_report(metrics: pd.DataFrame, summary: dict) -> None:
    lines = [
        "# V9 index core plus RSR sleeve audit",
        "",
        "## Scope",
        "",
        "This 2026 held-out-period audit adds the research-only RSR stock PnL to the formal V9 70% SPY/QQQ core-only path. Dollar PnL is combined rather than averaging two standalone returns: both modules size risk as a fraction of the same initial portfolio, and their unused zero-yield cash is counted only once.",
        "",
        "The result is hypothetical. RSR1/RSR2 are not promoted Rule E signals, and the combination cannot authorize an order or modify formal V9.",
        "",
        "## Results",
        "",
        "| Portfolio | Return | Max DD | Sharpe | Final value | Max combined gross |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in metrics.itertuples(index=False):
        lines.append(
            f"| {row.portfolio} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
            f"{num(row.sharpe)} | ${row.final_value:,.2f} | {pct(row.max_combined_gross)} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- The isolated V9 core returns `{pct(summary['core_return'])}`. Adding RSR1 raises it to `{pct(summary['combined_rsr1_return'])}`; RSR2 raises it to `{pct(summary['combined_rsr2_return'])}`.",
            f"- RSR2 adds `{pct(summary['rsr2_incremental_return'])}` to the core but worsens maximum drawdown by `{abs(summary['rsr2_drawdown_change']) * 100:.2f}` percentage points. The marginal result rests on only `{summary['rsr2_closed_trades']}` closed stock trades.",
            f"- With the optimistic fixed-path SGOV residual-cash proxy, core+RSR2 reaches `{pct(summary['combined_rsr2_sgov_return'])}`. This is cash-management research, not a tradable assumption.",
            f"- Maximum combined risky exposure is `{pct(summary['combined_rsr2_max_gross'])}`; no leverage is introduced. The index core, not the low-frequency stock sleeve, remains the dominant return and drawdown driver.",
            "- The correct profit-maximization question is therefore portfolio allocation between the validated index core, unproven stock sleeve and cash, not simply increasing RSR stock size. Continue separate forward evidence before changing the 70/30 governance.",
            "",
            "Research-only. Formal V9, RSR1 and RSR2 remain unchanged.",
        ]
    )
    (RESULTS / "combined_v9_portfolio_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    v9_panels, vix, meta = load_data()
    end = str(pd.Timestamp(meta["last_date"]).date())
    core_result = V9Backtester(
        v9_panels,
        vix,
        [],
        V9Config(v8_core_weight=0.70, info_sleeve_weight=0.0),
        [],
    ).run(warmup_start=WARMUP, trading_start=START, trading_end=end)
    core_curve = core_result.equity.astype(float)
    core_curve = core_curve / core_curve.iloc[0] * MODULE["INITIAL_NAV"]

    panels, all_symbols = MODULE["load_panels"]()
    universes, _ = UNIVERSE_MODULE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    stock_runs = {}
    for name, trigger, floor in (("rsr1", None, 0.0), ("rsr2", 0.15, 0.05)):
        stock_runs[name] = MODULE["simulate"](
            panels,
            symbols,
            UNIVERSE_MODULE["make_config"](True),
            "strict_veto",
            START,
            end,
            slippage=0.001,
            profit_lock_trigger=trigger,
            profit_lock_floor=floor,
        )
    stock_curves = {}
    stock_exposures = {}
    combined = {}
    for name, result in stock_runs.items():
        curve = pd.Series(result["equity"], dtype=float)
        curve.index = pd.to_datetime(curve.index)
        exposure = pd.Series(result["exposure"], dtype=float)
        exposure.index = pd.to_datetime(exposure.index)
        stock_curves[name] = curve
        stock_exposures[name] = exposure
        combined[name] = combine_curves(core_curve, curve)

    sgov = pd.read_csv(CASH_MODULE["CASH_PROXY"], parse_dates=["date"]).set_index("date")["adjusted_close"]
    cash_returns = sgov.pct_change(fill_method=None)
    combined_sgov = {}
    combined_zero_gross = {}
    combined_sgov_gross = {}
    for name in ("rsr1", "rsr2"):
        _, combined_zero_gross[name] = add_fixed_cash_sweep(
            combined[name],
            core_curve,
            core_result.weights,
            stock_curves[name],
            stock_exposures[name],
            cash_returns * 0.0,
        )
        combined_sgov[name], combined_sgov_gross[name] = add_fixed_cash_sweep(
            combined[name],
            core_curve,
            core_result.weights,
            stock_curves[name],
            stock_exposures[name],
            cash_returns,
        )

    rows = []
    core_weights = core_result.weights.reindex(core_curve.index).ffill().fillna(0.0)
    core_gross = core_weights.get("SPY", 0.0) + core_weights.get("QQQ", 0.0)
    for portfolio, curve, max_gross in [
        ("v9_core_70", core_curve, float(core_gross.max())),
        ("v9_core_plus_rsr1", combined["rsr1"], float(combined_zero_gross["rsr1"].max())),
        ("v9_core_plus_rsr2", combined["rsr2"], float(combined_zero_gross["rsr2"].max())),
        ("v9_core_plus_rsr1_sgov_proxy", combined_sgov["rsr1"], float(combined_sgov_gross["rsr1"].max())),
        ("v9_core_plus_rsr2_sgov_proxy", combined_sgov["rsr2"], float(combined_sgov_gross["rsr2"].max())),
    ]:
        rows.append({"portfolio": portfolio, **curve_metrics(curve), "max_combined_gross": max_gross})
    for benchmark in ("SPY", "QQQ"):
        benchmark_metrics = CASH_MODULE["buy_hold_metrics"](
            v9_panels["close"][benchmark], START, end
        )
        rows.append(
            {
                "portfolio": f"buy_hold_{benchmark}",
                **{key: benchmark_metrics[key] for key in ("final_value", "total_return", "cagr", "max_drawdown", "volatility", "sharpe")},
                "sessions": len(v9_panels["close"].loc[START:end]),
                "max_combined_gross": benchmark_metrics["max_exposure"],
            }
        )
    metrics = pd.DataFrame(rows)
    by_name = metrics.set_index("portfolio")
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "period": [START, end],
        "warmup_start": WARMUP,
        "research_only": True,
        "authorizes_trade": False,
        "v9_data_source": meta.get("source"),
        "core_return": by_name.at["v9_core_70", "total_return"],
        "combined_rsr1_return": by_name.at["v9_core_plus_rsr1", "total_return"],
        "combined_rsr2_return": by_name.at["v9_core_plus_rsr2", "total_return"],
        "combined_rsr2_sgov_return": by_name.at["v9_core_plus_rsr2_sgov_proxy", "total_return"],
        "rsr2_incremental_return": by_name.at["v9_core_plus_rsr2", "total_return"]
        - by_name.at["v9_core_70", "total_return"],
        "rsr2_drawdown_change": by_name.at["v9_core_plus_rsr2", "max_drawdown"]
        - by_name.at["v9_core_70", "max_drawdown"],
        "rsr2_closed_trades": stock_runs["rsr2"]["metrics"]["trade_count"],
        "combined_rsr2_max_gross": by_name.at["v9_core_plus_rsr2", "max_combined_gross"],
        "decision": "portfolio_context_only_keep_v9_rsr1_rsr2_unchanged",
    }
    metrics.to_csv(RESULTS / "combined_v9_portfolio_metrics.csv", index=False)
    pd.DataFrame(
        {
            "v9_core_70": core_curve,
            "v9_core_plus_rsr1": combined["rsr1"],
            "v9_core_plus_rsr2": combined["rsr2"],
            "v9_core_plus_rsr1_sgov_proxy": combined_sgov["rsr1"],
            "v9_core_plus_rsr2_sgov_proxy": combined_sgov["rsr2"],
        }
    ).to_csv(RESULTS / "combined_v9_portfolio_equity.csv")
    (RESULTS / "combined_v9_portfolio_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(metrics, summary)
    print(RESULTS / "combined_v9_portfolio_report.md")


if __name__ == "__main__":
    main()
