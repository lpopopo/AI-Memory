"""Validate forecast patterns against 2026 YTD SPY/QQQ data."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(r"D:\code\AI-Memory\domains\quant-strategy")
CLOSE = ROOT / "strategies/v9-execution/datasets/data_v9/close.csv"
OUT = ROOT / "work/validate_2026_drawdown_patterns.json"


def find_events(df: pd.DataFrame, col: str, ma200_col: str, thr: float = -0.05, start: str = "2026-01-01"):
    px = df[col].values
    dates = df["Date"].values
    ma = df[ma200_col].values
    peak = px[0]
    start_i = 0
    peak_start = px[0]
    trough = px[0]
    trough_i = 0
    in_dd = False
    events = []
    start_ts = pd.Timestamp(start)

    def maybe_append(open_flag: bool = False):
        dd = trough / peak_start - 1
        if dd > thr:
            return
        peak_d = pd.Timestamp(dates[start_i])
        trough_d = pd.Timestamp(dates[trough_i])
        if not (peak_d >= start_ts or trough_d >= start_ts):
            return
        peak_above = bool(px[start_i] > ma[start_i]) if pd.notna(ma[start_i]) else None
        trough_above = bool(trough > ma[trough_i]) if pd.notna(ma[trough_i]) else None
        events.append(
            {
                "peak": str(peak_d.date()),
                "trough": str(trough_d.date()),
                "peak_px": round(float(peak_start), 2),
                "trough_px": round(float(trough), 2),
                "dd": round(float(dd) * 100, 2),
                "days": int((trough_d - peak_d).days),
                "peak_above_ma200": peak_above,
                "trough_above_ma200": trough_above,
                "intact": bool(peak_above and trough_above),
                "open": open_flag,
            }
        )

    for i in range(len(px)):
        if px[i] >= peak:
            if in_dd:
                maybe_append(False)
                in_dd = False
            peak = px[i]
            start_i = i
            peak_start = peak
            trough = px[i]
            trough_i = i
        else:
            if px[i] < trough:
                trough = px[i]
                trough_i = i
            if trough / peak_start - 1 <= thr:
                in_dd = True
    if in_dd:
        maybe_append(True)
    return events


def main():
    close = pd.read_csv(CLOSE)
    close["Date"] = pd.to_datetime(close["Date"])
    close = close.sort_values("Date").reset_index(drop=True)

    for sym in ["SPY", "QQQ"]:
        close[f"{sym}_ma50"] = close[sym].rolling(50).mean()
        close[f"{sym}_ma150"] = close[sym].rolling(150).mean()
        close[f"{sym}_ma200"] = close[sym].rolling(200).mean()
        close[f"{sym}_hi63"] = close[sym].rolling(63).max()
        close[f"{sym}_dd63"] = close[sym] / close[f"{sym}_hi63"] - 1

    y2026 = close[close["Date"] >= "2026-01-01"].copy()
    out: dict = {
        "range": [str(y2026.Date.min().date()), str(y2026.Date.max().date())],
        "n_days": int(len(y2026)),
        "ytd_return": {},
        "ytd_max_drawdown": {},
        "current_from_ytd_high": {},
        "ma200_breach_2026": {},
        "dd63_min_2026": {},
        "monthly_returns": {},
        "events": {},
        "pattern_checks": {},
    }

    for sym in ["SPY", "QQQ"]:
        s = y2026[sym]
        out["ytd_return"][sym] = round(float(s.iloc[-1] / s.iloc[0] - 1) * 100, 2)
        runmax = s.cummax()
        dd = s / runmax - 1
        mdd_i = dd.idxmin()
        peak_before = s.loc[:mdd_i].idxmax()
        out["ytd_max_drawdown"][sym] = {
            "dd_pct": round(float(dd.min()) * 100, 2),
            "peak_date": str(close.loc[peak_before, "Date"].date()),
            "peak_px": round(float(s.loc[peak_before]), 2),
            "trough_date": str(close.loc[mdd_i, "Date"].date()),
            "trough_px": round(float(s.loc[mdd_i]), 2),
            "days": int((close.loc[mdd_i, "Date"] - close.loc[peak_before, "Date"]).days),
            "peak_above_ma200": bool(s.loc[peak_before] > y2026.loc[peak_before, f"{sym}_ma200"]),
            "trough_above_ma200": bool(s.loc[mdd_i] > y2026.loc[mdd_i, f"{sym}_ma200"]),
        }
        last_peak = s.idxmax()
        out["current_from_ytd_high"][sym] = {
            "pct": round(float(s.iloc[-1] / s.max() - 1) * 100, 2),
            "high_px": round(float(s.max()), 2),
            "high_date": str(close.loc[last_peak, "Date"].date()),
        }

        below = y2026[sym] < y2026[f"{sym}_ma200"]
        if below.any():
            idxs = below[below].index
            deep_i = (y2026[sym] / y2026[f"{sym}_ma200"] - 1).idxmin()
            out["ma200_breach_2026"][sym] = {
                "days_below": int(below.sum()),
                "first": str(y2026.loc[idxs[0], "Date"].date()),
                "last": str(y2026.loc[idxs[-1], "Date"].date()),
                "min_vs_ma200_pct": round(float((y2026[sym] / y2026[f"{sym}_ma200"] - 1).min()) * 100, 2),
                "deepest_date": str(y2026.loc[deep_i, "Date"].date()),
                "deepest_px": round(float(y2026.loc[deep_i, sym]), 2),
            }
        else:
            out["ma200_breach_2026"][sym] = {"days_below": 0}

        ddi = y2026[f"{sym}_dd63"].idxmin()
        out["dd63_min_2026"][sym] = {
            "pct": round(float(y2026[f"{sym}_dd63"].min()) * 100, 2),
            "date": str(y2026.loc[ddi, "Date"].date()),
        }

        tmp = y2026.set_index("Date")[sym]
        months = tmp.resample("ME").agg(["first", "last"])
        months["ret"] = months["last"] / months["first"] - 1
        out["monthly_returns"][sym] = {
            str(d.date()): round(float(r) * 100, 2) for d, r in months["ret"].items()
        }

    for thr_name, thr in [("ge3", -0.03), ("ge5", -0.05), ("ge8", -0.08), ("ge12", -0.12), ("ge20", -0.20)]:
        out["events"][thr_name] = {
            "SPY": find_events(close, "SPY", "SPY_ma200", thr),
            "QQQ": find_events(close, "QQQ", "QQQ_ma200", thr),
        }

    # Pattern checks against revised note claims
    spy_mdd = out["ytd_max_drawdown"]["SPY"]
    qqq_mdd = out["ytd_max_drawdown"]["QQQ"]
    checks = []

    # 1) QQQ usually deeper than SPY in same regime
    checks.append(
        {
            "claim": "QQQ drawdown typically deeper than SPY",
            "2026_evidence": f"YTD max DD SPY {spy_mdd['dd_pct']}% vs QQQ {qqq_mdd['dd_pct']}%",
            "supports": qqq_mdd["dd_pct"] < spy_mdd["dd_pct"],
            "note": "direction only; one episode",
        }
    )

    # 2) Intact trend (peak+trough above MA200) shallow ~5.8/7.8
    intact_spy = spy_mdd["peak_above_ma200"] and spy_mdd["trough_above_ma200"]
    intact_qqq = qqq_mdd["peak_above_ma200"] and qqq_mdd["trough_above_ma200"]
    checks.append(
        {
            "claim": "If peak+trough stay above MA200, DD near historical intact medians (~-5.8% SPY / ~-7.8% QQQ)",
            "2026_evidence": {
                "SPY": {"intact": intact_spy, "dd": spy_mdd["dd_pct"], "hist_med": -5.83},
                "QQQ": {"intact": intact_qqq, "dd": qqq_mdd["dd_pct"], "hist_med": -7.75},
            },
            "supports": None,  # filled below
            "note": "Compare only if intact; else test broken-trend path",
        }
    )
    if intact_spy and intact_qqq:
        # both intact: did DD stay in shallow neighborhood (within ~1.5x median or <10/12)?
        checks[-1]["supports"] = (spy_mdd["dd_pct"] > -12) and (qqq_mdd["dd_pct"] > -15)
    elif (not intact_spy) or (not intact_qqq):
        checks[-1]["supports"] = "N/A_trend_broke"
        checks[-1]["note"] = "2026 YTD max DD involved MA200 break; intact-median claim not applicable to that episode"

    # 3) MA200 break coincides with deeper path
    spy_broke = out["ma200_breach_2026"]["SPY"].get("days_below", 0) > 0
    qqq_broke = out["ma200_breach_2026"]["QQQ"].get("days_below", 0) > 0
    checks.append(
        {
            "claim": "Completed MA200 break raises odds of deeper (>~10-15%) path",
            "2026_evidence": {
                "SPY_broke": spy_broke,
                "QQQ_broke": qqq_broke,
                "SPY_mdd": spy_mdd["dd_pct"],
                "QQQ_mdd": qqq_mdd["dd_pct"],
            },
            "supports": (spy_broke and spy_mdd["dd_pct"] <= -10) or (qqq_broke and qqq_mdd["dd_pct"] <= -12),
            "note": "One year cannot calibrate odds; checks co-occurrence only",
        }
    )

    # 4) >=8% catalog median is NOT a forecast of typical shallow pullback
    ge8 = out["events"]["ge8"]
    checks.append(
        {
            "claim": "Do not use >=8% catalog median as typical shallow-pullback depth",
            "2026_evidence": {
                "SPY_ge8_events": ge8["SPY"],
                "QQQ_ge8_events": ge8["QQQ"],
                "ytd_mdd": {"SPY": spy_mdd["dd_pct"], "QQQ": qqq_mdd["dd_pct"]},
            },
            "supports": True,
            "note": "Methodological; 2026 shows at least one >=8% episode when it occurred, but depth must be measured case-by-case",
        }
    )

    # 5) Duration: intact historical ~21-25 days; compare 2026 mdd duration
    checks.append(
        {
            "claim": "Intact-trend pullbacks often resolve in ~3-4 weeks (hist med 21.5/25 days)",
            "2026_evidence": {
                "SPY_days": spy_mdd["days"],
                "QQQ_days": qqq_mdd["days"],
                "intact_spy": intact_spy,
                "intact_qqq": intact_qqq,
            },
            "supports": None,
            "note": "If trend broke, duration claim for intact sample does not apply",
        }
    )
    if intact_spy and intact_qqq:
        checks[-1]["supports"] = (10 <= spy_mdd["days"] <= 45) and (10 <= qqq_mdd["days"] <= 45)
    else:
        checks[-1]["supports"] = "N/A_trend_broke"

    # 6) Arithmetic bands from 2026-07-10 forecast are forward-looking; backtest bands from peaks
    # Reconstruct: from Feb 2025 style - from actual 2026 peaks before major DD
    # Use peak of YTD max DD episode
    for sym, mdd, hist_med in [
        ("SPY", spy_mdd, -5.83),
        ("QQQ", qqq_mdd, -7.75),
    ]:
        peak = mdd["peak_px"]
        implied_med = peak * (1 + hist_med / 100)
        checks.append(
            {
                "claim": f"{sym}: historical intact median as descriptive level from episode peak",
                "2026_evidence": {
                    "peak": peak,
                    "implied_median_trough": round(implied_med, 2),
                    "actual_trough": mdd["trough_px"],
                    "actual_dd": mdd["dd_pct"],
                    "error_pct_points": round(mdd["dd_pct"] - hist_med, 2),
                },
                "supports": abs(mdd["dd_pct"] - hist_med) <= 5.0 if (mdd["peak_above_ma200"] and mdd["trough_above_ma200"]) else "N/A",
                "note": "Only meaningful if intact; otherwise expect larger miss",
            }
        )

    # 7) Count ge5 intact events entirely in 2026
    intact_2026 = {
        "SPY": [e for e in out["events"]["ge5"]["SPY"] if e["intact"] and e["peak"] >= "2026-01-01"],
        "QQQ": [e for e in out["events"]["ge5"]["QQQ"] if e["intact"] and e["peak"] >= "2026-01-01"],
    }
    out["intact_ge5_events_2026"] = intact_2026
    checks.append(
        {
            "claim": "2026 should contain some intact >=5% pullbacks near hist depth if trend mostly held",
            "2026_evidence": {
                "SPY_n": len(intact_2026["SPY"]),
                "QQQ_n": len(intact_2026["QQQ"]),
                "SPY_events": intact_2026["SPY"],
                "QQQ_events": intact_2026["QQQ"],
            },
            "supports": len(intact_2026["SPY"]) + len(intact_2026["QQQ"]) >= 1,
            "note": "Presence check, not probability calibration",
        }
    )

    out["pattern_checks"] = checks

    # Summary verdict
    bool_checks = [c for c in checks if isinstance(c["supports"], bool)]
    out["summary"] = {
        "n_boolean_checks": len(bool_checks),
        "n_supported": sum(1 for c in bool_checks if c["supports"]),
        "n_rejected": sum(1 for c in bool_checks if c["supports"] is False),
        "n_na": sum(1 for c in checks if c["supports"] == "N/A_trend_broke" or c["supports"] == "N/A"),
        "verdict": (
            "PARTIAL: directional/co-occurrence patterns show limited support in 2026, "
            "but one YTD sample cannot validate calibrated timing/depth forecasts; "
            "intact-median claims are N/A when the main episode broke MA200."
        ),
    }

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out["summary"], indent=2))
    print("YTD MDD", json.dumps(out["ytd_max_drawdown"], indent=2))
    print("MA200", json.dumps(out["ma200_breach_2026"], indent=2))
    print("ge5", json.dumps(out["events"]["ge5"], indent=2))
    print("ge8", json.dumps(out["events"]["ge8"], indent=2))
    print("intact", json.dumps(intact_2026, indent=2))
    for c in checks:
        print("---")
        print(c["claim"])
        print(" supports:", c["supports"])
        print(" evidence:", c["2026_evidence"])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
