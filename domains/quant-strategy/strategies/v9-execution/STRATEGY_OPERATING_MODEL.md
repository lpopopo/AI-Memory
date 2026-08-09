# Strategy Operating Model

## Objective

Run one durable V9-managed U.S.-equity portfolio. V8 is the embedded SPY/QQQ
trend-allocation module; V9 Rule E governs the individual-stock module, cash,
concentration and portfolio-level risk.

## Portfolio structure

| Internal module | Instruments | Ceiling | Decision output |
| --- | --- | ---: | --- |
| V8 index core inside V9 | SPY, QQQ | 70% | target ETF weights |
| V9 Rule E stock sleeve | formal self-selected stocks | 30% | buy/watch/hold/trim/exit |
| V9 cash reserve | cash | residual | preserve optionality and risk capacity |

The ceilings are risk budgets, not targets. If either module lacks a valid
signal, its unused allocation stays in cash.

## Embedded V8 index core

- SPY and QQQ each earn half of the 70% core budget above MA150 and another
  half above MA200.
- Signals are reviewed monthly and execute at the next session close with
  costs; leverage is prohibited. Weights drift between reviews.
- The module supplies long-term index exposure but does not govern individual
  stock selection.
- Momentum-factor monitor (research-validated context, not a weight override):
  keep MA150/MA200 as the only formal index regime; treat QQQ ~1.3x drawdown
  amplification under SPY stress as a risk caution; do **not** use absolute or
  relative 63-day momentum continuation to chase or short. See
  `../../references/v9-index-core-momentum-monitor.md`.
- Prospect-theory, disposition-effect and momentum-crash research remains a
  non-authorizing supplement. Its panic-to-repair monitor and slow volatility
  scaling are validation candidates, not execution rules. See
  `BEHAVIORAL_MOMENTUM_SUPPLEMENT.md`.

## V9 Rule E individual-stock sleeve

1. Use locally archived, timestamped information to create a candidate.
2. Verify source identity, first-seen time, content integrity and the specific
   company/theme claim.
3. Require technical confirmation, relative strength, non-chase conditions and
   the V9 score threshold before a new recommendation.
4. Define entry zone, structural invalidation/stop, risk-based size, theme cap
   and review date before describing a buy.
5. Use technical exits, event invalidation, common-factor concentration and
   portfolio drawdown breakers for hold/trim/exit decisions.

V9.1, V9.1.1 breakout-tight and staged technical stops are separately labelled
experiments until independently promoted.

## Portfolio-wide controls

- The Market Fear Gate can reduce or prohibit all new risk.
- Fear-budget conflicts use `core_priority`: preserve the better-evidenced
  index core first and reduce the stock sleeve's available budget. Normal,
  elevated, stress and panic ceilings are respectively `70/25/5`, `70/5/25`,
  `55/0/45` and `35/0/65` for core/stocks/minimum cash. Core resizing is monthly
  except that `VIX >= 35` triggers a panic cut latched until the next month-end.
- Aggregate correlated AI-capex/semiconductor names as one common factor.
- Keep cash floors and concentration caps; do not average down into new lows
  without a confirmed recovery.
- Every recommendation must state its module, evidence/trigger, invalidation,
  size and review condition.
- Orders remain manual and broker-confirmed.

## Evidence boundary

V9 is user-promoted as the unified portfolio and stock-recommendation
authority. Its information alpha remains unproven because only 18 reliable
point-in-time events are available. This requires transparent forward tracking,
not fabricated historical information events or claims of established
outperformance. Behavioral explanations and historical factor returns do not
close this evidence gap.
