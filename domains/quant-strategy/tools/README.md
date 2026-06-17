# Quant Strategy Tools

## Realtime Public Source Checker

Use `realtime-public-source-checker.js` before writing a realtime public-source note.

Example:

```powershell
node D:\code\AI-Memory\domains\quant-strategy\tools\realtime-public-source-checker.js `
  --since 2026-06-03T12:30:34.033Z `
  --out D:\code\AI-Memory\domains\quant-strategy\work\realtime-public-source-latest.md
```

What it fixes:

- Reads X accounts through Jina Reader instead of relying only on direct `x.com` HTML.
- Uses the local Windows web stack for Jina Reader requests, which works better on machines whose network access depends on system proxy settings.
- Fetches individual `status` pages after the profile page exposes IDs.
- Derives X post time from the post ID snowflake, so missing visible timestamps do not automatically make the post unusable.
- Separates target-account posts, related official-account posts, reposts, and unreadable pages.
- For Xiaohongshu, checks the raw public HTML/SSR profile before falling back to Reader; the raw profile can expose visible note titles even when Reader only shows account metadata or login prompts.
- Writes a JSON diagnostics file next to the Markdown report so failures show which channel broke.

Evidence rules:

- Target-account `status` detail with matching author is high evidence for the public post fact.
- Related official NVIDIA handles from the `@nvidia` public timeline are medium-to-high evidence, but must be marked as not `@nvidia` original.
- Xiaohongshu raw-profile visible titles are low-to-medium evidence for topic/crowding only when note URL, timestamp, and body are missing. Do not treat them as full post facts.

## Institutional Research Checker

Use `institutional-research-checker.js` before writing the AQR / Citadel Securities / GMO / Man Group research-learning note.

Example:

```powershell
node D:\code\AI-Memory\domains\quant-strategy\tools\institutional-research-checker.js `
  --since 2026-06-08T14:21:03.357Z `
  --out D:\code\AI-Memory\domains\quant-strategy\work\institutional-research-latest.md
```

What it fixes:

- Reads official list pages through Jina Reader, so Citadel Securities is not marked unavailable just because direct browser access returns 403/security verification.
- Extracts official-domain article candidates from list pages.
- Fetches candidate detail pages separately, then classifies each item as `post_window_verified`, `pre_window_or_existing`, `date_unverified`, or `detail_blocked_no_date`.
- Writes a JSON diagnostics file next to the Markdown report so the automation can distinguish list-page visibility from detail-page blocking.

Evidence rules:

- Official-domain detail page with a stable title/date is high evidence for article existence.
- Official list page visibility with detail-page 403 is not enough for a new research framework; record it as a candidate or access limitation.
- Search/RSS snippets can help discover official URLs, but framework updates should be grounded in official-domain pages.

## Quote Workflow Smoke Test

Use the local quote clients before marking realtime quote data unavailable.

Node path:

```powershell
node -e "const {StockService}=require('D:/code/AI-Memory/skills/quant-stock-data/scripts/stock_service.js'); (async()=>console.log(JSON.stringify(await StockService.fetchQuotes(['MRVL','AMD','SPY','QQQ','SMH']),null,2)))()"
```

Python path:

```powershell
& 'C:\Users\lp\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -c "import sys,json; sys.path.insert(0, r'D:\code\AI-Memory\skills\quant-stock-data\scripts'); from resilient_stock_client import ResilientStockClient; print(json.dumps(ResilientStockClient().fetch_quotes(['MRVL','AMD','SPY','QQQ','SMH']), ensure_ascii=False, indent=2))"
```

What it fixes:

- Treats empty Tencent results as a failure rather than a completed empty quote set.
- Uses `Tencent -> Yahoo chart -> Sina` for U.S. tickers, so a local Sina `connect EACCES 198.18.0.42:443` error no longer kills the whole workflow.
- The Node quote client has its own transport fallback: `node:https -> PowerShell WebClient -> fetch`. A Node `AggregateError` is a transport failure, not proof that quotes are unavailable.
- Uses the Codex bundled Python path on Windows to avoid the Microsoft Store `python.exe` login-session stub.

Browser-visible fallback:

- If both local quote clients fail, or when a single ticker needs a quick sanity check, open a rendered Google Search or Google Finance stock card such as `https://www.google.com/search?q=RKLB` or `https://www.google.com/finance/quote/RKLB:NASDAQ`.
- Record the source as `Google browser-visible snapshot` with ticker, exchange, observed time, visible price, and visible percent change.
- Do not treat Google's redirect-only HTML as evidence; the price must be visible in the browser page or screenshot.
