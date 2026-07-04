# 2026-07-01 Strategy Revision and Intraday Plan

Run time: 2026-07-01 00:17 Asia/Shanghai / 2026-06-30 U.S. regular session intraday.

Scope: user-authorized strategy-rule revision plus intraday real-account reanalysis. Prices are intraday snapshots, not completed closes. No brokerage login or order submission was performed.

## 1. Stable strategy revision

The former broad-theme rule that froze net additions once a theme reached 40% is replaced with a graduated concentration framework:

- Below 40%: normal staged additions are allowed when market and stock filters agree.
- 40%-50%: leader-only net additions are allowed only in a `normal` fear regime, with stable breadth/credit, no unresolved hard stops, and a same-day net-theme expansion cap of 5% NAV.
- 50%-55%: rotation-only; any buy requires equal-notional reduction of a weaker same-theme holding.
- Above 55%: no buys; reduce below the hard cap.
- The 25% sub-theme cap, 15% normal single-stock cap, 20% high-conviction exception, event cooldown and trailing stops remain unchanged.
- Total equity exposure is managed separately. Controlled-aggressive mode retains a near-term operating range of about 45%-60% equity exposure in a `normal` market.

Reason: the old 40% freeze was derived from the 2026-06-25 one-day build-speed failure rather than an independent backtest. It reduced concentration risk but could create structural underinvestment in strong regimes.

## 2. Current data and risk state

Local Node quote workflow returned structured Tencent primary quotes at about 00:17 BJT. Yahoo Chart supplied daily-bar context and VIX/VIX3M.

| Symbol | Price | Day change | Technical context |
| --- | ---: | ---: | --- |
| SPY | 746.54 | +0.75% | Above 5/10/20/50-day averages |
| QQQ | 735.34 | +1.56% | Above 5/10/20/50-day averages |
| SMH | 653.05 | +3.33% | Above 20-day 622.35; leadership strong but narrow |
| RSP | 213.01 | -0.02% | Broad market flat while cap-weight tech leads |
| VIX / VIX3M | 16.77 / 19.18 | n/a | Normal term structure, ratio about 0.87 |

Provisional fear gate: `normal`, approximately 1/14. Breadth is not broken on a 21-day basis, but today's leadership is narrow, so flow fragility remains `elevated`.

## 3. Portfolio estimate

Latest user/broker-confirmed baseline remains GLW 2, TTMI 3, DRAM 4, MXL 6 and MU 1. User specifically reconfirmed that DRAM and MU remain held; no TTMI sale has been confirmed.

Using working cash USD 3,368.64:

| Holding | Shares | Intraday value | Approx. NAV weight | Action |
| --- | ---: | ---: | ---: | --- |
| GLW | 2 | 514.58 | 7.78% | Hold; no chase add |
| TTMI | 3 | 559.11 | 8.45% | Mandatory exit; completed close breached 188 |
| DRAM | 4 | 295.48 | 4.47% | Hold; no add |
| MXL | 6 | 714.84 | 10.80% | Hold; protect; no chase add |
| MU | 1 | 1,165.08 | 17.61% | Hold; no add; high-conviction-size position |

Conditional metrics:

- Estimated NAV: USD 6,617.73.
- Equity exposure before TTMI execution: 49.10%.
- Equity exposure after TTMI execution: 40.65%.
- Memory sub-theme (MU + DRAM): 22.07%, below but close to the 25% hard cap.

## 4. Current information mapping

- China June manufacturing PMI improved to 50.3 and high-tech manufacturing remained strong, supporting medium-term AI hardware and equipment demand. Source: [China NBS](https://www.stats.gov.cn/sj/zxfbhjd/202606/t20260630_1964032.html).
- U.S. semiconductors are rebounding after sharp prior-week volatility, but SMH materially outperforms RSP intraday; this supports the trend while warning that leadership is crowded and narrow.
- Micron/memory fundamentals remain supported by tight supply and long-term customer agreements, but the new U.S. DRAM price-fixing class-action allegation adds headline risk. Treat the allegation as unproven and do not change the thesis solely on the filing.
- The next U.S. session includes ADP and ISM manufacturing, followed by the Employment Situation the next day. New exposure should therefore be staged rather than filled at any price.

## 5. Revised intraday action plan

### Priority 0: execute the existing hard stop

- TTMI: sell 3 shares. The 2026-06-29 completed close was 186.80, below the 188 hard line. The revised concentration rule does not override a stock-level hard stop.

### Priority 1: conditional second-theme starter

- XLI: conditional buy 2 shares at USD 183.00 limit, only after TTMI is sold.
- Technical basis: XLI current 184.52; 5-day average 182.56, 10-day 181.31, 20-day 178.03, 20-day high 186.09. The order seeks a 5-day-average pullback instead of chasing the high.
- Position size: about USD 366 / 5.53% NAV. After TTMI sale and XLI fill, estimated equity exposure becomes about 46.18%, returning the account to the controlled-aggressive operating range while creating a second broad theme.
- Fee-adjusted breakeven: approximately USD 184.00 per share before FX/slippage, assuming USD 1 buy and USD 1 sell platform fees.
- Failure rule: completed close below USD 178 triggers exit review.
- Cancellation/no-chase: cancel if TTMI is not sold first, if broad market/credit deteriorates materially, or if XLI runs above USD 186.10 without a pullback. Do not place GLW/MXL/DRAM/MU additions on the same day.

### Existing holdings

- GLW: hold 2; completed-close protection at 227 minimum. At 257+, it is about 30% above its 20-day average, so no immediate add. Future pullback-add zone is approximately 235-240 after risk review.
- MXL: hold 6; completed-close protection at 104.30 minimum. At 119+, it is about 34% above its 20-day average and nearly +10% today; no add.
- DRAM: hold 4; maintain 70.50 hard protection. A 2-share add would be fee-inefficient, while 3 shares would push MU + DRAM beyond the 25% sub-theme cap; no add.
- MU: hold 1; maintain 1090 hard protection / 1100 completed-close risk line. One share already represents more than the normal 15% single-stock limit; no add.

## 6. Bottom line

The strategy revision changes today's posture from `zero new exposure` to `one conditional diversified starter after TTMI exit`. It does not authorize chasing the strongest AI names. The only new order candidate is XLI 2 shares at 183.00 under the stated sequence and cancellation conditions.

Not investment advice.
