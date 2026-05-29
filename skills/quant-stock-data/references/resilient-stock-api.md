# Resilient Stock API System

This reference captures the current stock data-source plan for 量外策略 work: Tencent Smartbox fuzzy search plus Tencent/Sina dual-source quote resilience.

## Endpoint Matrix

| Business function | Endpoint | Method | Header constraints | Encoding |
| --- | --- | --- | --- | --- |
| Smart fuzzy search | `https://smartbox.gtimg.cn/s3/?v=2&q=[keyword]&t=all` | GET | No special header, CORS supported | GBK |
| Real-time quote, primary | `https://qt.gtimg.cn/q=[symbols]` | GET | No special header, CORS supported | GBK |
| Real-time quote, fallback | `https://hq.sinajs.cn/list=[symbols]` | GET | Needs `Referer: https://finance.sina.com.cn/` in backend/client environments that allow it | GBK |
| Historical daily K-line | `https://data.gtimg.cn/flashdata/[category]/latest/daily/[symbol].js` | GET | No special header, CORS supported | GBK |
| Intraday minute trend | `https://data.gtimg.cn/flashdata/[category]/minute/[symbol].js` | GET | No special header, CORS supported | GBK |

## Symbol Normalization

Normalize user input before fetching:

- `sh600519`, `sz000002`, `hk00700`, `usAAPL` are accepted as already-prefixed symbols.
- Six-digit A-share codes beginning with `6` or `9` become `shxxxxxx`.
- Other six-digit A-share codes become `szxxxxxx`.
- One-to-five digit numeric codes become Hong Kong symbols padded to five digits, for example `700` -> `hk00700`.
- Pure alphabetic symbols become US symbols, for example `AAPL` -> `usAAPL`.

## Quote Shape

Return normalized quote objects with at least:

```json
{
  "symbol": "SH600519",
  "name": "贵州茅台",
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

Endpoint: `https://qt.gtimg.cn/q=sh600519,hk00700`

Response lines look like `v_sh600519="..."`. Split the quoted payload by `~`.

Common fields:

- `fields[1]`: name
- `fields[3]`: current price
- `fields[4]`: yesterday close
- `fields[5]`: open
- `fields[6]`: volume
- `fields[32]`: change percent
- `fields[33]`: high
- `fields[34]`: low

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

## Smartbox Search

Endpoint: `https://smartbox.gtimg.cn/s3/?v=2&q=茅台&t=all`

Response contains `v_hint="..."`. Split by `^`, then split each item by `~`.

Map fields:

- `fields[0] + fields[1]`: symbol, for example `sh600519`
- `fields[2]`: name
- `fields[3]`: pinyin or abbreviation
- `fields[0].toUpperCase()`: market
- `fields[4]`: type, such as `GP-A`, `GP`, or `ZS`

## Caveats

- Browser JavaScript cannot manually set the `Referer` header. Sina fallback should run server-side, in Node, Python, or behind a proxy.
- `TextDecoder('gbk')` is required for Chinese names. Modern browsers normally support it, but older Node runtimes may not. In old Node, use Node 18+ or add a GBK decoding library such as `iconv-lite` if readable Chinese names are required.
- These endpoints can change without notice. Strategy logic should tolerate empty results, partial symbol failure, and field drift.
- Always log the selected source and error path during strategy debugging.
