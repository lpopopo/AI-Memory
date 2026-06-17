# Data Sources

## Current Baseline

Use the local Codex skill `quant-stock-data` for the canonical data-source guide.

Core source plan:

- Smart fuzzy search: Tencent Smartbox, `https://smartbox.gtimg.cn/s3/?v=2&q=[keyword]&t=all`
- Primary real-time quote: Tencent, `https://qt.gtimg.cn/q=[symbols]`
- U.S. quote fallback: Yahoo Finance chart endpoint, `https://query1.finance.yahoo.com/v8/finance/chart/[ticker]?range=1d&interval=1m`
- Last-resort fallback quote: Sina, `https://hq.sinajs.cn/list=[symbols]`
- Browser-visible U.S. quote fallback: Google Search or Google Finance stock card, for example `https://www.google.com/search?q=RKLB` or `https://www.google.com/finance/quote/RKLB:NASDAQ`
- Historical daily K-line: Tencent flashdata daily endpoint
- Intraday minute data: Tencent flashdata minute endpoint

## Implementation Notes

- Decode Tencent/Sina responses with GBK.
- Do symbol normalization before requests.
- Treat an empty quote array as a source failure and continue to the next source.
- For U.S. tickers, use `Tencent -> Yahoo chart -> Sina` rather than `Tencent -> Sina`; this avoids repeated `connect EACCES 198.18.0.42:443` failures when Sina is blocked by the local proxy path.
- The Node client has a transport fallback inside each source request: `node:https -> PowerShell WebClient -> fetch`. If automation logs a Node `AggregateError`, retry through the same Node client after this fallback-enabled version rather than declaring local quotes unavailable.
- If local Node/Python quote paths fail or a sanity check is needed for a single ticker, open the Google Search or Google Finance stock card in a browser and record it as `Google browser-visible snapshot`, with ticker, exchange, observed time, visible price, and visible percent change. This is not a stable API and should not be scraped as the primary automated path.
- Browser-side Sina fallback is limited because scripts cannot set `Referer`.
- On Windows, prefer the Codex bundled Python executable or another real Python interpreter; the Microsoft Store `python.exe` stub can fail before the quote client starts.
- Older Node runtimes may lack GBK `TextDecoder`; use Node 18+/modern browsers, or add a GBK decoder when readable Chinese names are required.
- Store source names in quote objects to support later strategy diagnostics.
