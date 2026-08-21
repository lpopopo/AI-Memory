#!/usr/bin/env python3
"""Audit V9 core month-end whipsaw alternatives without changing formal V9."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
QUANT_ROOT = HERE.parents[2]
V9 = QUANT_ROOT / "strategies" / "v9-execution"
sys.path.insert(0, str(V9 / "scripts"))

from v9_data import load_data  # noqa: E402
from v9_information_strategy import V9Backtester, V9Config  # noqa: E402


RESULTS = HERE / "results"
WARMUP = "2024-01-02"
VARIANTS = {
    "current_1m": (1, 1, False),
    "confirm_2m_both": (2, 2, False),
    "confirm_2m_exit": (2, 1, False),
    "confirm_2m_entry": (1, 2, False),
    "ma200_only": (1, 1, True),
}


def completed_month_ends(index: pd.DatetimeIndex) -> list[pd.Timestamp]:
    """Return only visibly completed month ends; never infer an incomplete last row."""
    result = []
    for i, date in enumerate(index):
        if i + 1 < len(index):
            if index[i + 1].to_period("M") != date.to_period("M"):
                result.append(date)
        elif date.normalize() == (date + pd.offsets.BMonthEnd(0)).normalize():
            result.append(date)
    return result


def raw_monthly_targets(
    close: pd.DataFrame,
    ma150: pd.DataFrame,
    ma200: pd.DataFrame,
    ma200_only: bool = False,
) -> pd.DataFrame:
    rows = []
    for date in completed_month_ends(close.index):
        row = {"date": date}
        for symbol in ("SPY", "QQQ"):
            above_200 = int(close.at[date, symbol] > ma200.at[date, symbol])
            if ma200_only:
                row[symbol] = 0.5 * above_200
            else:
                above_150 = int(close.at[date, symbol] > ma150.at[date, symbol])
                row[symbol] = 0.25 * (above_150 + above_200)
        rows.append(row)
    return pd.DataFrame(rows).set_index("date")


def confirmed_daily_targets(
    index: pd.DatetimeIndex,
    monthly: pd.DataFrame,
    exit_confirm: int = 1,
    entry_confirm: int = 1,
) -> tuple[dict[pd.Timestamp, dict[str, float]], pd.DataFrame]:
    """Apply exact-target consecutive month confirmation, then forward-fill daily."""
    if exit_confirm < 1 or entry_confirm < 1:
        raise ValueError("confirmation months must be positive")
    state = {"SPY": 0.0, "QQQ": 0.0}
    candidate = {"SPY": None, "QQQ": None}
    count = {"SPY": 0, "QQQ": 0}
    decisions = []
    monthly_dates = set(monthly.index)
    daily = {}
    for date in index:
        if date in monthly_dates:
            decision = {"date": date}
            for symbol in ("SPY", "QQQ"):
                proposed = float(monthly.at[date, symbol])
                before = state[symbol]
                if proposed == before:
                    candidate[symbol] = None
                    count[symbol] = 0
                else:
                    if candidate[symbol] == proposed:
                        count[symbol] += 1
                    else:
                        candidate[symbol] = proposed
                        count[symbol] = 1
                    required = exit_confirm if proposed < before else entry_confirm
                    if count[symbol] >= required:
                        state[symbol] = proposed
                        candidate[symbol] = None
                        count[symbol] = 0
                decision[f"{symbol}_raw"] = proposed
                decision[f"{symbol}_before"] = before
                decision[f"{symbol}_confirmed"] = state[symbol]
                decision[f"{symbol}_pending"] = candidate[symbol]
                decision[f"{symbol}_pending_count"] = count[symbol]
            decisions.append(decision)
        daily[date] = dict(state)
    return daily, pd.DataFrame(decisions).set_index("date")


def curve_metrics(curve: pd.Series) -> dict[str, float]:
    returns = curve.pct_change().fillna(0.0)
    drawdown = curve / curve.cummax() - 1.0
    std = float(returns.std(ddof=0))
    return {
        "total_return": float(curve.iloc[-1] / curve.iloc[0] - 1.0),
        "max_drawdown": float(drawdown.min()),
        "sharpe": float(returns.mean() / std * math.sqrt(252)) if std else 0.0,
        "turnover": float("nan"),
        "trades": 0,
    }


def run_variant(
    panels: dict[str, pd.DataFrame],
    vix: pd.DataFrame,
    variant: str,
    start: str,
    end: str,
) -> tuple[dict, pd.Series, pd.DataFrame, pd.DataFrame]:
    exit_confirm, entry_confirm, use_ma200_only = VARIANTS[variant]
    engine = V9Backtester(
        panels,
        vix,
        [],
        V9Config(v8_core_weight=0.70, info_sleeve_weight=0.0),
        [],
    )
    monthly = raw_monthly_targets(
        engine.close, engine.ma150, engine.ma200, ma200_only=use_ma200_only
    )
    targets, decisions = confirmed_daily_targets(
        engine.close.index, monthly, exit_confirm, entry_confirm
    )
    for date in decisions.index:
        core_cap, _, fear = engine._effective_sleeve_caps(date)
        decisions.at[date, "core_cap"] = core_cap
        decisions.at[date, "fear_regime"] = fear["regime"]
        decisions.at[date, "fear_score"] = fear["score"]
        decisions.at[date, "fear_max_gross"] = fear["max_gross_exposure"]
        decisions.at[date, "positive_fear_signals"] = "; ".join(
            f"{signal['name']}:{signal['points']}"
            for signal in fear["signals"]
            if signal["points"] > 0
        )
        for symbol in ("SPY", "QQQ"):
            decisions.at[date, f"{symbol}_effective_target"] = (
                decisions.at[date, f"{symbol}_confirmed"] * core_cap
            )
    engine.v8_base_weights = targets
    result = engine.run(warmup_start=WARMUP, trading_start=start, trading_end=end)
    metrics = curve_metrics(result.equity)
    metrics.update(
        {
            "turnover": float(result.diagnostics["turnover"]),
            "trades": len(result.ledger),
        }
    )
    ledger = pd.DataFrame(result.ledger)
    if not ledger.empty:
        ledger.insert(0, "variant", variant)
        ledger.insert(1, "period", "train_2025" if start.startswith("2025") else "test_2026")
    return metrics, result.equity, decisions, ledger


def paired_screen(metrics: pd.DataFrame) -> pd.DataFrame:
    base = metrics.loc[metrics["variant"] == "current_1m"].set_index("period")
    rows = []
    for variant in metrics["variant"].drop_duplicates():
        if variant == "current_1m":
            continue
        sample = metrics.loc[metrics["variant"] == variant].set_index("period")
        checks = {}
        for period in ("train_2025", "test_2026"):
            checks[f"{period}_return_nonworse"] = bool(
                sample.at[period, "total_return"] >= base.at[period, "total_return"]
            )
            checks[f"{period}_drawdown_nonworse"] = bool(
                sample.at[period, "max_drawdown"] >= base.at[period, "max_drawdown"]
            )
            checks[f"{period}_sharpe_nonworse"] = bool(
                sample.at[period, "sharpe"] >= base.at[period, "sharpe"]
            )
        comparison_fields = ("total_return", "max_drawdown", "sharpe", "turnover", "trades")
        behaviorally_distinct = any(
            abs(float(sample.at[period, field]) - float(base.at[period, field])) > 1e-12
            for period in ("train_2025", "test_2026")
            for field in comparison_fields
        )
        has_strict_improvement = any(
            float(sample.at[period, field]) > float(base.at[period, field]) + 1e-12
            for period in ("train_2025", "test_2026")
            for field in ("total_return", "max_drawdown", "sharpe")
        )
        rows.append(
            {
                "variant": variant,
                **checks,
                "behaviorally_distinct": behaviorally_distinct,
                "has_strict_improvement": has_strict_improvement,
                "passes_promotion_gate": (
                    all(checks.values()) and behaviorally_distinct and has_strict_improvement
                ),
            }
        )
    return pd.DataFrame(rows)


def pct(value: float) -> str:
    return f"{value:.2%}"


def write_report(metrics: pd.DataFrame, screen: pd.DataFrame, summary: dict) -> None:
    lines = [
        "# V9 core month-end whipsaw audit",
        "",
        "## Scope",
        "",
        "This research-only audit isolates the formal 70% SPY/QQQ core with no information sleeve. Signals use completed month-end closes; transactions remain next-session close. The frozen V9 implementation is not modified.",
        "",
        "The candidate set was fixed before comparison: current one-month response, two-month confirmation on both directions, exit only, entry only, and MA200-only. A challenger must be non-worse on return, drawdown and Sharpe in both calendar-2025 training and 2026 held-out data.",
        "",
        "## Results",
        "",
        "| Period | Variant | Return | Max DD | Sharpe | Turnover | Core trades |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in metrics.itertuples(index=False):
        lines.append(
            f"| {row.period} | {row.variant} | {pct(row.total_return)} | "
            f"{pct(row.max_drawdown)} | {row.sharpe:.2f} | {row.turnover:.2f} | {row.trades} |"
        )
    lines.extend(
        [
            "",
            "## 2026 whipsaw anatomy",
            "",
            f"- The current rule sold both core ETFs on `{summary['current_exit_date']}` after the March month-end signal and repurchased them on `{summary['current_reentry_date']}` after the April month-end signal.",
            f"- This was a joint gate event. The MA150/MA200 vote cut each ETF's base target from 50% to 0%, while the independent `{summary['march_fear_regime']}` risk regime (score `{summary['march_fear_score']}`; positive components: `{summary['march_positive_fear_signals']}`) reduced the total 70% core budget to `{pct(summary['march_core_cap'])}`. The current rule therefore exited fully; the delayed-exit variant still cut to `{pct(summary['delayed_exit_total_effective_target'])}` total core exposure.",
            f"- From the exit close to the re-entry close, SPY returned `{pct(summary['spy_gap_return'])}` and QQQ returned `{pct(summary['qqq_gap_return'])}`. A fully invested 35%/35% core missed approximately `{pct(summary['weighted_gap_opportunity'])}`; the tested delayed-exit path retained only 17.5%/17.5%, so its directly retained contribution was approximately `{pct(summary['delayed_exit_retained_opportunity'])}` before costs and sizing drift.",
            f"- Requiring two consecutive month-end exit signals improved 2026 return by `{pct(summary['slow_exit_2026_return_delta'])}`, but its 2025 maximum drawdown worsened by `{summary['slow_exit_2025_dd_worsening_pp']:.2f}` percentage points.",
            "",
            "## Decision",
            "",
            f"`{summary['passing_challengers']}` of `{summary['challengers_tested']}` challengers passed the cross-period promotion gate. MA200-only was behaviorally identical to current V9 in both samples and is not counted as an improvement. Therefore the April opportunity is classified as the known insurance cost of the trend and risk-budget gates, not sufficient evidence of an implementation defect or a rule change.",
            "",
            "Keep formal V9 unchanged. Track future one-month exits as a named forward diagnostic; reconsider only after repeated independent cases, not this single favorable counterfactual.",
        ]
    )
    (RESULTS / "v9_core_whipsaw_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    panels, vix, meta = load_data()
    end_2026 = str(pd.Timestamp(meta["last_date"]).date())
    periods = {
        "train_2025": ("2025-01-02", "2025-12-31"),
        "test_2026": ("2026-01-02", end_2026),
    }
    metric_rows = []
    equity = {}
    decisions = []
    ledgers = []
    for period, (start, end) in periods.items():
        for variant in VARIANTS:
            result, curve, decision, ledger = run_variant(
                panels, vix, variant, start, end
            )
            metric_rows.append({"period": period, "variant": variant, **result})
            equity[f"{period}_{variant}"] = curve
            block = decision.loc[start:end].reset_index()
            block.insert(0, "variant", variant)
            block.insert(1, "period", period)
            decisions.append(block)
            if not ledger.empty:
                ledgers.append(ledger)

    metrics = pd.DataFrame(metric_rows)
    screen = paired_screen(metrics)
    ledger = pd.concat(ledgers, ignore_index=True)
    current_ledger = ledger.loc[
        (ledger["period"] == "test_2026")
        & (ledger["variant"] == "current_1m")
        & (ledger["reason"] == "v8_rebalance")
    ]
    sells = current_ledger.loc[current_ledger["action"] == "SELL"]
    buys_after = current_ledger.loc[
        (current_ledger["action"] == "BUY")
        & (pd.to_datetime(current_ledger["date"]) > pd.to_datetime(sells["date"]).min())
    ]
    exit_date = pd.Timestamp(sells["date"].iloc[0])
    reentry_date = pd.Timestamp(buys_after["date"].iloc[0])
    spy_gap = float(panels["close"].at[reentry_date, "SPY"] / panels["close"].at[exit_date, "SPY"] - 1)
    qqq_gap = float(panels["close"].at[reentry_date, "QQQ"] / panels["close"].at[exit_date, "QQQ"] - 1)
    decision_table = pd.concat(decisions, ignore_index=True)
    march_delayed = decision_table.loc[
        (decision_table["period"] == "test_2026")
        & (decision_table["variant"] == "confirm_2m_exit")
        & (decision_table["date"] == pd.Timestamp("2026-03-31"))
    ].iloc[0]
    by_key = metrics.set_index(["period", "variant"])
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "data_source": meta.get("source"),
        "data_last_date": end_2026,
        "research_only": True,
        "authorizes_trade": False,
        "current_exit_date": str(exit_date.date()),
        "current_reentry_date": str(reentry_date.date()),
        "spy_gap_return": spy_gap,
        "qqq_gap_return": qqq_gap,
        "weighted_gap_opportunity": 0.35 * (spy_gap + qqq_gap),
        "march_fear_regime": march_delayed["fear_regime"],
        "march_fear_score": int(march_delayed["fear_score"]),
        "march_positive_fear_signals": march_delayed["positive_fear_signals"],
        "march_core_cap": float(march_delayed["core_cap"]),
        "delayed_exit_total_effective_target": float(
            march_delayed["SPY_effective_target"] + march_delayed["QQQ_effective_target"]
        ),
        "delayed_exit_retained_opportunity": float(
            march_delayed["SPY_effective_target"] * spy_gap
            + march_delayed["QQQ_effective_target"] * qqq_gap
        ),
        "slow_exit_2026_return_delta": float(
            by_key.at[("test_2026", "confirm_2m_exit"), "total_return"]
            - by_key.at[("test_2026", "current_1m"), "total_return"]
        ),
        "slow_exit_2025_dd_worsening_pp": float(
            (by_key.at[("train_2025", "current_1m"), "max_drawdown"]
            - by_key.at[("train_2025", "confirm_2m_exit"), "max_drawdown"])
            * 100
        ),
        "passing_challengers": int(screen["passes_promotion_gate"].sum()),
        "challengers_tested": int(len(screen)),
        "decision": "retain_formal_v9_track_one_month_exit_whipsaws_forward",
    }
    metrics.to_csv(RESULTS / "v9_core_whipsaw_metrics.csv", index=False)
    screen.to_csv(RESULTS / "v9_core_whipsaw_screen.csv", index=False)
    ledger.to_csv(RESULTS / "v9_core_whipsaw_transactions.csv", index=False)
    decision_table.to_csv(
        RESULTS / "v9_core_whipsaw_monthly_targets.csv", index=False
    )
    pd.DataFrame(equity).to_csv(RESULTS / "v9_core_whipsaw_equity.csv")
    (RESULTS / "v9_core_whipsaw_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    write_report(metrics, screen, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
