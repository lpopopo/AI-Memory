# Strategic Reflection: Quant Portfolio Execution & System Drift (June 2026)

This document presents a comprehensive, high-level strategic reflection on the execution history of the Quant Strategy in the real account. By examining the entire memory timeline (from May 29 to June 19, 2026), we identify structural frictions, behavioral biases, and execution drift that separate our real-account outcomes from our 20-year systematic backtests.

---

## 1. Capital Baseline Volatility & "Position Anchoring Failure"

### The Issue
Over the past three weeks, the active capital baseline has been adjusted three times:
* **May 29**: HKD 40,000 baseline (~USD 5,128)
* **June 11**: Reduced to HKD 20,000 baseline (~USD 2,564)
* **June 19**: Increased to HKD 50,000 baseline (~USD 6,410)

In a systematic quantitative strategy, position sizing (e.g., 8-12% for core, 3-5% for satellites) is calculated directly as a percentage of the capital baseline. Frequent baseline changes cause **Position Anchoring Failure**:
1. **Relative Weights Distortion**: A core position of 1 share of MRVL (bought at $289.50) represented **11.3%** of the HKD 20,000 account. When the baseline was upgraded to HKD 50,000, this position’s weight automatically shrank to **4.5%**—converting it from a core holding to a satellite weight without any transaction occurring.
2. **Exposure Drag**: To restore MRVL to its core weight of 10%, the strategy must buy more shares. This forces us to "average up" at higher prices ($310.58), increasing our average cost basis and exposure risk. If we do not buy, the account remains under-exposed, creating an index-tracking drag.

### Strategic Correction
We must decouple active trading execution from raw cash inflows/outflows. 
* **Rule**: When capital increases/decreases, we do not automatically adjust existing holdings unless they drift more than 30% from their target weight. We apply the new sizing rules *only* to fresh entries (e.g., the TTMI and MXL orders planned on June 19 follow the HKD 50,000 sizing).

---

## 2. Quant Backtesting vs. Discretionary Thematic Drift

### The Issue
Our V5/V7 strategies achieved a ~20% CAGR over a 20-year backtest window ([compare_v5_v6_v7_20yr_summary.md](file:///D:/code/AI-Memory/domains/quant-strategy/experiments/2026-05-29-dual-sleeve-backtest/results/compare_v5_v6_v7_20yr_summary.md)). This performance relies on **strict, mechanical execution** of momentum z-scores, weekly rebalancing, and instant stop-loss orders.

In practice, our real-account execution has drifted significantly toward **Discretionary Thematic Trading**:
1. **Manual Watchlist Additions**: Adding RDW (Space), GLW (Fiber), and TTMI (PCB) was driven by qualitative analysis of Xiaohongshu/X content and institutional research overlays, rather than pure mechanical z-score rankings.
2. **Execution Discretion**: RDW fell below its $14.50 stop line on June 17, but instead of an instant cut, it was held through June 18 for "manual review."
3. **Implication**: We cannot expect the statistical benefits of the V7 backtest (such as the -31.05% max drawdown protection) if we apply subjective overrides to entries and exits.

### Strategic Correction
We must formally recognize that our active strategy is a **Hybrid Quantitative-Discretionary Strategy** (量化初筛 + 主观主题过滤 + 手动风控). 
* **Rule**: Quantitative indicators (V5/V7 scorecards) serve as the *initial filter* and *risk rails*, but the final trade execution must follow a structured **Discretionary Checklist** that explicitly documents why we are deviating from the strict model.

---

## 3. The "Notional Sizing Blindspot" in Small Accounts

### The Issue
Our portfolio concentration rules limit speculative satellite positions to **3% - 5%** of the account. However, in a USD 6,400 account:
* 1 share of **WDC** (~$794) represents **12.3%** of the account.
* 1 share of **ALAB** (~$417) represents **6.5%** of the account.

Because the minimum transaction size is **1 share**, we cannot execute a 3% satellite position in high-priced stocks. This forces a binary choice: either completely skip these market leaders (creating FOMO and tracking error), or buy 1 share and accept a highly concentrated risk exposure (12%) for a speculative name.

### Strategic Correction
We must establish a **Notional Ceiling Rule** in our [decisions.md](file:///D:/code/AI-Memory/domains/quant-strategy/memory/decisions.md):
* **Rule**: For accounts under USD 10,000, individual stocks with a share price > USD 300 are **strictly prohibited** from the satellite sleeve. They may only be held in the core sleeve, where a 10%-15% weight is appropriate. Satellites must be restricted to lower-priced names (e.g., MXL at $88 or RDW at $14) where 1-2 shares represent a true 3%-5% weight.

---

## 4. Macro Fear Gate vs. Micro Ticker-Level Stops

### The Issue
The Market Fear Gate ([market-fear-technical-framework.md](file:///D:/code/AI-Memory/domains/quant-strategy/references/market-fear-technical-framework.md)) classifies the market regime based on VIX and index drawdowns. 
* On June 18, the Fear Gate was **Normal** (VIX = 16.40), giving the portfolio a 100% risk multiplier.
* However, at the micro level, RDW experienced an absolute trend breakdown and broke its stop-loss.

A "Normal" macro regime can lull us into a false sense of security, encouraging us to hold or "average down" on declining individual stocks because "the broad market is healthy." This is a classic behavioral trap.

### Strategic Correction
We must formalize the hierarchy of risk controls:
* **Rule**: **Stock-specific stop-loss rules always take absolute precedence over the Macro Fear Gate.** The Fear Gate can only *restrict* exposure (e.g., lowering maximum exposure in stress/panic), it can never *relax* or override an individual stock's stop-loss execution. If a stop-loss is hit, it must be executed immediately, regardless of how bullish the macro Fear Gate is.
