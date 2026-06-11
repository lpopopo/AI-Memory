# 2026-06-11 美股盘前策略报告

Date: 2026-06-11
Run time: 2026-06-11 20:48 Asia/Shanghai / 08:48 ET
Session context: premarket
Data freshness: 已读取 quant-strategy 记忆、规则、模板、最近 daily 记录、2026-06-11 20:32 实时公共/机构监控产物，并刷新公开盘前行情与新闻。
Report type: daily strategy

本报告面向 USD 20,000 模型组合的策略框架和风险语言，但当前真实账户持仓只承认用户/券商确认记录：`MRVL` 1 股，成本 `USD 252.00`。旧 USD 20,000 模型账本已退休，`AMD`、`WDC`、`STX` 只作为历史模型/回放风险复核对象，不当作当前真实持仓。本报告不登录券商、不提交订单、不虚构成交。

## 1. 执行摘要

```text
Market regime: stress, with premarket rebound
Fear score: about 9 / 14
Cash target: 65%-75%
New buys: 不允许
Reduce/exit items: 历史模型 AMD、WDC、STX 维持 reduce/exit-review；真实 MRVL 为 defensive hold / near-stop monitor
Primary themes: AI interconnect/custom silicon、AI memory/storage、AI compute；AI application layer 单独 watch-only
Main risk: AI capex 拥挤交易在利率、油价/地缘、融资和高 capex 质疑下继续去风险
```

今天的核心动作是继续防守，而不是把盘前反弹当成重新买入信号。6 月 10 日正式收盘显示 SPY -1.58%、QQQ -2.00%、SMH -3.40%、SOXX -3.67%，AI/半导体链条仍是压力中心。6 月 11 日盘前 SPY、QQQ、SMH、SOXX 和 MRVL 等出现反弹，但这只把真实 `MRVL` 从隔夜警戒拉回 defensive hold，并不能取消 `AMD <492`、`WDC <500`、`STX <835` 的正式收盘复核。

优先级：不新增任何买入；核对真实 `MRVL` 是否仍有旧 `315` 限价单；若继续研究旧模型，`AMD/WDC/STX` 只能写 `reduce-review` 或 `exit-review`，不能写普通持有。

## 2. 市场恐慌门控

| Indicator | Current state | Signal |
| --- | --- | --- |
| VIX level/change | MarketWatch 6 月 10 日早盘 VIX `21.13`，高于长期均值且较上周 15 附近明显抬升；6 月 9 日曾冲至 `21.80`。 | elevated 上沿，贴近 stress 阈值。 |
| VIX/VIX3M | 未取得可靠同日 VIX3M。 | 数据缺口；不能据此下调风险。 |
| SPY trend/drawdown | SPY 6 月 10 日收 `725.43`，日跌 `1.58%`；6 月 11 日盘前 `728.85`，仅小幅修复。 | 大盘压力仍在，盘前反弹不足以解除 stress。 |
| QQQ trend/drawdown | QQQ 6 月 10 日收 `693.69`，日跌 `2.00%`；盘前 `699.19`。 | 成长/AI beta 仍弱。 |
| SMH/SOXX trend/drawdown | SMH 收 `570.91`，日跌 `3.40%`，盘前 `585.99`；SOXX 收 `541.51`，日跌 `3.67%`，盘前 `553.30`。 | 半导体正式收盘破坏，盘前反弹先看修复，不追。 |
| Breadth proxy | RSP 收 `206.53`，日跌 `1.27%`，相对 SPY 略好；Russell 也相对 Nasdaq 抗跌。 | 不是全面 panic，但组合主题更弱。 |
| Credit proxy | HYG 收 `79.47`，LQD 收 `108.16`，HYG/LQD 日内大致稳定。 | 信用没有同步崩坏；支持 stress 而非 panic。 |
| Macro/rates/oil | CPI 同比约 `4.2%`、10Y 约 `4.54%`、伊朗风险和油价波动仍压制长久期成长股；6 月 11 日盘前油价回落、收益率回落。 | 宏观短线缓和，但 growth_duration_high 仍在。 |

Decision:

```text
fear_regime: stress
risk_multiplier: 40%
max_new_buy_exposure: 框架上限 10%，今日操作上限 0%
cash_floor: 框架 45%，操作目标 65%-75%
```

## 3. Institutional Overlays

```text
trend_aligned_entry: trend_broken；所有新买入得分 0-2/5，不进入候选排序。
flow_fragility: acute；AI/半导体/存储正式收盘仍显示拥挤交易回撤。
AI_quality/capex_cycle: MRVL/AMD/WDC/STX 都是 high capex-cycle sensitive；ORCL 证明 AI 需求强，但也证明 capex/融资会被市场惩罚。
factor_macro_exposure: growth_duration_high, momentum_reversal_high, theme_overlap_high, sleeve_correlation_high, consumer_backstop_fragility, geopolitical_energy_inflation_risk。
bottleneck_watch: optical/interconnect、memory/storage、cloud AI factory 仍是长期观察主题；价格未确认前只能 watch。
action impact: 阻止所有新增 AI/半导体/存储/应用层买入；先处理 stop/reduce 和现金纪律。
```

### 3.1 Flow-Fragility Score

| Component | Score | Evidence |
| --- | ---: | --- |
| Narrow leadership | 2 | 前期指数高度依赖 AI/半导体，回撤时 Nasdaq/XLK/SOX 明显更弱。 |
| Semiconductor/AI concentration | 2 | SMH/SOXX 6 月 10 日跌幅显著大于 SPY/RSP。 |
| Spot-up-vol-up or options crowding | 1 | VIX 在 21 附近，AI 反弹频繁被卖；缺少期权流直接数据。 |
| Systematic/vol-control rebuild | 1 | VIX 从低位快速回升，存在系统性降风险可能。 |
| Buyback window risk | 1 | CPI、Fed、财报和地缘窗口叠加，回购支撑不确定。 |
| Hedging complacency | 2 | VIX 从上周低位快速抬升，保护需求重建。 |
| Levered/thematic crowding | 2 | 历史模型和观察池集中在 AI capex、storage、interconnect。 |
| **Total** | **11/14** | `acute` |

Interpretation:

```text
flow_fragility_state: acute
strategy_response: 不开新仓；先做相关性风险、止损和现金复核。
```

## 4. 板块与主题领导力

| Theme / sector | Evidence | Action |
| --- | --- | --- |
| Broad indices | 6 月 10 日 SPY/QQQ 下跌，6 月 11 日盘前反弹。 | 只视为修复，不视为风险解除。 |
| Technology / XLK | 科技板块受 AI capex、估值和融资压力拖累。 | 不新增科技仓位。 |
| Semiconductors / SMH/SOXX | 正式收盘跌幅最大，盘前弹性也大。 | 等正式收盘修复；不追盘前。 |
| AI compute | AMD 正式收盘 `452.40`，远低于 `492` 风险线。 | AMD `exit-review / reduce-review`。 |
| AI interconnect / optical | MRVL 收 `252.59`，盘前 `263.32`，仍是高 beta 事件波动。 | 真实 1 股 `defensive hold`；不加仓。 |
| AI memory / storage | WDC 收 `490.09`，STX 收 `815.99`，分别低于 `500`/`835` 复核线；盘前反弹不足以取消正式破线。 | `exit-review / reduce-review`。 |
| Cloud / AI factory | Oracle OCI/RPO 强劲，但股价因 capex、负自由现金流、融资和软件业务弱项下跌。 | AI 基建需求确认，但高 capex 股不能自动买。 |
| AI application / data owners | Adobe 将在盘后发布业绩；应用层必须看 ARR/ACV、付费客户、留存、利润率和相对强度。 | SNOW/CRWD/DDOG/NOW/CRM/ADBE/APP/PLTR watch-only。 |
| Physical AI / robotics | TSLA/TER/ROK/DE/ISRG 仍需公司级收入证据和趋势确认。 | watch-only。 |
| Defensive / non-AI leaders | RSP 相对 SPY 略好，能源/防御在宏观扰动中相对抗跌。 | 只作为市场风格观察，不新增模型主题。 |

## 5. 实时热点新闻地图

| News item | Source/time | Tickers | Theme | Direction | Price confirms? | Thesis impact |
| --- | --- | --- | --- | --- | --- | --- |
| 美股 6 月 10 日大跌后，6 月 11 日盘前期货反弹，Nasdaq-100 futures 一度涨超 1%。 | WSJ / Investopedia, 2026-06-11 | SPY, QQQ | 市场结构 | 短线偏多 | 只在盘前确认 | 反弹降低 panic 风险，但不解除 stress。 |
| VIX 6 月 10 日早盘升至 `21.13`，仍高于长期均值。 | MarketWatch, 2026-06-10 | SPY, QQQ | 市场结构 | 偏空 | 是 | 保持高现金和 no-new-buy。 |
| CPI 同比约 `4.2%`、10Y 约 `4.54%`，伊朗冲突和油价扰动仍影响通胀预期。 | WSJ, 2026-06-10/11 | QQQ, growth, oil | 宏观/利率/油价/地缘 | 偏空成长 | 是 | `growth_duration_high` 继续有效。 |
| Oracle 云收入和 OCI 增速强劲，RPO 达 `638B`，但股价因 AI 数据中心 capex、融资和自由现金流压力下跌。 | WSJ / IBD / Barron's / MarketWatch, 2026-06-11 | ORCL, AI infra | AI 基建 / 财报指引 | 基本面多、价格空 | 价格拒绝 | 强化“AI 需求强不等于股票可买”。 |
| Goldman 认为 AI capex 规模可能比市场预期更大，但同时强调电力、数据中心、劳动力和估值波动风险。 | Business Insider, 2026-06-11 | AI basket | AI 基建 | 中性偏多叙事 | 需价格确认 | 只支持 bottleneck watch，不触发买入。 |
| 2026-06-11 20:32 本地实时公共/机构监控未验证任何新增 X、小红书、AQR、Citadel、GMO、Man post-window 条目。 | Local monitor, 2026-06-11 | n/a | 社媒/机构持仓与研究 | 中性 | n/a | 不把未验证社媒或机构内容映射为交易信号。 |

新闻纪律：新闻只能解释价格、触发观察或削弱/强化候选，不能绕过趋势、相对强度、恐慌门控、仓位集中和止损规则。

AI 应用层单独监控：`ADBE` 盘后财报属于应用/创意软件验证，不和 GPU、数据中心、AI 基建混为一类。后续只看业绩验证、公司指引、付费客户案例、行业趋势和市场叙事是否被价格与相对强度确认。

## 6. 当前持仓复核

| Ticker | Role | AI class | Current action | Stop/reduce line | Trend/RS | Overlay impact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MRVL | 真实账户 1 股 starter；旧模型已退休 | cyclical_supplier / bottleneck | 持有但不加仓；核对旧 `315` 限价单是否存在 | 真实 ledger：正式收盘 `<245` 必须 cut-or-wait review；靠近 `235` 且 QQQ/SMH 弱为 thesis failure | 收 `252.59`，盘前 `263.32`；事件波动仍大 | flow acute，capex-cycle high | `defensive hold / near-stop monitor`；不是普通 core hold。 |
| AMD | 历史模型风险复核；真实账户 watch-only | cyclical_supplier | 不加仓；若继续模型跟踪，优先 reduce/exit review | 既定 `<492` 收盘止损已多日破坏；6/10 收 `452.40`，盘前 `457.60` | 明显未修复 | growth_duration_high + theme_overlap_high | `exit-review / reduce-review`。 |
| WDC | 历史模型风险复核；真实账户 watch-only | cyclical_supplier | 不加仓；旧模型应 exit-review | 6/10 收 `490.09`，低于 `<500`；盘前 `496.26` 仍低于 500 | storage thesis 在，价格破线 | bottleneck 叙事不能覆盖止损 | `exit-review`。 |
| STX | 历史模型风险复核；真实账户 watch-only | cyclical_supplier | 不加仓；旧模型应 exit-review | 6/10 收 `815.99`，低于 `<835`；盘前 `839.00` 只是盘前修复 | 高位回撤；单股价格对小账户过大 | 与 WDC 同源拥挤风险 | `exit-review`；正式收盘重新站回 835 后才可降级为复核持有。 |

止损语言约束：已经触发正式收盘风险线的 `AMD/WDC/STX` 不得写成普通持有，除非另有明确规则覆盖理由。今天没有覆盖理由。

## 7. 候选股排序

今天没有可执行新买入。所有新买入均未通过 `market fear gate + trend_aligned_entry + relative strength + concentration + stop priority`。

| Rank | Ticker | Theme | AI class | Entry condition | Risk line | Max size | Reason |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| n/a | n/a | n/a | n/a | n/a | n/a | 0 | fear_regime=stress，flow_fragility=acute，已有风险线需先处理。 |

Rejected or watch-only names:

| Ticker | Reason rejected | Recheck trigger |
| --- | --- | --- |
| NVDA/AVGO | 质量较高但仍处 AI capex/crowding 风险，需正式收盘确认。 | VIX <20，SMH/SOXX 重新转强，财报/指引与价格同步确认。 |
| MU/SNDK | 与 WDC/STX 属同一 memory/storage 拥挤链条。 | storage basket 重新跑赢，WDC/STX 收盘修复风险线。 |
| GLW/LITE/COHR/CIEN/ALAB | optical/interconnect 叙事仍在，但 MRVL 波动说明拥挤风险高。 | 放量 reclaim 或收盘支撑确认。 |
| ORCL/CRWV/NBIS/APLD/SMCI | AI data-center 需求强，但 capex、融资、现金流敏感。 | 订单、融资成本、现金流、RS 同时确认。 |
| SNOW/CRWD/DDOG/NOW/CRM/ADBE/APP/PLTR | AI 应用层需要独立业绩验证，不能借 AI 基建叙事买入。 | AI 收入/ARR/ACV、客户案例、利润率和相对 QQQ 强度同步改善。 |
| TSLA/QCOM/NOK/RKLB/RDW | 新增观察池主题，尚无 trend-aligned entry。 | 公司级收入/订单证据 + 相对强度 + 风险门控降级。 |

## 8. 组合构建

```text
Active holdings count: 真实账户确认 1 个（MRVL）；旧 USD 20,000 模型组合只作历史/回放。
Theme count: 真实账户 1 个 AI interconnect/custom silicon；历史模型实质高度重叠于 AI capex 链。
Cash: USD 20,000 模型策略目标 65%-75%；真实账户现金以用户/券商回报为准。
Largest position: 真实 MRVL 1 股，成本 USD 252.00；按盘前 263.32 约占 HKD 20,000 账户约 10% 出头，未计费用和 FX。
Theme overlap: 真实账户低但单一；历史模型高。
Max new exposure allowed: 0%。
```

集中持仓规则要求 4-6 个活跃股票、最多 8 个、2-3 个主题。但在 stress + flow acute 下，重点不是补齐持仓数量，而是避免把同一 AI capex beta 扩大。

## 9. 执行清单

| Priority | Action | Ticker | Trigger | Size | Notes |
| ---: | --- | --- | --- | --- | --- |
| 1 | No new buy | 全部候选 | stress gate + flow acute + trend broken | 0 | 包括看似便宜的 AI/半导体/存储和 AI 应用层。 |
| 2 | Defensive monitor | MRVL 真实 1 股 | 正式收盘 `<245` 触发 cut-or-wait review；靠近 `235` 且 QQQ/SMH 弱则 thesis failure | 1 股复核，不自动下单 | 盘前回到 `263.32`，短线缓和，但仍不加仓。 |
| 3 | Confirm old order status | MRVL | 旧 `315` 真实限价单是否仍存在 | n/a | 只要求用户/券商确认，不虚构撤单或成交。 |
| 4 | Exit-review | AMD 历史模型 | 收盘仍远低于 `<492` | 不虚构成交 | 不能降级为普通 hold。 |
| 5 | Exit-review | WDC 历史模型 | 6/10 收 `490.09`，低于 `<500` | 不虚构成交 | 分析师/存储叙事不能覆盖破线。 |
| 6 | Exit-review | STX 历史模型 | 6/10 收 `815.99`，低于 `<835` | 不虚构成交 | 盘前 `839.00` 需要正式收盘确认。 |
| 7 | Watchlist only | AI 应用层 | 财报/ARR/ACV/客户案例/RS 未同步确认 | 0 | 与 GPU/数据中心/AI 基建分开评估。 |

## 10. 策略反思

- 做对：高现金、禁止追涨、把新闻降级为观察项是正确的；Oracle 证明 AI 需求强，但股价仍可因 capex 和融资压力下跌。
- 漏项：行情源仍依赖公开网页，VIX/VIX3M 缺口未解决；AI 应用层需要等待更多业绩验证。
- 集中度：真实账户集中度可控；旧模型集中在同一 AI capex 链条，在 stress 日会放大回撤。
- 现金：现金目标应维持 `65%-75%`，不要因盘前反弹降低。
- 恐慌门控：没有过度保护；正式收盘和 VIX 仍支持 `stress`。
- Institutional overlays：`flow_fragility=acute` 和 `trend_aligned_entry=trend_broken` 有效阻止了“便宜就买”的错误。
- 假设：AI infrastructure 长期 capex 叙事未被证伪，但“利好新闻不能覆盖价格拒绝和现金流风险”的假设被强化。AI 应用层仍 watch-only。

## 11. 记忆同步

```text
Daily detail file: domains/quant-strategy/memory/daily/2026-06-11-us-stock-premarket-strategy.md
Trade plan file: 未单独新增；执行清单内嵌，且无新订单
Portfolio file: 真实账户继续以 domains/quant-strategy/memory/portfolio/2026-06-11-real-portfolio-summary.md 为准
Hypotheses updated: no
Decisions updated: no
References updated: no
Open todos: 修复 VIX/VIX3M 与信用/宽度数据源；核对 MRVL 旧 315 限价单；下次正式收盘复核 MRVL 245/235、AMD 492、WDC 500、STX 835
```

Sources used:

- Local memory/rules: `summary.md`, `decisions.md`, `daily-summaries.md`, 2026-06-11 recent daily records, `market-fear-technical-framework.md`, `portfolio-concentration-rules.md`, `daily-market-monitoring-framework.md`, `us-stock-daily-strategy-report-template.md`, `institutional-overlays-daily-checklist.md`, `institutional-overlay-scorecard.md`, `ai-quality-capex-cycle-classification.md`.
- Local realtime product: `domains/quant-strategy/memory/daily/2026-06-11-realtime-public-institutional-monitor.md`, plus `work/realtime-public-source-latest.md` and `work/institutional-research-latest.md`.
- Market data: StockAnalysis quote pages for MRVL, AMD, WDC, STX, SPY, QQQ, SMH, SOXX, RSP, HYG, LQD, accessed 2026-06-11 20:30-20:45 Asia/Shanghai.
- News: WSJ, MarketWatch, IBD, Barron's, Investopedia, Business Insider public snippets accessed 2026-06-11.
