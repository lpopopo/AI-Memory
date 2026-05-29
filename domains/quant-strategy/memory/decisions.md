# Decisions

## 2026-05-29

- Data source baseline: Tencent Smartbox for fuzzy search, Tencent quotes as primary, Sina quotes as fallback.
- All quote text responses should be decoded as GBK.
- Strategy analysis should consume normalized quote objects rather than raw endpoint payloads.
- Quote outputs should preserve `source` for debugging and data-quality review.
- Runtime caveat: old Node can fetch Tencent data but may not decode GBK Chinese names correctly without a decoder.
