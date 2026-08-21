# RSR1 evidence synthesis

## Current decision

Keep the strict SMH MA50 veto. Reject the below-MA50 relative-strength and
breadth exceptions. Keep the frozen combined `ATR14/close <= 4%` plus signal-day
close-location >= 50% rule as `RSR1-shadow` only. Do not change formal V9 or use
the shadow to authorize an order.

## Evidence hierarchy

| Evidence | Result | Weight |
| --- | --- | --- |
| Fixed current-list OHLCV (36 listed; 35 tradable after excluding duplicate index vehicle QQQM), exact matched rules | Combined return 17.81% versus 5.91%; win rate 66.67% versus 44.44%; max DD -2.33% versus -5.32% | Promising but post-hoc and survivorship-biased |
| Exact ablation | ATR-only and close-location-only both help; combined is best in 2025 and 2026 YTD | Supports keeping the combined frozen challenger |
| Leave-one-symbol-out | Combined return/Sharpe/drawdown/win rate better in all 35 runs | Reduces single-symbol-concentration concern, but reuses the same history |
| Exit neighbors | Filter beats paired baseline in all 9 stop/hold cells | Reduces exit-parameter dependence concern |
| Position sizing | 12% has the highest retrospective dollars but only two peak names and a whole-share execution cliff; 8% has the best full-sample Sharpe and supports three names | Keep frozen 8%; no sizing challenger |
| Execution delay/gap | Delays of two/three sessions reduce full return to 11.34%/11.61%, but the filter comparison remains broadly positive; historical next-open gaps max at 4.57% | Edge weakens with latency but does not disappear; record actual gap |
| Universe scope audit | Candidate improves paired-baseline return, drawdown and Sharpe in training and 2026 for all 4 predefined scopes | Scope result is not dependent on one universe; freeze the semantically aligned 32-name `ai_capex_broad` shadow before observation |
| Timing/regime audit | 23 candidate trades occur across 21 signal dates; candidate PnL is positive in all three SMH/MA50 buffer buckets and 6 of 7 active quarters | Low same-day crowding and no single SMH-strength bucket explains the edge; 2026 remains only three trades |
| Profit protection | A 15% close-confirmed trigger with a +5% next-session stop raises full return from 15.68% to 18.11% and win rate from 65.22% to 69.57%; 8/9 nearby cells pass the non-worse screen | Track as separate RSR2 shadow only; improvement comes from just two protected exits and cannot modify RSR1 |
| Cash and opportunity cost | SGOV proxy raises fixed-path RSR1 from 15.68% to 27.94%, while full-period SPY/QQQ/SMH buy-and-hold return 68.03%/81.34%/242.00% with much larger drawdowns | RSR is a low-exposure stock sleeve, not a whole-portfolio substitute; cash proxy is operational research only |
| Operational cash-sweep economics | With USD 3,756.49 working cash, a 50% SGOV tranche leaves USD 1,945.41 available; under commissions plus a conservative 10 bps-per-side stress it breaks even in 31.5 days pre-tax or 45.0 days after a 30% distribution haircut. Reserving three 8% RSR entries caps the sweep at 23 shares/61.57% of cash | Do not use a 30-day tactical sweep. A 50%-60% upper bound is only a liquidity scenario, not an order, pending account-specific interest, tax, settlement and fee facts |
| Combined V9 context | In 2026, the 70% V9 core returns 1.41%; adding RSR1/RSR2 raises it to 2.04%/2.23% while RSR2 changes drawdown from -7.26% to -7.61% | The core remains the main portfolio engine; only three RSR trades make the incremental result too weak for governance changes |
| V9 core allocation and shared capital | Core-only testing made 80/20 the sole higher-cap challenger: 20-year CAGR 8.24% vs 7.42% at 70%, DD -19.29% vs -17.94%, identical 57.50% monthly win. The preregistered whole-share shared-cash follow-up then failed at both USD 6,000 and USD 5,751.77: 80/20 had lower 2024-2025/full return and Sharpe after its 20% stock cap omitted four RSR trades | Remove 80/20 as a challenger and retain formal 70/30. The formal-path advantage is concentrated in one omitted MU winner, so this is a governance retention result, not proof that 70/30 is universally optimal |
| V9 core whipsaw audit | The March month-end MA vote went to zero while the Fear Gate cut the 70% budget to 35%; the current path exited on April 1 and re-entered May 1 after SPY/QQQ rose 9.98%/15.38%. Delaying exits improved 2026 by 4.58pp but worsened 2025 max drawdown by 3.08pp and Sharpe | Zero of four predefined challengers passed the distinct, non-worse return/drawdown/Sharpe gate across both periods; classify as insurance cost and keep formal V9 unchanged |
| Latest-week missed leaders | AAOI rose 10.80% and six watchlist names rose more than 15% from Aug 7–14, but the exact 35-name replay produced zero RSR1 signals. AAOI exceeded the 4% ATR and 12% extension limits on all five sessions | Treat as outcome regret and a separate high-volatility trend diagnostic, not evidence for weakening the frozen low-volatility sleeve |
| High-volatility trend branch | The frozen central event definition showed positive 20-session averages in both historical periods, but the whole-share risk-budget portfolio had only 17.65% development win rate and 0.32 Sharpe; 2026 replay was 58.33%/1.12 | Failed the preregistered portfolio gate despite positive returns. Stop the sleeve branch and keep high-volatility leaders diagnostic-only |
| Conditional winner extension | Extending only profitable, above-MA20, positive-RS RSR2 positions to 30 days raised 2026 replay from 0.82% to 2.60%, but cut 2024–2025 return from 17.18% to 15.95%, worsened drawdown and lowered Sharpe/win rate | All three registered extensions failed the cross-period screen; retain RSR2's 20-session maximum |
| Point-in-time adjusted-close universe | Lower drawdown and fewer close-stop failures, but lower final-period return/Sharpe and fewer +10% winners | Warns that a binary low-volatility rule may sacrifice convex winners |
| Point-in-time exact OHLCV transfer audit | 631/633 frozen symbols usable and median active-member coverage 99.3%-100.0%. The pair improved 2020-2022 return (-7.58% vs -8.30%) and DD (-9.35% vs -10.06%), but Sharpe slipped (-0.840 vs -0.837) and mean trade return remained slightly worse/negative (-1.22% vs -1.19%). It passed all gates only in 2023-2025 (1.62% vs 0.11% return; 42.34% vs 41.73% win) | Fails the preregistered two-period transferability screen. Exact broad-universe evidence does not support a hard ATR/close-location veto; keep RSR1 shadow-only |
| Parameter-selection-bias audit | Across all 252 symmetric time-block splits, PBO is 13.1%, the frozen 4%/50% cell is selected in 154 splits, median selected OOS rank is 95%, and the 19-challenger family-wise block-bootstrap p-value is 0.063 (unadjusted fixed-cell p=0.022). However, the frozen cell improves return/Sharpe in only 6/10 registered blocks; three blocks have no activity and cannot be removed. It improves 6/7 active blocks | The edge is more structured than a random best-of-20 winner, but the preregistered selection-bias gate still fails because temporal evidence is sparse. Treat current-list headline confidence as discounted, not disproved; forward evidence remains decisive |
| Genuine forward sample | Three completed sessions through 2026-08-19, zero RSR1/RSR2/baseline signals and zero closed trades | Observing has begun, but no win-rate or expectancy denominator exists; decisive evidence still missing |
| Forward opportunity diagnostics | Three immutable rows record 23 raw high-volatility missed-leader observations, 16 primary episodes after overlap control, zero central high-vol signals and zero core reversals. The new Aug 19 raw observation is SNDK. Exact 5/20-session return/MFE/MAE outcomes are frozen but none is mature | Infrastructure is active. Do not infer success from the August 18 reversal or the SNDK observation; wait for registered horizons and original event thresholds |
| Forward expectancy scorecard | Genuine-forward rows are `awaiting_sample` after three sessions and zero trades. Retrospective calibration remains unchanged: RSR2 observed win rate 69.57% with Wilson 95% lower bound 49.13%, payoff 2.74, expectancy 9.64% and clustered-bootstrap p05 +4.57% | Track hit-rate uncertainty, payoff, expectancy and concentration together. Historical calibration contributes zero forward evidence and no gate changes |
| Forward economic-edge attribution | Immutable baseline/RSR1/RSR2 ledgers are paired to track avoided losses, missed winners, direct RSR2 exit effect and capital/whole-share path residual. Through 2026-08-19 all three ledgers have zero closed trades, so both attribution blocks are `awaiting_*` and dollar fields are unavailable | The machinery is ready but contains no evidence. Never convert an empty denominator into 0% or $0; update only from closed, source-complete forward rows |
| Forward zero-signal bottleneck | Across 96 symbol-days, the broad gate passed all three sessions. SMH below MA50 was the first-zero layer on Aug 18-19. On Aug 17, only AXTI survived through the volume layer, but it was 48.55% above MA20 and had 12.59% ATR; no stock-level matched-baseline candidate existed even before broad/SMH gates | The current absence of trades is not evidence that the 4%/50% pair alone is too strict. Do not remove the SMH veto, extension cap or ATR control to manufacture observations from a highly extended high-volatility name |
| Forward power and duration audit | At 20 candidate trades, exact power against the historical payoff-derived break-even rate is 94.9% for RSR1 and 98.1% for RSR2, but power to establish a majority win rate is only 25.2%/40.0%. Equal candidate/baseline arms need about 59/43 trades for 80% relative power. Historical RSR1 arrival is 23 trades/659 sessions, implying 573 sessions/2.3 years expected for 20 trades and less than 0.01% probability of reaching 20 within 126 sessions | Keep 20 trades as the immutable first-stage economic/falsification minimum, not proof of a 65%-70% future hit rate. The trade-count condition is the binding clock. Larger sample figures are second-stage confidence benchmarks only; do not loosen rules to accelerate arrivals |
| Capital-constrained entry ranking | At USD 6,000 and 10 bps, the current RS-plus-volume order returned 17.18% in 2024-2025 versus 13.36% RS-only, 13.57% low-ATR-first and 17.05% balanced-rank. At current NAV the comparison was 16.15%, 13.05%, 13.56% and 16.05%. All policies were identical in the three-trade 2026 segment because no ranking contention occurred | Retain the current ordering. Alternatives fail or are insufficient; low-volatility priority notably sacrifices the MU right-tail winner. No new forward ranking shadow is justified |
| Whole-share partial-profit overlay | Selling half after the existing +15% close trigger raised development Sharpe from 2.13 to 2.16 and marginally improved DD, but cut USD 6,000 development return from 17.18% to 14.33%, full return from 18.11% to 16.17% and win rate from 69.57% to 66.67%. Common-trade P&L lost USD 74.70 and released capacity added a USD 41.31 losing WDC trade | Reject automatic scale-out. It exchanges right-tail profit for smoother marks and has only one executable partial exit in the 2026 monitor; retain whole-position RSR2 profit lock |
| Research saturation inventory | All 23 registered branches are classified: 13 historical branches closed/rejected, two frozen forward shadows, seven retained controls and one external-account conditional item. The exact point-in-time transfer screen failed, the selection-bias concern remains uncontained, and genuine forward evidence is only three sessions with zero closed trades/outcomes | Freeze further parameter searches on the same historical data. The unresolved question is now forward-only; continue immutable collection without weakening gates or expanding the universe to manufacture observations |
| Backtest integrity audit | Future-row perturbation preserved all feature/signal prefixes; all RSR2 entries/exits passed chronology and OHLC-fill reconstruction; entry-time exposure peaked at 23.49%, cash stayed positive and common RSR1/RSR2 fills matched. Removing nine artificial period-end exits changed return by at most 0.0715pp and still failed the point-in-time transfer screen. Six malformed provider OHLC bars affected zero held paths | No implementation finding rescues or invalidates the main decision. Keep the negative transfer conclusion, disclose mark-to-market sensitivity, preserve missing-open exit orders, and continue forward-only validation |
| Economic edge and opportunity-cost decomposition | Of 23 direct quality exclusions, 16 were losers with $554.79 historical loss and seven were winners with $159.37 profit. RSR1's top three winners supply 50.15% of net P&L, but leave-top-three P&L remains +$469.10. RSR2 adds $145.34: $77.95/53.63% is direct exit effect on frozen RSR1 shares and $67.39/46.37% is later capital-path/whole-share sizing | The quality pair behaves mainly as a loss-avoidance filter but has explicit convex-winner cost. RSR2's headline gain is sparse and partly path-dependent; track protected exits and missed winners together rather than optimizing either statistic alone |

## Component interpretation

- ATR is the stronger independent discriminator: ATR-only full-period return was
  11.89%, Sharpe 1.15 and win rate 52.94% versus baseline 5.91%, 0.49 and 44.44%.
- Close location alone was weaker but positive: 10.28% return, Sharpe 0.88 and
  win rate 48.72%.
- The combined rule improved further to 17.81%, Sharpe 1.77 and win rate 66.67%.
  This interaction is why the already-frozen close-location condition is not
  removed before forward observation.
- At 20 bps per side the combined result remained 14.46%, versus 5.39% for the
  matched baseline.
- Fixed-path repricing of the exact same 8% trades from 10 to 20 bps reduced
  return from 17.81% to 17.41%. The lower 14.46% full-rerun figure includes a
  different COHR trade and therefore mixes cost with an execution-path change.
- The all-35 exact comparison returned 17.81% versus 5.91% for baseline. The
  semantically aligned 32-name AI-capex scope returned 15.68% versus 5.39%; it
  also retained the paired advantage in training and 2026. KO/RKLB/RDW stay in
  full-watchlist analysis but do not enter the SMH-gated forward ledger.

## Why this is not complete

The exact current-list evidence still comes from a watchlist chosen with
hindsight. The first broader historical-membership panel could not reproduce
exact ATR or close location and gave a materially less favorable proxy result.
The new 631-symbol point-in-time OHLCV audit can reproduce both fields, but the
pair failed its preregistered 2020-2022 validation gates even though it passed
2023-2025. It also still lacks complete delisting returns and permanent
identifiers. The 20-cell selection-bias audit finds a low 13.1% PBO and a
borderline family-wise p-value of 0.063, but fails its fixed 7/10 time-block
stability gates because only seven blocks contain return observations and one
of those seven is negative. Resampling the same post-hoc history and repeatedly
removing one symbol do not create genuine forward information.

The conflict can be resolved only by the preregistered forward comparison. The
minimum remains 126 completed sessions, 20 closed candidate trades, three
subthemes, controlled profit concentration, and all return/win-rate/Sharpe/
drawdown/cost gates. Power calibration shows that 20 trades can be an economic
first-stage screen but cannot precisely establish the 65%-70% retrospective hit
rate; forward payoff and expectancy therefore matter more than the headline
win percentage. Until the original gate is reached, the filter remains
diagnostic.

The historical research tree is therefore saturated, while validation remains
incomplete. Reopening a closed branch requires an independently motivated
mechanism, genuinely fresh data and preregistration before the new outcome is
observed. A later single winner, including AAOI, is not a valid reopen trigger.
