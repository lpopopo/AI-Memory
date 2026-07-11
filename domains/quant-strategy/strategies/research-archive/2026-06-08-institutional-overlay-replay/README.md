# 2026-06-08 Institutional Overlay Replay

Purpose: compare existing strategy rules against experimental institutional overlays after the 2026-06-05 AI/semiconductor/storage drawdown.

Status: setup only. Do not treat template rows as completed backtest results.

Key references:

- `../../references/institutional-overlay-replay-protocol.md`
- `../../references/institutional-overlay-scorecard.md`
- `../../references/institutional-overlay-data-proxies.md`
- `../../memory/daily/2026-06-08-institutional-overlay-replay-2026-06-05.md`

Files:

- `replay-ledger-template.csv`: manual or script-fill ledger for baseline versus overlay comparison.

First replay target:

- T0: 2026-06-05 close.
- T1: 2026-06-08 close or best verified regular-session snapshot.
- T2-T5: next four completed trading days after T1.

Rule:

- Do not pre-fill future rows. Add rows only after data exists and the source/timestamp is recorded.
