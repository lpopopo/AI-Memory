# 2026-07-01 Full Watchlist Unification

User requested that every symbol already present in the codebase manual watchlist be promoted to formal self-selected status and included in analysis.

## Scope decision

- Included: the 31 tradable symbols in `tools/us_stock_scanner.py` manual watchlist.
- Excluded from self-selected status: the separate 516-stock S&P 500 / Nasdaq-100 historical constituent database. It remains the broad research and ranking universe.
- Context-only: `SPCX` / SpaceX, because it is not a public tradable ticker.

## Canonical self-selected universe

`DRAM`, `MU`, `WDC`, `STX`, `SNDK`, `MRVL`, `AVGO`, `ALAB`, `COHR`, `LITE`, `AAOI`, `MXL`, `AXTI`, `CRDO`, `SMCI`, `ORCL`, `TER`, `ASML`, `AMAT`, `KLAC`, `LRCX`, `RKLB`, `RDW`, `TSLA`, `QCOM`, `NVDA`, `AMD`, `INTC`, `GLW`, `NOK`, `TTMI`.

Canonical source: `references/user-selected-watchlist.json`.

## Code and analysis changes

- The scanner now loads the canonical JSON with a hardcoded fallback for resilience.
- Removed the old scanner line that discarded `SNDK`, so every canonical tradable symbol is retained.
- Added `user_selected_watchlist` and `watchlist_analysis` to scanner JSON output.
- Added a full-watchlist Markdown table with price, MA50, MA200, 21/63-day momentum, trend state and screen state.
- Names with missing data remain visible as `data_unavailable`; names failing V6/V7 remain visible as repair/defensive or trend watch.

This update changes monitoring coverage only. It does not create orders or convert all 31 names into buy candidates.

## Verification

Verification at 2026-07-01 00:28 Asia/Shanghai used the local resilient quote/chart workflow:

- Canonical symbols: 31.
- Structured realtime quotes returned: 31/31.
- One-year daily chart data returned: 31/31.
- Missing quote/chart symbols: none.
- Trend state: 19 above both MA50 and MA200; 9 below MA50 but above MA200 / repairing; 3 below MA200.

The bundled Python environment available in this thread does not include the scanner's pre-existing `yfinance` dependency, so the full Python Top 10/Top 5 job was not rerun here. Syntax compilation, canonical-list loading and SNDK retention were verified separately, and current full-list quote/chart coverage was verified through the local Node quote client without installing new system dependencies.
