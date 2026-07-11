"""Momentum-factor induction + recent validation for SPY/QQQ.

Research-only. Does not change V8/V9 rules.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(r"D:\code\AI-Memory\domains\quant-strategy")
LONG = ROOT / "strategies/v9-execution/datasets/data_long"
V9 = ROOT / "strategies/v9-execution/datasets/data_v9/close.csv"
OUT = ROOT / "work/momentum_factor_induction_validation.json"


def load_long(sym: str) -> pd.Series:
    df = pd.read_csv(LONG / f"{sym}_adjusted_close.csv")
    df.columns = ["date", "close"]
    df["date"] = pd.to_datetime(df["date"])
    return df.set_index("date")["close"].sort_index()


def load_panel() -> pd.DataFrame:
    spy = load_long("SPY")
    qqq = load_long("QQQ")
    v9 = pd.read_csv(V9)
    v9["Date"] = pd.to_datetime(v9["Date"])
    v9 = v9.set_index("Date")[["SPY", "QQQ"]].sort_index()
    # Prefer v9 closes when overlapping (unadjusted/session close); extend history with long
    panel = pd.DataFrame({"SPY": spy, "QQQ": qqq})
    panel = panel.combine_first(v9)  # fill missing from v9? wrong direction
    # Better: start from long, update with v9 for overlapping dates
    panel = pd.DataFrame({"SPY": spy, "QQQ": qqq})
    for c in ["SPY", "QQQ"]:
        panel.loc[v9.index.intersection(panel.index), c] = v9.loc[v9.index.intersection(panel.index), c]
        # append v9-only dates
        extra = v9.index.difference(panel.index)
        if len(extra):
            panel = pd.concat([panel, v9.loc[extra, [c] if False else ["SPY", "QQQ"]]])
    panel = panel[~panel.index.duplicated(keep="last")].sort_index()
    panel = panel.dropna()
    return panel


def add_factors(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for sym in ["SPY", "QQQ"]:
        px = out[sym]
        out[f"{sym}_ma50"] = px.rolling(50).mean()
        out[f"{sym}_ma150"] = px.rolling(150).mean()
        out[f"{sym}_ma200"] = px.rolling(200).mean()
        out[f"{sym}_mom21"] = px.pct_change(21)
        out[f"{sym}_mom63"] = px.pct_change(63)
        out[f"{sym}_mom126"] = px.pct_change(126)
        out[f"{sym}_dd63"] = px / px.rolling(63).max() - 1
        out[f"{sym}_above_ma150"] = px > out[f"{sym}_ma150"]
        out[f"{sym}_above_ma200"] = px > out[f"{sym}_ma200"]
        # V8-like exposure score 0/0.5/1
        out[f"{sym}_v8_score"] = out[f"{sym}_above_ma150"].astype(float) * 0.5 + out[f"{sym}_above_ma200"].astype(float) * 0.5
        # Forward returns
        out[f"{sym}_fwd21"] = px.shift(-21) / px - 1
        out[f"{sym}_fwd63"] = px.shift(-63) / px - 1
    out["rel_mom21"] = out["QQQ_mom21"] - out["SPY_mom21"]
    out["rel_mom63"] = out["QQQ_mom63"] - out["SPY_mom63"]
    out["rel_fwd21"] = out["QQQ_fwd21"] - out["SPY_fwd21"]
    return out


def bucket_stats(s: pd.Series, y: pd.Series, q: int = 5) -> dict:
    d = pd.DataFrame({"x": s, "y": y}).dropna()
    if len(d) < 100:
        return {"n": int(len(d))}
    d["bucket"] = pd.qcut(d["x"], q, labels=False, duplicates="drop")
    g = d.groupby("bucket")["y"].agg(["count", "mean", "median"])
    return {
        "n": int(len(d)),
        "bucket_mean": [round(float(v) * 100, 2) for v in g["mean"].values],
        "bucket_n": [int(v) for v in g["count"].values],
        "spread_top_minus_bottom_pct": round(float(g["mean"].iloc[-1] - g["mean"].iloc[0]) * 100, 2),
        "corr": round(float(d["x"].corr(d["y"])), 3),
    }


def regime_forward(df: pd.DataFrame, sym: str, period: str = "full") -> dict:
    if period == "2026":
        d = df[df.index >= "2026-01-01"]
    elif period == "recent_2y":
        d = df[df.index >= "2024-01-01"]
    else:
        d = df
    rows = {}
    for name, mask in {
        "above_both": d[f"{sym}_above_ma150"] & d[f"{sym}_above_ma200"],
        "above_150_only": d[f"{sym}_above_ma150"] & ~d[f"{sym}_above_ma200"],
        "below_both": ~d[f"{sym}_above_ma150"] & ~d[f"{sym}_above_ma200"],
        "below_200": ~d[f"{sym}_above_ma200"],
    }.items():
        sub = d.loc[mask, [f"{sym}_fwd21", f"{sym}_fwd63", f"{sym}_dd63"]].dropna(how="all")
        rows[name] = {
            "n": int(len(sub)),
            "avg_fwd21_pct": round(float(sub[f"{sym}_fwd21"].mean()) * 100, 2) if sub[f"{sym}_fwd21"].notna().any() else None,
            "avg_fwd63_pct": round(float(sub[f"{sym}_fwd63"].mean()) * 100, 2) if sub[f"{sym}_fwd63"].notna().any() else None,
            "avg_dd63_pct": round(float(sub[f"{sym}_dd63"].mean()) * 100, 2) if sub[f"{sym}_dd63"].notna().any() else None,
            "pct_days": round(float(mask.mean()) * 100, 1) if len(d) else 0,
        }
    return rows


def validate_hypotheses(df: pd.DataFrame) -> list[dict]:
    """Induce factor claims on full sample, test on 2026 and 2024-2026."""
    full = df.dropna(subset=["SPY_mom63", "SPY_fwd21", "QQQ_mom63", "QQQ_fwd21"])
    y2026 = df[df.index >= "2026-01-01"]
    recent = df[df.index >= "2024-01-01"]

    hyps = []

    # H1: Trend momentum (above MA200) -> better next 63d than below
    for sym in ["SPY", "QQQ"]:
        for label, sample in [("full", full), ("2024_2026", recent), ("2026YTD", y2026)]:
            a = sample.loc[sample[f"{sym}_above_ma200"], f"{sym}_fwd63"].dropna()
            b = sample.loc[~sample[f"{sym}_above_ma200"], f"{sym}_fwd63"].dropna()
            if len(a) < 5 or len(b) < 5:
                support = "insufficient_n"
                spread = None
            else:
                spread = float(a.mean() - b.mean()) * 100
                support = spread > 0
            hyps.append(
                {
                    "id": f"H1_{sym}_MA200_fwd63",
                    "claim": f"{sym} above MA200 has higher avg next-63d return than below",
                    "sample": label,
                    "above_mean_pct": round(float(a.mean()) * 100, 2) if len(a) else None,
                    "below_mean_pct": round(float(b.mean()) * 100, 2) if len(b) else None,
                    "spread_pct": round(spread, 2) if spread is not None else None,
                    "n_above": int(len(a)),
                    "n_below": int(len(b)),
                    "supports": support,
                }
            )

    # H2: High 63d momentum predicts higher next 21d (continuation) — quintile spread
    for sym in ["SPY", "QQQ"]:
        for label, sample in [("full", full), ("2024_2026", recent), ("2026YTD", y2026)]:
            st = bucket_stats(sample[f"{sym}_mom63"], sample[f"{sym}_fwd21"])
            support = st.get("spread_top_minus_bottom_pct", 0) > 0 if "spread_top_minus_bottom_pct" in st else "insufficient_n"
            hyps.append(
                {
                    "id": f"H2_{sym}_mom63_fwd21",
                    "claim": f"{sym} high mom63 quintile beats low quintile over next 21d",
                    "sample": label,
                    "stats": st,
                    "supports": support,
                }
            )

    # H3: QQQ has higher beta/momentum amplification — |dd63| larger when SPY dd63 negative
    for label, sample in [("full", full), ("2024_2026", recent), ("2026YTD", y2026)]:
        m = sample[["SPY_dd63", "QQQ_dd63"]].dropna()
        stress = m[m["SPY_dd63"] < -0.05]
        if len(stress) < 5:
            support = "insufficient_n"
            amp = None
        else:
            amp = float((stress["QQQ_dd63"] / stress["SPY_dd63"]).median())
            support = amp > 1.0
        hyps.append(
            {
                "id": "H3_QQQ_amplifies_SPY_stress",
                "claim": "When SPY 63d DD < -5%, QQQ DD / SPY DD median > 1",
                "sample": label,
                "median_amplification": round(amp, 2) if amp is not None else None,
                "n_stress_days": int(len(stress)),
                "supports": support,
            }
        )

    # H4: Relative momentum continuation — high QQQ-SPY mom63 -> higher rel fwd21
    for label, sample in [("full", full), ("2024_2026", recent), ("2026YTD", y2026)]:
        st = bucket_stats(sample["rel_mom63"], sample["rel_fwd21"])
        support = st.get("spread_top_minus_bottom_pct", 0) > 0 if "spread_top_minus_bottom_pct" in st else "insufficient_n"
        hyps.append(
            {
                "id": "H4_rel_mom_continuation",
                "claim": "High QQQ-SPY relative mom63 associated with higher relative next-21d",
                "sample": label,
                "stats": st,
                "supports": support,
            }
        )

    # H5: Deep negative mom63 (<-10%) followed by worse fwd21 than mild (-5 to -8) while still above MA200
    for sym in ["SPY", "QQQ"]:
        for label, sample in [("full", full), ("2024_2026", recent), ("2026YTD", y2026)]:
            intact = sample[sample[f"{sym}_above_ma200"]]
            mild = intact[(intact[f"{sym}_dd63"] <= -0.05) & (intact[f"{sym}_dd63"] > -0.08)][f"{sym}_fwd21"].dropna()
            deep = intact[intact[f"{sym}_dd63"] <= -0.10][f"{sym}_fwd21"].dropna()
            # Also compare broken trend deep
            broken = sample[(~sample[f"{sym}_above_ma200"]) & (sample[f"{sym}_dd63"] <= -0.08)][f"{sym}_fwd21"].dropna()
            if len(mild) < 3 or len(deep) < 3:
                support = "insufficient_n"
            else:
                # claim: deep intact still recovers better than broken
                support = (float(deep.mean()) > float(broken.mean())) if len(broken) >= 3 else "insufficient_broken"
            hyps.append(
                {
                    "id": f"H5_{sym}_intact_vs_broken_after_stress",
                    "claim": f"{sym}: after stress, intact(MA200) deep-DD days have better next-21d than broken",
                    "sample": label,
                    "mild_intact_fwd21_pct": round(float(mild.mean()) * 100, 2) if len(mild) else None,
                    "deep_intact_fwd21_pct": round(float(deep.mean()) * 100, 2) if len(deep) else None,
                    "broken_fwd21_pct": round(float(broken.mean()) * 100, 2) if len(broken) else None,
                    "n_mild": int(len(mild)),
                    "n_deep": int(len(deep)),
                    "n_broken": int(len(broken)),
                    "supports": support,
                }
            )

    return hyps


def recent_snapshot(df: pd.DataFrame) -> dict:
    r = df.iloc[-1]
    # key dates
    dates = {
        "asof": str(df.index[-1].date()),
        "spy": round(float(r["SPY"]), 2),
        "qqq": round(float(r["QQQ"]), 2),
        "factors": {},
    }
    for sym in ["SPY", "QQQ"]:
        dates["factors"][sym] = {
            "mom21_pct": round(float(r[f"{sym}_mom21"]) * 100, 2),
            "mom63_pct": round(float(r[f"{sym}_mom63"]) * 100, 2),
            "mom126_pct": round(float(r[f"{sym}_mom126"]) * 100, 2),
            "dd63_pct": round(float(r[f"{sym}_dd63"]) * 100, 2),
            "above_ma150": bool(r[f"{sym}_above_ma150"]),
            "above_ma200": bool(r[f"{sym}_above_ma200"]),
            "v8_score": float(r[f"{sym}_v8_score"]),
            "ma150": round(float(r[f"{sym}_ma150"]), 2),
            "ma200": round(float(r[f"{sym}_ma200"]), 2),
        }
    dates["rel_mom21_pct"] = round(float(r["rel_mom21"]) * 100, 2)
    dates["rel_mom63_pct"] = round(float(r["rel_mom63"]) * 100, 2)

    # Episode snapshots
    episodes = {}
    for name, dt in [("pre_q1_peak", "2026-01-27"), ("q1_trough", "2026-03-30"), ("june_peak", "2026-06-02"), ("june_trough", "2026-06-10"), ("now", str(df.index[-1].date()))]:
        if pd.Timestamp(dt) in df.index:
            row = df.loc[pd.Timestamp(dt)]
        else:
            # nearest prior
            idx = df.index[df.index <= pd.Timestamp(dt)]
            if len(idx) == 0:
                continue
            row = df.loc[idx[-1]]
            dt = str(idx[-1].date())
        episodes[name] = {
            "date": dt,
            "SPY_mom63": round(float(row["SPY_mom63"]) * 100, 2),
            "QQQ_mom63": round(float(row["QQQ_mom63"]) * 100, 2),
            "SPY_dd63": round(float(row["SPY_dd63"]) * 100, 2),
            "QQQ_dd63": round(float(row["QQQ_dd63"]) * 100, 2),
            "rel_mom63": round(float(row["rel_mom63"]) * 100, 2),
            "SPY_above_ma200": bool(row["SPY_above_ma200"]),
            "QQQ_above_ma200": bool(row["QQQ_above_ma200"]),
            "SPY_v8": float(row["SPY_v8_score"]),
            "QQQ_v8": float(row["QQQ_v8_score"]),
        }
    dates["episodes"] = episodes
    return dates


def main():
    panel = load_panel()
    # Fix panel merge properly
    spy = load_long("SPY")
    qqq = load_long("QQQ")
    v9 = pd.read_csv(V9)
    v9["Date"] = pd.to_datetime(v9["Date"])
    v9 = v9.set_index("Date")[["SPY", "QQQ"]].sort_index()
    panel = pd.DataFrame({"SPY": spy, "QQQ": qqq}).sort_index()
    # overwrite overlapping with v9, append new
    panel.update(v9)
    panel = pd.concat([panel, v9.loc[v9.index.difference(panel.index)]]).sort_index()
    panel = panel[~panel.index.duplicated(keep="last")].dropna()

    df = add_factors(panel)
    # Use trading-day MAs from v9-aligned series for 2026 consistency: recompute MAs on full panel is fine

    out = {
        "range": [str(df.index.min().date()), str(df.index.max().date())],
        "factor_definitions": {
            "trend_momentum": "close > MA150 / MA200 (V8 half-weights)",
            "absolute_momentum": "21/63/126 trading-day returns",
            "drawdown_momentum": "close / 63d high - 1",
            "relative_momentum": "QQQ mom - SPY mom",
        },
        "regime_forward_full": {s: regime_forward(df, s, "full") for s in ["SPY", "QQQ"]},
        "regime_forward_2024_2026": {s: regime_forward(df, s, "recent_2y") for s in ["SPY", "QQQ"]},
        "regime_forward_2026": {s: regime_forward(df, s, "2026") for s in ["SPY", "QQQ"]},
        "hypotheses": validate_hypotheses(df),
        "snapshot": recent_snapshot(df),
    }

    # Summary counts
    hyps = out["hypotheses"]
    summary = {"by_sample": {}}
    for sample in ["full", "2024_2026", "2026YTD"]:
        subset = [h for h in hyps if h["sample"] == sample]
        bools = [h for h in subset if isinstance(h["supports"], bool)]
        summary["by_sample"][sample] = {
            "n": len(subset),
            "supported": sum(1 for h in bools if h["supports"]),
            "rejected": sum(1 for h in bools if h["supports"] is False),
            "insufficient": sum(1 for h in subset if h["supports"] == "insufficient_n" or str(h["supports"]).startswith("insufficient")),
        }
    out["summary"] = summary

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print("snapshot", json.dumps(out["snapshot"]["factors"], indent=2))
    print("episodes", json.dumps(out["snapshot"]["episodes"], indent=2))
    # print key hyps for 2026 and full H1 H3
    for h in hyps:
        if h["sample"] in ("full", "2026YTD") and h["id"].startswith(("H1_", "H3_", "H5_")):
            print(h["id"], h["sample"], "supports=", h["supports"], {k: h[k] for k in h if k not in ("claim", "id", "sample", "stats")})
    print("wrote", OUT)


if __name__ == "__main__":
    main()
