# Data Sources

## Current Baseline

Use the local Codex skill `quant-stock-data` for the canonical data-source guide.

Core source plan:

- Smart fuzzy search: Tencent Smartbox, `https://smartbox.gtimg.cn/s3/?v=2&q=[keyword]&t=all`
- Primary real-time quote: Tencent, `https://qt.gtimg.cn/q=[symbols]`
- Fallback real-time quote: Sina, `https://hq.sinajs.cn/list=[symbols]`
- Historical daily K-line: Tencent flashdata daily endpoint
- Intraday minute data: Tencent flashdata minute endpoint

## Implementation Notes

- Decode responses with GBK.
- Do symbol normalization before requests.
- Browser-side Sina fallback is limited because scripts cannot set `Referer`.
- Older Node runtimes may lack GBK `TextDecoder`; use Node 18+/modern browsers, or add a GBK decoder when readable Chinese names are required.
- Store source names in quote objects to support later strategy diagnostics.
