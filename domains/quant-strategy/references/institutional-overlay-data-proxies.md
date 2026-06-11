# Institutional Overlay Data Proxies

Date created: 2026-06-08

Purpose: define practical data proxies for the institutional overlay scorecard when direct hedge-fund-grade data is unavailable.

Status: experimental data contract. Use these proxies in daily reports and backtests until better sources are available.

## 1. Flow-Fragility Proxies

### Narrow Leadership

Preferred:

- Percentage of S&P 500 constituents outperforming SPY over 20 or 30 trading days.
- Percentage of Nasdaq 100 constituents outperforming QQQ over 20 or 30 trading days.

Fallback:

- RSP/SPY 21-day return.
- QQEW/QQQ 21-day return, if equal-weight Nasdaq proxy is available.
- Count of active AI watchlist names outperforming QQQ and SMH.

Score guide:

- `0`: equal-weight proxies outperform or keep pace.
- `1`: equal-weight proxies lag by 1%-3%.
- `2`: equal-weight proxies lag by more than 3% or only a few mega-cap leaders drive gains.

### Semiconductor / AI Concentration

Preferred:

- SMH or SOXX return versus QQQ.
- Top 10 AI watchlist contribution to active-universe gains.

Fallback:

- SMH/QQQ 21-day return.
- AI basket equal-weight return versus QQQ.

Score guide:

- `0`: leadership is broad across sectors.
- `1`: AI/semis lead but other sectors participate.
- `2`: AI/semis dominate while broader market or equal-weight proxies lag.

### Options / Crowding Behavior

Preferred:

- Nasdaq and semiconductor implied volatility versus spot.
- Put/call ratio, skew, single-name options premium, or options volume.

Fallback:

- VIX level/change.
- VXN or QQQ implied volatility if available.
- Qualitative public reports about retail/options concentration.
- Price behavior: strong rally with rising implied vol, or sharp reversal after call-driven extension.

Score guide:

- `0`: normal vol response.
- `1`: some upside call demand or skew flattening.
- `2`: spot-up-vol-up, heavy call demand, or visibly crowded upside chase.

### Systematic / Vol-Control Exposure

Preferred:

- CTA exposure model.
- Vol-control exposure estimates.

Fallback:

- Recent index rally after volatility compression.
- SPY/QQQ above short-term trend with VIX falling rapidly.
- Public commentary on systematic exposure.

Score guide:

- `0`: low or recently delevered exposure.
- `1`: exposure likely rebuilding.
- `2`: exposure likely high after sharp rally and volatility compression.

### Buyback Window Support

Preferred:

- Corporate buyback blackout/open-window calendar.
- Actual buyback execution estimates.

Fallback:

- Earnings-season calendar.
- Approximate blackout windows before quarterly reporting.

Score guide:

- `0`: open window supportive.
- `1`: support may fade soon.
- `2`: blackout or weaker buyback support.

### Hedging Complacency

Preferred:

- Index skew.
- Put/call ratios.
- Downside implied volatility relative to upside volatility.

Fallback:

- VIX low versus realized risk.
- Public commentary on cheap hedges or collapsed downside demand.

Score guide:

- `0`: hedges normal or expensive.
- `1`: hedges cheaper.
- `2`: downside protection appears unusually cheap or under-owned.

### Levered / Thematic Crowding

Preferred:

- Levered ETF AUM and flows by theme.
- Semiconductor/technology thematic ETF flows.

Fallback:

- Public commentary on levered ETF concentration.
- Strong retail or ETF-driven flow into same theme.

Score guide:

- `0`: low or normal concentration.
- `1`: moderate concentration.
- `2`: high concentration in owned theme.

## 2. Trend-Aligned Entry Proxies

Use daily OHLCV:

- 20-day moving average.
- 50-day moving average.
- 200-day moving average.
- Relative strength versus QQQ.
- Relative strength versus theme basket.
- Volume on pullback or reclaim day.

Fallback when intraday data is incomplete:

- Use official close only.
- Mark the signal `unknown` rather than forcing a positive score.

## 3. AI Quality / Capex-Cycle Proxies

Preferred:

- Revenue growth and segment revenue.
- Gross margin and operating margin.
- Free cash flow.
- Net cash or debt.
- Customer concentration.
- Backlog, bookings, RPO, ARR/ACV where relevant.
- Management guidance tied to AI demand.

Fallback:

- Latest earnings-summary notes.
- Public company presentations.
- Analyst consensus revisions.
- Repeated supply-chain evidence, clearly marked as lower quality than revenue evidence.

## 4. Factor-Macro Exposure Proxies

Growth/duration:

- QQQ/SPY.
- Long-duration growth basket versus SPY.
- 10-year Treasury yield change.

Inflation/value:

- IWD/IWF or value/growth ETF ratio.
- XLE/XLF/XLI leadership.
- Oil and 10-year yield changes.

Momentum reversal:

- VIX falling after stress.
- High prior 20/63-day momentum.
- Sudden outperformance by laggards or low-quality catch-up basket.

Theme overlap:

- Holdings mapped to the same AI capex chain.
- Pairwise correlation or same-day drawdown clustering.

Consumer backstop fragility:

- Retail sales trend.
- Consumer confidence.
- Personal savings rate.
- Serious delinquency rates for credit cards, auto loans, or consumer credit.
- Gasoline/energy price shocks.
- Consumer discretionary versus staples relative strength.
- Equal-weight consumer discretionary versus mega-cap consumer/platform leaders.

K-shaped consumption risk:

- Equity-market wealth concentration.
- Luxury/high-income spending resilience versus mass-market weakness.
- Credit stress concentrated in lower-income or lower-credit-score cohorts.
- Market leadership dependent on top-income consumer or equity-wealth effects.

## 5. Data Quality Labels

Every overlay reading should include one of:

- `high`: direct data source and current timestamp.
- `medium`: public proxy is available but indirect.
- `low`: qualitative inference only.
- `unknown`: do not score unless necessary; explain the gap.

## 6. Daily Minimum Viable Overlay

If time is limited, collect only:

- VIX level/change.
- SPY/QQQ/SMH returns and trend.
- RSP/SPY breadth proxy.
- Active AI basket returns.
- Current position stop/near-stop table.
- News/catalyst confirmation or rejection.

This is enough to flag obvious theme-crowding risk even without options or CTA data.
