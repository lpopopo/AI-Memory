# 2026-06-11 美股盘前策略报告

Date: 2026-06-11
Run time: 2026-06-11 20:30 Asia/Shanghai / 08:30 ET
Session context: premarket
Data freshness: 已读取本地 quant-strategy 记忆、规则、模板、最新 2026-06-10 realtime monitor；未发现 2026-06-11 当天 20:30 实时资讯任务产物。市场与新闻数据使用 2026-06-10 美股收盘及公开盘前新闻快照。
Report type: daily strategy

本报告面向 USD 20,000 模型组合的策略复盘与行动清单；不登录券商、不提交真实订单、不虚构成交。用户已确认的真实账户仍只有 `1` 股 `MRVL`，成本 `USD 252.00`，必须和已退休的旧模型组合分开记录。

## 1. 执行摘要

```text
Market regime: stress
Fear score: 9-10 / 14
Cash target: 65%-75%
New buys: 不允许
Reduce/exit items: AMD、WDC、STX 为已触发或接近触发的 stop/reduce 复核；MRVL 真实 1 股进入价格核验后的 defensive/exit review
Primary themes: AI interconnect/custom silicon、AI memory/storage、AI compute；AI application layer 单独 watch-only
Main risk: AI/半导体从拥挤回撤升级为科技板块 correction，叠加 CPI、油价、伊朗冲突和利率压力
```

今天的策略不是寻找低吸机会，而是把风险状态从 `stress-leaning elevated` 上调到 `stress`，保持高现金、禁止所有新买入，并优先检查已有风险线。WDC 已收在 `490.09`，低于既定 `<500` 复核线；STX 已收在 `815.99`，低于 `<835` 复核线；AMD 已远低于既定 `492` 收盘止损。MRVL 没有拿到可靠的 2026-06-10 精确收盘价，但公开报道显示 Marvell 自 6 月 4 日以来大幅回撤，需要先核验是否触发 `<245` 或接近 `235` 失败线，不能继续写成普通 core hold。

## 2. 市场恐慌门控

| Indicator | Current state | Signal |
| --- | --- | --- |
| VIX level/change | MarketWatch 报道 2026-06-10 早盘 VIX `21.13`，较前一日继续处在长期均值上方；6 月 9 日曾冲到约 `21.80`。 | `elevated` 上沿，接近 `22` stress 阈值。 |
| VIX/VIX3M | 未取得可靠同日 VIX3M。 | 数据缺口；不得因此下调风险。 |
| SPY / S&P 500 | AP 报道 S&P 500 于 2026-06-10 收 `7,266.99`，跌 `1.6%`，连续两日下跌。 | 指数层面进入 stress 复核。 |
| QQQ / Nasdaq | Nasdaq Composite 收 `25,169.50`，跌 `2.0%`；AI/科技为主要拖累。 | 成长/AI beta 明显转弱。 |
| SMH/SOXX / SOX | MarketWatch 报道 SOX 自 6 月 3 日高点回撤 `12.3%`，XLK 自 6 月 2 日高点回撤 `10.9%`，科技进入 correction。 | 半导体趋势破坏，禁止新增。 |
| RSP/SPY / IWM | Russell 2000 跌 `1.1%`，弱于防御但好于 Nasdaq；前一日宽度曾优于大型科技。 | 不是全面 panic，但组合暴露主题明显更弱。 |
| HYG/LQD | 未取得可靠同日刷新。 | 信用数据缺口；维持保守。 |
| 利率/美元/油价/地缘 | WSJ 报道 CPI 同比 `4.2%`、10Y 约 `4.54%`、Brent 约 `93.10`，伊朗冲突推升能源和通胀压力。 | growth_duration_high，压制 AI 长久期估值。 |

Decision:

```text
fear_regime: stress
risk_multiplier: 40%
max_new_buy_exposure: 0%（框架 stress 可允许 10%，但今日 trend/flow/stop 均不支持新买）
cash_floor: 框架 45%；操作目标 65%-75%
```

## 3. Institutional overlays

```text
trend_aligned_entry: 全部新买入为 trend_broken；没有 4-5/5 的可执行候选。
flow_fragility: acute，AI/半导体拥挤回撤已经压低 XLK/SOX。
AI_quality/capex_cycle: MRVL/AMD/WDC/STX 均是 high capex-cycle sensitivity；真实 MRVL 1 股只允许按防守线管理。
factor_macro_exposure: growth_duration_high, momentum_reversal_high, theme_overlap_high, sleeve_correlation_high, consumer_backstop_fragility, geopolitical_energy_inflation_risk。
bottleneck_watch: optical/interconnect 和 storage 需求叙事仍在，但价格已经拒绝追涨；只能保留观察，不能加仓。
action impact: 所有新增买入归零；优先执行 stop/reduce/exit review；AI 应用层独立观察，不与 GPU/数据中心混写。
```

### 3.1 Flow-Fragility Score

| Component | Score | Evidence |
| --- | ---: | --- |
| Narrow leadership | 2 | 前期指数高度依赖 AI/半导体，回撤时 Nasdaq/XLK/SOX 明显弱。 |
| Semiconductor/AI concentration | 2 | SOX 自高点回撤 `12.3%`，AI 供应链领跌。 |
| Spot-up-vol-up or options crowding | 1 | VIX 维持 21 附近，AI 反弹被卖出；未取得期权流直接证据。 |
| Systematic/vol-control rebuild | 1 | 前期 VIX 从低位反弹，存在系统性去风险可能；缺 CTA 直接数据。 |
| Buyback window risk | 1 | CPI/Fed/财报与地缘事件周，回购支撑不确定。 |
| Hedging complacency | 2 | VIX 从上周低位快速回到 elevated，上行保护需求重建。 |
| Levered/thematic crowding | 2 | 持仓与观察池集中在 AI capex、storage、interconnect。 |
| **Total** | **11/14** | `acute` |

Interpretation:

```text
flow_fragility_state: acute
strategy_response: 不开新仓；先处理 correlated-risk、止损和现金。
```

## 4. 板块与主题领导力

| Theme / sector | Evidence | Action |
| --- | --- | --- |
| Broad indices | S&P 500 -1.6%、Dow -1.9%、Nasdaq -2.0%、Russell -1.1%。 | 风险偏空；提高现金。 |
| Technology / XLK | XLK 从 6 月 2 日高点回撤 `10.9%`，进入 correction。 | 不新增科技仓。 |
| Semiconductors / SMH/SOX | SOX 从 6 月 3 日高点回撤 `12.3%`。 | 半导体不允许趋势外低吸。 |
| AI compute | AMD 收 `452.40`，低于既定 `492` 止损；NVDA/AVGO 也受 AI beta 压力。 | AMD `exit-review / reduce-review`；其余 watch-only。 |
| AI interconnect / optical | MRVL 自 6 月 4 日以来大幅回撤；S&P 500 纳入与 Jensen Huang 叙事未能保护价格。 | 真实 1 股 MRVL 先核验收盘价，不加仓。 |
| AI memory / storage | WDC 收 `490.09`，STX 收 `815.99`，分别跌破 `<500` 和 `<835` 复核线。 | 从 defensive hold 下调为 `exit-review`。 |
| Cloud / AI factory | Oracle、SMCI、AI 数据中心融资/订单仍是热点，但高 capex 和融资敏感。 | 叙事观察，不买。 |
| AI application / data owners | AI 应用层需看 ARR、ACV、付费客户、留存、利润率和相对强度；今日没有独立买点。 | SNOW/CRWD/DDOG/NOW/CRM/ADBE/APP/PLTR watch-only。 |
| Physical AI / robotics | TSLA/TER/ROK/DE/ISRG 仍需公司级收入证据与趋势确认。 | watch-only。 |
| Defensive / non-AI leaders | 能源受油价支撑，部分防御板块相对抗跌。 | 仅作为市场风格观察，不为 USD 20,000 模型组合新增主题。 |

## 5. 实时热点新闻地图

| News item | Source/time | Tickers | Theme | Direction | Price confirms? | Thesis impact |
| --- | --- | --- | --- | --- | --- | --- |
| 美股 6 月 10 日大跌，S&P 500 -1.6%、Nasdaq -2.0%，AI 股票继续被抛售。 | AP, 2026-06-10 | SPY, QQQ, AI basket | 市场结构 | 偏空 | 是 | 市场从 elevated 上调到 stress。 |
| CPI 同比约 `4.2%`，油价/伊朗冲突强化通胀压力，10Y 约 `4.54%`。 | WSJ, 2026-06-10 | QQQ, growth, oil | 宏观/利率/油价/地缘 | 偏空成长 | 是 | 触发 growth_duration_high，不加 AI beta。 |
| VIX 维持 21 附近，较上周低位明显抬升。 | MarketWatch, 2026-06-10 | SPY, QQQ | 市场结构 | 偏空 | 是 | 保持高现金和 no-new-buy。 |
| XLK 进入 correction，SOX 自高点回撤 `12.3%`。 | MarketWatch, 2026-06-10 | XLK, SOX, MRVL, AMD, MU, INTC | AI 基建/半导体 | 偏空 | 是 | flow_fragility=acute。 |
| WDC/STX 因 AI storage bottleneck 获分析师上调目标价后继续回撤。 | IBD 2026-06-08 + MarketWatch 2026-06-10 | WDC, STX | AI memory/storage | 基本面多、价格空 | 价格拒绝 | 新闻只能保留 thesis watch，不能覆盖止损。 |
| MRVL S&P 500 纳入、Jensen Huang 叙事后仍大幅波动。 | Investopedia/MarketWatch, 2026-06-08/10 | MRVL | AI interconnect/custom silicon | 叙事多、价格弱 | 价格拒绝 | 从 core narrative 转为 risk-line 管理。 |
| 2026-06-11 当天 20:30 实时资讯任务产物缺失；最新本地实时监控仍为 2026-06-10。 | Local memory | n/a | 来源质量 | 中性 | n/a | 不使用未验证社媒/机构信息作为交易触发。 |

新闻纪律：新闻只能解释价格、触发观察或削弱/强化候选，不得绕过趋势、相对强度、恐慌门控、仓位集中度和止损规则。

## 6. 当前持仓复核

| Ticker | Role | AI class | Current action | Stop/reduce line | Trend/RS | Overlay impact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MRVL | 真实账户 1 股 starter；旧模型组合已退休 | cyclical_supplier / bottleneck | 先核验 2026-06-10 官方收盘；不加仓 | 真实 ledger：收盘 `<245` 必须 cut-or-wait review；接近 `235` 且 QQQ/SMH 弱为 thesis failure | S&P 500 纳入和 AI 叙事被价格波动削弱；未取得可靠同日精确收盘 | flow_fragility acute；capex-cycle high | `defensive hold / exit-review if close <245`；不能写普通 core hold。 |
| AMD | 旧模型风险复核；真实账户 watch-only | cyclical_supplier | 不加仓；若仍按旧模型跟踪，应优先 reduce/exit review | 既定 `<492` 收盘止损已被多日破坏；6/10 收 `452.40` | 明显弱于原规则 | growth_duration_high + theme_overlap_high | `exit-review / reduce-review`，不是 normal hold。 |
| WDC | 旧模型风险复核；真实账户 watch-only | cyclical_supplier | 不加仓；若仍按旧模型跟踪，应 exit review | 6/10 收 `490.09`，低于 `<500` 复核线 | AI storage 基本面叙事仍在，但价格破线 | storage bottleneck 叙事不能覆盖止损 | `exit-review`。 |
| STX | 旧模型风险复核；真实账户 watch-only | cyclical_supplier | 不加仓；若仍按旧模型跟踪，应 exit review | 6/10 收 `815.99`，低于 `<835` 复核线 | 高位回撤，单股价格对小账户尺寸过大 | 与 WDC 同源拥挤风险 | `exit-review`。 |

## 7. 候选股排序

今天没有可执行新买入。所有新买入都未通过 `market fear gate + trend_aligned_entry + relative strength + concentration + stop priority` 的组合要求。

| Rank | Ticker | Theme | AI class | Entry condition | Risk line | Max size | Reason |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| n/a | n/a | n/a | n/a | n/a | n/a | 0 | fear_regime=stress，flow_fragility=acute，已有持仓先处理止损。 |

Rejected or watch-only names:

| Ticker | Reason rejected | Recheck trigger |
| --- | --- | --- |
| MU/SNDK | memory/storage 同一拥挤链条；WDC/STX 已破线。 | SOX/QQQ 修复，storage 价格重新跑赢且 VIX 回落。 |
| NVDA/AVGO | AI 质量较高，但仍受 capex-cycle 与估值/拥挤影响。 | VIX <20、SOX 重回上升趋势、财报/指引与价格同步确认。 |
| GLW/LITE/COHR/CIEN/ALAB | optical/interconnect 叙事未消失，但 MRVL 回撤说明拥挤风险高。 | 放量 reclaim 或收盘支撑确认。 |
| CRWV/NBIS/APLD/SMCI | AI data-center 叙事强，但融资和 capex 敏感。 | 订单、融资成本、现金流和 RS 同时确认。 |
| SNOW/CRWD/DDOG/NOW/CRM/ADBE/APP/PLTR | AI 应用层必须独立监控；当前没有足够业绩验证和趋势确认。 | AI 收入/ARR/ACV、客户案例、利润率、价格相对 QQQ 同步改善。 |
| TSLA/TER/ROK/DE/ISRG | physical AI/robotics 仍以叙事或长期选项为主。 | 公司级收入证据和 trend-aligned entry。 |

## 8. 组合构建

```text
Active holdings count: 真实账户确认 1 个（MRVL）；旧 USD 20,000 模型组合已退休，仅作历史/规则复核。
Theme count: 真实账户 1 个主题；历史模型暴露集中在 AI capex / storage / compute。
Cash: 真实账户应保持高现金；USD 20,000 模型组合目标现金 65%-75%。
Largest position: 真实 MRVL 1 股，成本 USD 252.00；需核验当前市值。
Theme overlap: 历史模型高；真实账户当前低但主题单一。
Max new exposure allowed: 0%。
```

如果用户仍希望保留旧 USD 20,000 模型组合用于研究跟踪，今日应把 AMD/WDC/STX 从 defensive hold 下调为 exit-review，而不是继续当作普通持仓。真实账户层面不记录任何未确认成交。

## 9. 执行清单

| Priority | Action | Ticker | Trigger | Size | Notes |
| ---: | --- | --- | --- | --- | --- |
| 1 | No new buy | 全部候选 | stress gate + flow acute + trend broken | 0 | 包括看似便宜的 AI/半导体/存储。 |
| 2 | Price verification / exit review | MRVL 真实 1 股 | 官方收盘 `<245` 或接近 `235` 且 QQQ/SMH 弱 | 1 股复核，不自动下单 | 先核验价格，再由用户确认是否执行。 |
| 3 | Exit-review | AMD 历史模型 | 已远低于 `<492` | 不虚构成交 | 若继续跟踪模型，应优先处理。 |
| 4 | Exit-review | WDC 历史模型 | 收 `490.09`，低于 `<500` | 不虚构成交 | 分析师上调目标价不能覆盖价格破线。 |
| 5 | Exit-review | STX 历史模型 | 收 `815.99`，低于 `<835` | 不虚构成交 | 与 WDC 同源风险。 |
| 6 | Watchlist only | AI 应用层 | 需要业绩验证 + 指引 + 客户案例 + RS | 0 | 与 GPU/数据中心/AI 基建分开评估。 |

## 10. 策略反思

- 做对：高现金、禁止追涨、把新闻降级为观察项是正确的；AI 回撤升级证明不能用叙事覆盖门控。
- 漏项：2026-06-11 当天 20:30 实时资讯产物缺失，来源质量不完整；MRVL 精确收盘价仍需补齐。
- 集中度：历史模型过于集中在 AI capex cluster，今天集中度明显伤害组合；真实账户只有 1 股 MRVL，风险可控但仍需按线复核。
- 现金：现金显著有用，应提高到 65%-75%。
- 恐慌门控：没有过度保护；在 XLK/SOX correction 后，stress 判断比 elevated 更合适。
- Institutional overlays：有用，尤其是 `flow_fragility=acute` 和 `trend_aligned_entry=trend_broken`，直接阻止新买入。
- 假设变化：AI infrastructure 长期 capex 叙事未被证伪，但“高位拥挤时新闻利好不能追”的假设被强化。AI 应用层仍未获得可交易确认。

## 11. 记忆同步

```text
Daily detail file: domains/quant-strategy/memory/daily/2026-06-11-us-stock-premarket-strategy.md
Trade plan file: 未单独创建；今日执行清单内嵌，且无新订单
Portfolio file: 真实账户仍以 domains/quant-strategy/memory/daily/2026-06-10-model-portfolio-retired.md 和 real-position start 记录为准
Hypotheses updated: no
Decisions updated: no
References updated: no
Open todos: 补 2026-06-11 realtime monitor；核验 MRVL 2026-06-10/06-11 官方价格；若继续研究旧模型，处理 AMD/WDC/STX exit-review
```

Sources used:

- Local memory and rules: `summary.md`, `decisions.md`, `daily-summaries.md`, latest daily records, market fear framework, portfolio concentration rules, daily monitoring framework, daily strategy template, institutional checklist/scorecard, AI quality/capex classification.
- Local realtime product: latest available `2026-06-10-realtime-public-institutional-monitor.md`; no 2026-06-11 product found.
- AP, 2026-06-10: major U.S. index closes.
- MarketWatch, 2026-06-10: VIX, XLK/SOX correction, WDC/STX/AMD price evidence.
- WSJ, 2026-06-10: CPI, oil, Iran conflict, 10Y yield context.
- IBD, 2026-06-08/10: storage analyst target hikes and AI/futures caution.
- Investopedia, 2026-06-08/10: MRVL S&P 500 inclusion and premarket macro/company headlines.
