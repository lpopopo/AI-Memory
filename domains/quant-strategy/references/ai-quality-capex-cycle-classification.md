# AI Quality and Capex-Cycle Classification

Date created: 2026-06-08

Purpose: classify AI-linked US equities by business resilience, capex-cycle sensitivity, and current strategy role. This file supports candidate ranking and position sizing; it is not a buy list.

Status: initial qualitative classification. Update after earnings, guidance, relative-strength evidence, and backtest results.

## Classification Rules

### Platform / Hyperscaler

Traits:

- Diversified revenue base.
- Strong cash flow and balance sheet.
- Controls or funds AI capex directly.
- AI upside is meaningful but not the only business driver.

Typical sizing:

- Can become core if valuation, trend, and market fear allow.
- Lower capex-cycle fragility than pure suppliers, but still rate-sensitive.

### Diversified Supplier

Traits:

- Benefits from AI buildout.
- Has multiple customers, product lines, or non-AI revenue support.
- Can compound through several AI cycles if margins and order visibility hold.

Typical sizing:

- Core or satellite depending on relative strength, customer concentration, and valuation.

### Cyclical Supplier

Traits:

- Strong upside during capex acceleration.
- Revenue or valuation can reset quickly if hyperscaler growth capex pauses.
- Often exposed to hardware cycles, inventory cycles, or customer concentration.

Typical sizing:

- Usually satellite or tactical core only during confirmed leadership.
- Needs stricter trims after vertical extensions.

### Application / Data Owner

Traits:

- Monetizes AI through workflow, data control, pricing, retention, or productivity.
- Needs evidence of revenue, ARR/ACV, margins, paid usage, or customer expansion.

Typical sizing:

- Watchlist until revenue and relative strength confirm.
- Can become core if AI monetization is proven and price confirms.

### Speculative Bottleneck Beneficiary

Traits:

- Strong narrative tied to optical, interconnect, power, cooling, memory, storage, robotics, or edge AI.
- Revenue durability, margin capture, or customer concentration may be unclear.

Typical sizing:

- Watchlist or small satellite only.
- Cannot become core without earnings/guidance confirmation and price leadership.

## Initial Ticker Map

| Ticker | Primary class | Capex-cycle sensitivity | Strategy role now | Notes |
| --- | --- | --- | --- | --- |
| MSFT | platform_hyperscaler | medium | watch/core candidate | Strong enterprise/software/cloud AI exposure; monitor valuation and AI margin burden. |
| GOOGL | platform_hyperscaler | medium | watch/core candidate | Search/cloud/data owner; AI capex is large but diversified cash flow helps resilience. |
| AMZN | platform_hyperscaler | medium | watch/core candidate | AWS plus retail cash flow; monitor cloud AI monetization and capex intensity. |
| META | platform_hyperscaler | medium | watch/core candidate | Ads and AI infrastructure; capex risk exists but core cash generation is strong. |
| ORCL | platform_cloud / AI_factory | medium-high | watch | Cloud infrastructure, database, and AI capacity/backlog exposure; monitor capex burden, margin, debt, and durable AI revenue conversion. |
| NVDA | diversified_supplier | high | core watch, not automatic buy | AI leader but still exposed to hyperscaler capex expectations and crowded positioning. |
| AVGO | diversified_supplier | medium-high | core watch | Custom silicon/networking/software mix may be more diversified than pure accelerator exposure. |
| QCOM | diversified_supplier / edge_inference | medium-high | watch | Mobile, handset, automotive, PC, and edge-AI inference exposure; needs device-cycle recovery, AI monetization evidence, and RS confirmation. |
| INTC | cyclical_supplier / foundry_turnaround | high | watch/satellite only | AI PC, x86 server, foundry, and turnaround optionality; execution, margin, roadmap, and competitive risk require strict confirmation. |
| AMD | cyclical_supplier | high | active reduce-review in current memory | AI accelerator upside but execution and relative strength must confirm; current stop breach requires review. |
| MRVL | cyclical_supplier / bottleneck | high | existing position, profit-protection bias | Custom silicon/interconnect exposure; high theme upside but crowded and capex-sensitive. |
| MU | cyclical_supplier | high | watch | Memory cycle leverage; needs storage/memory pricing and RS confirmation. |
| WDC | cyclical_supplier | high | existing defensive hold | Storage bottleneck exposure; close to risk zone in current memory. |
| STX | cyclical_supplier | high | existing defensive hold | Storage bottleneck exposure; close to risk zone in current memory. |
| SNDK | cyclical_supplier | high | watch | Storage/memory cycle exposure; validate liquidity and data quality. |
| ALAB | speculative_bottleneck | high | watch/satellite only | AI interconnect narrative; requires revenue durability and valuation discipline. |
| LITE | speculative_bottleneck | high | watch | Optical component exposure; validate earnings and relative strength. |
| COHR | speculative_bottleneck | high | watch | Optical/compound semiconductor exposure; monitor balance sheet and margin volatility. |
| CIEN | diversified_supplier / bottleneck | medium-high | watch | Networking/optical exposure; needs AI data-center revenue confirmation. |
| NOK | network_infrastructure / edge_ai | medium | watch | Telecom/network infrastructure and private-network edge-AI optionality; requires order growth, margin evidence, and price leadership before any trade role. |
| GLW | diversified_supplier / bottleneck | medium | watch | Optical/fiber exposure; more diversified but AI revenue pass-through must be verified. |
| CRWV | speculative_bottleneck / platform | high | watch | AI cloud exposure; likely high capex and financing sensitivity. |
| NBIS | speculative_bottleneck / platform | high | watch | AI infrastructure exposure; needs durable revenue and financing validation. |
| RKLB | speculative_space / edge_ai_infrastructure | high | watch/satellite only | Space launch, satellite systems, and edge/satellite infrastructure optionality; high volatility and financing/execution risk require strict price and revenue confirmation. |
| RDW | speculative_space / satellite_infrastructure | high | watch/satellite only | Space infrastructure, satellite components, and national-security/space-economy optionality; requires backlog, revenue quality, margin, debt/financing, and RS confirmation. |
| SNOW | application_data_owner | medium | watch only | AI data platform thesis; require AI revenue/retention and RS confirmation. |
| CRWD | application_data_owner | medium | watch only | Security data and AI workflow potential; track ARR, margins, and RS. |
| DDOG | application_data_owner | medium | watch only | Observability/data workflow; needs AI monetization evidence. |
| NOW | application_data_owner | medium | watch/core candidate | Workflow owner; AI monetization evidence and valuation matter. |
| CRM | application_data_owner | medium | watch | Enterprise data/workflow; needs margin and AI product monetization proof. |
| ADBE | application_data_owner | medium | watch | Creative AI monetization must overcome competitive/pricing concerns. |
| APP | application_data_owner | medium-high | watch | AI ad-tech monetization; high momentum/crowding risk possible. |
| PLTR | application_data_owner | high | watch/satellite only | AI narrative and government/commercial data platform; valuation/crowding risk high. |
| TSLA | application/physical_ai | high | watch/satellite only | Autonomous/robotics option value; car-cycle, margin, execution, and valuation risk remain high. Reaffirmed as watchlist-only per user request on 2026-06-11. |
| TER | application/physical_ai | medium-high | watch | Robotics/automation test exposure; needs cycle and RS confirmation. |
| ROK | application/physical_ai | medium | watch | Industrial automation; slower AI monetization but potentially more diversified. |
| DE | application/physical_ai | medium | watch | Autonomy/agtech exposure but cyclical macro sensitivity. |
| ISRG | application/physical_ai | medium | watch/core candidate | Robotics healthcare quality angle; AI link must be evidence-based, not narrative-only. |

## Current Portfolio Implications

As of the latest 2026-06-08 memory state:

- AMD is no longer a normal hold; it is an active reduce-review item because its prior stop level was breached.
- MRVL remains an existing AI bottleneck position but should be treated with profit-protection discipline after crowding stress.
- WDC and STX remain defensive holds, not fresh adds, because both were near risk zones after the 2026-06-05 storage/AI selloff.
- New AI application-layer names remain watch-only until revenue evidence and price relative strength confirm.

## Update Fields

When updating this classification, record:

- Latest earnings or guidance evidence.
- AI revenue or capex linkage.
- Customer concentration.
- Balance sheet and financing pressure.
- Relative strength versus QQQ and relevant theme basket.
- Current market fear regime.
- Current flow-fragility state.
