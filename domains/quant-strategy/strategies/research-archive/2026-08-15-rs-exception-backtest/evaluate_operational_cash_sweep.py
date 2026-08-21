#!/usr/bin/env python3
"""Whole-share cash-sweep break-even analysis for the working real-account cash."""
from __future__ import annotations

import json
import math
from pathlib import Path

import pandas as pd


HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
WORKING_CASH = 3_756.49
WORKING_NAV = 5_751.77
COMMISSION_PER_SIDE = 1.0
RSR_TARGET_WEIGHT = 0.08
ALLOCATIONS = (0.25, 0.50, 0.75, 1.00)
HOLDING_DAYS = (7, 14, 30, 60, 90, 180, 365)
TAX_HAIRCUTS = (0.0, 0.15, 0.30)
FRICTION_SCENARIOS = {
    "quoted_spread_roundtrip_1bp": 0.0001,
    "strategy_stress_10bps_each_side": 0.0020,
}
INSTRUMENTS = {
    "SGOV": {
        "price": 100.56,
        "sec_yield": 0.0360,
        "expense_ratio": 0.0009,
        "median_spread": 0.0001,
        "yield_as_of": "2026-08-13",
        "price_as_of": "2026-08-14",
        "source": "https://www.ishares.com/us/products/overview-v3-ishares-fund-data?portfolioId=314116",
    },
    "BIL": {
        "price": 91.53,
        "sec_yield": 0.0357,
        "expense_ratio": 0.001353,
        "median_spread": 0.0001,
        "yield_as_of": "2026-08-13",
        "price_as_of": "2026-08-14",
        "source": "https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil",
    },
}


def whole_share_position(cash: float, allocation: float, price: float) -> dict:
    budget = cash * allocation
    shares = max(0, math.floor((budget - COMMISSION_PER_SIDE) / price))
    notional = shares * price
    immediate_cash = cash - notional - (COMMISSION_PER_SIDE if shares else 0.0)
    return {
        "budget": budget,
        "shares": shares,
        "notional": notional,
        "immediate_cash": immediate_cash,
        "deployed_pct_total_cash": notional / cash if cash else 0.0,
    }


def scenario_rows() -> pd.DataFrame:
    rows = []
    for ticker, instrument in INSTRUMENTS.items():
        for allocation in ALLOCATIONS:
            position = whole_share_position(WORKING_CASH, allocation, instrument["price"])
            for friction_name, roundtrip_friction in FRICTION_SCENARIOS.items():
                for tax_haircut in TAX_HAIRCUTS:
                    after_tax_yield = instrument["sec_yield"] * (1.0 - tax_haircut)
                    variable_cost = position["notional"] * roundtrip_friction
                    total_cost = variable_cost + (2 * COMMISSION_PER_SIDE if position["shares"] else 0.0)
                    daily_income = position["notional"] * after_tax_yield / 365.0
                    break_even = total_cost / daily_income if daily_income > 0 else None
                    for days in HOLDING_DAYS:
                        income = daily_income * days
                        rows.append(
                            {
                                "ticker": ticker,
                                "allocation": allocation,
                                **position,
                                "friction_scenario": friction_name,
                                "roundtrip_friction": roundtrip_friction,
                                "tax_haircut": tax_haircut,
                                "sec_yield": instrument["sec_yield"],
                                "after_tax_yield": after_tax_yield,
                                "holding_days": days,
                                "gross_after_tax_income": income,
                                "roundtrip_cost": total_cost,
                                "net_income": income - total_cost,
                                "break_even_days": break_even,
                            }
                        )
    return pd.DataFrame(rows)


def max_shares_with_rsr_buffer(price: float, entries: int) -> dict:
    required_cash = WORKING_NAV * RSR_TARGET_WEIGHT * entries + COMMISSION_PER_SIDE * entries
    shares = max(0, math.floor((WORKING_CASH - required_cash - COMMISSION_PER_SIDE) / price))
    notional = shares * price
    remaining = WORKING_CASH - notional - (COMMISSION_PER_SIDE if shares else 0.0)
    return {
        "rsr_entries_reserved": entries,
        "required_immediate_cash": required_cash,
        "max_sweep_shares": shares,
        "sweep_notional": notional,
        "remaining_cash": remaining,
        "sweep_pct_cash": notional / WORKING_CASH,
    }


def write_report(scenarios: pd.DataFrame, liquidity: pd.DataFrame, summary: dict) -> None:
    focus = scenarios.loc[
        scenarios["ticker"].eq("SGOV")
        & scenarios["allocation"].isin([0.50, 1.00])
        & scenarios["friction_scenario"].eq("strategy_stress_10bps_each_side")
        & scenarios["tax_haircut"].isin([0.0, 0.30])
        & scenarios["holding_days"].isin([30, 60, 90])
    ]
    lines = [
        "# Operational cash-sweep break-even audit",
        "",
        "## Current official inputs",
        "",
        "| Instrument | Price | 30-day SEC yield | Expense ratio | Median spread | Official date |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for ticker, item in INSTRUMENTS.items():
        lines.append(
            f"| {ticker} | ${item['price']:.2f} | {item['sec_yield']:.2%} | "
            f"{item['expense_ratio']:.4%} | {item['median_spread']:.2%} | yield {item['yield_as_of']}; price {item['price_as_of']} |"
        )
    lines.extend(
        [
            "",
            f"Working inputs: USD `{WORKING_CASH:,.2f}` cash, USD `{WORKING_NAV:,.2f}` NAV, USD `{COMMISSION_PER_SIDE:.2f}` commission per side, whole shares, and an 8% RSR target weight. SEC yield is already net of fund operating expenses but not investor-specific tax, brokerage or FX.",
            "",
            "## SGOV net-dollar focus",
            "",
            "| Cash allocation | Shares | Immediate cash | Tax haircut | Days | Income after haircut | Round-trip cost | Net income | Break-even |",
            "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in focus.itertuples(index=False):
        lines.append(
            f"| {row.allocation:.0%} | {row.shares} | ${row.immediate_cash:,.2f} | {row.tax_haircut:.0%} | "
            f"{row.holding_days} | ${row.gross_after_tax_income:,.2f} | ${row.roundtrip_cost:,.2f} | "
            f"${row.net_income:,.2f} | {row.break_even_days:.1f} days |"
        )
    lines.extend(
        [
            "",
            "## RSR liquidity reserve",
            "",
            "| Reserved future RSR entries | Required cash | Max SGOV shares | SGOV notional | Remaining cash | Sweep % of cash |",
            "| ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in liquidity.itertuples(index=False):
        lines.append(
            f"| {row.rsr_entries_reserved} | ${row.required_immediate_cash:,.2f} | {row.max_sweep_shares} | "
            f"${row.sweep_notional:,.2f} | ${row.remaining_cash:,.2f} | {row.sweep_pct_cash:.2%} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"- SGOV has a slightly higher SEC yield and lower expense ratio than BIL, but BIL's lower share price deploys nearly all of this small cash balance. At whole-share size their estimated annual pre-tax income is nearly identical: `${summary['sgov_full_annual_income']:.2f}` versus `${summary['bil_full_annual_income']:.2f}`.",
            f"- Under the conservative 10 bps-per-side stress plus commissions, a 50% SGOV tranche breaks even after `{summary['sgov_half_breakeven_pre_tax']:.1f}` days pre-tax and `{summary['sgov_half_breakeven_30tax']:.1f}` days with a 30% distribution haircut. A 30-day hold is not reliably economic under that stress.",
            f"- Reserving cash for all three possible 8% RSR positions permits at most `{summary['sgov_three_entry_shares']}` SGOV shares, or `{summary['sgov_three_entry_pct']:.2%}` of working cash. A simple 50% tranche leaves `${summary['sgov_half_immediate_cash']:.2f}` immediately available, more than the three-entry reserve.",
            "- Do not automate or treat SGOV/BIL as cash until the broker confirms USD settlement, sale-proceeds availability, distribution withholding/tax, commissions/platform fees and whether the account already pays interest on idle cash.",
            "",
            "Research-only. This audit authorizes no ETF order.",
        ]
    )
    (RESULTS / "operational_cash_sweep_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    scenarios = scenario_rows()
    liquidity = pd.DataFrame(max_shares_with_rsr_buffer(INSTRUMENTS["SGOV"]["price"], entries) for entries in (1, 2, 3))
    full_sgov = whole_share_position(WORKING_CASH, 1.0, INSTRUMENTS["SGOV"]["price"])
    full_bil = whole_share_position(WORKING_CASH, 1.0, INSTRUMENTS["BIL"]["price"])
    focus = scenarios.set_index(["ticker", "allocation", "friction_scenario", "tax_haircut", "holding_days"])
    half_position = whole_share_position(WORKING_CASH, 0.50, INSTRUMENTS["SGOV"]["price"])
    three = liquidity.set_index("rsr_entries_reserved").loc[3]
    summary = {
        "generated_at_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "working_cash": WORKING_CASH,
        "working_nav": WORKING_NAV,
        "research_only": True,
        "authorizes_trade": False,
        "sgov_full_shares": full_sgov["shares"],
        "bil_full_shares": full_bil["shares"],
        "sgov_full_annual_income": full_sgov["notional"] * INSTRUMENTS["SGOV"]["sec_yield"],
        "bil_full_annual_income": full_bil["notional"] * INSTRUMENTS["BIL"]["sec_yield"],
        "sgov_half_immediate_cash": half_position["immediate_cash"],
        "sgov_half_breakeven_pre_tax": float(focus.at[("SGOV", 0.50, "strategy_stress_10bps_each_side", 0.0, 30), "break_even_days"]),
        "sgov_half_breakeven_30tax": float(focus.at[("SGOV", 0.50, "strategy_stress_10bps_each_side", 0.30, 30), "break_even_days"]),
        "sgov_three_entry_shares": int(three["max_sweep_shares"]),
        "sgov_three_entry_pct": float(three["sweep_pct_cash"]),
        "decision": "operationally_conditional_no_order_until_broker_and_tax_facts",
    }
    scenarios.to_csv(RESULTS / "operational_cash_sweep_scenarios.csv", index=False)
    liquidity.to_csv(RESULTS / "operational_cash_sweep_liquidity.csv", index=False)
    (RESULTS / "operational_cash_sweep_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(scenarios, liquidity, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
