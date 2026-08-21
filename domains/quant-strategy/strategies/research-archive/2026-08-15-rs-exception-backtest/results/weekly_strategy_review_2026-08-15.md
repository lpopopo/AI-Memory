# Weekly strategy error and missed-opportunity review — 2026-08-15

## Bottom line

No broker account, submitted-order or confirmed-fill evidence was available, so this review cannot label any real-account trade as an execution error. The evidence supports one analytical correction, two material opportunity costs, and no formal rule change.

The analytical correction is important: the April V9 core exit was not caused by the moving-average rule alone. At the March month-end, both SPY and QQQ fell below MA150/MA200 and the separate Fear Gate was also in `panic`. The two controls jointly drove the formal core to zero. Any review that attributes the entire miss to one filter is incomplete.

## What was actually wrong

| Item | Evidence | Classification | Correction |
| --- | --- | --- | --- |
| Core whipsaw explanation | Exact targets and shares show that delaying the MA exit would still have cut the 70% core to 35% because the Fear Gate remained active | Analysis error, now corrected | Always decompose base target, risk-budget cap and actual shares separately |
| Idle-cash assumption | Original simulations assigned 0% return to unused cash; an SGOV adjusted-close proxy materially raises reported returns | Model omission, not proven live loss | Keep zero-yield base case, show fixed-path cash proxy separately, and require broker sweep mechanics before operational use |
| AAOI explanation | AAOI gained 10.80% from Aug 7 to Aug 14, but exact daily diagnostics show no RSR1 signal on any session | Outcome regret; prior no-buy result remains rule-consistent | Record the failed conditions numerically at decision time, not only a generic “too risky/extended” label |
| Profit giveback | RSR2 improves full-sample return from 15.68% to 18.11%, but the gain comes from only INTC and KLAC | Plausible weakness, statistically thin | Keep RSR2 as a separate preregistered shadow; do not retrofit RSR1 |

## Lost opportunities, quantified

### 1. April core rebound

The formal V9 core sold SPY and QQQ on 2026-04-01 and repurchased on 2026-05-01. Between those closes, SPY rose 9.98% and QQQ rose 15.38%. A 35%/35% allocation therefore missed about 8.88 percentage points of portfolio contribution before costs.

The best-looking predefined repair, requiring two month-end exit confirmations, retained only a 17.5%/17.5% core because the Fear Gate still capped total exposure at 35%. It improved 2026 return by 4.58 percentage points, but worsened 2025 maximum drawdown from -7.46% to -10.54% and lowered 2025 Sharpe from 0.79 to 0.73. Zero of four challengers passed the two-period promotion gate.

Conclusion: this was a costly false defensive signal, but not yet a repairable rule error. It is the insurance premium paid by the existing trend/risk system.

### 2. Latest-week high-volatility leaders

From Aug 7 to Aug 14, the largest watchlist moves included SNDK +35.38%, SMCI +27.98%, SKHY +20.61%, STX +19.77%, WDC +17.15% and AAOI +10.80%. None generated an exact RSR1 strict-veto entry during Aug 10–14.

For AAOI specifically:

- ATR was 11.37%–12.45% every day versus the frozen 4% ceiling.
- Extension above MA20 was 15.12%–30.24% versus the 12% ceiling.
- It lacked a 20-day breakout on four of five sessions and lacked 1.2× volume on three.
- On Aug 14 it finally had strong relative strength, volume and close location, but was still 30.24% above MA20 with 11.37% ATR.

Conclusion: AAOI was outside the design domain of the low-volatility RSR sleeve. Buying it would require a separately defined high-volatility trend strategy, not an exception made after observing the gain.

### 3. Residual cash

In the 2026 combined audit, adding the fixed-path SGOV proxy raises core+RSR2 from 2.23% to 3.05%, about 0.82 percentage points. Across the longer RSR path, fixed-path SGOV raises RSR1 from 15.68% to 27.94% and RSR2 from 18.11% to 30.46%.

Conclusion: cash yield is the cleanest capital-efficiency opportunity found, but the proxy is optimistic and cannot be promoted without knowing the real account's currency conversion, sweep vehicle, settlement, fees and liquidity.

The operational break-even audit narrows that conclusion. At USD 3,756.49 cash, 18 SGOV shares use about 50% and leave USD 1,945.41 immediately available. With USD 1 commissions and a conservative 10 bps-per-side friction stress, that tranche needs 31.5 days to break even before investor tax and about 45.0 days after a 30% distribution haircut. A 30-day tactical sweep is therefore not robust. Reserving all three possible 8% RSR entries limits the maximum sweep to 23 SGOV shares, or 61.57% of cash; a 100% sweep is rejected on liquidity grounds. This is a conditional scenario only and authorizes no order.

## Changes that should not be made

- Do not relax AAOI's ATR or extension limits because one excluded stock rallied.
- Do not replace the V9 core with a two-month exit rule based on the April counterfactual.
- Do not raise the 30% stock-sleeve budget; only three 2026 RSR trades support the incremental result.
- Do not merge RSR2 into RSR1 before independent forward trades exist.

## Next controlled measurements

1. Start the frozen 32-name RSR1 and separate RSR2 forward ledgers on the first completed session on or after 2026-08-17.
2. Add a non-trading `high_vol_trend_miss` diagnostic for names with weekly gain above 10% that fail only because ATR/extension/event-gap constraints are outside RSR1's domain. Measure subsequent 5/20-day return and maximum adverse excursion.
3. Add a non-trading `one_month_core_whipsaw` diagnostic whenever a core reduction reverses at the next month-end. Reconsider confirmation only after repeated independent cases.
4. Keep zero-yield cash as the conservative base case and SGOV as a separate opportunity-cost overlay until broker mechanics are documented.

Formal V9, RSR1 and RSR2 remain unchanged. This report authorizes no order.

## High-volatility branch follow-up

The registered follow-up has now been completed. The central event definition looked promising at a fixed 20-session horizon, but the executable portfolio exposed the convexity problem hidden by event averages: development-period return was +2.12% with -4.36% drawdown and profit factor 1.25, yet win rate was only 17.65% and Sharpe only 0.32. The 2026 replay improved to +3.93%, 58.33% win rate and 1.12 Sharpe, but the two periods were not consistent enough to pass.

The high-volatility sleeve branch is therefore stopped without parameter rescue. `high_vol_trend_miss` remains a non-trading diagnostic only.

## Conditional winner-extension follow-up

The separate winner-extension study also failed. Extending qualifying RSR2 winners from 20 to 30 sessions raised the 2026 replay from +0.82% to +2.60%, but reduced 2024–2025 return from +17.18% to +15.95%, worsened drawdown from -1.91% to -2.56%, lowered Sharpe from 2.13 to 1.80 and reduced win rate from 70% to 65%. Extending to 40 sessions was weaker again.

### 6. Index-core allocation frontier

The 70% core ceiling is a governance choice rather than a profit optimum. A preregistered 50%-100% audit held the MA150/MA200 signal, Fear Gate, next-session execution and 10 bps one-way cost fixed across development 2006-2014, validation 2015-2019, final test 2020-2025 and the 2026 held-out monitor.

Only 80% passed. On the continuous 2006-2025 history, 70% produced 7.42% CAGR, -17.94% maximum drawdown, 0.82 Sharpe and 57.50% monthly win rate; 80% produced 8.24%, -19.29%, 0.83 and the same 57.50%. The higher ceiling also improved total return in validation, final and 2026. The 90% and 100% ceilings failed because validation drawdown/Sharpe deteriorated and full-history drawdown exceeded the frozen -20% boundary.

Conclusion: 80/20 is a credible research challenger for reducing cash drag, but it does not improve hit rate and cannot yet replace formal 70/30. At maximum exposure it leaves only 20% for all stocks, so the next audit must enforce shared capital and whole-share execution rather than simply add historical core and RSR returns.

### 7. Shared-capital and whole-share follow-up

The required follow-up rejects that challenger. One integrated ledger shared cash between whole-share SPY/QQQ and frozen RSR2, charged USD 1 per order plus 10 bps slippage, and tested both USD 6,000 and the current USD 5,751.77 working NAV.

At USD 5,751.77, formal-core-plus-RSR-capacity returned 41.71% in 2024-2025 with -8.62% drawdown and 1.78 Sharpe. The 80/20 challenger returned 41.68%, -9.41% and 1.63. Across 2024 through 2026-08-07 the comparison was 45.42%/1.46 versus 45.36%/1.32. The challenger did better in the short 2026 monitor, 2.67% versus 1.43%, but failed the frozen requirement to improve training and full-period return at both account sizes.

The 20% stock cap omitted four training trades: COHR and CEG losses plus KLAC and MU winners. Their net formal-path contribution was USD 178.66 at the current NAV, dominated by the USD 189.98 MU winner. This concentration means the result does not prove 70/30 is universally optimal; it does prove that 80/20 cannot be promoted from this history after shared-capital effects are included. Remove the challenger and retain formal 70/30.

### 8. Win rate versus economic expectancy

The new forward scorecard freezes a more complete definition of trade quality before the first Aug 17 observation. It reports Wilson hit-rate uncertainty, average winner/loss, payoff ratio, break-even win rate, net expectancy, profit factor, loss streak, top-symbol profit concentration and a 10,000-sample entry-date-cluster bootstrap. It is read-only and does not change the original RSR promotion gates.

The retrospective calibration is instructive but not forward evidence. RSR2 closed 23 trades with 69.57% observed win rate, yet the Wilson 95% interval is 49.13%-84.40%; the data do not establish a precisely known 70% future hit rate. Its economics are stronger than that uncertainty alone suggests: average-win/average-loss payoff is 2.74, break-even win rate is only 26.76%, mean net return per trade is 9.64%, profit factor is 6.49, and the clustered-bootstrap 5th percentile remains +4.57% with a 0.05% estimated probability of nonpositive expectancy. Top-symbol gross-profit share is 25.43%, below the frozen 35% boundary.

RSR1 is directionally similar: 65.22% observed win rate, 2.70 payoff, 27.04% break-even win rate, 8.95% expectancy and +3.79% bootstrap p05. The matched baseline is much weaker: 43.18% win rate, 1.89 payoff, 1.86% expectancy, and -1.68% bootstrap p05 with 20.18% nonpositive-expectancy probability. This supports observing the frozen filter, but current-list hindsight and only 21 entry-date clusters still prohibit promotion.

Conclusion: optimize future decisions for positive, diversified expectancy after costs—not the highest headline win rate. Genuine-forward scorecard rows remain empty until the first eligible completed session.

This branch is stopped. The evidence-backed RSR2 maximum remains 20 sessions.

### 9. Capital-constrained signal ranking

The next preregistered audit changed only the order of already-qualified RSR2
entries when limited capacity forced a choice. Entry filters, 8% target weight,
three-name limit, 25% sleeve cap, RSR2 exits, commissions and next-open execution
were held fixed. The current ordering combines RS20 and volume; challengers used
RS alone, lowest ATR first, or equal ranks of RS, volume, close location and low
ATR.

At USD 6,000 and 10 bps slippage, the current order returned 17.18% in
2024-2025 with 70.00% win rate and 2.13 Sharpe. RS-only returned 13.36%,
low-ATR-first 13.57%, and balanced-rank 17.05%; all three had 65.00% win rates.
At the current USD 5,751.77 NAV the same comparison was 16.15%, 13.05%, 13.56%
and 16.05%. The ordering mattered on only six to seven development dates.

The 2026 local OHLCV segment ends on 2026-08-07 and contains only three closed
trades and zero ranking conflicts. Every policy therefore returned the same
0.82%-0.85%, leaving no cross-period evidence. Low-ATR-first also replaced the
large MU winner in one constrained path, illustrating why suppressing
volatility can improve neither hit rate nor total profit when it removes the
right tail.

Conclusion: retain the current RS-plus-volume ordering. Do not create another
forward shadow, and do not reopen ranking weights until independent forward
capacity conflicts exist.

### 10. Whole-share partial-profit follow-up

The single preregistered scale-out candidate sold half the executable whole
shares at the next open after the existing RSR2 +15% completed-close trigger.
The remaining shares kept the +5% profit-lock stop and every ordinary exit.
Partial and final proceeds were aggregated into one trade, so the extra sale
could not inflate win rate; the additional USD 1 commission and USD 200 minimum
sale were enforced.

At USD 6,000, 2024-2025 return fell from 17.18% to 14.33% and win rate from
70.00% to 66.67%. Maximum drawdown improved slightly from -1.91% to -1.84% and
Sharpe rose from 2.13 to 2.16. Across the full period, return fell from 18.11%
to 16.17%, while drawdown improved to -1.84% and Sharpe to 1.90. The current
USD 5,751.77 NAV showed the same trade-off: full return fell from 17.01% to
15.59%.

At USD 6,000/10 bps, common-trade P&L declined USD 74.70. The largest losses
were from trimming the September MU winner (USD -83.63 versus baseline) and the
October NOK winner (USD -42.45); partial exits helped KLAC, INTC and TER but not
enough to offset the lost right tail. Released capacity also admitted one
additional WDC trade that lost USD 41.31. Only one partial exit executed in the
2026 monitor, below the frozen minimum of two.

Conclusion: automatic half-position profit taking smooths the curve but does
not maximize profit or preserve win rate. Reject the overlay and retain the
whole-position RSR2 +15%/+5% profit lock.
