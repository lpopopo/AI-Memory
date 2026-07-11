# V9 Index-Core Momentum Monitor

Status: **V9 operating monitor / risk-context only**. Does not change formal V8
MA150/MA200 execution weights, does not authorize stock trades, and does not
promote absolute/relative momentum continuation as alpha.

Evidence:
`memory/daily/2026-07-11-momentum-factor-induction-validation.md`,
`memory/daily/2026-07-11-validate-patterns-on-2026ytd.md`,
`memory/daily/2026-07-11-drawdown-events-historical-analogs.md`,
`work/momentum_factor_induction_validation.json`.

## Factor stack used by V9 context

| Layer | Definition | V9 use |
| --- | --- | --- |
| Trend momentum | SPY/QQQ close vs MA150 / MA200 | Formal embedded V8 index-core weights |
| Drawdown momentum | close / 63-day high − 1 | Fear Gate input; stress sizing context |
| Absolute momentum | 21 / 63 / 126-day returns | Monitor only; **not** an entry/exit rule |
| Relative momentum | QQQ mom − SPY mom | Describe QQQ vs SPY stress; **not** a chase signal |

## Validated operating conclusions

1. **Keep as regime control:** MA150/MA200 monthly V8 core remains the only
   promoted index allocation rule. Full-sample evidence supports better average
   forward conditions above MA200; 2026YTD showed V-recovery after brief MA200
   breaks, so broken-trend days must not be shorted as a momentum signal.
2. **Keep as stress amplifier:** When SPY 63-day drawdown is below about −5%,
   QQQ drawdown / SPY drawdown median amplification is about **1.3x** in both
   the full sample and 2026YTD. Under market stress, treat QQQ / Nasdaq-linked
   and high-beta AI-capex risk as larger than SPY beta.
3. **Do not promote short-horizon momentum continuation:** Absolute mom63 and
   QQQ−SPY relative mom63 continuation into the next 21 days are weak or
   rejected on recent samples (2024–2026 / 2026YTD). High momentum after a
   rally is a **pullback-watch** flag, not a buy-more signal.
4. **Event overlays stay descriptive:** Geopolitical oil shocks and hot-payrolls
   hawkish repricing can explain drawdown episodes; they do not create
   calibrated timing probabilities or override stops / Fear Gate / V9 Rule E.

## Required checklist in V9 daily / post-close reviews

When reviewing the embedded index core or market gate:

1. Record SPY/QQQ vs MA150 and MA200 (V8 score 0 / 0.5 / 1.0 each).
2. Record 63-day drawdowns and whether Fear Gate is normal / elevated / stress /
   panic.
3. If SPY 63-day drawdown &lt; −5%, explicitly note expected QQQ amplification
   (~1.3x) and tighten common-factor / new-buy caution for Nasdaq-beta names.
4. If QQQ mom63 is extended while drawdowns are still shallow, flag
   **pulse-pullback risk** (data or geopolitics), not a confirmed bear market.
5. Never use mom63 quintiles, relative-momentum continuation, or “below MA200
   stays weak for 63 days” as authorization to buy, add, or short.

## Explicit non-goals

- No change to the 70% index-core / 30% stock-sleeve ceilings.
- No replacement of Fear Gate by sentiment or momentum scores.
- No promotion of a standalone momentum sleeve inside V9.
- Scenario bands in the SPY/QQQ drawdown note remain risk-budget monitors, not
  win-rate forecasts.
