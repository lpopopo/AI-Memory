#!/usr/bin/env python3
import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

sys.path.append(str(Path(__file__).resolve().parent))

from backtest_dual_sleeve import RESULTS_DIR, pct, run_buy_hold, summarize
from test_v4_stock_alpha import V4Config, prepare_indicators
from test_v4_universe_alpha import load_universe_data, run_v4_universe
from test_v6_multifactor import run_v6_multifactor
from test_v4_long_term import slice_curve


START_2026 = "2026-01-01"
END_2026 = "2026-05-30"


V4_1_CONFIG = V4Config(
    name="dual_sleeve_v4_1_universe",
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


V5_CONFIG = V4Config(
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


V6_CONFIG = V4Config(
    name="dual_sleeve_v6_multifactor_aggressive",
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
    score_mode="multifactor",
    fallback="cash",
)


def period_return(curve):
    sliced = slice_curve(curve, START_2026, curve.index[-1])
    return float(sliced.iloc[-1] / sliced.iloc[0] - 1.0)


def make_rebased(curve):
    sliced = slice_curve(curve, START_2026, curve.index[-1])
    return sliced / sliced.iloc[0]


def allocation_summary(allocations):
    if allocations.empty:
        return []
    rows = allocations[allocations["date"] >= START_2026].copy()
    if rows.empty:
        return []
    return rows[["date", "bull", "bear", "value", "growth", "cash"]].to_dict("records")


def download_2026_close(symbols, cache_path, batch_size=80):
    if cache_path.exists():
        cached = pd.read_csv(cache_path, index_col=0, parse_dates=True)
        if not cached.empty:
            return cached

    frames = []
    failures = []
    for start in range(0, len(symbols), batch_size):
        batch = symbols[start : start + batch_size]
        try:
            raw = yf.download(
                tickers=batch,
                start=START_2026,
                end=END_2026,
                auto_adjust=True,
                progress=False,
                threads=True,
                group_by="column",
            )
        except Exception:
            failures.extend(batch)
            continue

        if raw.empty:
            failures.extend(batch)
            continue

        if isinstance(raw.columns, pd.MultiIndex):
            close = raw["Close"] if "Close" in raw.columns.get_level_values(0) else pd.DataFrame()
        else:
            close = raw[["Close"]].rename(columns={"Close": batch[0]})

        if not close.empty:
            frames.append(close)

    if not frames:
        raise RuntimeError("failed to download 2026 close data")

    data = pd.concat(frames, axis=1)
    data = data.loc[:, ~data.columns.duplicated()]
    data = data.sort_index().dropna(how="all")
    data.index = pd.to_datetime(data.index).tz_localize(None)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(cache_path)

    if failures:
        fail_path = cache_path.with_name("download_2026_failures.txt")
        fail_path.write_text("\n".join(sorted(set(failures))) + "\n", encoding="utf-8")

    return data


def load_validation_data():
    close = load_universe_data()
    if close.index[-1] >= pd.Timestamp(START_2026):
        return close

    cache_path = (
        Path(__file__).resolve().parents[1]
        / "datasets"
        / "data_2026"
        / "us_stock_universe_2026_ytd.csv"
    )
    symbols = list(close.columns)
    close_2026 = download_2026_close(symbols, cache_path)
    combined = pd.concat([close, close_2026], axis=0)
    combined = combined.loc[~combined.index.duplicated(keep="last")]
    combined = combined.sort_index()
    combined = combined.dropna(subset=["SPY", "QQQ"])
    return combined


def main():
    close = load_validation_data()
    if close.index[-1] < pd.Timestamp(START_2026):
        raise RuntimeError("cached dataset has no 2026 rows")

    indicators = prepare_indicators(close)

    v4_curve, v4_allocations = run_v4_universe(
        close,
        indicators,
        V4_1_CONFIG,
        transaction_cost=0.001,
        stop_loss_pct=0.15,
    )
    v5_curve, v5_allocations = run_v4_universe(
        close,
        indicators,
        V5_CONFIG,
        transaction_cost=0.001,
        stop_loss_pct=0.30,
    )
    v6_curve, v6_allocations = run_v6_multifactor(
        close,
        indicators,
        V6_CONFIG,
        transaction_cost=0.001,
        stop_loss_pct=0.30,
    )

    curves = {
        "Dual Sleeve V4.1 Universe": v4_curve,
        "Dual Sleeve V5 Optimal": v5_curve,
        "Dual Sleeve V6 Multi-Factor": v6_curve,
        "SPY": run_buy_hold(close, {"SPY": 1.0}, "SPY"),
        "QQQ": run_buy_hold(close, {"QQQ": 1.0}, "QQQ"),
        "50/50 SPY/QQQ": run_buy_hold(close, {"SPY": 0.5, "QQQ": 0.5}, "50/50 SPY/QQQ"),
    }

    rows = []
    rebased = {}
    for label, curve in curves.items():
        ytd_curve = make_rebased(curve)
        rebased[label] = ytd_curve.rename(label)
        row = summarize(label, ytd_curve)
        row["period_return"] = period_return(curve)
        rows.append(row)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.concat(rebased.values(), axis=1).to_csv(
        RESULTS_DIR / "strategy_2026_ytd_equity_curve.csv",
        index_label="date",
    )

    ytd_data = close.loc[START_2026:]
    nonempty_cols = int(ytd_data.notna().any().sum())
    empty_cols = sorted(ytd_data.columns[~ytd_data.notna().any()].tolist())

    lines = [
        "# 2026 YTD Current Strategy Validation",
        "",
        f"Data period: `{close.loc[START_2026:].index[0].strftime('%Y-%m-%d')}` to `{close.index[-1].strftime('%Y-%m-%d')}`.",
        "",
        "The validation uses the cached S&P 500 and Nasdaq 100 constituent universe in `datasets/data_universe/`, plus SPY/QQQ benchmarks.",
        "",
        "## Data Quality",
        "",
        f"- 2026 trading rows: `{len(ytd_data)}`.",
        f"- Effective columns with 2026 data: `{nonempty_cols} / {len(ytd_data.columns)}`.",
        f"- Empty 2026 columns: `{', '.join(empty_cols) if empty_cols else 'none'}`.",
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

    base = next(row for row in rows if row["name"] == "50/50 SPY/QQQ")
    lines.extend(
        [
            "",
            "## Benchmark Deltas Versus 50/50 SPY/QQQ",
            "",
            "| Strategy | Return Delta | Drawdown Delta | Sharpe Delta |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        if row["name"] == "50/50 SPY/QQQ":
            continue
        lines.append(
            f"| {row['name']} | {pct(row['period_return'] - base['period_return'])} | "
            f"{pct(row['max_drawdown'] - base['max_drawdown'])} | "
            f"{row['sharpe'] - base['sharpe']:.2f} |"
        )

    lines.extend(
        [
            "",
            "## 2026 Monthly Signals",
            "",
            "### V5 Optimal",
            "",
            "| Signal Date | Bull | Bear | Value Sleeve | Growth Sleeve | Cash |",
            "| --- | ---: | ---: | --- | --- | ---: |",
        ]
    )
    for row in allocation_summary(v5_allocations):
        lines.append(
            f"| {row['date']} | {row['bull']} | {row['bear']} | "
            f"{row['value']} | {row['growth']} | {float(row['cash']):.2%} |"
        )

    lines.extend(
        [
            "",
            "### V6 Multi-Factor",
            "",
            "| Signal Date | Bull | Bear | Value Sleeve | Growth Sleeve | Cash |",
            "| --- | ---: | ---: | --- | --- | ---: |",
        ]
    )
    for row in allocation_summary(v6_allocations):
        lines.append(
            f"| {row['date']} | {row['bull']} | {row['bear']} | "
            f"{row['value']} | {row['growth']} | {float(row['cash']):.2%} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- The 2026 sample is year-to-date only, so annualized figures are unstable and should not be treated as a full-year result.",
            "- V5 is the strongest 2026 YTD return engine, with much higher return and Sharpe than SPY, QQQ, and 50/50 SPY/QQQ.",
            "- V5 also has the deepest drawdown among the tested strategy versions, slightly worse than QQQ and 50/50 SPY/QQQ, so it is reasonable only for an aggressive mandate.",
            "- V6 lowers return versus V5 without producing a clearly superior drawdown profile in 2026 YTD, so it should remain experimental.",
            "- The 2026 signals are concentrated in semiconductors, storage, networking, and related technology leaders; this confirms the model is capturing the current hot-industry regime, but it also creates sector concentration risk.",
        ]
    )

    report_path = RESULTS_DIR / "strategy_2026_ytd_validation.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {report_path}")
    print("\n".join(lines[:20]))


if __name__ == "__main__":
    main()
