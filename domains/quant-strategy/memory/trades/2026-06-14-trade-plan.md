# 2026-06-14 Trade Plan

Run time: 2026-06-14 05:52 Asia/Shanghai.

Scope: daily U.S. stock execution preparation and portfolio accounting. This is a weekend / premarket preparation note, not a broker instruction and not the formal 04:15 post-close audit. Do not log in to a broker, do not submit real orders, and do not treat replay figures as real holdings.

## Account and Execution Boundary

| Category | Status |
| --- | --- |
| Confirmed real-account equity holdings | None |
| Latest confirmed real trade | `MRVL` 1 share bought at `USD 252.00`, sold at `USD 267.020`; gross realized P/L about `USD +15.020` / `+5.96%`, before fees and FX |
| New real trades today | None |
| Pending user-confirmed orders | None ready for submission |
| Model / replay simulated trades today | None |
| Broker cash / fees / FX / tax | Unconfirmed by user or broker |

## Data Quality

| Data | Time | Source | Quality | Gap |
| --- | --- | --- | --- | --- |
| Stock / ETF quotes | Latest available 2026-06-12 U.S. regular-session close; local run 2026-06-14 05:52 Asia/Shanghai | Local Node and bundled Python quote clients, `Tencent (Primary)` / `Tencent` | Medium-high for equities and ETFs; both local paths returned non-empty normalized quote objects | Weekend data, not live Sunday trading |
| Broad index close | 2026-06-12 close | AP / MarketWatch public market reports | High for index direction and major closes | ETF and index values differ by instrument, use labels precisely |
| VIX | 2026-06-12 close | Cboe / MarketWatch / Yahoo / Investing.com public pages | High for VIX close `17.68` | Local Tencent VIX returned stale-looking `21.67` with zero OHLC; VIX/VIX3M term structure still unavailable |
| Real-account cash / open orders | Current | User / broker confirmation required | Unavailable | Do not record broker-side cash, fees, FX, tax, margin, or old orders without confirmation |
| Same-day daily strategy report / 20:30 monitor | 2026-06-14 | Local memory search | Missing | Latest usable daily strategy and monitor products remain 2026-06-12 |

Key local quote snapshots:

| Ticker | Reference price | Change | Open | High | Low | Volume | Execution-prep status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| MRVL | 279.70 | -0.36% | 270.07 | 287.98 | 267.31 | 42,162,220 | `watch only / no chase` |
| AMD | 511.57 | +4.73% | 499.69 | 521.71 | 494.00 | 31,618,462 | historical replay: repair confirmed above `492`; real account: watch only |
| WDC | 562.93 | +6.35% | 541.99 | 572.29 | 531.96 | 6,291,421 | historical replay: defensive hold / repair confirmed |
| STX | 931.04 | +7.25% | 880.19 | 946.24 | 868.14 | 3,194,682 | historical replay: defensive hold / repair confirmed |
| SPY | 741.75 | +0.54% | 740.71 | 744.44 | 735.03 | 57,079,533 | broad repair |
| QQQ | 721.34 | +0.59% | 717.61 | 724.01 | 711.28 | 51,236,021 | growth repair |
| SMH | 619.96 | +1.72% | 607.95 | 624.62 | 602.21 | 8,986,716 | semiconductor repair, still high beta |
| HYG | 79.94 | 0.00% | 79.94 | 80.00 | 79.80 | 29,873,323 | credit proxy neutral |
| LQD | 109.01 | -0.06% | 108.88 | 109.07 | 108.64 | 23,422,978 | investment-grade credit/rate proxy slightly soft |
| IWM | 292.95 | +0.87% | 291.63 | 295.72 | 290.31 | 34,415,247 | breadth repair |
| RSP | 211.65 | +0.91% | 210.70 | 212.12 | 209.65 | 11,412,467 | equal-weight repair |

## Market Gate

```text
market_regime: elevated / repair watch
fear_score: 4-5 / 14
risk_multiplier: about 70%-80%
real_account_equity_exposure: 0% confirmed
new_buy_permission: no immediate buy; only conditional watch items after trend-aligned entry and user confirmation
cash_target: real account remains no confirmed equity holdings; historical replay cash remains a diagnostic only
```

The risk state improved because the S&P 500, Nasdaq, Russell 2000, semiconductors, equal-weight proxy, and credit proxies repaired into the 2026-06-12 close, and VIX closed below 20 at `17.68`. It is still not a clean `normal` downgrade because VIX/VIX3M is missing, AI/semiconductor/storage remains high-beta and crowded, and this run occurs on a weekend with no new trading tape.

## Institutional Overlay Summary

```text
flow_fragility_state: medium / elevated watch
flow_fragility_score: 6/14
trend_aligned_entry_state: cheap_but_unconfirmed for new real-account buys; repair_confirmed for historical AMD/WDC/STX risk labels
AI_quality/capex_cycle: MRVL/AMD/WDC/STX remain high capex-cycle sensitive; new exposure still needs evidence of trend, revenue/cash-flow quality, and technical entry basis
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high for historical replay basket; token_cost_elasticity; VIX_term_structure_data_gap
action_impact: no chase buys; no immediate real order; keep cash until a fresh setup passes trend-aligned entry
```

## Holding and Watch Labels

Real account has no confirmed equity holding. AMD/WDC/STX labels below apply only to historical replay / watchlist risk language, not to real-account positions.

| Ticker | Account scope | Current label | Reference price | Trigger / stop line | Judgment |
| --- | --- | --- | ---: | --- | --- |
| MRVL | Real account is flat; model/watch only | `watch only / no chase` | 279.70 | Old real-account `<245/<235` lines are inactive because there is no position; any re-entry needs fresh setup | Event pullback from intraday high did not create a technical buy; no chase after prior sale |
| AMD | Historical replay only; real account watch only | `reduce-review -> repair watch` for replay; `watch only` real account | 511.57 | Existing replay close-stop line `492` | 2026-06-12 close reclaimed the line, so replay risk can be downgraded from active reduce-review; no fresh buy without trend-aligned entry |
| WDC | Historical replay only; real account watch only | `defensive hold / repair confirmed` | 562.93 | Existing replay line `500` | Repair continues above the line, but storage theme remains crowded and cyclical |
| STX | Historical replay only; real account watch only | `defensive hold / repair confirmed` | 931.04 | Existing replay line `835` | Strong repair, but single-share size is too large for a HKD 20,000 real account unless a very strong setup appears |

## Pending Execution Checklist

| Status | Ticker | Direction | Quantity | Target amount | Portfolio weight | Reference price | Trigger condition | Stop price | Invalidation | Strategy reason | Risk |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| Only observe | MRVL | No buy | 0 | USD 0 | 0% real | 279.70 | A fresh setup only: pullback holds prior support / VWAP area, or breakout retest confirms while QQQ/SMH stay constructive | New rule required; old `<245/<235` line inactive for flat account | Continues higher without pullback, or breaks below 267 area without support | AI interconnect/custom silicon remains a watch theme | Event/CFO catalyst and capex-cycle sensitivity can reverse quickly |
| Only observe | AMD | No buy; replay repair review | 0 | USD 0 | 0% real | 511.57 | Continued closes above `492-500` and relative strength versus QQQ/SMH before candidate ranking | Replay line `492`; no real stop because no real position | Closes back below `492` | AI compute beta repaired, but prior stop breach requires discipline | High beta, execution and valuation sensitivity |
| Only observe | WDC | No buy; replay defensive hold | 0 | USD 0 | 0% real | 562.93 | Multiple closes above `500`, storage leadership persists, and a technical pullback basis appears | Replay line `500` | Closes back below `500` or storage chain weakens with SMH | Storage bottleneck theme remains valid | Theme overlap with STX/MU; cyclical valuation risk |
| Only observe | STX | No buy; replay defensive hold | 0 | USD 0 | 0% real | 931.04 | Multiple closes above `835`, relative strength persists, and small-account sizing is acceptable | Replay line `835` | Closes back below `835` or storage chain weakens | Storage repair is strong | High single-share notional for the real account |
| Only observe | NVDA / AVGO / QCOM / ORCL / AI application names | No buy | 0 | USD 0 | 0% real | n/a | Individual technical basis, RS, and revenue/cash-flow evidence all confirm | Per ticker | AI narrative without price/quality confirmation | Keep the watch universe intact | AI capex, token-cost, application conversion, and valuation risks |

## Buy / Sell / Reduce / Add / Cancel

- Buy: none. No new buy passes both `trend_aligned_entry` and technical entry-price-basis requirements.
- Sell: none. Real account has no confirmed equity holding.
- Reduce: none in real account. Historical AMD reduce-review can be downgraded to replay repair watch after the 2026-06-12 close, but this is not a real trade.
- Add: none.
- Cancel: no confirmed live order to cancel. If an old broker-side MRVL order still exists, user must confirm its status from the broker side before it can be recorded.

## Replay Ledger

Replay protocol is applicable because 2026-06-12 is a completed close in the 2026-06-05 AI/semiconductor/storage replay window. Add only the 2026-06-12 close row; do not prefill 2026-06-15 or any future date.

## User Confirmation Items

- Confirm whether any old broker-side MRVL limit order remains open.
- Confirm real-account cash, settlement, fees, FX, tax, and margin status.
- Decide later whether the next real starter should be one best single name only, rather than rebuilding MRVL/AMD/WDC/STX as one overlapping AI-capex basket.

## Data Gaps

- VIX/VIX3M synchronized term structure.
- Broker cash and open-order state.
- No 2026-06-14 daily strategy report or 20:30 realtime/institutional monitor product exists locally; latest input remains 2026-06-12.

## Sources

- Local memory: `summary.md`, `decisions.md`, `daily-summaries.md`, latest 2026-06-12 daily/trade/portfolio records, and required institutional overlay references.
- Local quote clients: Node `StockService.fetchQuotes` and bundled Python `ResilientStockClient`, both returning Tencent quote objects on 2026-06-14 05:52 Asia/Shanghai.
- Public market context: AP and MarketWatch 2026-06-12 market close reports; Cboe, MarketWatch, Yahoo Finance, and Investing.com VIX pages showing VIX close `17.68`.
