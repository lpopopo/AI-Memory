# V9 Behavioral and Momentum-Risk Supplement

Status: **research supplement / pending validation**. This document does not
change V9 allocations, authorize trades, override stops, or promote a momentum
sleeve.

## Purpose

Summarize the decision-useful implications of prospect theory, disposition-
effect research, and momentum-crash research for the V9 portfolio. Separate
well-supported risk lessons from hypotheses that still require point-in-time,
cost-aware, out-of-sample validation.

## Scope boundary

V9 is not the strategy studied in the classic momentum-crash literature:

- The embedded V8 core is a **long-only time-series trend allocation** in SPY
  and QQQ using monthly MA150/MA200 signals.
- V9 Rule E is a **long-only, event-driven stock sleeve** with technical,
  concentration, stop and evidence gates.
- Classic WML/XSMOM is a **cross-sectional long-winner/short-loser portfolio**.
  Its most severe crashes are usually driven by the short loser leg during
  sharp bear-market rebounds.

Therefore, WML results may inform V9 risk monitoring, but they cannot be copied
into V9 weights or used to infer that SPY/QQQ trend rules will behave the same
way.

## Evidence synthesis

### 1. Prospect theory is descriptive, not a trading rule

Prospect theory models gains and losses relative to a reference point and uses
decision weights rather than objective probabilities. Cumulative prospect
theory extends the original model to ranked multi-outcome distributions and
preserves stochastic dominance.

Decision-useful implications:

- Investors may become risk-seeking after losses and realize gains too early.
- Cost basis, recent peaks, target prices and expectations can become unstable
  psychological reference points.
- Small-probability outcomes may receive excessive weight.

Evidence boundary:

- The reference point and degree of narrow framing are usually not directly
  observed.
- The disposition effect is real in many account datasets, but it does not
  uniquely identify prospect theory; beliefs, attention, regret, taxes and
  realization utility can produce similar behavior.
- Experimental parameter estimates are not stable strategy parameters for a
  live equity portfolio.

V9 implication: broker cost basis and prior unrealized profit/loss must not
replace the predefined technical invalidation, completed-close stop, position
cap or portfolio risk gate.

### 2. Behavioral explanations do not establish tradable alpha

Grinblatt and Han connect reference prices and the disposition effect to price
underreaction and momentum through an aggregate capital-gains-overhang proxy.
Later work finds related predictive structure in prospect-theory value,
lottery-like returns and extreme past gains.

These results remain research inputs because:

- reference-price proxies are model-dependent;
- results overlap with size, liquidity, reversal, volatility, skewness and
  standard momentum factors;
- small, illiquid and difficult-to-short stocks can dominate paper returns;
- historical gross returns do not establish net, forward, implementable alpha;
- published anomaly returns commonly weaken out of sample and after discovery.

V9 implication: prospect-theory value, capital-gains overhang, MAX or skewness
may be tested as diagnostics or candidate-ranking features, but none may enter
Rule E scoring without an incremental point-in-time validation.

### 3. Momentum crashes are state-dependent and short-leg dominated

The most robust momentum-crash pattern is:

1. the market experiences a large prior decline;
2. volatility is high and past losers become high-beta/distressed;
3. the market rebounds abruptly;
4. the loser short leg rises much faster than the winner long leg;
5. long-winner/short-loser momentum suffers a negatively skewed crash.

Daniel and Moskowitz estimate a dynamic WML weight proportional to forecast
mean divided by forecast variance:

`weight(t-1) ∝ expected_return(t-1) / forecast_variance(t-1)`.

The exact conditional-mean model and reported Sharpe improvement are less
portable than the underlying risk lesson. They depend on rare crash episodes,
estimation choices, leverage, financing, short availability and transaction
costs.

V9 implication:

- A `stress/panic -> repair/rebound` transition is a crowding and high-beta
  reversal warning, not a standalone buy or sell signal.
- The mechanism is only a partial analogy for V9 because V9 has no systematic
  loser short leg.
- High mom63 after a rally remains a pullback-watch condition, not continuation
  alpha or a short authorization.

### 4. Slow risk scaling is more credible than unconstrained optimization

Across follow-up studies, volatility management is most defensible for
momentum when it uses a slow risk estimate, liquidity controls and a leverage
cap. Fast inverse-variance scaling can create excessive turnover and unstable
weights; unrestricted optimal weights are not suitable for a small manual
account.

V9 implication: any future risk-scaling experiment should use completed data,
a slow window such as 126 trading days, no leverage by default, fixed caps and
explicit cost accounting. It must be tested as an overlay against unchanged V9,
not embedded before validation.

## Does V9 need improvement?

**Yes at the research and audit layer; no immediate formal allocation change is
supported.**

### Already adequate

- MA150/MA200 remains the only formal index-core weight rule.
- Fear Gate already reduces or prohibits new risk in stress/panic.
- Completed-close stops and the unresolved-stop veto counter loss-domain
  gambling and reference-point drift.
- Common-factor aggregation addresses winner/theme crowding.
- QQQ drawdown amplification near 1.3x under SPY stress is already monitored.
- Absolute and relative mom63 continuation are already rejected as trade
  authorization.

### Gaps worth validating

1. **Panic-to-repair transition monitor**
   - Detect prior market drawdown, elevated volatility and subsequent sharp
     breadth/market rebound.
   - Use as a shadow warning for high-beta/theme concentration only.
2. **Behavioral execution audit**
   - Record whether a hold/add/exit rationale depends on cost basis, prior peak,
     break-even desire or reluctance to realize a loss.
   - The audit may expose process violations but may not create a price signal.
3. **Slow volatility-risk overlay**
   - Test 126-day realized-volatility scaling with fixed exposure floors and
     ceilings, no leverage and one-way costs.
4. **Winner-crowding / reversal diagnostics**
   - Track theme breadth, QQQ/SMH beta, relative strength, mom63 extension,
     volume and common-factor concentration during fear-regime transitions.
5. **Factor-definition separation**
   - Every test must label XSMOM, TSMOM, MA trend, drawdown momentum and Rule E
     relative strength separately. Results from one cannot validate another.

## Pre-registered validation plan

### Required data

- Point-in-time S&P 500 and Nasdaq-100 membership with permanent identifiers,
  deletions, delistings and delisting returns.
- Adjusted SPY, QQQ, SMH and stock OHLCV with causal completed-bar indicators.
- VIX, VIX3M, RSP/SPY, IWM/SPY and HYG/LQD histories with publication dates.
- Ken French UMD/WML returns or a reproducible point-in-time reconstruction.
- Realistic spreads, slippage, financing and borrow availability for any
  long-short comparator.
- Timestamped V9 Rule E events and immutable forward decisions.

### Experiment sequence

1. Freeze definitions before seeing evaluation results.
2. Build a static V9 comparator with existing MA, Fear Gate and Rule E rules.
3. Label panic-to-repair windows using only lagged market drawdown, volatility
   and rebound information.
4. Measure WML, long-winner, short-loser, SPY/QQQ and V9 stock-sleeve behavior
   separately over 1/5/21/63 trading days.
5. Test the slow volatility overlay independently from the transition monitor.
6. Report gross and net CAGR, Sharpe, max drawdown, expected shortfall, skew,
   turnover, cash drag, false reductions and missed winners.
7. Run expanding/rolling walk-forward tests. The inspected 2019-2025 interval
   is not a fresh out-of-sample period.
8. Start genuine forward tracking only after code, parameters and data contract
   are frozen.

### Promotion gates

No candidate changes V9 unless it:

- improves drawdown or expected shortfall without material net-return damage;
- remains useful after realistic costs and fixed exposure caps;
- adds information beyond the existing Fear Gate and MA150/MA200 rules;
- is stable across subperiods rather than dependent on 1932/2009-like episodes;
- does not increase false reductions or missed-winner rates beyond a
  predeclared tolerance;
- passes genuinely new forward evidence;
- never overrides stops, unresolved-stop veto, common-factor limits, Rule E
  evidence requirements or the 70%/30% module ceilings.

## Current decision

- Keep V9 formal execution unchanged.
- Treat behavioral and momentum-crash findings as research context and audit
  controls.
- Add no standalone momentum sleeve.
- Do not convert subjective pullback scenarios into probabilities.
- Validate panic-to-repair monitoring and slow risk scaling as separate shadow
  candidates before considering any V9 revision.
- Pre-registered contracts and first-pass experiment outputs live under
  `validation/` and `results/validation/`.

## Primary references

- Kahneman & Tversky (1979), *Prospect Theory: An Analysis of Decision under
  Risk*: https://doi.org/10.2307/1914185
- Tversky & Kahneman (1992), *Advances in Prospect Theory*: 
  https://doi.org/10.1007/BF00122574
- Odean (1998), *Are Investors Reluctant to Realize Their Losses?*:
  https://doi.org/10.1111/0022-1082.00072
- Grinblatt & Han (2005), *Prospect Theory, Mental Accounting, and Momentum*:
  https://doi.org/10.1016/j.jfineco.2004.10.006
- Daniel & Moskowitz (2016), *Momentum Crashes*:
  https://doi.org/10.1016/j.jfineco.2015.12.002
- Barroso & Santa-Clara (2015), *Momentum Has Its Moments*:
  https://doi.org/10.1016/j.jfineco.2014.11.010
- Moreira & Muir (2017), *Volatility-Managed Portfolios*:
  https://doi.org/10.1111/jofi.12513
- Cederburg et al. (2020), *On the Performance of Volatility-Managed
  Portfolios*: https://doi.org/10.1016/j.jfineco.2020.04.015
- Barberis, Mukherjee & Wang (2016), *Prospect Theory and Stock Returns*:
  https://doi.org/10.1093/rfs/hhw049
