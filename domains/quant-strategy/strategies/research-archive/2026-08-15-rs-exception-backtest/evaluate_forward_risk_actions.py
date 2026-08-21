#!/usr/bin/env python3
"""Evaluate paper risk-review actions without inferring real orders."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
EVENTS_PATH = HERE / "forward_risk_action_events.csv"
DATA_DIR = HERE.parents[1] / "v9-execution" / "datasets" / "data_v9"
STATUS_PATH = RESULTS / "forward_shadow_status.json"
HORIZONS = (1, 5, 20)
POLICIES = ("full_exit", "half_exit")
SLIPPAGE = 0.001
COMMISSION = 1.0
OUTPUT_COLUMNS = [
    "trigger_date",
    "symbol",
    "review_state",
    "observation_class",
    "policy",
    "documented_shares",
    "action_shares",
    "execution_date",
    "raw_open",
    "net_sell_price",
    "horizon",
    "horizon_date",
    "horizon_close",
    "mature",
    "gross_benefit_vs_hold",
    "net_benefit_vs_hold",
    "beneficial",
    "real_order_assumed",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def truthy(value) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def load_panel(path: Path, as_of: pd.Timestamp) -> pd.DataFrame:
    panel = pd.read_csv(path, index_col=0, parse_dates=True).sort_index()
    panel.index = pd.DatetimeIndex(panel.index).normalize()
    return panel.loc[panel.index <= as_of].apply(pd.to_numeric, errors="coerce")


def validate_events(events: pd.DataFrame) -> pd.DataFrame:
    required = {
        "trigger_date",
        "symbol",
        "shares",
        "review_state",
        "observation_class",
        "real_order_assumed",
    }
    missing = required - set(events.columns)
    if missing:
        raise RuntimeError(f"risk-action event schema missing: {sorted(missing)}")
    data = events.copy()
    data["trigger_date"] = pd.to_datetime(data["trigger_date"], errors="raise").dt.normalize()
    data["shares"] = pd.to_numeric(data["shares"], errors="raise")
    if ((data["shares"] <= 0) | (data["shares"] % 1 != 0)).any():
        raise RuntimeError("documented shares must be positive integers")
    if data.duplicated(["trigger_date", "symbol"]).any():
        raise RuntimeError("duplicate trigger_date + symbol risk-action event")
    allowed = {"retrospective_seed", "genuine_forward"}
    unknown = set(data["observation_class"].astype(str)) - allowed
    if unknown:
        raise RuntimeError(f"unknown observation_class: {sorted(unknown)}")
    if data["real_order_assumed"].map(truthy).any():
        raise RuntimeError("risk-action ledger must never assume a real order")
    return data.sort_values(["trigger_date", "symbol"]).reset_index(drop=True)


def action_shares(shares: int, policy: str) -> int:
    if policy == "full_exit":
        return shares
    if policy == "half_exit":
        return math.floor(shares / 2)
    raise ValueError(f"unknown policy: {policy}")


def first_execution_date(
    trigger_date: pd.Timestamp, symbol: str, opens: pd.DataFrame, closes: pd.DataFrame
) -> pd.Timestamp | None:
    if symbol not in opens or symbol not in closes:
        return None
    valid = opens[symbol].notna() & closes[symbol].notna() & (opens.index > trigger_date)
    dates = opens.index[valid]
    return dates[0] if len(dates) else None


def fixed_horizon_point(
    execution_date: pd.Timestamp, symbol: str, closes: pd.DataFrame, horizon: int
) -> tuple[pd.Timestamp | None, float | None]:
    valid = closes.loc[closes.index >= execution_date, symbol].dropna()
    if len(valid) < horizon:
        return None, None
    date = valid.index[horizon - 1]
    return date, float(valid.iloc[horizon - 1])


def mark_point(symbol: str, closes: pd.DataFrame) -> tuple[pd.Timestamp | None, float | None]:
    if symbol not in closes:
        return None, None
    valid = closes[symbol].dropna()
    if valid.empty:
        return None, None
    return valid.index[-1], float(valid.iloc[-1])


def outcome_row(
    event: pd.Series,
    policy: str,
    execution_date: pd.Timestamp | None,
    raw_open: float | None,
    horizon,
    horizon_date: pd.Timestamp | None,
    horizon_close: float | None,
) -> dict:
    documented = int(event["shares"])
    shares = action_shares(documented, policy)
    mature = bool(
        execution_date is not None
        and raw_open is not None
        and shares > 0
        and horizon_date is not None
        and horizon_close is not None
    )
    net_sell_price = float(raw_open * (1 - SLIPPAGE)) if raw_open is not None else None
    gross = float(shares * (raw_open - horizon_close)) if mature else None
    net = float(shares * (net_sell_price - horizon_close) - COMMISSION) if mature else None
    return {
        "trigger_date": event["trigger_date"].strftime("%Y-%m-%d"),
        "symbol": str(event["symbol"]),
        "review_state": str(event["review_state"]),
        "observation_class": str(event["observation_class"]),
        "policy": policy,
        "documented_shares": documented,
        "action_shares": shares,
        "execution_date": execution_date.strftime("%Y-%m-%d") if execution_date is not None else None,
        "raw_open": raw_open,
        "net_sell_price": net_sell_price,
        "horizon": str(horizon),
        "horizon_date": horizon_date.strftime("%Y-%m-%d") if horizon_date is not None else None,
        "horizon_close": horizon_close,
        "mature": mature,
        "gross_benefit_vs_hold": gross,
        "net_benefit_vs_hold": net,
        "beneficial": bool(net > 0) if net is not None else None,
        "real_order_assumed": False,
    }


def evaluate_events(events: pd.DataFrame, opens: pd.DataFrame, closes: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for _, event in events.iterrows():
        symbol = str(event["symbol"])
        execution_date = first_execution_date(event["trigger_date"], symbol, opens, closes)
        raw_open = float(opens.at[execution_date, symbol]) if execution_date is not None else None
        for policy in POLICIES:
            for horizon in HORIZONS:
                date, close = (None, None)
                if execution_date is not None:
                    date, close = fixed_horizon_point(execution_date, symbol, closes, horizon)
                rows.append(outcome_row(event, policy, execution_date, raw_open, horizon, date, close))
            date, close = mark_point(symbol, closes)
            if execution_date is None or (date is not None and date < execution_date):
                date, close = None, None
            rows.append(outcome_row(event, policy, execution_date, raw_open, "as_of", date, close))
    return pd.DataFrame(rows).reindex(columns=OUTPUT_COLUMNS)


def summarize(outcomes: pd.DataFrame, observation_class: str, policy: str, horizon: str) -> dict:
    rows = outcomes.loc[
        outcomes["observation_class"].eq(observation_class)
        & outcomes["policy"].eq(policy)
        & outcomes["horizon"].eq(str(horizon))
    ]
    mature = rows.loc[rows["mature"]]
    if mature.empty:
        return {
            "eligible_events": int(len(rows)),
            "mature_events": 0,
            "beneficial_events": None,
            "beneficial_rate": None,
            "total_net_benefit": None,
            "average_net_benefit": None,
        }
    values = pd.to_numeric(mature["net_benefit_vs_hold"], errors="raise")
    beneficial = int((values > 0).sum())
    return {
        "eligible_events": int(len(rows)),
        "mature_events": int(len(mature)),
        "beneficial_events": beneficial,
        "beneficial_rate": float(beneficial / len(mature)),
        "total_net_benefit": float(values.sum()),
        "average_net_benefit": float(values.mean()),
    }


def build_summary(events: pd.DataFrame, outcomes: pd.DataFrame, as_of: str) -> dict:
    summaries = {}
    for sample in ("retrospective_seed", "genuine_forward"):
        summaries[sample] = {
            policy: {
                str(horizon): summarize(outcomes, sample, policy, str(horizon))
                for horizon in (*HORIZONS, "as_of")
            }
            for policy in POLICIES
        }
    return {
        "research_only": True,
        "formal_v9_modified": False,
        "real_account_modified": False,
        "live_order_authorization": False,
        "as_of": as_of,
        "costs": {"slippage_one_way": SLIPPAGE, "commission_per_paper_sale": COMMISSION},
        "event_counts": {
            "total": int(len(events)),
            "retrospective_seed": int(events["observation_class"].eq("retrospective_seed").sum()),
            "genuine_forward": int(events["observation_class"].eq("genuine_forward").sum()),
        },
        "summaries": summaries,
        "genuine_forward_policy_selection_available": False,
        "input_hashes": {
            "events": digest(EVENTS_PATH),
            "open": digest(DATA_DIR / "open.csv"),
            "close": digest(DATA_DIR / "close.csv"),
            "status": digest(STATUS_PATH),
        },
    }


def money(value) -> str:
    return "unavailable" if value is None else f"${value:.2f}"


def rate(value) -> str:
    return "unavailable" if value is None else f"{value:.2%}"


def write_report(summary: dict, outcomes: pd.DataFrame) -> None:
    seed = outcomes.loc[
        outcomes["observation_class"].eq("retrospective_seed")
        & outcomes["policy"].eq("full_exit")
        & outcomes["horizon"].isin(["1", "as_of"])
        & outcomes["mature"]
    ].copy()
    seed["label"] = seed["symbol"] + " / " + seed["horizon"].replace({"1": "1-session"})
    lines = [
        "# Forward risk-action counterfactual scorecard",
        "",
        "## Boundary",
        "",
        f"- Completed-close as of: `{summary['as_of']}`",
        f"- Retrospective seed / genuine-forward events: `{summary['event_counts']['retrospective_seed']} / {summary['event_counts']['genuine_forward']}`",
        "- Paper-only; no broker order, fill, strategy change, or automatic sale is assumed.",
        "- Sell costs: 10 bps adverse slippage plus USD 1 per paper sale.",
        "",
        "## Retrospective seed results",
        "",
        "| Event / horizon | Execution | Mark | Full-exit net benefit vs hold |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in seed.itertuples(index=False):
        lines.append(
            f"| {row.label} | {row.raw_open:.2f} on {row.execution_date} | {row.horizon_close:.2f} on {row.horizon_date} | {money(row.net_benefit_vs_hold)} |"
        )
    lines.extend(["", "| Policy / horizon | Mature | Beneficial | Rate | Total net benefit |", "| --- | ---: | ---: | ---: | ---: |"])
    for policy in POLICIES:
        for horizon in ("1", "as_of"):
            item = summary["summaries"]["retrospective_seed"][policy][horizon]
            beneficial = "unavailable" if item["beneficial_events"] is None else str(item["beneficial_events"])
            lines.append(
                f"| {policy} / {horizon} | {item['mature_events']} | {beneficial} | {rate(item['beneficial_rate'])} | {money(item['total_net_benefit'])} |"
            )
    lines.extend(
        [
            "",
            "The one-session seeds are mixed, and the current `as_of` mark is not a fixed horizon. Three observed events cannot select full reduction, half reduction, or a quality-class exception. Five- and twenty-session fields remain unavailable until mature.",
            "",
            "## Decision",
            "",
            "Keep measuring. Do not alter formal V9/RSR1/RSR2, the long-term reclassification, or the real account. A genuine-forward event must be frozen before its next-session open; retrospective seeds never count toward policy selection.",
        ]
    )
    (RESULTS / "forward_risk_action_counterfactual_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    status = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
    as_of = pd.Timestamp(status["as_of"]).normalize()
    events = validate_events(pd.read_csv(EVENTS_PATH))
    opens = load_panel(DATA_DIR / "open.csv", as_of)
    closes = load_panel(DATA_DIR / "close.csv", as_of)
    outcomes = evaluate_events(events, opens, closes)
    summary = build_summary(events, outcomes, as_of.strftime("%Y-%m-%d"))
    RESULTS.mkdir(exist_ok=True)
    outcomes.to_csv(RESULTS / "forward_risk_action_counterfactual.csv", index=False)
    (RESULTS / "forward_risk_action_counterfactual.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    write_report(summary, outcomes)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
