from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
QUANT_ROOT = HERE.parents[2]
DATASETS = QUANT_ROOT / "strategies" / "v9-execution" / "datasets"
PIT_DIR = DATASETS / "data_point_in_time"
LONG_DIR = DATASETS / "data_long"
OUT_DIR = HERE / "results"

START = pd.Timestamp("2006-01-03")
END = pd.Timestamp("2025-12-30")
TOP_N = 5
COST_BPS = 10.0


@dataclass(frozen=True)
class Variant:
    name: str
    absolute_vol_cap: float | None = None
    cross_sectional_vol_percentile: float | None = None


VARIANTS = (
    Variant("baseline"),
    Variant("rv40", absolute_vol_cap=0.40),
    Variant("rv_percentile_60", cross_sectional_vol_percentile=0.60),
    Variant("dual_rv40_p60", absolute_vol_cap=0.40, cross_sectional_vol_percentile=0.60),
)


def load_series(symbol: str) -> pd.Series:
    frame = pd.read_csv(LONG_DIR / f"{symbol}_adjusted_close.csv", parse_dates=["Date"])
    return frame.set_index("Date")[symbol].sort_index().astype(float)


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    prices = pd.read_csv(PIT_DIR / "adjusted_close.csv", index_col=0, parse_dates=True)
    prices = prices.sort_index().loc[START:END].astype(float)
    membership = pd.read_csv(PIT_DIR / "membership_history.csv")
    membership["opt-in"] = pd.to_datetime(membership["opt-in"])
    membership["opt-out"] = pd.to_datetime(membership["opt-out"]).fillna(pd.Timestamp.max.normalize())
    market = pd.concat({symbol: load_series(symbol) for symbol in ("SPY", "QQQ", "SMH")}, axis=1)
    market = market.reindex(prices.index).ffill(limit=3)
    return prices, membership, market


def active_symbols(membership: pd.DataFrame, date: pd.Timestamp, available: pd.Index) -> pd.Index:
    active = membership.loc[
        (membership["opt-in"] <= date) & (membership["opt-out"] > date), "symbol"
    ].drop_duplicates()
    return pd.Index(active[active.isin(available)])


def weekly_signal_dates(index: pd.DatetimeIndex) -> pd.DatetimeIndex:
    marker = pd.Series(index=index, data=index)
    return pd.DatetimeIndex(marker.groupby(index.to_period("W-FRI")).max().values)


def calculate_features(prices: pd.DataFrame, market: pd.DataFrame) -> dict[str, pd.DataFrame | pd.Series]:
    returns = prices.pct_change(fill_method=None)
    spy_return_126 = market["SPY"].pct_change(126, fill_method=None)
    features: dict[str, pd.DataFrame | pd.Series] = {
        "ma50": prices.rolling(50, min_periods=50).mean(),
        "ma200": prices.rolling(200, min_periods=200).mean(),
        "prior_high126": prices.shift(1).rolling(126, min_periods=126).max(),
        "mom126": prices.pct_change(126, fill_method=None),
        "rv20": returns.rolling(20, min_periods=20).std() * np.sqrt(252),
        "spy_mom126": spy_return_126,
        "market_gate": (market["SPY"] > market["SPY"].rolling(200).mean())
        & (market["QQQ"] > market["QQQ"].rolling(100).mean()),
    }
    return features


def candidate_snapshot(
    date: pd.Timestamp,
    prices: pd.DataFrame,
    membership: pd.DataFrame,
    features: dict[str, pd.DataFrame | pd.Series],
) -> pd.DataFrame:
    if not bool(features["market_gate"].get(date, False)):
        return pd.DataFrame()
    symbols = active_symbols(membership, date, prices.columns)
    if symbols.empty:
        return pd.DataFrame()
    frame = pd.DataFrame(
        {
            "close": prices.loc[date, symbols],
            "ma50": features["ma50"].loc[date, symbols],
            "ma200": features["ma200"].loc[date, symbols],
            "prior_high126": features["prior_high126"].loc[date, symbols],
            "mom126": features["mom126"].loc[date, symbols],
            "rv20": features["rv20"].loc[date, symbols],
        }
    ).dropna()
    if frame.empty:
        return frame
    frame["rs126"] = frame["mom126"] - float(features["spy_mom126"].loc[date])
    frame["rv_percentile"] = frame["rv20"].rank(pct=True, method="average")
    frame["momentum_percentile"] = frame["mom126"].rank(pct=True, method="average")
    frame = frame.loc[
        (frame["close"] >= 5.0)
        & (frame["close"] > frame["ma50"])
        & (frame["ma50"] > frame["ma200"])
        & (frame["close"] >= 0.98 * frame["prior_high126"])
        & (frame["rs126"] > 0.0)
        & (frame["momentum_percentile"] >= 0.70)
    ].copy()
    if not frame.empty:
        frame["rank_score"] = 0.6 * frame["momentum_percentile"] + 0.4 * frame["rs126"].rank(pct=True)
    return frame.sort_values(["rank_score", "mom126"], ascending=False)


def apply_variant(frame: pd.DataFrame, variant: Variant) -> pd.DataFrame:
    if frame.empty:
        return frame
    selected = frame
    if variant.absolute_vol_cap is not None:
        selected = selected.loc[selected["rv20"] <= variant.absolute_vol_cap]
    if variant.cross_sectional_vol_percentile is not None:
        selected = selected.loc[selected["rv_percentile"] <= variant.cross_sectional_vol_percentile]
    return selected.head(TOP_N)


def build_target_weights(
    prices: pd.DataFrame,
    membership: pd.DataFrame,
    features: dict[str, pd.DataFrame | pd.Series],
    variants: tuple[Variant, ...] = VARIANTS,
) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    dates = weekly_signal_dates(prices.index)
    records: dict[str, list[pd.Series]] = {variant.name: [] for variant in variants}
    event_rows: list[dict[str, float | str | pd.Timestamp]] = []
    for date in dates:
        snapshot = candidate_snapshot(date, prices, membership, features)
        if not snapshot.empty:
            for symbol, row in snapshot.iterrows():
                event_rows.append(
                    {
                        "signal_date": date,
                        "symbol": symbol,
                        "rv20": row["rv20"],
                        "rv_percentile": row["rv_percentile"],
                        "mom126": row["mom126"],
                        "rs126": row["rs126"],
                    }
                )
        for variant in variants:
            picked = apply_variant(snapshot, variant)
            weights = pd.Series(0.0, index=prices.columns, name=date)
            if not picked.empty:
                weights.loc[picked.index] = 1.0 / len(picked)
            records[variant.name].append(weights)
    targets = {name: pd.DataFrame(rows) for name, rows in records.items()}
    events = pd.DataFrame(event_rows)
    return targets, events


def simulate(
    prices: pd.DataFrame,
    targets: pd.DataFrame,
    cost_bps: float = COST_BPS,
    missing_return: float = 0.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw_returns = prices.pct_change(fill_method=None)
    weights = pd.DataFrame(0.0, index=prices.index, columns=prices.columns)
    turnover = pd.Series(0.0, index=prices.index)
    current = pd.Series(0.0, index=prices.columns)
    schedule = {date: targets.loc[date] for date in targets.index}
    signal_dates = set(targets.index)
    pending: pd.Series | None = None
    holdings_records: list[dict[str, str | float | pd.Timestamp]] = []
    for date in prices.index:
        if pending is not None:
            new = pending.reindex(prices.columns).fillna(0.0)
            turnover.loc[date] = (new - current).abs().sum()
            current = new
            pending = None
        weights.loc[date] = current
        for symbol, weight in current[current > 0].items():
            holdings_records.append({"date": date, "symbol": symbol, "weight": weight})
        if date in signal_dates:
            pending = schedule[date]
    asset_returns = raw_returns.copy()
    if missing_return != 0.0:
        lost_quote = prices.shift(1).notna() & prices.isna()
        asset_returns = asset_returns.mask(lost_quote, missing_return)
    asset_returns = asset_returns.fillna(0.0)
    gross = (weights * asset_returns).sum(axis=1)
    # Target weights are decided at a completed close and become effective on the
    # following session. Charging turnover on that same following session keeps
    # both signal timing and costs conservative and explicit.
    net = gross - turnover * (cost_bps / 10_000.0)
    result = pd.DataFrame(
        {
            "gross_return": gross,
            "turnover": turnover,
            "cost": turnover * (cost_bps / 10_000.0),
            "return": net,
            "exposure": weights.sum(axis=1),
        }
    )
    result["nav"] = (1.0 + result["return"]).cumprod()
    return result, pd.DataFrame(holdings_records)


def metric_row(returns: pd.Series, turnover: pd.Series, exposure: pd.Series) -> dict[str, float]:
    returns = returns.dropna()
    years = max(len(returns) / 252.0, 1 / 252)
    nav = (1.0 + returns).cumprod()
    total_return = float(nav.iloc[-1] - 1.0)
    cagr = float(nav.iloc[-1] ** (1.0 / years) - 1.0)
    volatility = float(returns.std(ddof=0) * np.sqrt(252))
    sharpe = float(returns.mean() / returns.std(ddof=0) * np.sqrt(252)) if returns.std(ddof=0) > 0 else np.nan
    downside = returns.clip(upper=0).std(ddof=0) * np.sqrt(252)
    sortino = float(returns.mean() * 252 / downside) if downside > 0 else np.nan
    drawdown = nav / nav.cummax() - 1.0
    monthly = (1.0 + returns).resample("ME").prod() - 1.0
    losses = returns[returns <= returns.quantile(0.05)]
    return {
        "total_return": total_return,
        "cagr": cagr,
        "annual_volatility": volatility,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown": float(drawdown.min()),
        "calmar": float(cagr / abs(drawdown.min())) if drawdown.min() < 0 else np.nan,
        "monthly_win_rate": float((monthly > 0).mean()),
        "daily_es_5": float(losses.mean()) if not losses.empty else np.nan,
        "annual_turnover": float(turnover.loc[returns.index].sum() / years),
        "average_exposure": float(exposure.loc[returns.index].mean()),
    }


def period_metrics(result: pd.DataFrame, name: str, missing_mode: str) -> list[dict[str, float | str]]:
    periods = {
        "development_2006_2014": ("2006-01-03", "2014-12-31"),
        "validation_2015_2019": ("2015-01-01", "2019-12-31"),
        "final_2020_2025": ("2020-01-01", "2025-12-30"),
        "full_2006_2025": ("2006-01-03", "2025-12-30"),
    }
    rows: list[dict[str, float | str]] = []
    for period, (start, end) in periods.items():
        sliced = result.loc[start:end]
        if sliced.empty:
            continue
        rows.append(
            {
                "variant": name,
                "missing_mode": missing_mode,
                "period": period,
                **metric_row(sliced["return"], sliced["turnover"], sliced["exposure"]),
            }
        )
        mapped = sliced.copy()
        mapped["return"] *= 0.25
        mapped["turnover"] *= 0.25
        mapped["exposure"] *= 0.25
        rows.append(
            {
                "variant": f"{name}_mapped_25pct",
                "missing_mode": missing_mode,
                "period": period,
                **metric_row(mapped["return"], mapped["turnover"], mapped["exposure"]),
            }
        )
    return rows


def add_event_outcomes(events: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    if events.empty:
        return events
    positions = pd.Series(np.arange(len(prices.index)), index=prices.index)
    rows = []
    for row in events.itertuples(index=False):
        start = int(positions.loc[row.signal_date])
        if start + 20 >= len(prices.index):
            continue
        path = prices[row.symbol].iloc[start + 1 : start + 21]
        entry = prices.at[row.signal_date, row.symbol]
        if pd.isna(entry) or path.isna().all():
            continue
        relative = path / entry - 1.0
        rows.append(
            {
                **row._asdict(),
                "forward_20d": float(relative.iloc[-1]) if pd.notna(relative.iloc[-1]) else np.nan,
                "mae_20d": float(relative.min()),
                "mfe_20d": float(relative.max()),
                "positive_20d": bool(relative.iloc[-1] > 0) if pd.notna(relative.iloc[-1]) else False,
                "close_stop_8pct": bool(relative.min() <= -0.08),
                "winner_10pct": bool(relative.max() >= 0.10),
                "passes_rv40": bool(row.rv20 <= 0.40),
                "passes_p60": bool(row.rv_percentile <= 0.60),
                "passes_dual": bool(row.rv20 <= 0.40 and row.rv_percentile <= 0.60),
            }
        )
    return pd.DataFrame(rows)


def event_summary(events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    masks = {
        "baseline": pd.Series(True, index=events.index),
        "rv40": events["passes_rv40"],
        "rv_percentile_60": events["passes_p60"],
        "dual_rv40_p60": events["passes_dual"],
        "rejected_by_dual": ~events["passes_dual"],
    }
    periods = {
        "development_2006_2014": ("2006-01-03", "2014-12-31"),
        "validation_2015_2019": ("2015-01-01", "2019-12-31"),
        "final_2020_2025": ("2020-01-01", "2025-12-30"),
    }
    for period, (start, end) in periods.items():
        period_mask = events["signal_date"].between(start, end)
        for name, mask in masks.items():
            sample = events.loc[period_mask & mask]
            rows.append(
                {
                    "period": period,
                    "group": name,
                    "events": len(sample),
                    "mean_forward_20d": sample["forward_20d"].mean(),
                    "median_forward_20d": sample["forward_20d"].median(),
                    "positive_20d_rate": sample["positive_20d"].mean(),
                    "close_stop_8pct_rate": sample["close_stop_8pct"].mean(),
                    "winner_10pct_rate": sample["winner_10pct"].mean(),
                }
            )
    return pd.DataFrame(rows)


def parameter_stability(
    prices: pd.DataFrame,
    membership: pd.DataFrame,
    features: dict[str, pd.DataFrame | pd.Series],
) -> pd.DataFrame:
    variants = tuple(
        [Variant(f"abs_{int(cap * 100)}", absolute_vol_cap=cap) for cap in (0.30, 0.35, 0.40, 0.45, 0.50)]
        + [Variant(f"pct_{int(pct * 100)}", cross_sectional_vol_percentile=pct) for pct in (0.40, 0.50, 0.60, 0.70)]
    )
    targets, _ = build_target_weights(prices, membership, features, variants)
    rows = []
    for variant in variants:
        result, _ = simulate(prices, targets[variant.name])
        for metric in period_metrics(result, variant.name, "zero_return"):
            if not str(metric["variant"]).endswith("mapped_25pct"):
                rows.append(metric)
    return pd.DataFrame(rows)


def cost_sensitivity(prices: pd.DataFrame, targets: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    for name in ("baseline", "dual_rv40_p60"):
        for cost_bps in (0.0, 10.0, 20.0, 50.0):
            result, _ = simulate(prices, targets[name], cost_bps=cost_bps)
            for metric in period_metrics(result, name, "zero_return"):
                if metric["period"] in ("validation_2015_2019", "final_2020_2025", "full_2006_2025") and not str(
                    metric["variant"]
                ).endswith("mapped_25pct"):
                    rows.append({"cost_bps": cost_bps, **metric})
    return pd.DataFrame(rows)


def rolling_three_year_comparison(
    baseline: pd.DataFrame, candidate: pd.DataFrame
) -> tuple[pd.DataFrame, dict[str, float]]:
    rows = []
    for end_year in range(2010, 2026):
        start = f"{end_year - 2}-01-01"
        end = f"{end_year}-12-31"
        base_slice = baseline.loc[start:end]
        candidate_slice = candidate.loc[start:end]
        if len(base_slice) < 600 or len(candidate_slice) < 600:
            continue
        base_metrics = metric_row(base_slice["return"], base_slice["turnover"], base_slice["exposure"])
        candidate_metrics = metric_row(
            candidate_slice["return"], candidate_slice["turnover"], candidate_slice["exposure"]
        )
        rows.append(
            {
                "window": f"{end_year - 2}-{end_year}",
                "baseline_cagr": base_metrics["cagr"],
                "candidate_cagr": candidate_metrics["cagr"],
                "baseline_max_drawdown": base_metrics["max_drawdown"],
                "candidate_max_drawdown": candidate_metrics["max_drawdown"],
                "baseline_sharpe": base_metrics["sharpe"],
                "candidate_sharpe": candidate_metrics["sharpe"],
                "baseline_monthly_win_rate": base_metrics["monthly_win_rate"],
                "candidate_monthly_win_rate": candidate_metrics["monthly_win_rate"],
            }
        )
    frame = pd.DataFrame(rows)
    summary = {
        "windows": float(len(frame)),
        "higher_cagr_rate": float((frame["candidate_cagr"] > frame["baseline_cagr"]).mean()),
        "better_drawdown_rate": float(
            (frame["candidate_max_drawdown"] > frame["baseline_max_drawdown"]).mean()
        ),
        "higher_sharpe_rate": float((frame["candidate_sharpe"] > frame["baseline_sharpe"]).mean()),
        "higher_monthly_win_rate": float(
            (frame["candidate_monthly_win_rate"] > frame["baseline_monthly_win_rate"]).mean()
        ),
    }
    return frame, summary


def pct(value: float) -> str:
    return "NA" if pd.isna(value) else f"{value:.2%}"


def num(value: float) -> str:
    return "NA" if pd.isna(value) else f"{value:.2f}"


def write_report(
    metrics: pd.DataFrame,
    events: pd.DataFrame,
    stability: pd.DataFrame,
    costs: pd.DataFrame,
    rolling_summary: dict[str, float],
    coverage: dict[str, float],
) -> None:
    lines = [
        "# Point-in-time low-volatility breakout proxy",
        "",
        "## Research boundary",
        "",
        "- Universe membership is point-in-time S&P 500 plus Nasdaq-100, deduplicated at each weekly signal close.",
        "- The price panel is partial: 698 of 945 membership symbols have adjusted-close history. It lacks OHLCV and complete delisting returns.",
        "- Therefore `rv20 <= 40%` is a close-return volatility proxy for the post-hoc `ATR14 / close <= 4%` idea; it is not an ATR replication.",
        "- Signals use the completed weekly close; new weights begin on the following trading session. Results include 10 bps one-way turnover costs.",
        "- The stock sleeve holds up to five equal-weight names. The `_mapped_25pct` rows show the same sleeve diluted to the formal 25% stock-sleeve cap.",
        "- Research-only. No V9 or live-account permission is changed.",
        "",
        "## Coverage",
        "",
        f"- Membership symbols: {int(coverage['membership_symbols'])}",
        f"- Price symbols: {int(coverage['price_symbols'])}",
        f"- Missing symbols: {int(coverage['missing_symbols'])}",
        f"- Median month-end coverage: {coverage['median_monthly_coverage']:.1%}",
        "",
        "## Portfolio results: normal missing-price assumption",
        "",
        "| Variant | Period | CAGR | Max DD | Sharpe | Monthly win | Annual turnover | Exposure |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    normal = metrics.loc[(metrics["missing_mode"] == "zero_return") & ~metrics["variant"].str.endswith("mapped_25pct")]
    for row in normal.itertuples(index=False):
        lines.append(
            f"| {row.variant} | {row.period} | {pct(row.cagr)} | {pct(row.max_drawdown)} | {num(row.sharpe)} | "
            f"{pct(row.monthly_win_rate)} | {num(row.annual_turnover)} | {pct(row.average_exposure)} |"
        )
    lines.extend(
        [
            "",
            "## Missing/delisting stress",
            "",
            "When a held symbol loses its quote immediately after a valid quote, the stress case assigns that position a -100% return on that day. "
            "This is intentionally harsher than many acquisitions but exposes sensitivity to the unavailable delisting-return field.",
            "",
            "| Variant | Period | CAGR | Max DD | Sharpe |",
            "| --- | --- | ---: | ---: | ---: |",
        ]
    )
    stressed = metrics.loc[(metrics["missing_mode"] == "minus_100pct") & ~metrics["variant"].str.endswith("mapped_25pct")]
    for row in stressed.itertuples(index=False):
        lines.append(f"| {row.variant} | {row.period} | {pct(row.cagr)} | {pct(row.max_drawdown)} | {num(row.sharpe)} |")
    lines.extend(
        [
            "",
            "## Breakout event outcomes (20 trading sessions)",
            "",
            "| Group | Period | Events | Mean return | Positive | Close-stop <= -8% | Reached +10% |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in events.itertuples(index=False):
        if row.group in ("baseline", "dual_rv40_p60", "rejected_by_dual"):
            lines.append(
                f"| {row.group} | {row.period} | {row.events} | {pct(row.mean_forward_20d)} | "
                f"{pct(row.positive_20d_rate)} | {pct(row.close_stop_8pct_rate)} | {pct(row.winner_10pct_rate)} |"
            )
    lines.extend(
        [
            "",
            "## Rolling three-year consistency",
            "",
            f"Across {int(rolling_summary['windows'])} overlapping three-year windows, `dual_rv40_p60` beat baseline on CAGR in "
            f"{rolling_summary['higher_cagr_rate']:.1%}, max drawdown in {rolling_summary['better_drawdown_rate']:.1%}, "
            f"Sharpe in {rolling_summary['higher_sharpe_rate']:.1%}, and monthly win rate in "
            f"{rolling_summary['higher_monthly_win_rate']:.1%} of windows.",
            "",
            "## Cost sensitivity (final 2020-2025)",
            "",
            "| Variant | One-way cost | CAGR | Max DD | Sharpe |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    final_costs = costs.loc[costs["period"] == "final_2020_2025"]
    for row in final_costs.itertuples(index=False):
        lines.append(
            f"| {row.variant} | {row.cost_bps:.0f} bps | {pct(row.cagr)} | {pct(row.max_drawdown)} | {num(row.sharpe)} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation rule",
            "",
            "The proxy is useful only if it improves validation and final-period downside/win behavior without relying mainly on cash exposure. "
            "A better full-sample headline alone is insufficient. Parameter neighbors must tell the same directional story, and the forward RSR1 shadow remains mandatory.",
            "",
            "## Parameter-neighbor file",
            "",
            "See `pit_parameter_stability.csv` for absolute realized-volatility caps of 30%-50% and cross-sectional cutoffs of 40%-70%. No neighbor is promoted from this retrospective run.",
        ]
    )
    (OUT_DIR / "pit_low_vol_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prices, membership, market = load_inputs()
    features = calculate_features(prices, market)
    targets, raw_events = build_target_weights(prices, membership, features)
    metric_rows: list[dict[str, float | str]] = []
    for variant in VARIANTS:
        for missing_mode, missing_return in (("zero_return", 0.0), ("minus_100pct", -1.0)):
            result, holdings = simulate(prices, targets[variant.name], missing_return=missing_return)
            metric_rows.extend(period_metrics(result, variant.name, missing_mode))
            if missing_mode == "zero_return":
                result.to_csv(OUT_DIR / f"pit_daily_{variant.name}.csv", index_label="date")
                holdings.to_csv(OUT_DIR / f"pit_holdings_{variant.name}.csv", index=False)
    metrics = pd.DataFrame(metric_rows)
    outcomes = add_event_outcomes(raw_events, prices)
    events = event_summary(outcomes)
    stability = parameter_stability(prices, membership, features)
    costs = cost_sensitivity(prices, targets)
    baseline_result, _ = simulate(prices, targets["baseline"])
    candidate_result, _ = simulate(prices, targets["dual_rv40_p60"])
    rolling, rolling_summary = rolling_three_year_comparison(baseline_result, candidate_result)
    coverage_monthly = pd.read_csv(PIT_DIR / "coverage_by_month.csv")
    coverage = {
        "membership_symbols": float(membership["symbol"].nunique()),
        "price_symbols": float(prices.shape[1]),
        "missing_symbols": float(membership["symbol"].nunique() - prices.shape[1]),
        "median_monthly_coverage": float(coverage_monthly["price_coverage"].median()),
    }
    metrics.to_csv(OUT_DIR / "pit_portfolio_metrics.csv", index=False)
    outcomes.to_csv(OUT_DIR / "pit_breakout_events.csv", index=False)
    events.to_csv(OUT_DIR / "pit_event_summary.csv", index=False)
    stability.to_csv(OUT_DIR / "pit_parameter_stability.csv", index=False)
    costs.to_csv(OUT_DIR / "pit_cost_sensitivity.csv", index=False)
    rolling.to_csv(OUT_DIR / "pit_rolling_3y.csv", index=False)
    with (OUT_DIR / "pit_low_vol_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "research_only": True,
                "formal_v9_modified": False,
                "live_authorization": False,
                "coverage": coverage,
                "variants": [asdict(variant) for variant in VARIANTS],
            },
            handle,
            indent=2,
        )
    write_report(metrics, events, stability, costs, rolling_summary, coverage)
    print(OUT_DIR / "pit_low_vol_report.md")


if __name__ == "__main__":
    main()
