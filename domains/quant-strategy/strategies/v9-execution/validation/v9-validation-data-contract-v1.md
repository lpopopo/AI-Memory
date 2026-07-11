# V9 Validation Data Contract v1

Status: **frozen for research validation**. This contract does not authorize a
live V9 rule change.

## Purpose

Define the data, lag, cost and eligibility rules for all experiments listed in
`BEHAVIORAL_MOMENTUM_SUPPLEMENT.md` and the pre-registered plans under this
folder.

## Market data

| Series | Source | Lag rule |
| --- | --- | --- |
| SPY / QQQ / SMH OHLCV | completed daily bars in `datasets/data_v9` or `data_v87_forward` | signals use completed close only |
| VIX / VIX3M | completed daily bars | same-session close is allowed for same-day diagnostics; no intraday peek |
| RSP / IWM / HYG / LQD | optional breadth/credit proxies | missing series score 0 points, never optimistic fill |
| Ken French UMD / WML | `datasets/data_factor/ff_mom_daily.csv` or monthly fallback | factor returns dated by French publication calendar |

## Point-in-time universe

| Field | Rule |
| --- | --- |
| Membership | S&P 500 and Nasdaq-100 membership as of each date |
| Deletions | included through deletion date |
| Delisting returns | required when available; if missing, mark coverage gap |
| Survivorship | current-constituent caches are **not** decision-grade |
| Manifest | `datasets/data_point_in_time/manifest.json` must record coverage and missing IDs |

## Event archive

| Field | Rule |
| --- | --- |
| Effective time | `first_seen_at` for PIT events |
| Retrospective | excluded from trading replay |
| Reliability floor | source_completeness >= 15 and PIT eligible |
| Split gate | Rule E statistical validation requires >= 50 reliable PIT events |
| Embargo | 5 calendar days between chronological splits |

## Costs and leverage

| Setting | Value |
| --- | --- |
| Baseline one-way cost | 0.10% |
| Frozen shadow base | 0.20% |
| Stress cost | 0.50% |
| Leverage | prohibited for V9 overlays |
| Vol-scale floor / ceiling | 0.25 / 1.00 |

## Metrics

Every experiment must report:

- net CAGR
- Sharpe
- max drawdown
- expected shortfall (5%)
- skew
- turnover
- cash drag
- false reductions
- missed winners

## Non-goals

- No conversion of subjective drawdown scenarios into probabilities.
- No WML result may validate MA trend or Rule E relative strength.
- No override of stops, unresolved-stop veto, common-factor caps, or 70/30 ceilings.
