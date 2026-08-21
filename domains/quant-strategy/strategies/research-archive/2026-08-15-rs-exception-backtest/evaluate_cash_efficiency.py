#!/usr/bin/env python3
"""Audit zero-yield cash, an SGOV total-return proxy, and passive benchmarks."""
from __future__ import annotations

import json
import math
import runpy
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE_MODULE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
PROTECTION_MODULE = runpy.run_path(str(HERE / "evaluate_profit_protection.py"))
RESULTS = HERE / "results"
CASH_PROXY = RESULTS / "sgov_total_return_proxy.csv"


def load_sgov(start: pd.Timestamp, end: pd.Timestamp) -> tuple[pd.Series, dict]:
    error = None
    for _ in range(3):
        try:
            data = yf.download(
                "SGOV",
                start=str((start - pd.Timedelta(days=10)).date()),
                end=str((end + pd.Timedelta(days=3)).date()),
                auto_adjust=True,
                progress=False,
                threads=False,
            )
            if data.empty:
                raise RuntimeError("empty SGOV download")
            close = data["Close"]
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
            close.index = pd.to_datetime(close.index).tz_localize(None)
            close = pd.to_numeric(close, errors="coerce").dropna().sort_index()
            pd.DataFrame({"date": close.index, "adjusted_close": close.values}).to_csv(
                CASH_PROXY, index=False
            )
            return close, {
                "source": "Yahoo Finance via yfinance",
                "auto_adjust": True,
                "fetched_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
                "fallback": False,
            }
        except Exception as exc:  # public endpoint, retry then use traceable cache
            error = str(exc)
    if not CASH_PROXY.exists():
        raise RuntimeError(f"SGOV download failed and no cache exists: {error}")
    cached = pd.read_csv(CASH_PROXY, parse_dates=["date"]).set_index("date")["adjusted_close"]
    return cached.sort_index(), {
        "source": "cached Yahoo Finance via yfinance",
        "auto_adjust": True,
        "fetched_at_utc": None,
        "fallback": True,
        "refresh_error": error,
    }


def buy_hold_metrics(series: pd.Series, start: str, end: str) -> dict:
    prices = series.loc[start:end].dropna()
    if len(prices) < 2:
        raise RuntimeError(f"insufficient benchmark data for {start}..{end}")
    initial_nav = MODULE["INITIAL_NAV"]
    slippage = 0.001
    commission = MODULE["COMMISSION"]
    raw_entry = float(prices.iloc[0])
    entry_fill = raw_entry * (1.0 + slippage)
    shares = math.floor((initial_nav - commission) / entry_fill)
    cash = initial_nav - shares * entry_fill - commission
    equity = cash + shares * prices
    raw_exit = float(prices.iloc[-1])
    exit_fill = raw_exit * (1.0 - slippage)
    proceeds = shares * exit_fill - commission
    final_value = cash + proceeds
    equity.iloc[-1] = final_value
    trade = {
        "pnl": proceeds - (shares * entry_fill + commission),
        "return": (proceeds - (shares * entry_fill + commission)) / (shares * entry_fill + commission),
        "entry_type": "normal",
    }
    exposure = shares * prices / equity
    turnover = shares * entry_fill + shares * exit_fill
    costs = 2 * commission + shares * raw_entry * slippage + shares * raw_exit * slippage
    metrics = MODULE["_metrics"](equity, [trade], exposure, turnover, costs)
    metrics.update(
        {
            "shares": shares,
            "cash_yield_earned": 0.0,
            "max_exposure": float(exposure.max()),
        }
    )
    return metrics


def fixed_path_cash_overlay(result: dict, panels: dict[str, pd.DataFrame], cash_returns: pd.Series | None) -> dict:
    dates = pd.to_datetime(list(result["equity"]))
    entries: dict[pd.Timestamp, list[dict]] = {}
    exits_before_entry: dict[pd.Timestamp, list[dict]] = {}
    same_day_exits: dict[pd.Timestamp, list[dict]] = {}
    for trade in result["trades"]:
        entry_date = pd.Timestamp(trade["entry_date"])
        exit_date = pd.Timestamp(trade["exit_date"])
        entries.setdefault(entry_date, []).append(trade)
        target = same_day_exits if exit_date == entry_date else exits_before_entry
        target.setdefault(exit_date, []).append(trade)
    cash = MODULE["INITIAL_NAV"]
    positions: dict[str, dict] = {}
    cash_yield_earned = 0.0
    equity_rows = []
    exposure_rows = []
    for index, date in enumerate(dates):
        for trade in exits_before_entry.get(date, []):
            cash += trade["shares"] * trade["exit_price"] - MODULE["COMMISSION"]
            positions.pop(trade["symbol"], None)
        for trade in entries.get(date, []):
            cash -= trade["shares"] * trade["entry_price"] + MODULE["COMMISSION"]
            positions[trade["symbol"]] = trade
        for trade in same_day_exits.get(date, []):
            cash += trade["shares"] * trade["exit_price"] - MODULE["COMMISSION"]
            positions.pop(trade["symbol"], None)
        if cash_returns is not None and index > 0:
            cash_return = cash_returns.get(date, np.nan)
            if not np.isfinite(cash_return):
                raise RuntimeError(f"missing fixed-path cash return for {date.date()}")
            earned = cash * float(cash_return)
            cash += earned
            cash_yield_earned += earned
        if cash < -1e-8:
            raise RuntimeError(f"fixed path requires negative cash on {date.date()}")
        stock_value = sum(
            trade["shares"] * float(panels["close"].at[date, symbol])
            for symbol, trade in positions.items()
        )
        equity = cash + stock_value
        equity_rows.append((date, equity))
        exposure_rows.append((date, stock_value / equity if equity else 0.0))
    equity = pd.Series(dict(equity_rows), dtype=float)
    exposure = pd.Series(dict(exposure_rows), dtype=float)
    metrics = MODULE["_metrics"](
        equity,
        result["trades"],
        exposure,
        result["metrics"]["turnover"] * MODULE["INITIAL_NAV"],
        result["metrics"]["costs"],
    )
    metrics["cash_yield_earned"] = float(cash_yield_earned)
    return {"metrics": metrics, "equity": equity}


def pct(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2%}"


def num(value) -> str:
    return "n/a" if value is None or pd.isna(value) else f"{value:.2f}"


def evaluate(panels, symbols, cash_returns, end: str):
    periods = {
        "train_2024_2025": ("2024-01-02", "2025-12-31"),
        "2026": ("2026-01-01", end),
        "full": ("2024-01-02", end),
    }
    variants = {
        "matched_baseline": (UNIVERSE_MODULE["make_config"](False), None, 0.0),
        "rsr1": (UNIVERSE_MODULE["make_config"](True), None, 0.0),
        "rsr2": (UNIVERSE_MODULE["make_config"](True), 0.15, 0.05),
    }
    rows = []
    runs = {}
    for variant, (config, trigger, floor) in variants.items():
        for period, interval in periods.items():
            for cash_mode, returns in (("zero_yield", None), ("sgov_proxy", cash_returns)):
                result = MODULE["simulate"](
                    panels,
                    symbols,
                    config,
                    "strict_veto",
                    *interval,
                    slippage=0.001,
                    profit_lock_trigger=trigger,
                    profit_lock_floor=floor,
                    cash_returns=returns,
                )
                runs[(variant, period, cash_mode)] = result
                rows.append(
                    {
                        "variant": variant,
                        "period": period,
                        "cash_mode": cash_mode,
                        **result["metrics"],
                    }
                )
    return pd.DataFrame(rows), runs


def write_report(metrics, benchmarks, summary) -> None:
    focus = metrics.loc[metrics["variant"].isin(["rsr1", "rsr2"])]
    lines = [
        "# Cash efficiency and passive opportunity-cost audit",
        "",
        "## Assumptions",
        "",
        "The original simulator pays 0% on uninvested cash. This audit adds an optional SGOV adjusted-close total-return series to post-execution cash at each session close. It is an optimistic cash-sweep proxy, not an executable assumption: taxes, spreads, settlement, broker eligibility and the need to liquidate an ETF before next-open stock entries are not modeled.",
        "",
        f"SGOV source: `{summary['sgov_source']['source']}`; coverage `{summary['sgov_start']}` through `{summary['sgov_end']}`; full-period proxy return `{pct(summary['sgov_proxy_price_return_full'])}`.",
        "",
        "## Active strategies: zero-yield cash versus SGOV proxy",
        "",
        "| Period | Variant | Cash mode | Return | Max DD | Sharpe | Average stock exposure | Cash yield earned | Trades |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for period in ("train_2024_2025", "2026", "full"):
        for variant in ("rsr1", "rsr2"):
            for cash_mode in ("zero_yield", "sgov_proxy"):
                row = focus.loc[
                    focus["period"].eq(period)
                    & focus["variant"].eq(variant)
                    & focus["cash_mode"].eq(cash_mode)
                ].iloc[0]
                lines.append(
                    f"| {period} | {variant} | {cash_mode} | {pct(row.total_return)} | "
                    f"{pct(row.max_drawdown)} | {num(row.sharpe)} | {pct(row.exposure)} | "
                    f"${row.cash_yield_earned:,.2f} | {row.trade_count} |"
                )
    lines.extend(
        [
            "",
            "## Full-period passive benchmarks at 10 bps per side",
            "",
            "| Benchmark | Return | Max DD | Sharpe | Exposure |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in benchmarks.itertuples(index=False):
        lines.append(
            f"| {row.benchmark} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
            f"{num(row.sharpe)} | {pct(row.exposure)} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            f"- RSR1's full return rises from `{pct(summary['rsr1_zero_return'])}` to `{pct(summary['rsr1_sgov_return'])}` under the SGOV proxy; RSR2 rises from `{pct(summary['rsr2_zero_return'])}` to `{pct(summary['rsr2_sgov_return'])}`.",
            f"- Holding the original RSR1 shares and trade dates fixed, the SGOV proxy raises return to `{pct(summary['rsr1_fixed_path_sgov_return'])}`. The dynamic full rerun reaches `{pct(summary['rsr1_sgov_return'])}`; the extra `{pct(summary['rsr1_dynamic_minus_fixed_return'])}` comes from changed whole-share sizing and capacity.",
            f"- The dynamic cash overlay changes RSR1 from `{summary['rsr1_zero_trades']}` to `{summary['rsr1_sgov_trades']}` trades and adds a losing ASML trade. Larger share counts elsewhere more than offset it, so the full-rerun gain must not be labeled pure interest.",
            f"- Exact fixed-path cash yield is `${summary['rsr1_fixed_path_cash_yield_earned']:,.2f}`. The zero-yield reconstruction matches the original equity path to within `${summary['rsr1_zero_reconstruction_max_error']:.8f}`.",
            "- Passive indices provide the relevant wealth opportunity cost but carry much larger continuous market exposure and drawdown. The active strategy is a low-exposure timing sleeve, not a substitute for a fully invested core benchmark.",
            "- Do not add an SGOV trade or assume broker interest without verifying the user's broker sweep mechanics, settlement availability, tax treatment and next-open buying power. No RSR3 version is created from this optimistic proxy.",
            "",
            "Research-only. No live order or formal V9 change is authorized.",
        ]
    )
    (RESULTS / "cash_efficiency_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, all_symbols = MODULE["load_panels"]()
    universes, _ = UNIVERSE_MODULE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    data_start = panels["close"].index.min()
    data_end = panels["close"][["SPY", "QQQ", "SMH"]].dropna().index[-1]
    sgov, source = load_sgov(data_start, data_end)
    sgov_returns = sgov.pct_change(fill_method=None).reindex(panels["close"].index)
    missing = sgov_returns.loc[data_start:data_end].iloc[1:].isna()
    if missing.any():
        raise RuntimeError(f"SGOV cash proxy missing {int(missing.sum())} required session returns")
    metrics, runs = evaluate(panels, symbols, sgov_returns, str(data_end.date()))
    benchmark_rows = []
    for name, prices in {
        "SPY": panels["close"]["SPY"],
        "QQQ": panels["close"]["QQQ"],
        "SMH": panels["close"]["SMH"],
        "SGOV": sgov,
    }.items():
        benchmark_rows.append(
            {
                "benchmark": name,
                **buy_hold_metrics(prices, str(data_start.date()), str(data_end.date())),
            }
        )
    benchmarks = pd.DataFrame(benchmark_rows)
    rsr1_zero = runs[("rsr1", "full", "zero_yield")]
    rsr1_sgov = runs[("rsr1", "full", "sgov_proxy")]
    rsr2_zero = runs[("rsr2", "full", "zero_yield")]
    rsr2_sgov = runs[("rsr2", "full", "sgov_proxy")]
    rsr1_fixed_zero = fixed_path_cash_overlay(rsr1_zero, panels, None)
    rsr1_fixed_sgov = fixed_path_cash_overlay(rsr1_zero, panels, sgov_returns)
    rsr2_fixed_zero = fixed_path_cash_overlay(rsr2_zero, panels, None)
    rsr2_fixed_sgov = fixed_path_cash_overlay(rsr2_zero, panels, sgov_returns)
    rsr1_original_equity = pd.Series(rsr1_zero["equity"], dtype=float)
    rsr1_original_equity.index = pd.to_datetime(rsr1_original_equity.index)
    rsr1_reconstruction_error = float(
        (rsr1_fixed_zero["equity"] - rsr1_original_equity).abs().max()
    )
    if rsr1_reconstruction_error > 1e-8:
        raise RuntimeError(f"fixed-path reconstruction mismatch: {rsr1_reconstruction_error}")
    zero_keys = {(trade["signal_date"], trade["symbol"]) for trade in rsr1_zero["trades"]}
    sweep_keys = {(trade["signal_date"], trade["symbol"]) for trade in rsr1_sgov["trades"]}
    added_trades = [
        trade for trade in rsr1_sgov["trades"]
        if (trade["signal_date"], trade["symbol"]) in sweep_keys - zero_keys
    ]
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_end": str(data_end.date()),
        "research_only": True,
        "authorizes_trade": False,
        "sgov_source": source,
        "sgov_start": str(sgov.index.min().date()),
        "sgov_end": str(sgov.index.max().date()),
        "sgov_proxy_price_return_full": float(
            sgov.loc[data_start:data_end].iloc[-1] / sgov.loc[data_start:data_end].iloc[0] - 1.0
        ),
        "rsr1_zero_return": rsr1_zero["metrics"]["total_return"],
        "rsr1_sgov_return": rsr1_sgov["metrics"]["total_return"],
        "rsr2_zero_return": rsr2_zero["metrics"]["total_return"],
        "rsr2_sgov_return": rsr2_sgov["metrics"]["total_return"],
        "rsr1_zero_trades": rsr1_zero["metrics"]["trade_count"],
        "rsr1_sgov_trades": rsr1_sgov["metrics"]["trade_count"],
        "rsr1_cash_yield_earned": rsr1_sgov["metrics"]["cash_yield_earned"],
        "rsr1_final_value_improvement": rsr1_sgov["metrics"]["final_value"]
        - rsr1_zero["metrics"]["final_value"],
        "rsr1_fixed_path_sgov_return": rsr1_fixed_sgov["metrics"]["total_return"],
        "rsr2_fixed_path_sgov_return": rsr2_fixed_sgov["metrics"]["total_return"],
        "rsr1_fixed_path_cash_yield_earned": rsr1_fixed_sgov["metrics"]["cash_yield_earned"],
        "rsr2_fixed_path_cash_yield_earned": rsr2_fixed_sgov["metrics"]["cash_yield_earned"],
        "rsr1_dynamic_minus_fixed_return": rsr1_sgov["metrics"]["total_return"]
        - rsr1_fixed_sgov["metrics"]["total_return"],
        "rsr2_dynamic_minus_fixed_return": rsr2_sgov["metrics"]["total_return"]
        - rsr2_fixed_sgov["metrics"]["total_return"],
        "rsr1_zero_reconstruction_max_error": rsr1_reconstruction_error,
        "rsr1_dynamic_added_trades": [
            {
                "symbol": trade["symbol"],
                "signal_date": trade["signal_date"],
                "pnl": trade["pnl"],
                "return": trade["return"],
            }
            for trade in added_trades
        ],
        "rsr1_path_identical": PROTECTION_MODULE["path_signature"](rsr1_zero)
        == PROTECTION_MODULE["path_signature"](rsr1_sgov),
        "rsr2_path_identical": PROTECTION_MODULE["path_signature"](rsr2_zero)
        == PROTECTION_MODULE["path_signature"](rsr2_sgov),
        "decision": "cash_sweep_is_operational_research_only_no_rsr3",
    }
    metrics.to_csv(RESULTS / "cash_efficiency_metrics.csv", index=False)
    benchmarks.to_csv(RESULTS / "cash_efficiency_benchmarks.csv", index=False)
    pd.DataFrame(
        [
            {"variant": "rsr1", "cash_mode": "zero_yield", **rsr1_fixed_zero["metrics"]},
            {"variant": "rsr1", "cash_mode": "sgov_proxy", **rsr1_fixed_sgov["metrics"]},
            {"variant": "rsr2", "cash_mode": "zero_yield", **rsr2_fixed_zero["metrics"]},
            {"variant": "rsr2", "cash_mode": "sgov_proxy", **rsr2_fixed_sgov["metrics"]},
        ]
    ).to_csv(RESULTS / "cash_efficiency_fixed_path.csv", index=False)
    (RESULTS / "cash_efficiency_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(metrics, benchmarks, summary)
    print(RESULTS / "cash_efficiency_report.md")


if __name__ == "__main__":
    main()
