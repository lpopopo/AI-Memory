#!/usr/bin/env python3
"""Research-only V9 index-core allocation frontier audit."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


HERE = Path(__file__).resolve().parent
QUANT_ROOT = HERE.parents[2]
V9 = QUANT_ROOT / "strategies" / "v9-execution"
sys.path.insert(0, str(V9 / "scripts"))

from v9_data import load_data  # noqa: E402
from v9_information_strategy import V9Backtester, V9Config  # noqa: E402


RESULTS = HERE / "results"
CAPS = (0.50, 0.60, 0.70, 0.80, 0.90, 1.00)
REFERENCE_CAP = 0.70
PERIODS = {
    "development_2006_2014": ("2006-01-03", "2014-12-31", "2005-01-03"),
    "validation_2015_2019": ("2015-01-02", "2019-12-31", "2014-01-02"),
    "final_2020_2025": ("2020-01-02", "2025-12-31", "2019-01-02"),
    "heldout_2026": ("2026-01-02", None, "2024-01-02"),
    "full_2006_2025": ("2006-01-03", "2025-12-31", "2005-01-03"),
}
SCREEN_PERIODS = ("validation_2015_2019", "final_2020_2025", "heldout_2026")
INITIAL_NAV = 6_000.0
ROLLING_SESSIONS = 756
ROLLING_STEP = 21
LONG_CACHE = RESULTS / "core_allocation_frontier_long_history.csv"
LONG_START = "2005-01-01"
LONG_END_EXCLUSIVE = "2026-01-02"


def _download_series(symbol: str, field: str) -> pd.Series:
    last_error = None
    for _ in range(3):
        try:
            data = yf.download(
                symbol,
                start=LONG_START,
                end=LONG_END_EXCLUSIVE,
                auto_adjust=True,
                progress=False,
                threads=False,
            )
            if data.empty:
                raise RuntimeError(f"empty download for {symbol}")
            values = data[field]
            if isinstance(values, pd.DataFrame):
                values = values.iloc[:, 0]
            values.index = pd.to_datetime(values.index).tz_localize(None)
            return pd.to_numeric(values, errors="coerce").dropna().sort_index()
        except Exception as exc:  # public endpoint: retry, then traceable cache
            last_error = exc
    raise RuntimeError(f"download failed for {symbol}/{field}: {last_error}")


def _read_long_cache() -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    cached = pd.read_csv(LONG_CACHE, parse_dates=["date"]).set_index("date").sort_index()
    panels = {}
    for field in ("open", "high", "low", "close", "volume"):
        panels[field] = pd.DataFrame(
            {
                "SPY": cached[f"SPY_{field}"],
                "QQQ": cached[f"QQQ_{field}"],
            },
            index=cached.index,
        )
    vix = cached[["VIX_close", "VIX3M_close"]].rename(
        columns={"VIX_close": "^VIX", "VIX3M_close": "^VIX3M"}
    ).ffill()
    return panels, vix


def load_long_history() -> tuple[dict[str, pd.DataFrame], pd.DataFrame, dict]:
    if LONG_CACHE.exists():
        panels, vix = _read_long_cache()
        return panels, vix, {
            "source": "cached Yahoo Finance via yfinance auto_adjust=True",
            "cache": str(LONG_CACHE),
            "fallback": True,
        }
    series = {}
    for symbol in ("SPY", "QQQ"):
        for api_field, field in (
            ("Open", "open"),
            ("High", "high"),
            ("Low", "low"),
            ("Close", "close"),
            ("Volume", "volume"),
        ):
            series[f"{symbol}_{field}"] = _download_series(symbol, api_field)
    series["VIX_close"] = _download_series("^VIX", "Close")
    try:
        series["VIX3M_close"] = _download_series("^VIX3M", "Close")
        vix3m_fallback = False
    except RuntimeError:
        series["VIX3M_close"] = series["VIX_close"].copy()
        vix3m_fallback = True
    index = series["SPY_close"].index.intersection(series["QQQ_close"].index)
    flat = pd.DataFrame(index=index)
    for name, values in series.items():
        flat[name] = values.reindex(index)
    flat.index.name = "date"
    flat.to_csv(LONG_CACHE)
    panels, vix = _read_long_cache()
    return panels, vix, {
        "source": "Yahoo Finance via yfinance auto_adjust=True",
        "cache": str(LONG_CACHE),
        "fallback": False,
        "vix3m_fallback_to_vix": vix3m_fallback,
    }


def _period_returns(curve: pd.Series, frequency: str) -> pd.Series:
    labels = curve.index.to_period(frequency)
    end_values = curve.groupby(labels).last()
    returns = end_values.pct_change()
    if len(returns):
        returns.iloc[0] = end_values.iloc[0] / curve.iloc[0] - 1.0
    return returns.replace([np.inf, -np.inf], np.nan).dropna()


def curve_metrics(curve: pd.Series) -> dict[str, float]:
    curve = pd.to_numeric(curve, errors="coerce").dropna().astype(float)
    if len(curve) < 2 or (curve <= 0).any():
        raise ValueError("equity curve must contain at least two positive values")
    daily = curve.pct_change(fill_method=None).dropna()
    drawdown = curve / curve.cummax() - 1.0
    years = max((curve.index[-1] - curve.index[0]).days / 365.25, 1 / 252)
    total_return = float(curve.iloc[-1] / curve.iloc[0] - 1.0)
    cagr = float((curve.iloc[-1] / curve.iloc[0]) ** (1.0 / years) - 1.0)
    std = float(daily.std(ddof=0))
    downside = daily[daily < 0]
    downside_std = float(downside.std(ddof=0)) if len(downside) else 0.0
    monthly = _period_returns(curve, "M")
    annual = _period_returns(curve, "Y")
    q05 = float(daily.quantile(0.05)) if len(daily) else 0.0
    tail = daily[daily <= q05]
    max_dd = float(drawdown.min())
    return {
        "final_value": float(INITIAL_NAV * curve.iloc[-1] / curve.iloc[0]),
        "total_return": total_return,
        "cagr": cagr,
        "max_drawdown": max_dd,
        "volatility": std * math.sqrt(252),
        "sharpe": float(daily.mean() / std * math.sqrt(252)) if std else 0.0,
        "sortino": (
            float(daily.mean() / downside_std * math.sqrt(252)) if downside_std else 0.0
        ),
        "calmar": float(cagr / abs(max_dd)) if max_dd else 0.0,
        "monthly_win_rate": float((monthly > 0).mean()) if len(monthly) else 0.0,
        "positive_year_rate": float((annual > 0).mean()) if len(annual) else 0.0,
        "expected_shortfall_95": float(tail.mean()) if len(tail) else 0.0,
        "sessions": int(len(curve)),
    }


def run_core(
    panels: dict[str, pd.DataFrame],
    vix: pd.DataFrame,
    cap: float,
    start: str,
    end: str,
    warmup: str,
):
    engine = V9Backtester(
        panels,
        vix,
        [],
        V9Config(v8_core_weight=cap, info_sleeve_weight=0.0),
        [],
    )
    result = engine.run(warmup_start=warmup, trading_start=start, trading_end=end)
    curve = result.equity.astype(float)
    weights = result.weights.reindex(curve.index).ffill().fillna(0.0)
    gross = weights.get("SPY", 0.0) + weights.get("QQQ", 0.0)
    metrics = curve_metrics(curve)
    metrics.update(
        {
            "average_gross": float(gross.mean()),
            "max_gross": float(gross.max()),
            "turnover": float(result.diagnostics["turnover"]),
            "transactions": int(len(result.ledger)),
        }
    )
    return metrics, curve


def rolling_metrics(curve: pd.Series) -> pd.DataFrame:
    rows = []
    if len(curve) < ROLLING_SESSIONS:
        return pd.DataFrame()
    for end_pos in range(ROLLING_SESSIONS - 1, len(curve), ROLLING_STEP):
        window = curve.iloc[end_pos - ROLLING_SESSIONS + 1 : end_pos + 1]
        metrics = curve_metrics(window)
        rows.append(
            {
                "start": window.index[0],
                "end": window.index[-1],
                "total_return": metrics["total_return"],
                "cagr": metrics["cagr"],
                "max_drawdown": metrics["max_drawdown"],
                "sharpe": metrics["sharpe"],
            }
        )
    return pd.DataFrame(rows)


def summarize_rolling(rows: pd.DataFrame) -> dict[str, float]:
    if rows.empty:
        return {
            "rolling_windows": 0,
            "rolling_positive_return_rate": 0.0,
            "rolling_median_cagr": 0.0,
            "rolling_min_cagr": 0.0,
            "rolling_median_sharpe": 0.0,
            "rolling_min_sharpe": 0.0,
            "rolling_worst_drawdown": 0.0,
        }
    return {
        "rolling_windows": int(len(rows)),
        "rolling_positive_return_rate": float((rows["total_return"] > 0).mean()),
        "rolling_median_cagr": float(rows["cagr"].median()),
        "rolling_min_cagr": float(rows["cagr"].min()),
        "rolling_median_sharpe": float(rows["sharpe"].median()),
        "rolling_min_sharpe": float(rows["sharpe"].min()),
        "rolling_worst_drawdown": float(rows["max_drawdown"].min()),
    }


def balanced_challenger_screen(
    metrics: pd.DataFrame, rolling_summary: pd.DataFrame
) -> pd.DataFrame:
    by_key = metrics.set_index(["period", "core_cap"])
    rolling = rolling_summary.set_index("core_cap")
    rows = []
    for cap in [value for value in CAPS if value > REFERENCE_CAP]:
        checks: dict[str, bool | float] = {}
        for period in SCREEN_PERIODS:
            candidate = by_key.loc[(period, cap)]
            reference = by_key.loc[(period, REFERENCE_CAP)]
            checks[f"{period}_return_higher"] = bool(
                candidate["total_return"] > reference["total_return"] + 1e-12
            )
            checks[f"{period}_dd_within_3pp"] = bool(
                candidate["max_drawdown"] >= reference["max_drawdown"] - 0.03 - 1e-12
            )
            checks[f"{period}_sharpe_within_005"] = bool(
                candidate["sharpe"] >= reference["sharpe"] - 0.05 - 1e-12
            )
            checks[f"{period}_monthly_win_within_1pp"] = bool(
                candidate["monthly_win_rate"]
                >= reference["monthly_win_rate"] - 0.01 - 1e-12
            )
        full_dd_ok = bool(
            by_key.loc[("full_2006_2025", cap), "max_drawdown"] >= -0.20 - 1e-12
        )
        rolling_ok = bool(
            rolling.at[cap, "rolling_positive_return_rate"]
            >= rolling.at[REFERENCE_CAP, "rolling_positive_return_rate"] - 1e-12
        )
        checks["full_drawdown_not_worse_than_20pct"] = full_dd_ok
        checks["rolling_positive_rate_nonworse"] = rolling_ok
        rows.append(
            {
                "core_cap": cap,
                **checks,
                "passes_balanced_challenger_screen": bool(all(checks.values())),
            }
        )
    return pd.DataFrame(rows)


def pct(value: float) -> str:
    return f"{value:.2%}"


def write_report(
    metrics: pd.DataFrame,
    rolling_summary: pd.DataFrame,
    screen: pd.DataFrame,
    summary: dict,
) -> None:
    by_key = metrics.set_index(["period", "core_cap"])
    screen_by_cap = screen.set_index("core_cap")
    lines = [
        "# V9 core-allocation frontier audit",
        "",
        "## Scope",
        "",
        "This research-only audit changes only the V9 SPY/QQQ index-core ceiling. The MA150/MA200 vote, Fear Gate, next-session execution and 10 bps one-way proportional transaction cost are unchanged. No stock alpha, cash yield, leverage, tax or broker-specific whole-share assumption is included.",
        "",
        "## Cross-period frontier",
        "",
        "| Core cap | Validation return | Final return | 2026 return | Full CAGR | Full max DD | Full Sharpe | Monthly win | Balanced screen |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for cap in CAPS:
        validation = by_key.loc[("validation_2015_2019", cap)]
        final = by_key.loc[("final_2020_2025", cap)]
        heldout = by_key.loc[("heldout_2026", cap)]
        full = by_key.loc[("full_2006_2025", cap)]
        screen_text = "reference" if cap == REFERENCE_CAP else "n/a"
        if cap > REFERENCE_CAP:
            screen_text = (
                "pass"
                if bool(screen_by_cap.at[cap, "passes_balanced_challenger_screen"])
                else "fail"
            )
        lines.append(
            f"| {pct(cap)} | {pct(validation.total_return)} | {pct(final.total_return)} | "
            f"{pct(heldout.total_return)} | {pct(full.cagr)} | {pct(full.max_drawdown)} | "
            f"{full.sharpe:.2f} | {pct(full.monthly_win_rate)} | {screen_text} |"
        )
    lines.extend(
        [
            "",
            "## Rolling three-year robustness",
            "",
            "| Core cap | Windows | Positive | Median CAGR | Minimum CAGR | Median Sharpe | Minimum Sharpe | Worst DD |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rolling_summary.itertuples(index=False):
        lines.append(
            f"| {pct(row.core_cap)} | {row.rolling_windows} | "
            f"{pct(row.rolling_positive_return_rate)} | {pct(row.rolling_median_cagr)} | "
            f"{pct(row.rolling_min_cagr)} | {row.rolling_median_sharpe:.2f} | "
            f"{row.rolling_min_sharpe:.2f} | {pct(row.rolling_worst_drawdown)} |"
        )
    selected = summary["selected_research_challenger"]
    lines.extend(["", "## Decision", ""])
    if selected is None:
        lines.append(
            "- No higher core ceiling passed the preregistered balanced-challenger screen. Retain 70% with no allocation challenger."
        )
    else:
        cap = float(selected)
        full_candidate = by_key.loc[("full_2006_2025", cap)]
        full_reference = by_key.loc[("full_2006_2025", REFERENCE_CAP)]
        lines.extend(
            [
                f"- The lowest passing ceiling is `{pct(cap)}`. It raises full-period CAGR by `{(full_candidate.cagr - full_reference.cagr) * 100:.2f}` percentage points while worsening full-period maximum drawdown by `{(full_reference.max_drawdown - full_candidate.max_drawdown) * 100:.2f}` percentage points.",
                f"- This is only a research challenger. A `{pct(cap)}` core leaves at most `{pct(1.0 - cap)}` for all individual stocks at maximum core exposure; the shared-capital core-plus-RSR interaction has not yet passed a separate audit.",
            ]
        )
    reference = by_key.loc[("full_2006_2025", REFERENCE_CAP)]
    highest = by_key.loc[("full_2006_2025", 1.0)]
    lines.extend(
        [
            f"- Moving from 70% to 100% raises full-period CAGR from `{pct(reference.cagr)}` to `{pct(highest.cagr)}`, but maximum drawdown moves from `{pct(reference.max_drawdown)}` to `{pct(highest.max_drawdown)}`. Allocation changes profit magnitude, not the underlying signal hit rate.",
            "- Formal V9 remains 70% core / 30% stock ceiling. No order or live allocation change is authorized.",
            "",
            "See `core-allocation-frontier-preregistration.md` for the frozen screen.",
        ]
    )
    (RESULTS / "core_allocation_frontier_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    current_panels, current_vix, meta = load_data()
    historical_panels, historical_vix, long_meta = load_long_history()
    latest = str(pd.Timestamp(meta["last_date"]).date())
    metric_rows = []
    full_curves: dict[str, pd.Series] = {}
    rolling_rows = []
    rolling_summaries = []
    for cap in CAPS:
        for period, (start, configured_end, warmup) in PERIODS.items():
            end = latest if configured_end is None else configured_end
            if period == "heldout_2026":
                panels, vix = current_panels, current_vix
            else:
                panels, vix = historical_panels, historical_vix
            metrics, curve = run_core(panels, vix, cap, start, end, warmup)
            metric_rows.append(
                {
                    "period": period,
                    "core_cap": cap,
                    "start": start,
                    "end": end,
                    **metrics,
                }
            )
            if period == "full_2006_2025":
                full_curves[f"core_{int(cap * 100)}"] = curve / curve.iloc[0]
                rolling = rolling_metrics(curve)
                rolling.insert(0, "core_cap", cap)
                rolling_rows.append(rolling)
                rolling_summaries.append({"core_cap": cap, **summarize_rolling(rolling)})
    metrics = pd.DataFrame(metric_rows)
    rolling = pd.concat(rolling_rows, ignore_index=True)
    rolling_summary = pd.DataFrame(rolling_summaries)
    screen = balanced_challenger_screen(metrics, rolling_summary)
    passing = screen.loc[screen["passes_balanced_challenger_screen"], "core_cap"]
    selected = float(passing.min()) if len(passing) else None
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_source": meta.get("source"),
        "long_history_data_source": long_meta,
        "latest_completed_date": latest,
        "research_only": True,
        "authorizes_trade": False,
        "formal_core_cap": REFERENCE_CAP,
        "caps_tested": list(CAPS),
        "selected_research_challenger": selected,
        "challengers_passing": int(screen["passes_balanced_challenger_screen"].sum()),
        "formal_decision": "keep_v9_70_30_unchanged_pending_shared_capital_audit",
    }
    metrics.to_csv(RESULTS / "core_allocation_frontier_metrics.csv", index=False)
    rolling.to_csv(RESULTS / "core_allocation_frontier_rolling.csv", index=False)
    rolling_summary.to_csv(
        RESULTS / "core_allocation_frontier_rolling_summary.csv", index=False
    )
    screen.to_csv(RESULTS / "core_allocation_frontier_screen.csv", index=False)
    pd.DataFrame(full_curves).to_csv(RESULTS / "core_allocation_frontier_equity.csv")
    (RESULTS / "core_allocation_frontier_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(metrics, rolling_summary, screen, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
