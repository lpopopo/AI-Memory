#!/usr/bin/env python3
"""Decompose the frozen RSR edge without searching any new parameter."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
RSR = runpy.run_path(str(HERE / "run_backtest.py"))
UNIVERSE = runpy.run_path(str(HERE / "evaluate_universe_scope.py"))
START = "2024-01-02"
END = "2026-08-18"


def trade_key(trade: dict) -> tuple[str, str]:
    return str(trade["symbol"]), str(trade["signal_date"])


def keyed(trades: list[dict]) -> dict[tuple[str, str], dict]:
    result = {trade_key(trade): trade for trade in trades}
    if len(result) != len(trades):
        raise RuntimeError("duplicate symbol/signal-date trade identity")
    return result


def economics(trades: list[dict]) -> dict:
    closed = [trade for trade in trades if trade.get("pnl") is not None]
    pnl = [float(trade["pnl"]) for trade in closed]
    returns = [float(trade["return"]) for trade in closed]
    gross_profit = sum(value for value in pnl if value > 0)
    gross_loss = -sum(value for value in pnl if value < 0)
    return {
        "trades": len(closed),
        "wins": sum(value > 0 for value in pnl),
        "losses": sum(value <= 0 for value in pnl),
        "win_rate": sum(value > 0 for value in pnl) / len(pnl) if pnl else None,
        "mean_return": sum(returns) / len(returns) if returns else None,
        "gross_profit": gross_profit,
        "gross_loss": gross_loss,
        "net_pnl": sum(pnl),
        "profit_factor": gross_profit / gross_loss if gross_loss else None,
    }


def winner_concentration(trades: list[dict]) -> dict:
    closed = [trade for trade in trades if trade.get("pnl") is not None]
    winners = sorted((trade for trade in closed if float(trade["pnl"]) > 0), key=lambda trade: float(trade["pnl"]), reverse=True)
    gross_profit = sum(float(trade["pnl"]) for trade in winners)
    net_pnl = sum(float(trade["pnl"]) for trade in closed)
    rows = []
    for count in (1, 2, 3):
        removed = sum(float(trade["pnl"]) for trade in winners[:count])
        rows.append(
            {
                "top_winners": count,
                "removed_pnl": removed,
                "share_of_gross_profit": removed / gross_profit if gross_profit else None,
                "share_of_net_pnl": removed / net_pnl if net_pnl else None,
                "leave_out_net_pnl": net_pnl - removed,
            }
        )
    return {
        "largest_winners": [
            {
                "rank": rank,
                "symbol": trade["symbol"],
                "signal_date": trade["signal_date"],
                "pnl": float(trade["pnl"]),
                "return": float(trade["return"]),
            }
            for rank, trade in enumerate(winners[:5], 1)
        ],
        "top_k": rows,
    }


def exclusion_reason(atr_pct: float, close_location: float) -> str:
    failures = []
    if atr_pct > 0.04:
        failures.append("atr_pct")
    if close_location < 0.50:
        failures.append("close_location")
    return "+".join(failures) if failures else "portfolio_path"


def direct_exit_effect(rsr1_trade: dict, rsr2_trade: dict) -> float:
    return float(
        int(rsr1_trade["shares"])
        * (float(rsr2_trade["exit_price"]) - float(rsr1_trade["exit_price"]))
    )


def evaluate() -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    panels, all_symbols = RSR["load_panels"]()
    universes, _ = UNIVERSE["universe_definitions"](all_symbols)
    symbols = universes["ai_capex_broad"]
    baseline_config = UNIVERSE["make_config"](False)
    rsr1_config = UNIVERSE["make_config"](True)
    baseline = RSR["simulate"](panels, symbols, baseline_config, "strict_veto", START, END)
    rsr1 = RSR["simulate"](panels, symbols, rsr1_config, "strict_veto", START, END)
    rsr2 = RSR["simulate"](
        panels,
        symbols,
        rsr1_config,
        "strict_veto",
        START,
        END,
        profit_lock_trigger=0.15,
        profit_lock_floor=0.05,
    )
    if any(trade.get("exit_reason") == "terminal" for result in (baseline, rsr1, rsr2) for trade in result["trades"]):
        raise RuntimeError("current-list decomposition must not contain terminal liquidations")

    features = RSR["build_features"](panels, symbols, baseline_config)
    baseline_map, rsr1_map, rsr2_map = map(keyed, (baseline["trades"], rsr1["trades"], rsr2["trades"]))
    common_keys = sorted(set(baseline_map) & set(rsr1_map))
    baseline_only_keys = sorted(set(baseline_map) - set(rsr1_map))
    rsr1_only_keys = sorted(set(rsr1_map) - set(baseline_map))
    attribution_rows = []
    for group, keys, source in (
        ("common", common_keys, baseline_map),
        ("baseline_only", baseline_only_keys, baseline_map),
        ("rsr1_only_replacement", rsr1_only_keys, rsr1_map),
    ):
        for key in keys:
            trade = source[key]
            date, symbol = pd.Timestamp(trade["signal_date"]), trade["symbol"]
            atr = float(features["atr_pct"].at[date, symbol])
            location = float(features["close_location"].at[date, symbol])
            reason = exclusion_reason(atr, location) if group == "baseline_only" else None
            attribution_rows.append(
                {
                    "group": group,
                    "reason": reason,
                    "symbol": symbol,
                    "signal_date": trade["signal_date"],
                    "entry_date": trade["entry_date"],
                    "exit_date": trade["exit_date"],
                    "exit_reason": trade["exit_reason"],
                    "atr_pct": atr,
                    "close_location": location,
                    "pnl": float(trade["pnl"]),
                    "return": float(trade["return"]),
                }
            )
    attribution = pd.DataFrame(attribution_rows)

    direct = attribution.loc[
        attribution["group"].eq("baseline_only") & attribution["reason"].ne("portfolio_path")
    ]
    direct_losers = direct.loc[direct["pnl"] <= 0]
    direct_winners = direct.loc[direct["pnl"] > 0]

    overlay_keys = sorted(set(rsr1_map) & set(rsr2_map))
    delta_rows = []
    for key in overlay_keys:
        left, right = rsr1_map[key], rsr2_map[key]
        delta_rows.append(
            {
                "symbol": key[0],
                "signal_date": key[1],
                "rsr1_entry_date": left["entry_date"],
                "rsr2_entry_date": right["entry_date"],
                "rsr1_exit_date": left["exit_date"],
                "rsr2_exit_date": right["exit_date"],
                "rsr1_exit_reason": left["exit_reason"],
                "rsr2_exit_reason": right["exit_reason"],
                "rsr1_shares": int(left["shares"]),
                "rsr2_shares": int(right["shares"]),
                "rsr1_pnl": float(left["pnl"]),
                "rsr2_pnl": float(right["pnl"]),
                "pnl_delta": float(right["pnl"] - left["pnl"]),
                "direct_exit_effect_on_rsr1_shares": direct_exit_effect(left, right),
                "profit_lock_activated": bool(right.get("profit_lock_date")),
            }
        )
    deltas = pd.DataFrame(delta_rows).sort_values("pnl_delta", ascending=False)
    deltas["capital_path_and_sizing_residual"] = (
        deltas["pnl_delta"] - deltas["direct_exit_effect_on_rsr1_shares"]
    )
    total_delta = float(deltas["pnl_delta"].sum())
    direct_delta = float(deltas["direct_exit_effect_on_rsr1_shares"].sum())
    residual_delta = float(deltas["capital_path_and_sizing_residual"].sum())
    positive = deltas.loc[deltas["pnl_delta"] > 1e-9, "pnl_delta"].sort_values(ascending=False)

    group_summary = {}
    for group in ("common", "baseline_only", "rsr1_only_replacement"):
        rows = attribution.loc[attribution["group"].eq(group)].to_dict("records")
        group_summary[group] = economics(rows)
    summary = {
        "research_only": True,
        "formal_v9_modified": False,
        "live_authorization": False,
        "period": [START, END],
        "universe": "ai_capex_broad",
        "symbols": len(symbols),
        "cost_model": {"initial_nav": 6000.0, "commission": 1.0, "slippage_per_side": 0.001},
        "variant_economics": {
            "matched_baseline": economics(baseline["trades"]),
            "RSR1-shadow": economics(rsr1["trades"]),
            "RSR2-profit-lock-shadow": economics(rsr2["trades"]),
        },
        "path_groups": group_summary,
        "direct_quality_exclusions": {
            "trades": int(len(direct)),
            "avoided_losing_trades": int(len(direct_losers)),
            "avoided_loss_dollars": float(-direct_losers["pnl"].sum()),
            "missed_winning_trades": int(len(direct_winners)),
            "missed_profit_dollars": float(direct_winners["pnl"].sum()),
            "net_pnl_removed": float(direct["pnl"].sum()),
            "win_rate": float((direct["pnl"] > 0).mean()) if len(direct) else None,
            "mean_return": float(direct["return"].mean()) if len(direct) else None,
            "by_reason": {
                reason: economics(group.to_dict("records"))
                for reason, group in direct.groupby("reason")
            },
        },
        "winner_concentration": {
            "RSR1-shadow": winner_concentration(rsr1["trades"]),
            "RSR2-profit-lock-shadow": winner_concentration(rsr2["trades"]),
        },
        "profit_lock_attribution": {
            "paired_trades": int(len(deltas)),
            "improved": int((deltas["pnl_delta"] > 1e-9).sum()),
            "worsened": int((deltas["pnl_delta"] < -1e-9).sum()),
            "unchanged": int((deltas["pnl_delta"].abs() <= 1e-9).sum()),
            "aggregate_pnl_delta": total_delta,
            "aggregate_direct_exit_effect": direct_delta,
            "aggregate_capital_path_and_sizing_residual": residual_delta,
            "direct_exit_effect_share": direct_delta / total_delta if total_delta else None,
            "capital_path_and_sizing_share": residual_delta / total_delta if total_delta else None,
            "trades_with_nonzero_direct_exit_effect": int(
                (deltas["direct_exit_effect_on_rsr1_shares"].abs() > 1e-9).sum()
            ),
            "largest_positive_delta_share": float(positive.iloc[:1].sum() / total_delta) if total_delta else None,
            "two_largest_positive_delta_share": float(positive.iloc[:2].sum() / total_delta) if total_delta else None,
            "lock_activations": int(deltas["profit_lock_activated"].sum()),
            "profit_lock_exits": int(deltas["rsr2_exit_reason"].eq("profit_lock").sum()),
        },
        "decision": "diagnostic_only_keep_frozen_forward_rules",
    }
    return summary, attribution, deltas


def pct(value) -> str:
    return "n/a" if value is None else f"{value:.2%}"


def write_report(summary: dict) -> None:
    direct = summary["direct_quality_exclusions"]
    overlay = summary["profit_lock_attribution"]
    lines = [
        "# Economic edge and opportunity-cost decomposition",
        "",
        "## Bottom line",
        "",
        "The historical RSR1 edge is primarily an avoided-loss effect, but it also rejects profitable trades. RSR2's incremental benefit is sparse and must not be treated as a broad improvement until forward protected exits accumulate.",
        "",
        "## Variant economics",
        "",
        "| Variant | Trades | Win rate | Gross profit | Gross loss | Net P&L | PF |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name, row in summary["variant_economics"].items():
        profit_factor = "n/a" if row["profit_factor"] is None else f"{row['profit_factor']:.2f}"
        lines.append(
            f"| {name} | {row['trades']} | {pct(row['win_rate'])} | ${row['gross_profit']:.2f} | "
            f"${row['gross_loss']:.2f} | ${row['net_pnl']:.2f} | "
            f"{profit_factor} |"
        )
    lines.extend(
        [
            "",
            "## Direct quality-filter exclusions",
            "",
            f"- Directly excluded trades: {direct['trades']}",
            f"- Avoided losers: {direct['avoided_losing_trades']}, historical losses avoided ${direct['avoided_loss_dollars']:.2f}",
            f"- Missed winners: {direct['missed_winning_trades']}, historical profit missed ${direct['missed_profit_dollars']:.2f}",
            f"- Net P&L removed from the baseline path: ${direct['net_pnl_removed']:.2f}",
            f"- Excluded-trade win rate / mean return: {pct(direct['win_rate'])} / {pct(direct['mean_return'])}",
            "",
            "Avoided losses are not earned profit, and RSR1-only replacements remain path-dependent. This decomposition cannot be converted into a new threshold.",
            "",
            "## Winner concentration",
            "",
            "| Variant | Top winners removed | Share gross profit | Share net P&L | Remaining net P&L |",
            "| --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for variant, block in summary["winner_concentration"].items():
        for row in block["top_k"]:
            lines.append(
                f"| {variant} | {row['top_winners']} | {pct(row['share_of_gross_profit'])} | "
                f"{pct(row['share_of_net_pnl'])} | ${row['leave_out_net_pnl']:.2f} |"
            )
    lines.extend(
        [
            "",
            "## RSR2 incremental attribution",
            "",
            f"- Paired trades: {overlay['paired_trades']}",
            f"- Improved / worsened / unchanged: {overlay['improved']} / {overlay['worsened']} / {overlay['unchanged']}",
            f"- Aggregate P&L delta versus RSR1: ${overlay['aggregate_pnl_delta']:.2f}",
            f"- Direct exit effect on frozen RSR1 shares: ${overlay['aggregate_direct_exit_effect']:.2f} ({pct(overlay['direct_exit_effect_share'])})",
            f"- Capital-path and whole-share sizing residual: ${overlay['aggregate_capital_path_and_sizing_residual']:.2f} ({pct(overlay['capital_path_and_sizing_share'])})",
            f"- Trades with a nonzero direct exit effect: {overlay['trades_with_nonzero_direct_exit_effect']}",
            f"- Largest positive delta share: {pct(overlay['largest_positive_delta_share'])}",
            f"- Two largest positive deltas share: {pct(overlay['two_largest_positive_delta_share'])}",
            f"- Profit-lock activations / exits: {overlay['lock_activations']} / {overlay['profit_lock_exits']}",
            "",
            "## Decision",
            "",
            "Keep RSR1 and RSR2 unchanged as separate forward shadows. Forward reviews must report avoided-loss behavior and missed-winner opportunity cost together, and must identify whether RSR2 improvement remains concentrated in one or two protected exits. No order is authorized.",
        ]
    )
    (RESULTS / "economic_edge_decomposition_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    summary, attribution, deltas = evaluate()
    (RESULTS / "economic_edge_decomposition_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    attribution.to_csv(RESULTS / "economic_edge_trade_attribution.csv", index=False)
    deltas.to_csv(RESULTS / "economic_edge_profit_lock_deltas.csv", index=False)
    write_report(summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
