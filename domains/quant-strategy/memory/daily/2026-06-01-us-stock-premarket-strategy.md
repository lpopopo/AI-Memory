# 2026-06-01 US Stock Premarket Strategy

Run time: 2026-06-01 20:49 Asia/Shanghai / 08:49 ET.

Purpose: weekday premarket recommendation for a hypothetical USD 20,000 account. This is research planning, not guaranteed return or personalized financial advice. The account is assumed to have no confirmed fills because brokerage positions were not provided.

## 1. Real-Time Hot News

| Category | Source / recency | News | Related tickers / sectors | Read-through | Price confirmation | Horizon |
| --- | --- | --- | --- | --- | --- | --- |
| Macro / oil / geopolitics | Reuters Morning Bid, 2026-06-01 | U.S.-Iran strikes resumed; Strait of Hormuz traffic remains constrained. Brent rose about 3% to around USD 94 and WTI about 4% to around USD 91. | XLE, broad equities, long-duration technology | Mixed: energy benefits, but inflation and rate risk rise. | Confirmed by oil and U.S. 10Y yield near 4.47%. | Medium-term risk if shipping disruption persists. |
| Liquidity / risk appetite | Reuters / market pages, 2026-06-01 premarket | Dow, S&P 500, and Nasdaq 100 futures were up roughly 0.2%-0.3% despite oil. VIX was around 15.84. | SPY, QQQ, SMH | Mildly bullish but narrow. | Confirmed by positive futures; contradicted by rising VIX and oil. | Short-term until ISM and jobs data. |
| AI infrastructure | Reuters / Computex, 2026-06-01 | Nvidia and Microsoft introduced RTX Spark for AI PCs. Nvidia was up about 1.6% premarket; Microsoft about 2.8%; AMD and Intel fell about 3.4% and 2.9% in the Reuters snapshot. ARM also rallied sharply in later reports. | NVDA, MSFT, ARM, AMD, INTC, QCOM | Bullish for NVDA/MSFT/ARM; bearish catalyst for x86 PC exposure. | Confirmed by premarket dispersion. | Medium-term watch item, but product adoption still needs validation. |
| AI export controls | Reuters, updated 2026-05-31 22:37 ET | U.S. Commerce guidance closes a loophole for advanced AI-chip exports to subsidiaries of China-headquartered firms outside China. | NVDA, AMD, semiconductor supply chain | Mixed-to-bearish for compute vendors with China exposure. | AMD weakness confirms caution; NVDA strength shows Computex catalyst is offsetting it. | Medium-term regulatory overhang. |
| Earnings / guidance | Reuters and Dell earnings call, 2026-05-28 to 2026-05-29 | Dell raised FY2027 AI-server revenue outlook to about USD 60B; infrastructure solutions revenue jumped strongly. | DELL, NVDA, storage, networking, SMH | Bullish for AI factory, storage, and networking demand. | Confirmed by Dell's large post-earnings rally and tech leadership on 2026-05-29. | Medium-term thesis strengthening. |
| Earnings / guidance | Marvell earnings, 2026-05-27 | MRVL Q1 revenue USD 2.42B and EPS USD 0.80 modestly beat estimates; Q2 revenue midpoint USD 2.70B exceeded consensus. | MRVL, optical / custom silicon | Bullish fundamental update. | Mixed: stock initially sold off after earnings, then recovered to USD 205 on 2026-05-29. | Medium-term thesis strengthening; execution remains price-sensitive. |
| Analyst / positioning | UBS commentary, 2026-05-26; Situational Awareness filing covered 2026-06-01 | UBS raised MU target sharply on long-term supply agreements. Situational Awareness LP disclosed a 5.6% NBIS stake. | MU, WDC, STX, SNDK, NBIS, cloud / AI factory | Bullish, but crowded. | Confirmed by MU rally and storage-group premarket strength; NBIS trades near highs. | Medium-term thesis support, not a chase signal. |

News remains an explanation and candidate trigger. It does not override trend, relative-strength, fear-gate, concentration, or stop-loss rules.

## 2. Market Fear / Risk State

The local Python executable could not run `market_fear.py`, so today's gate uses equivalent latest public data plus the last validated close:

- Latest web VIX: about `15.84`, below the framework's elevated threshold of `16`, but rising with Gulf headlines.
- Last validated close on 2026-05-29: regime `normal`, score `0`, VIX/VIX3M about `0.82`, SPY/QQQ/SMH trends intact, breadth and credit stable.
- Premarket confirmation: index futures modestly positive; U.S. 10Y about `4.47%`; Brent around `94`; WTI around `91`.
- Classification: `normal` with event-risk caution.
- Framework risk multiplier: `100%`.
- Framework cash floor: `5%`.
- Operational cash target: `55%-65%` because AI leadership is crowded, oil is rising, and today's chip tape is highly dispersed.

## 3. Daily Market Monitoring

### Index / Sector State

- Previous session: major U.S. indices closed at records. On 2026-05-29 technology led (`XLK +2.23%`) and financials followed (`XLF +0.60%`).
- Previous-session laggards: `XLP -1.85%`, `XLE -1.11%`, `XLY -0.97%`, `XLV -0.93%`, `XLRE -0.92%`, `XLU -0.47%`, `XLI -0.39%`, `XLB -0.37%`.
- Premarket: energy should be monitored for a geopolitical reversal because oil jumped; technology remains supported by Nvidia but internal breadth is narrower.
- `SMH` / `SOXX`: AI semiconductor leadership remains structurally strong, but today's AMD/INTC weakness means semiconductor exposure must be selected stock by stock.
- `XLC`: no fresh leadership confirmation found before the open.

### AI Infrastructure Themes

| Theme | State | Leaders / watch names | Action |
| --- | --- | --- | --- |
| Optical / custom silicon / networking | Strong but selective | MRVL, CLS, CIEN, LITE, COHR | Keep MRVL as the preferred executable name; keep others watch-only. |
| Storage / memory bottleneck | Strong and crowded | MU, WDC, STX, SNDK | Use pullback limits only for WDC/STX; do not chase MU/SNDK. |
| Compute / inference / AI PC | Strong but rotating | NVDA, ARM, AVGO, AMD, INTC | NVDA/ARM are event leaders; AMD pauses pending stabilization; INTC remains excluded. |
| Cloud / AI factory | Strong | DELL, NBIS, MSFT, AMZN, META | DELL/NBIS move to watchlist only because entry risk is high after sharp runs. |

### Active Pool Emotion Distribution

- Risk-on: futures are positive and AI infrastructure remains the dominant capital-allocation theme.
- Narrow / crowded: previous-session sector leadership was concentrated in technology; storage leaders are extended.
- Event-sensitive: oil, yields, and chip export rules can quickly reverse expensive technology.
- Notable winners: NVDA, MSFT, ARM, MU, WDC, DELL, CLS, NBIS.
- Notable losers / relative laggards: AMD, INTC; CIEN remains weaker than the preferred core list.

## 4. Concentrated Portfolio Rule

- Active target: `3-4` executable positions today, below the normal `4-6` target because event risk is high.
- Hard maximum: `8`.
- Active themes: `2` for executable orders: optical/custom silicon and storage.
- AI compute stays watch-only until AMD stabilizes or NVDA/ARM provide a lower-risk setup.
- Avoid small scattered buys in MU, SNDK, ARM, ALAB, CIEN, DELL, CLS, and NBIS.

## 5. Review of Previous Recommendations

| Ticker | Prior plan | Review | Today |
| --- | --- | --- | --- |
| MRVL | USD 2,600 at 202 / 199 / 195; reduce below 194 | 2026-05-29 close around USD 205. Thesis improved after earnings, but post-earnings reaction was mixed. | Keep staged limits; do not chase. |
| AMD | USD 2,400 at 511 / 505 / 492; reduce below 492 | 2026-05-29 close USD 516.02. Today's Nvidia AI-PC launch and export-control news created premarket weakness. | Cancel automatic limits; observe stabilization first. |
| WDC | USD 2,000 at 528 / 520 / 508; reduce below 500 | 2026-05-29 close USD 531.21. Storage group remains strong; WDC was indicated up about 1% premarket in a public market-news report. | Keep pullback-only limits. |
| STX | USD 2,000 at 878 / 860 / 840; reduce below 835-840 | 2026-05-29 close USD 879.80. Entry zone is close, but the storage trade is crowded. | Keep smaller pullback-only limits. |
| CIEN | Watch only | Weaker relative behavior than MRVL; no clean new price confirmation found. | Watch only. |
| INTC | Optional 3%-5% satellite | 2026-05-29 close USD 114.68; Nvidia's AI-PC launch creates a direct competitive headline and premarket weakness. | Remove from executable pool. |

No fills are assumed. If orders were already placed, reconcile brokerage fills before using today's plan.

## 6. Today's Operations

### Executable Limit Orders

| Ticker | Direction | Max amount | Weight | Staged limit orders | Stop / invalidation |
| --- | --- | ---: | ---: | --- | --- |
| MRVL | Buy on pullback | USD 2,600 | 13% | USD 900 at `202`; USD 900 at `199`; USD 800 at `195` | Stop adding and reduce if daily close `<194`, or if QQQ and SMH both lose 20-day trend. |
| WDC | Buy on pullback | USD 2,000 | 10% | USD 700 at `528`; USD 700 at `520`; USD 600 at `508` | Reduce if daily close `<500`, or if MU/WDC/STX broadly reverse after a gap-up. |
| STX | Buy on pullback | USD 1,400 | 7% | USD 500 at `872`; USD 500 at `855`; USD 400 at `835` | Reduce if daily close `<835`; do not add after a gap-up extension. |

Maximum executable deployment today: `USD 6,000 / 30%`. Maintain at least `USD 11,000 / 55%` cash after fills; unallocated capital remains deliberate.

### Observe Only

| Ticker | Status | Activation condition |
| --- | --- | --- |
| AMD | Observe only; cancel old automatic limits | Reconsider only after the first 30-60 minutes if it reclaims `505-511`, export-control selling stabilizes, and QQQ/SMH remain constructive. Maximum later allocation: USD 1,600 / 8%. |
| NVDA | Observe only | Event leader, but do not chase a Computex gap. Wait for consolidation. |
| ARM | Observe only | Sharp event move; wait for a multi-session base. |
| MU / SNDK | Observe only | Memory leaders are too extended. Wait for pullback or consolidation. |
| CIEN / LITE / COHR / ALAB | Observe only | Promote only after relative strength improves versus MRVL and SMH. |
| DELL / CLS / NBIS | Observe only | AI-factory thesis strengthened, but recent gaps make risk/reward unattractive for a fresh entry. |
| INTC | Avoid | Direct competitive headline and weak premarket price action invalidate the tactical satellite setup. |

## 7. Strategy Reflection

- The concentration rule helped: it prevented an automatic INTC satellite buy before a direct competitive catalyst.
- The fear gate remains useful but insufficient by itself. VIX can stay calm while oil and single-stock dispersion rise, so the execution layer must keep a larger tactical cash buffer.
- The prior AMD rule was too static for an event-driven open. Repair: require a stabilization/reclaim condition before activating orders when a core name gaps down on new competitive or regulatory news.
- Storage remains a valid medium-term bottleneck theme, but crowding argues for lower STX size and pullback-only orders.
- No stable framework file needs revision yet. Re-evaluate the event-gap execution repair after several daily observations.

## Sources

- Reuters Morning Bid via Investing.com: https://ca.investing.com/news/economy-news/morning-bid-who-needs-oil-when-theres-ai-to-buy-4667586
- Reuters futures report via Yahoo Finance: https://uk.finance.yahoo.com/news/wall-street-futures-gain-ai-095009105.html
- Reuters export-control report via Investing.com: https://m.investing.com/news/stock-market-news/us-takes-step-to-halt-nvidia-ai-chip-shipments-to-chinese-firms-outside-china-4717939?ampMode=1
- Dell Reuters coverage: https://www.marketscreener.com/news/dell-raises-annual-forecasts-as-ai-data-center-buildout-fuels-demand-ce7f5ddade8cf024
- MRVL earnings: https://www.investing.com/news/earnings/marvell-earnings-beat-by-001-revenue-topped-estimates-4713140
- Previous-session sector recap: https://deanfi.com/insights/marketpulse/2026-05-29
- WDC 2026-05-29 close: https://www.marketbeat.com/stocks/NASDAQ/WDC/
- STX 2026-05-29 close: https://www.marketbeat.com/stocks/NASDAQ/STX/
- AMD 2026-05-29 close: https://www.marketbeat.com/stocks/NASDAQ/AMD/
- INTC 2026-05-29 close: https://www.marketbeat.com/stocks/NASDAQ/INTC/
