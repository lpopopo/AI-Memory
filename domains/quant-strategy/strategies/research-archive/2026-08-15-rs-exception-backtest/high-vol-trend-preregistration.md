# High-volatility trend participation study registration

Frozen before reading the study outputs on 2026-08-15. Research-only; no order authorization and no change to V9, RSR1 or RSR2.

## Purpose

Test the stable `strong-trend participation module` in `memory/decisions.md` as a separate diagnostic. This study must not weaken RSR1's low-volatility filter merely to capture AAOI or another realized winner.

## Bias boundary

The current watchlist is selected with hindsight. The numerical definitions below were specified after observing 2026, including the Aug 10–14 rally. Therefore neither 2024–2025 nor 2026 is genuine forward evidence for this new module. The split is only a temporal consistency check. Any surviving idea still requires a newly frozen forward ledger.

## Shared signal contract

- Universe: the fixed 32-name `ai_capex_broad` scope.
- Signal: completed daily close; hypothetical entry: next-session open.
- Market: SPY above MA200, QQQ above MA100, VIX below 25, VIX/VIX3M below 1, and SMH at or above MA50.
- Stock: above MA20 and MA50, close above the previous 20-session high, positive extension, and no 10% opening-gap cooldown block.
- Deduplicate each symbol for 20 sessions after a selected signal.
- Costs for event returns: 10 bps at entry and 10 bps at exit.
- Outcome windows: 5, 10 and 20 sessions from the next open; record return, excess over QQQ, MAE and MFE.

## Fixed definitions

| Variant | RS20 vs SMH | Volume | ATR14/close | MA20 extension | Close location |
| --- | ---: | ---: | ---: | ---: | ---: |
| `hv_relaxed` | >= 3% | >= 1.2x | >4%, <=12% | >12%, <=30% | >=50% |
| `hv_central` | >= 5% | >= 1.5x | >4%, <=12% | >12%, <=25% | >=60% |
| `hv_strict` | >=10% | >= 2.0x | >4%, <=10% | >12%, <=20% | >=70% |
| `rsr1_low_vol_comparator` | >=3% | >=1.2x | <=4% | 0%–12% | >=50% |

## Temporal reporting

- `development_2024_2025`: 2024-01-02 through 2025-12-31.
- `retrospective_2026`: 2026-01-02 through the cached completed 2026-08-07 session.

## Event-study continuation gate

The central definition may proceed to a portfolio simulation only if all are true:

1. At least 15 completed 20-session events in development and at least 5 in retrospective 2026.
2. Net 20-session mean return, median return and mean excess over QQQ are positive in both periods.
3. Net 20-session win rate is at least 50% in both periods.
4. Mean MFE divided by absolute mean MAE is at least 1.25 in both periods.
5. No symbol contributes more than 35% of central-definition positive 20-session return.
6. At least two of the three high-volatility definitions have positive mean, median and mean excess in both periods.

Failure stops the branch. A failed branch must not be rescued by searching additional thresholds on the same data.
