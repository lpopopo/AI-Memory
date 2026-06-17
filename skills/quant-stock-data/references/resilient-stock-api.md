# Resilient Stock API System

This reference captures the current stock data-source plan for quant-strategy work: Tencent Smartbox fuzzy search plus Tencent/Yahoo/Sina quote resilience.

## Endpoint Matrix

| Business function | Endpoint | Method | Header constraints | Encoding |
| --- | --- | --- | --- | --- |
| Smart fuzzy search | `https://smartbox.gtimg.cn/s3/?v=2&q=[keyword]&t=all` | GET | No special header, CORS supported | GBK |
| Real-time quote, primary | `https://qt.gtimg.cn/q=[symbols]` | GET | No special header, CORS supported | GBK |
| U.S. quote fallback | `https://query1.finance.yahoo.com/v8/finance/chart/[ticker]?range=1d&interval=1m` | GET | No special header usually required | UTF-8 JSON |
| Real-time quote, last resort | `https://hq.sinajs.cn/list=[symbols]` | GET | Needs `Referer: https://finance.sina.com.cn/` in backend/client environments that allow it | GBK |
| Browser-visible fallback | Google Search / Google Finance stock card, e.g. `https://www.google.com/search?q=RKLB` or `https://www.google.com/finance/quote/RKLB:NASDAQ` | Browser | Requires visible browser rendering; not a stable API | HTML/JS |
| Historical daily K-line | `https://data.gtimg.cn/flashdata/[category]/latest/daily/[symbol].js` | GET | No special header, CORS supported | GBK |
| Intraday minute trend | `https://data.gtimg.cn/flashdata/[category]/minute/[symbol].js` | GET | No special header, CORS supported | GBK |

## Symbol Normalization

Normalize user input before fetching:

- `sh600519`, `sz000002`, `hk00700`, `usAAPL` are accepted as already-prefixed symbols.
- Six-digit A-share codes beginning with `6` or `9` become `shxxxxxx`.
- Other six-digit A-share codes become `szxxxxxx`.
- One-to-five digit numeric codes become Hong Kong symbols padded to five digits, for example `700` -> `hk00700`.
- Pure alphabetic symbols become U.S. symbols, for example `AAPL` -> `usAAPL`.

## Quote Shape

Return normalized quote objects with at least:

```json
{
  "symbol": "USMRVL",
  "name": "Marvell Technology, Inc.",
  "price": 0,
  "yesterdayClose": 0,
  "open": 0,
  "changePercent": 0,
  "high": 0,
  "low": 0,
  "volume": 0,
  "source": "Tencent (Primary)"
}
```

## Tencent Parsing Notes

Endpoint: `https://qt.gtimg.cn/q=usMRVL,usAMD`

Response lines look like `v_usMRVL="..."`. Split the quoted payload by `~`.

Common fields:

- `fields[1]`: name
- `fields[3]`: current price
- `fields[4]`: yesterday close
- `fields[5]`: open
- `fields[6]`: volume
- `fields[32]`: change percent
- `fields[33]`: high
- `fields[34]`: low

## Yahoo Parsing Notes

Endpoint: `https://query1.finance.yahoo.com/v8/finance/chart/MRVL?range=1d&interval=1m`

Use this before Sina for U.S. tickers when Tencent fails or returns no usable rows.

Common fields:

- `chart.result[0].meta.regularMarketPrice`: latest or close snapshot
- `chart.result[0].meta.previousClose` or `chartPreviousClose`: previous close
- `chart.result[0].indicators.quote[0]`: open, high, low, close, volume arrays

The latest minute arrays can be sparse after hours or post-close, so fall back to `regularMarketPrice` for the main price.

## Sina Parsing Notes

Endpoint: `https://hq.sinajs.cn/list=sh600519,hk00700`

Response lines look like `var hq_str_sh600519="..."`. Split the quoted payload by comma.

Common A-share fields:

- `fields[0]`: name
- `fields[1]`: open
- `fields[2]`: yesterday close
- `fields[3]`: current price
- `fields[4]`: high
- `fields[5]`: low
- `fields[8]`: volume in shares; divide by 100 for lots

Compute `changePercent = (price - yesterdayClose) / yesterdayClose * 100` when `yesterdayClose > 0`.

## Google Browser Snapshot Notes

Use Google Search or Google Finance only as a browser-visible fallback or sanity check, not as the primary automated API.

Examples:

- Search card: `https://www.google.com/search?q=RKLB`
- Finance card: `https://www.google.com/finance/quote/RKLB:NASDAQ`

Record:

- ticker and exchange shown on the card
- visible price
- visible change or percent change
- observed time and timezone
- source label: `Google browser-visible snapshot`

Do not treat a bare Google redirect HTML response as a usable quote. The price must be visible in the rendered browser page or screenshot.

## Smartbox Search

Endpoint: `https://smartbox.gtimg.cn/s3/?v=2&q=[keyword]&t=all`

Response contains `v_hint="..."`. Split by `^`, then split each item by `~`.

Map fields:

- `fields[0] + fields[1]`: symbol, for example `sh600519`
- `fields[2]`: name
- `fields[3]`: pinyin or abbreviation
- `fields[0].toUpperCase()`: market
- `fields[4]`: type, such as `GP-A`, `GP`, or `ZS`

## Caveats

- Browser JavaScript cannot manually set the `Referer` header. Sina fallback should run server-side, in Node, Python, or behind a proxy.
- For U.S. tickers, prefer `Tencent -> Yahoo -> Sina`. Sina can fail with local proxy errors such as `connect EACCES 198.18.0.42:443`; do not let that error erase a usable Yahoo fallback.
- In Node on Windows, each source request should try `node:https -> PowerShell WebClient -> fetch`. `AggregateError` usually means the first transport path failed, not that the quote source has no data.
- Treat an empty result array from any source as a source failure and continue down the hierarchy.
- Google Search/Finance can expose a useful real-time stock card in the browser, but it is not a stable machine API. Use it after local quote clients fail, or as a one-ticker sanity check before preparing order prices.
- On Windows, avoid the Microsoft Store `python.exe` stub for smoke tests. Use a real interpreter path, such as Codex's bundled Python, when running `scripts/resilient_stock_client.py`.
- `TextDecoder('gbk')` is required for Chinese names. Modern browsers normally support it, but older Node runtimes may not. In old Node, use Node 18+ or add a GBK decoding library such as `iconv-lite` if readable Chinese names are required.
- These endpoints can change without notice. Strategy logic should tolerate empty results, partial symbol failure, and field drift.
- Always log the selected source and error path during strategy debugging.
