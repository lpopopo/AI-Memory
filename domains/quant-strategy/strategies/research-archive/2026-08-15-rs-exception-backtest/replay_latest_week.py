#!/usr/bin/env python3
"""Research-only 2026-08-10..14 replay without modifying formal V9 caches."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import pandas as pd
import yfinance as yf


HERE = Path(__file__).resolve().parent
MODULE = runpy.run_path(str(HERE / "run_backtest.py"))
RESULTS = HERE / "results"
FIELDS = ("Open", "High", "Low", "Close", "Volume")
CBOE = {
    "^VIX": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv",
    "^VIX3M": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv",
}


def series(data: pd.DataFrame, field: str) -> pd.Series:
    selected = data[field]
    if isinstance(selected, pd.DataFrame):
        selected = selected.iloc[:, 0]
    selected.index = pd.to_datetime(selected.index).tz_localize(None)
    return pd.to_numeric(selected, errors="coerce").dropna()


def extend_panels():
    panels, symbols = MODULE["load_panels"]()
    required = sorted(set(symbols) | {"SPY", "QQQ", "SMH", "^VIX", "^VIX3M"})
    status = {}
    for symbol in required:
        if symbol in CBOE:
            continue
        try:
            data = yf.download(
                symbol, start="2026-08-07", end="2026-08-15", auto_adjust=True,
                progress=False, threads=False,
            )
            if data.empty:
                raise RuntimeError("empty download")
            for field in FIELDS:
                values = series(data, field)
                name = field.lower()
                index = panels[name].index.union(values.index)
                panels[name] = panels[name].reindex(index)
                panels[name].loc[values.index, symbol] = values
            status[symbol] = {"source": "Yahoo Finance via yfinance", "last_date": str(values.index[-1].date())}
        except Exception as error:
            status[symbol] = {"source": None, "error": str(error)}
    for symbol, url in CBOE.items():
        data = pd.read_csv(url)
        data.columns = [str(column).strip().upper() for column in data.columns]
        data.index = pd.to_datetime(data.pop("DATE"), errors="coerce")
        for field in ("OPEN", "HIGH", "LOW", "CLOSE"):
            values = pd.to_numeric(data[field], errors="coerce").dropna().loc[:"2026-08-14"]
            name = field.lower()
            index = panels[name].index.union(values.index)
            panels[name] = panels[name].reindex(index)
            panels[name].loc[values.index, symbol] = values
        status[symbol] = {"source": "Cboe official daily history", "last_date": str(values.index[-1].date())}
    equity_dates = panels["close"]["SPY"].dropna().index
    panels = {field: frame.reindex(equity_dates).sort_index() for field, frame in panels.items()}
    return panels, symbols, status


def candidate_rows(panels, symbols, config):
    features = MODULE["build_features"](panels, symbols, config)
    rows = []
    for date in panels["close"].loc["2026-08-10":"2026-08-14"].index:
        for symbol in symbols:
            strong = bool(features["signal"].at[date, symbol])
            repair = bool(features["repair_signal"].at[date, symbol])
            if not strong and not repair:
                continue
            rows.append({
                "date": str(date.date()),
                "symbol": symbol,
                "close": float(panels["close"].at[date, symbol]),
                "broad_healthy": bool(features["broad_healthy"].at[date]),
                "smh_healthy": bool(features["smh_healthy"].at[date]),
                "strong_breakout_signal": strong,
                "breadth_repair_signal": repair,
                "rs20": float(features["rs20"].at[date, symbol]),
                "rs10": float(features["rs10"].at[date, symbol]),
                "volume_ratio": float(features["volume_ratio"].at[date, symbol]),
                "atr_pct": float(features["atr_pct"].at[date, symbol]),
                "close_location": float(features["close_location"].at[date, symbol]),
                "breadth_score": float(features["breadth_score"].at[date, symbol]),
            })
    return rows


def main() -> None:
    panels, symbols, status = extend_panels()
    last_date = panels["close"].dropna(subset=["SPY", "QQQ", "SMH"]).index[-1]
    if str(last_date.date()) != "2026-08-14":
        raise RuntimeError(f"research replay stale at {last_date.date()}")
    default = MODULE["Config"]()
    risk = MODULE["Config"](
        rs20_min=0.03, volume_ratio_min=1.2, max_extension=0.12,
        max_hold_days=20, stop_loss=0.08, max_atr_pct=0.04,
        min_close_location=0.50,
    )
    runs = {}
    for label, config in (("default", default), ("risk_filter", risk)):
        for variant in ("strict_veto", "rs_exception", "breadth_exception"):
            result = MODULE["simulate"](
                panels, symbols, config, variant, "2026-01-01", "2026-08-14"
            )
            runs[f"{label}_{variant}"] = MODULE["compact"](result)
    candidates = {
        "default": candidate_rows(panels, symbols, default),
        "risk_filter": candidate_rows(panels, symbols, risk),
    }
    output = {
        "as_of": str(last_date.date()),
        "research_only": True,
        "formal_cache_modified": False,
        "authorizes_trade": False,
        "source_status": status,
        "runs": runs,
        "candidate_rows": candidates,
        "note": "The risk filter and exception hypotheses were defined after observing parts of this week; this is retrospective replay, not forward evidence.",
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "latest_week_replay.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = [
        "# Latest-Week Research Replay",
        "",
        f"- Completed through: `{last_date.date()}`",
        "- Formal V9 cache modified: `false`",
        "- Authorizes trade: `false`",
        "",
        "## Candidate signals",
        "",
        "| Config | Date | Symbol | Close | SMH healthy | Strong breakout | Breadth repair | RS20 | ATR% |",
        "| --- | --- | --- | ---: | --- | --- | --- | ---: | ---: |",
    ]
    for label, rows in candidates.items():
        for row in rows:
            lines.append(
                f"| {label} | {row['date']} | {row['symbol']} | {row['close']:.2f} | "
                f"{row['smh_healthy']} | {row['strong_breakout_signal']} | {row['breadth_repair_signal']} | "
                f"{row['rs20']:.2%} | {row['atr_pct']:.2%} |"
            )
    lines += [
        "",
        "This is a retrospective replay. A candidate row is not a live authorization; strict-veto entries still require SMH above MA50.",
    ]
    (RESULTS / "latest_week_replay.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"as_of": output["as_of"], "candidate_rows": candidates}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
