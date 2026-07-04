# 2026-06-29 Portfolio Summary

Run time: 2026-06-29 23:19 Asia/Shanghai.
Scope: U.S. intraday real-account estimate. This is not a broker statement and not a completed-close audit.

## Confirmed holdings baseline

Latest confirmed real-account holdings from memory remain GLW `2`, TTMI `3`, DRAM `4`, MXL `6`, and MU `1`. No new real fill or sale was confirmed during this automation run.

Important caveat: DRAM traded below the stated `70.50` intraday protective trigger, and MU traded below the optional `1090` hard-protection reference. If those broker-side stop orders were active, the real account may differ from the estimate below. Do not record an actual sale until the user or broker confirms it.

## Intraday estimate if all holdings are still open

| Ticker | Shares | Cost basis | Intraday price | Market value | Gross unrealized P/L | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 181.50 | 239.08 | 478.16 | +115.16 | `core hold` |
| TTMI | 3 | 213.00 | 181.61 | 544.83 | -94.17 | `exit-review intraday / not formal close` |
| DRAM | 4 | 76.43 | 68.45 | 273.80 | -31.92 | `exit-confirmation-needed` |
| MXL | 6 | 90.70 | 101.21 | 607.26 | +63.06 | `core/reclassified hold pending post-close` |
| MU | 1 | 1155.00 | 1068.68 | 1068.68 | -86.32 | `core defensive hold / close-risk review` |

## Account metrics

| Metric | Value |
| --- | ---: |
| Working cash placeholder | USD 3,368.64 |
| Equity market value if all positions still held | USD 2,972.73 |
| Estimated NAV if all positions still held | USD 6,341.37 |
| Change vs USD 6,410.26 baseline | -USD 68.89 / -1.07% |
| Cash / equity exposure | 53.12% / 46.88% |
| Largest position | MU, 16.85% |
| Active holdings / effective theme | 5 / one broad AI-capex chain |
| Optical/interconnect sleeve | GLW + TTMI + MXL = USD 1,630.25 / 25.71% |
| Memory sleeve | DRAM + MU = USD 1,342.48 / 21.17% |

Exact cash, fees, FX, taxes, settlement, open orders, stop fills and NAV require user or broker confirmation.

## Risk state

```text
data_time: 2026-06-29 23:19 Asia/Shanghai
equity_source: Tencent (Primary) structured quote objects
volatility_source: Yahoo Chart direct via local StockService._requestJson
data_quality: high usable intraday equities/ETFs; low-quality Tencent VIX ignored; usable Yahoo VIX/VIX3M
session_context: U.S. regular session intraday; not formal close
provisional_fear_regime: normal-to-elevated boundary, about 3/14
cash_floor: formal floor not binding if positions still held
operational_new_buy_cap: 0% due to unresolved stops and theme concentration
flow_fragility: elevated
trend_aligned_entry: trend_broken for new correlated-theme entries
flags: theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high;
  memory_concentration_high; semiconductor_intraday_shakeout; stop_confirmation_gap
```

## Holding controls

- GLW: intraday `239.08`, above `210`; hold/no add.
- TTMI: intraday `181.61`, below both `200` and `188`; because the rule is completed-close based, mark `exit-review intraday` and defer formal trigger to post-close audit.
- DRAM: intraday `68.45`, low `66.47`, below the `70.50` protective trigger; urgently confirm whether broker stop-market order executed.
- MXL: intraday `101.21`, above old `86` and suggested `91-92` upgraded core-style protection; hold/no add.
- MU: intraday `1068.68`, below `1100`; if `1090` hard stop existed, confirm whether it executed. Otherwise formal close below `1100` requires risk review.
- MRVL/AMD/WDC/STX are replay/watch context only, not real holdings.

Not investment advice.
