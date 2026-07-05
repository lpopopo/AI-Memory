#!/usr/bin/env python3
"""Export event lifecycles using only information completed by --as-of."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import pandas as pd

SCRIPTS = Path(__file__).resolve().parent
ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))
from validate_v9_information_strategy import load_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--account", default="v9_e")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--run-id", help="Required when exporting a namespaced engineering dry-run")
    args = parser.parse_args()
    as_of = pd.Timestamp(args.as_of)
    mode = "dry_run" if args.dry_run else "forward"
    base = ROOT / "results" / "shadow_portfolio" / mode
    if args.dry_run:
        if not args.run_id: raise ValueError("--run-id is required for dry-run lifecycle export")
        base = base / args.run_id
    decisions = base / "decisions" / args.account
    executions = base / "executions" / args.account
    state_path = base / "accounts" / args.account / f"{as_of.date()}_state.json"
    if not state_path.exists():
        raise FileNotFoundError(f"missing state for {args.account} on {as_of.date()}")
    state = json.loads(state_path.read_text(encoding="utf-8"))
    rows = {}

    def item(event_id, symbol):
        key = (event_id or "unknown", symbol)
        rows.setdefault(key, {"event_id": key[0], "symbol": symbol, "account": args.account, "status": "DISCOVERED", "first_route_date": None, "fill_date": None, "fill_price": None, "exit_date": None, "exit_price": None})
        return rows[key]

    for path in sorted(decisions.glob("*_close_decision.json")):
        date = pd.Timestamp(path.name[:10])
        if date > as_of:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for event in payload.get("funnel", []):
            event_id, symbol, reason = event.get("event_id"), event["symbol"], event["reason"]
            row = item(event_id, symbol)
            row["first_route_date"] = row["first_route_date"] or str(date.date())
            row["last_reason"] = reason
            if reason == "added_to_d1_waitlist": row["status"] = "ROUTED_D1_WAITING"
            elif reason == "added_to_d2_waitlist": row["status"] = "ROUTED_D2_WAITING"
            elif reason == "accepted": row["status"] = "ORDER_PENDING"
            elif reason.startswith("waitlist_expired"): row["status"] = "EXPIRED"
            elif reason == "waitlist_cancelled": row["status"] = "CANCELLED"
            elif row["status"] == "DISCOVERED": row["status"] = "REJECTED"

    for path in sorted(executions.glob("*_open_execution.json")):
        date = pd.Timestamp(path.name[:10])
        if date > as_of:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        for trade in payload.get("rows", []):
            if not trade.get("is_info"):
                continue
            row = item(trade.get("event_id"), trade["symbol"])
            if trade["action"] == "BUY":
                row.update({"status": "FILLED_OBSERVATION" if trade.get("is_observation") else "OFFICIAL", "fill_date": str(date.date()), "fill_price": float(trade["price"])})
            else:
                row.update({"status": "EXITED", "exit_date": str(date.date()), "exit_price": float(trade["price"])})

    for key_text in state.get("waitlist", {}):
        event_id, symbol = json.loads(key_text)
        row = item(event_id, symbol)
        if "WAITING" not in row["status"]: row["status"] = "WAITING"
    for symbol, position in state.get("positions", {}).items():
        row = item(position.get("event_id"), symbol)
        row["status"] = "FILLED_OBSERVATION" if position.get("is_observation") else "OFFICIAL"

    panels, _, _ = load_data()
    for row in rows.values():
        if not row["fill_date"] or row["symbol"] not in panels["close"]:
            continue
        dates = panels["close"].loc[row["fill_date"]:str(as_of.date())].index
        if len(dates) == 0:
            continue
        price = row["fill_price"]
        symbol = row["symbol"]
        row["completed_sessions"] = int(len(dates))
        row["mfe_as_of"] = float(panels["high"].loc[dates, symbol].max() / price - 1)
        row["mae_as_of"] = float(panels["low"].loc[dates, symbol].min() / price - 1)
        row["return_as_of"] = float(panels["close"].loc[dates[-1], symbol] / price - 1)
        if len(dates) >= 2: row["return_1d_completed"] = float(panels["close"].loc[dates[1], symbol] / price - 1)
        if len(dates) >= 6: row["return_5d_completed"] = float(panels["close"].loc[dates[5], symbol] / price - 1)

    output = sorted(rows.values(), key=lambda x: (x["first_route_date"] or "", x["event_id"], x["symbol"]))
    out_dir = base / "lifecycle" / args.account
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / f"{as_of.date()}_lifecycle.json"
    json_path.write_text(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
    csv_path = out_dir / f"{as_of.date()}_lifecycle.csv"
    fields = sorted({key for row in output for key in row})
    with csv_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(output)
    print(json.dumps({"rows": len(output), "json": str(json_path), "csv": str(csv_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
