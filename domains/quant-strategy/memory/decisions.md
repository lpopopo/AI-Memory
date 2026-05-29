# Decisions

## 2026-05-29

- Data source baseline: Tencent Smartbox for fuzzy search, Tencent quotes as primary, Sina quotes as fallback.
- All quote text responses should be decoded as GBK.
- Strategy analysis should consume normalized quote objects rather than raw endpoint payloads.
- Quote outputs should preserve `source` for debugging and data-quality review.
- Runtime caveat: old Node can fetch Tencent data but may not decode GBK Chinese names correctly without a decoder.
- Repository memory model: use layered storage with root-level `docs/`, `domains/`, `skills/`, `templates/`, and `archive/`. Stable conclusions live in `memory/decisions.md`; running notes live in `memory/strategy-log.md`; factual contracts live in `references/`; reusable workflows live in `skills/`.
- Strategy market focus: prioritize US-listed stocks and ETFs first. Treat A/H/other markets as later extensions, not the initial strategy target.
- Initial strategy direction: build a daily, long-only, medium-frequency US equity strategy before adding complex alternative data or intraday execution.
