from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve().parent
QUANT_ROOT = HERE.parents[2]
PIT_DIR = QUANT_ROOT / "strategies" / "v9-execution" / "datasets" / "data_point_in_time"
DATA_DIR = HERE / "datasets" / "pit_exact_ohlcv"
OUT_DIR = HERE / "results"

INITIAL_NAV = 6_000.0
COMMISSION = 1.0
SLIPPAGE = 0.001
TARGET_WEIGHT = 0.08
SINGLE_MAX = 0.15
SLEEVE_MAX = 0.25
MAX_NAMES = 3
STOP_LOSS = 0.08
MAX_HOLD = 20
MAX_ENTRY_GAP = 0.05

PERIODS = {
    "development_2015_2019": (pd.Timestamp("2015-01-01"), pd.Timestamp("2019-12-31")),
    "validation_2020_2022": (pd.Timestamp("2020-01-01"), pd.Timestamp("2022-12-31")),
    "final_2023_2025": (pd.Timestamp("2023-01-01"), pd.Timestamp("2025-12-31")),
}


def load_inputs() -> tuple[dict[str, pd.DataFrame], pd.DataFrame, list[str]]:
    panels = {
        field: pd.read_csv(DATA_DIR / f"{field}.csv", index_col=0, parse_dates=True).sort_index()
        for field in ("open", "high", "low", "close", "volume")
    }
    dates = panels["close"]["SPY"].dropna().index
    panels = {field: frame.reindex(dates) for field, frame in panels.items()}
    if dates.max() > pd.Timestamp("2025-12-31"):
        raise RuntimeError("post-2025 data is forbidden by the preregistration")
    required_market = ["SPY", "QQQ", "SMH", "^VIX", "^VIX3M"]
    missing_columns = [symbol for symbol in required_market if symbol not in panels["close"]]
    missing_market = {
        symbol: int(panels["close"][symbol].isna().sum())
        for symbol in required_market
        if symbol in panels["close"] and panels["close"][symbol].isna().any()
    }
    if missing_columns or missing_market:
        raise RuntimeError(
            f"market close panel is incomplete: missing={missing_columns}, gaps={missing_market}"
        )
    symbols = pd.read_csv(DATA_DIR / "frozen_symbols.csv")
    stocks = [
        symbol
        for symbol in symbols.loc[symbols["role"] == "stock", "symbol"]
        if symbol in panels["close"].columns
    ]
    membership = pd.read_csv(PIT_DIR / "membership_history.csv")
    membership["opt-in"] = pd.to_datetime(membership["opt-in"])
    membership["opt-out"] = pd.to_datetime(membership["opt-out"], errors="coerce").fillna(
        pd.Timestamp.max.normalize()
    )
    return panels, membership, stocks


def membership_mask(
    membership: pd.DataFrame, dates: pd.DatetimeIndex, symbols: list[str]
) -> pd.DataFrame:
    values = np.zeros((len(dates), len(symbols)), dtype=bool)
    locations = {symbol: offset for offset, symbol in enumerate(symbols)}
    intervals = membership[["symbol", "opt-in", "opt-out"]]
    for symbol, opt_in, opt_out in intervals.itertuples(index=False, name=None):
        if symbol not in locations:
            continue
        start = dates.searchsorted(opt_in, side="left")
        end = dates.searchsorted(opt_out, side="left")
        if start < end:
            values[start:end, locations[symbol]] = True
    return pd.DataFrame(values, index=dates, columns=symbols)


def build_features(
    panels: dict[str, pd.DataFrame], stocks: list[str], members: pd.DataFrame
) -> dict[str, pd.DataFrame | pd.Series]:
    close = panels["close"]
    stock_close = close[stocks]
    high = panels["high"][stocks]
    low = panels["low"][stocks]
    open_ = panels["open"][stocks]
    volume = panels["volume"][stocks]

    ma20 = stock_close.rolling(20, min_periods=20).mean()
    ma50 = stock_close.rolling(50, min_periods=50).mean()
    prior_high20 = high.rolling(20, min_periods=20).max().shift(1)
    rs20 = stock_close.pct_change(20, fill_method=None).sub(
        close["SMH"].pct_change(20, fill_method=None), axis=0
    )
    volume_ratio = volume / volume.rolling(20, min_periods=20).mean().shift(1)
    extension = stock_close / ma20 - 1.0
    prior_close = stock_close.shift(1)
    true_range = pd.DataFrame(
        np.maximum.reduce(
            [
                (high - low).to_numpy(),
                (high - prior_close).abs().to_numpy(),
                (low - prior_close).abs().to_numpy(),
            ]
        ),
        index=stock_close.index,
        columns=stocks,
    )
    atr_pct = true_range.rolling(14, min_periods=14).mean() / stock_close
    close_location = (stock_close - low) / (high - low).replace(0.0, np.nan)
    positive_gap = open_ / prior_close - 1.0 >= 0.10
    day_range = (high - low) / open_
    event_block = positive_gap | positive_gap.shift(1).fillna(False)
    event_block |= positive_gap.shift(2).fillna(False) & (day_range >= 0.03)

    market_gate = (
        (close["SPY"] > close["SPY"].rolling(200, min_periods=200).mean())
        & (close["QQQ"] > close["QQQ"].rolling(100, min_periods=100).mean())
        & (close["SMH"] >= close["SMH"].rolling(50, min_periods=50).mean())
        & (close["^VIX"] < 25.0)
        & (close["^VIX"] / close["^VIX3M"] < 1.0)
    ).fillna(False)

    common = (
        members
        & stock_close.notna()
        & (stock_close > ma20)
        & (stock_close > ma50)
        & (stock_close > prior_high20)
        & (rs20 >= 0.03)
        & (volume_ratio >= 1.20)
        & (extension >= 0.0)
        & (extension <= 0.12)
        & ~event_block
    )
    common = common.mul(market_gate, axis=0).fillna(False)
    combined = common & (atr_pct <= 0.04) & (close_location >= 0.50)
    if (combined & ~common).to_numpy().any():
        raise RuntimeError("candidate signal must be a strict subset of the matched baseline")
    score = rs20 * 100.0 + volume_ratio.clip(upper=5.0)
    return {
        "ma20": ma20,
        "rs20": rs20,
        "volume_ratio": volume_ratio,
        "atr_pct": atr_pct,
        "close_location": close_location,
        "score": score,
        "matched_baseline": common,
        "combined_4pct_50pct": combined,
        "market_gate": market_gate,
    }


def safe_value(frame: pd.DataFrame, date: pd.Timestamp, symbol: str) -> float | None:
    value = frame.at[date, symbol]
    return float(value) if pd.notna(value) and float(value) > 0 else None


def trade_statistics(trades: pd.DataFrame) -> dict[str, float | int]:
    if trades.empty:
        return {
            "trade_count": 0,
            "win_rate": np.nan,
            "mean_trade_return": np.nan,
            "profit_factor": np.nan,
            "payoff_ratio": np.nan,
            "breakeven_win_rate": np.nan,
        }
    returns = pd.to_numeric(trades["return"], errors="coerce").dropna()
    pnl = pd.to_numeric(trades["pnl"], errors="coerce").dropna()
    wins = returns[returns > 0]
    losses = returns[returns <= 0]
    gross_profit = float(pnl[pnl > 0].sum())
    gross_loss = float(-pnl[pnl < 0].sum())
    average_win = float(wins.mean()) if not wins.empty else np.nan
    average_loss = float(-losses.mean()) if not losses.empty else np.nan
    payoff = average_win / average_loss if average_loss and np.isfinite(average_loss) else np.nan
    return {
        "trade_count": int(len(returns)),
        "win_rate": float((returns > 0).mean()) if not returns.empty else np.nan,
        "mean_trade_return": float(returns.mean()) if not returns.empty else np.nan,
        "profit_factor": gross_profit / gross_loss if gross_loss > 0 else np.inf,
        "payoff_ratio": payoff,
        "breakeven_win_rate": 1.0 / (1.0 + payoff) if np.isfinite(payoff) else np.nan,
    }


def portfolio_statistics(equity: pd.DataFrame, trades: pd.DataFrame) -> dict[str, float | int]:
    nav = equity["equity"]
    returns = nav.pct_change(fill_method=None).fillna(0.0)
    drawdown = nav / nav.cummax() - 1.0
    volatility = returns.std(ddof=0)
    return {
        "total_return": float(nav.iloc[-1] / nav.iloc[0] - 1.0),
        "max_drawdown": float(drawdown.min()),
        "sharpe": float(returns.mean() / volatility * np.sqrt(252)) if volatility > 0 else np.nan,
        "average_exposure": float(equity["exposure"].mean()),
        **trade_statistics(trades),
    }


def simulate_period(
    panels: dict[str, pd.DataFrame],
    features: dict[str, pd.DataFrame | pd.Series],
    stocks: list[str],
    variant: str,
    start: pd.Timestamp,
    end: pd.Timestamp,
    liquidate_final: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    dates = panels["close"].index[(panels["close"].index >= start) & (panels["close"].index <= end)]
    cash = INITIAL_NAV
    positions: dict[str, dict] = {}
    last_exit: dict[str, pd.Timestamp] = {}
    pending_entries: list[dict] = []
    pending_exits: set[str] = set()
    trades: list[dict] = []
    equity_rows: list[dict] = []
    last_prices: dict[str, float] = {}

    for date_number, date in enumerate(dates):
        open_ = panels["open"]
        close = panels["close"]
        low = panels["low"]

        still_pending: set[str] = set()
        for symbol in sorted(pending_exits):
            if symbol not in positions:
                continue
            price = safe_value(open_, date, symbol)
            if price is None:
                still_pending.add(symbol)
                continue
            position = positions.pop(symbol)
            fill = price * (1.0 - SLIPPAGE)
            proceeds = position["shares"] * fill - COMMISSION
            cash += proceeds
            pnl = proceeds - position["cost_basis"]
            trades[position["trade_index"]].update(
                {
                    "exit_date": str(date.date()),
                    "exit_price": fill,
                    "exit_reason": "signal",
                    "pnl": pnl,
                    "return": pnl / position["cost_basis"],
                }
            )
            last_exit[symbol] = date
        pending_exits = still_pending

        open_equity = cash + sum(
            position["shares"]
            * (safe_value(open_, date, symbol) or last_prices.get(symbol, position["entry_price"]))
            for symbol, position in positions.items()
        )
        stock_value = open_equity - cash
        for order in pending_entries:
            symbol = order["symbol"]
            if symbol in positions or len(positions) >= MAX_NAMES:
                continue
            price = safe_value(open_, date, symbol)
            if price is None:
                continue
            gap = price / order["signal_close"] - 1.0
            if gap > MAX_ENTRY_GAP:
                continue
            fill = price * (1.0 + SLIPPAGE)
            shares = math.floor(max(open_equity * TARGET_WEIGHT - COMMISSION, 0.0) / fill)
            if shares < 1 and fill + COMMISSION <= open_equity * SINGLE_MAX:
                shares = 1
            if shares < 1:
                continue
            notional = shares * fill
            if notional + COMMISSION > cash:
                continue
            if notional > open_equity * SINGLE_MAX + 1e-9:
                continue
            if stock_value + notional > open_equity * SLEEVE_MAX + 1e-9:
                continue
            cash -= notional + COMMISSION
            trade = {
                "variant": variant,
                "symbol": symbol,
                "signal_date": order["signal_date"],
                "entry_date": str(date.date()),
                "entry_price": fill,
                "shares": shares,
                "entry_gap": gap,
                "atr_pct_on_signal": order["atr_pct"],
                "close_location_on_signal": order["close_location"],
                "rs20_on_signal": order["rs20"],
                "volume_ratio_on_signal": order["volume_ratio"],
                "excluded_by_quality_pair": bool(
                    order["atr_pct"] > 0.04 or order["close_location"] < 0.50
                ),
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
                "stop": fill * (1.0 - STOP_LOSS),
                "entry_number": date_number,
                "trade_index": len(trades) - 1,
            }
            stock_value += notional
        pending_entries = []

        for symbol in list(positions):
            position = positions[symbol]
            day_open = safe_value(open_, date, symbol)
            day_low = safe_value(low, date, symbol)
            if day_open is None or day_low is None or day_low > position["stop"]:
                continue
            raw_fill = day_open if day_open <= position["stop"] else position["stop"]
            fill = raw_fill * (1.0 - SLIPPAGE)
            proceeds = position["shares"] * fill - COMMISSION
            cash += proceeds
            pnl = proceeds - position["cost_basis"]
            trades[position["trade_index"]].update(
                {
                    "exit_date": str(date.date()),
                    "exit_price": fill,
                    "exit_reason": "stop",
                    "pnl": pnl,
                    "return": pnl / position["cost_basis"],
                }
            )
            positions.pop(symbol)
            pending_exits.discard(symbol)
            last_exit[symbol] = date

        holdings_value = 0.0
        for symbol, position in positions.items():
            price = safe_value(close, date, symbol)
            if price is not None:
                last_prices[symbol] = price
            holdings_value += position["shares"] * last_prices.get(symbol, position["entry_price"])
        equity = cash + holdings_value
        equity_rows.append(
            {
                "date": date,
                "equity": equity,
                "exposure": holdings_value / equity if equity > 0 else 0.0,
            }
        )

        for symbol, position in positions.items():
            close_price = safe_value(close, date, symbol)
            ma20 = safe_value(features["ma20"], date, symbol)
            rs20 = features["rs20"].at[date, symbol]
            held = date_number - position["entry_number"]
            if close_price is not None and ma20 is not None and (
                close_price < ma20 or (pd.notna(rs20) and rs20 < 0.0) or held >= MAX_HOLD
            ):
                pending_exits.add(symbol)

        signal = features[variant].loc[date, stocks]
        candidates = [
            symbol
            for symbol in stocks
            if bool(signal[symbol])
            and symbol not in positions
            and (symbol not in last_exit or (date - last_exit[symbol]).days > 3)
        ]
        if candidates:
            score = features["score"].loc[date, candidates].sort_values(ascending=False)
            available = max(MAX_NAMES - len(positions), 0)
            for symbol in score.index[:available]:
                pending_entries.append(
                    {
                        "symbol": symbol,
                        "signal_date": str(date.date()),
                        "signal_close": float(close.at[date, symbol]),
                        "atr_pct": float(features["atr_pct"].at[date, symbol]),
                        "close_location": float(features["close_location"].at[date, symbol]),
                        "rs20": float(features["rs20"].at[date, symbol]),
                        "volume_ratio": float(features["volume_ratio"].at[date, symbol]),
                    }
                )

    if liquidate_final:
        final_date = dates[-1]
        for symbol, position in list(positions.items()):
            price = safe_value(panels["close"], final_date, symbol) or last_prices.get(symbol)
            if price is None:
                continue
            fill = price * (1.0 - SLIPPAGE)
            proceeds = position["shares"] * fill - COMMISSION
            cash += proceeds
            pnl = proceeds - position["cost_basis"]
            trades[position["trade_index"]].update(
                {
                    "exit_date": str(final_date.date()),
                    "exit_price": fill,
                    "exit_reason": "terminal",
                    "pnl": pnl,
                    "return": pnl / position["cost_basis"],
                }
            )
            positions.pop(symbol)
        if equity_rows:
            equity_rows[-1]["equity"] = cash
            equity_rows[-1]["exposure"] = 0.0
    return pd.DataFrame(equity_rows).set_index("date"), pd.DataFrame(trades)


def coverage_by_month(
    close: pd.DataFrame, members: pd.DataFrame, stocks: list[str]
) -> pd.DataFrame:
    monthly_dates = pd.Series(close.index, index=close.index).groupby(close.index.to_period("M")).max()
    rows = []
    for date in monthly_dates:
        active = members.loc[date, stocks]
        active_count = int(active.sum())
        covered = int((active & close.loc[date, stocks].notna()).sum())
        rows.append(
            {
                "date": date,
                "active_members": active_count,
                "covered_members": covered,
                "coverage": covered / active_count if active_count else np.nan,
            }
        )
    return pd.DataFrame(rows)


def period_coverage(coverage: pd.DataFrame) -> dict[str, float]:
    result = {}
    for period, (start, end) in PERIODS.items():
        sliced = coverage.loc[(coverage["date"] >= start) & (coverage["date"] <= end), "coverage"]
        result[period] = float(sliced.median())
    return result


def screen(metrics: pd.DataFrame, coverage: dict[str, float]) -> tuple[bool, list[dict]]:
    rows = []
    overall = True
    for period in ("validation_2020_2022", "final_2023_2025"):
        baseline = metrics.loc[
            (metrics["period"] == period) & (metrics["variant"] == "matched_baseline")
        ].iloc[0]
        candidate = metrics.loc[
            (metrics["period"] == period) & (metrics["variant"] == "combined_4pct_50pct")
        ].iloc[0]
        checks = {
            "coverage": bool(coverage[period] >= 0.70),
            "sample": bool(candidate.trade_count >= 20),
            "return": bool(candidate.total_return > baseline.total_return),
            "sharpe": bool(candidate.sharpe > baseline.sharpe),
            "drawdown": bool(candidate.max_drawdown >= baseline.max_drawdown),
            "win_rate": bool(candidate.win_rate >= baseline.win_rate),
            "expectancy": bool(candidate.mean_trade_return > 0.0),
        }
        passed = bool(all(checks.values()))
        overall = bool(overall and passed)
        rows.append({"period": period, **checks, "passed": passed})
    return overall, rows


def pct(value: float) -> str:
    return "n/a" if pd.isna(value) else f"{value:.2%}"


def num(value: float) -> str:
    return "n/a" if pd.isna(value) else f"{value:.2f}"


def write_report(
    metrics: pd.DataFrame,
    coverage: dict[str, float],
    excluded: pd.DataFrame,
    passed: bool,
    screen_rows: list[dict],
    manifest: dict,
) -> None:
    lines = [
        "# Point-in-time exact OHLCV filter audit",
        "",
        "## Bottom line",
        "",
        (
            "The frozen 4% ATR / 50% close-location pair **passed** the registered cross-period screen."
            if passed
            else "The frozen 4% ATR / 50% close-location pair **failed** the registered cross-period screen."
        ),
        "This is a broad point-in-time transferability audit, not a promotion of RSR1 and not an order authorization.",
        "",
        "## Data coverage",
        "",
        f"- Frozen stock symbols: {manifest['frozen_stock_symbols']}",
        f"- Usable OHLCV stock symbols: {manifest['usable_stock_symbols']}",
        f"- Provider failures: {len(manifest['failed_stock_symbols'])} ({', '.join(manifest['failed_stock_symbols']) or 'none'})",
    ]
    for period, value in coverage.items():
        lines.append(f"- Median active-membership coverage, {period}: {value:.1%}")
    lines.extend(
        [
            "",
            "## Portfolio results",
            "",
            "| Period | Variant | Return | Max DD | Sharpe | Win rate | Trades | Mean trade | PF | Payoff | Exposure |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in metrics.itertuples(index=False):
        lines.append(
            f"| {row.period} | {row.variant} | {pct(row.total_return)} | {pct(row.max_drawdown)} | "
            f"{num(row.sharpe)} | {pct(row.win_rate)} | {int(row.trade_count)} | "
            f"{pct(row.mean_trade_return)} | {num(row.profit_factor)} | {num(row.payoff_ratio)} | "
            f"{pct(row.average_exposure)} |"
        )
    lines.extend(
        [
            "",
            "## Registered screen",
            "",
            "| Period | Coverage | n>=20 | Return | Sharpe | DD | Win | Expectancy | Pass |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in screen_rows:
        yn = lambda value: "yes" if value else "no"
        lines.append(
            f"| {row['period']} | {yn(row['coverage'])} | {yn(row['sample'])} | {yn(row['return'])} | "
            f"{yn(row['sharpe'])} | {yn(row['drawdown'])} | {yn(row['win_rate'])} | "
            f"{yn(row['expectancy'])} | {yn(row['passed'])} |"
        )
    lines.extend(
        [
            "",
            "## Baseline trades removed by the quality pair",
            "",
            "| Period | Group | Trades | Win rate | Mean trade | Net PnL |",
            "| --- | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in excluded.itertuples(index=False):
        lines.append(
            f"| {row.period} | {row.group} | {int(row.trade_count)} | {pct(row.win_rate)} | "
            f"{pct(row.mean_trade_return)} | ${row.net_pnl:,.2f} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The experiment uses point-in-time membership but still lacks complete delisting returns and permanent identifiers. "
            "The universe is broader than the AI-capex sleeve, so it can test whether the quality pair transfers to another "
            "breakout population, not whether formal V9 should change. Development results cannot rescue either registered "
            "out-of-sample period. Formal V9, RSR1, RSR2, and the real account remain unchanged.",
        ]
    )
    (OUT_DIR / "pit_exact_filter_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    panels, membership, stocks = load_inputs()
    members = membership_mask(membership, panels["close"].index, stocks)
    features = build_features(panels, stocks, members)
    coverage_frame = coverage_by_month(panels["close"], members, stocks)
    coverage = period_coverage(coverage_frame)

    metric_rows = []
    trade_frames = []
    for period, (start, end) in PERIODS.items():
        for variant in ("matched_baseline", "combined_4pct_50pct"):
            equity, trades = simulate_period(panels, features, stocks, variant, start, end)
            trades["period"] = period
            trade_frames.append(trades)
            metric_rows.append(
                {"period": period, "variant": variant, **portfolio_statistics(equity, trades)}
            )
            equity.to_csv(OUT_DIR / f"pit_exact_filter_equity_{period}_{variant}.csv")
    metrics = pd.DataFrame(metric_rows)
    all_trades = pd.concat(trade_frames, ignore_index=True)

    baseline = all_trades.loc[all_trades["variant"] == "matched_baseline"].copy()
    baseline["group"] = np.where(
        baseline["excluded_by_quality_pair"], "excluded_by_pair", "passed_pair"
    )
    excluded_rows = []
    for (period, group), frame in baseline.groupby(["period", "group"]):
        stats = trade_statistics(frame)
        excluded_rows.append(
            {
                "period": period,
                "group": group,
                **stats,
                "net_pnl": float(pd.to_numeric(frame["pnl"], errors="coerce").sum()),
            }
        )
    excluded = pd.DataFrame(excluded_rows)
    passed, screen_rows = screen(metrics, coverage)
    manifest = json.loads((DATA_DIR / "manifest.json").read_text(encoding="utf-8"))

    metrics.to_csv(OUT_DIR / "pit_exact_filter_metrics.csv", index=False)
    all_trades.to_csv(OUT_DIR / "pit_exact_filter_trades.csv", index=False)
    excluded.to_csv(OUT_DIR / "pit_exact_filter_excluded_baseline.csv", index=False)
    coverage_frame.to_csv(OUT_DIR / "pit_exact_filter_coverage_by_month.csv", index=False)
    summary = {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "preregistration": "pit-exact-filter-preregistration.md",
        "transferability_screen_passed": passed,
        "coverage": coverage,
        "screen": screen_rows,
        "frozen_stock_symbols": manifest["frozen_stock_symbols"],
        "usable_stock_symbols": manifest["usable_stock_symbols"],
        "failed_stock_symbols": manifest["failed_stock_symbols"],
    }
    (OUT_DIR / "pit_exact_filter_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_report(metrics, coverage, excluded, passed, screen_rows, manifest)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
