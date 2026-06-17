# 2026-06-12 美股盘前策略报告

Date: 2026-06-12
Run time: 2026-06-12 20:49 Asia/Shanghai / 08:49 ET
Session context: premarket
Data freshness: 已读取 quant-strategy 核心记忆、规则、模板、最近 daily 记录、2026-06-12 20:31-20:32 实时公共/机构监控产物；本地行情 Python 路径返回结构化 Tencent quote objects；Node 路径失败并保留源级错误。
Report type: daily strategy

本报告面向 `USD 20,000` 模型组合的策略框架，但真实账户持仓只承认用户或券商确认记录。当前确认真实股票持仓为零；最近真实交易是 `MRVL` 1 股以 `USD 267.020` 卖出，较 `USD 252.00` 买入价实现约 `USD +15.020` / `+5.96%` 的毛利润，未计费用和汇率。本报告不登录券商、不提交真实订单、不虚构成交。

## 1. 执行摘要

```text
Market regime: elevated / repair watch
Fear score: 5-6 / 14
Cash target: 60%-70% for the USD 20,000 model; real account remains cash until a fresh setup appears
New buys: today no immediate buy; only conditional watch after trend-aligned entry confirmation
Reduce/exit items: AMD remains reduce-review below 492; MRVL watch-only/no chase; WDC/STX defensive hold / repair review
Primary themes: AI interconnect/custom silicon, AI memory/storage, AI compute; AI application layer monitored separately
Main risk: one-day AI/semiconductor rebound after stress can fail if VIX, rates, oil/geopolitics, or AI capex financing concerns reverse
```

今天的策略从 `stress` 降到 `elevated / repair watch`，但不直接降为 `normal`。2026-06-11 正式收盘显示 SPY、QQQ、SMH/SOXX、RSP、IWM 与 HYG/LQD 同步修复，6 月 12 日盘前新闻也显示股指期货继续偏强、油价因美伊协议希望大跌、VIX 早盘约 `18.5`。这改善了系统性风险，但 AI/半导体/存储的反弹仍是高 beta 修复，不是无条件追买信号。

组合动作：真实账户继续空仓观察；USD 20,000 模型组合若用于策略演示，现金目标维持 `60%-70%`，不因单日强反弹把现金快速降到正常牛市水平。优先复核 `AMD <492` 的 reduce-review；`WDC/STX` 因重新站回 `500/835` 风险线，可从 exit-review 降为 `defensive hold / repair review`，但仍不新增；`MRVL` 已无真实持仓，`280.71` 收盘后的正确语言是 `watch only / no chase`。

## 2. 市场恐慌门控

本地行情质量：

- Node smoke test: 返回空数组并打印源级失败，`Tencent failed: AggregateError | Yahoo failed: AggregateError | Sina failed: connect EACCES 123.125.107.29:443`。按规则视为源失败，不视为“无行情”。
- Python smoke test: 使用 `C:\Users\lp\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` 成功返回结构化 quote objects，核心标的 `source=腾讯/Tencent`，数据质量为高；主要为 2026-06-11 正式收盘快照。
- 盘前方向补充：公开新闻显示 2026-06-12 美股期货偏强、油价大跌、VIX 早盘降至约 `18.5`，但这些是盘前/早盘方向，不替代正式收盘触发。

| Indicator | Current state | Signal |
| --- | --- | --- |
| VIX level/change | 2026-06-11 约 `19.9`；6 月 12 日早盘公开报道约 `18.5` | 从 stress 缓和到 elevated；低于 20 但仍需确认 |
| VIX/VIX3M | 未取得可靠同步 quote | 数据缺口；不得据此降为 normal |
| SPY trend/drawdown | Tencent: `737.76`, +1.70%, 前收 `725.43` | 广度修复，风险下降 |
| QQQ trend/drawdown | Tencent: `717.12`, +3.38%, 前收 `693.69` | 成长股强修复 |
| SMH/SOXX trend/drawdown | SMH `609.45`, +6.75%; SOXX `586.93`, +8.39% | 半导体强反弹，但高 beta |
| Breadth proxy | RSP `209.75`, +1.56%; IWM `290.41`, +2.96% | 反弹不只由少数大盘股驱动，panic 风险下降 |
| Credit proxy | HYG `79.94`, +0.59%; LQD `109.08`, +0.85%; HYG/LQD 约 `0.7329` | 信用无同步崩坏 |
| Macro/oil/rates | 公开新闻：油价因美伊协议希望下跌约 3%-5%；10Y 约 `4.46%-4.50%` | 油价缓和利好风险偏好，但利率仍高 |

Decision:

```text
fear_regime: elevated / repair watch
risk_multiplier: 70%
max_new_buy_exposure: framework 25%; today operational 0%-10% only after trend-aligned confirmation
cash_floor: framework 25%; operational cash target 60%-70%
```

## 3. Institutional overlays

```text
trend_aligned_entry: cheap_but_unconfirmed; broad rebound helps, but one repair close after synchronized AI drawdown is not enough for immediate buys
flow_fragility_score: 7/14 -> elevated
AI_quality/capex_cycle: MRVL/AMD/WDC/STX remain high capex-cycle sensitive; ORCL and ADBE show that AI demand without clean cash-flow/ARR conversion can be rejected by price
factor_macro_flags: growth_duration_high; momentum_reversal_high; theme_overlap_high; token_cost_elasticity; VIX_term_structure_data_gap
bottleneck_watch: optical/interconnect, memory/storage, cloud AI factory remain watch themes; token-cost economics added as AI adoption constraint
action impact: no chase buy; allow only support/reclaim entries after QQQ/SMH and stock-level RS confirm
```

### 3.1 Flow-Fragility Score

| Component | Score | Evidence |
| --- | ---: | --- |
| Narrow leadership | 1 | 6 月 11 日反弹较广，IWM/RSP 也上涨，但 AI/半导体弹性最大 |
| Semiconductor/AI concentration | 2 | SMH/SOXX 单日涨幅远高于 SPY，AI beta 仍主导风险 |
| Spot-up-vol-up or options crowding | 1 | VIX 回落但仍在刚脱离 20 区间，缺少期权流直接数据 |
| Systematic/vol-control rebuild | 1 | 强反弹后可能有系统性补仓，但尚未稳定 |
| Buyback window risk | 1 | 财报、地缘、利率窗口仍有不确定性 |
| Hedging complacency | 1 | VIX 下降改善情绪，但地缘结果未最终确认 |
| Levered/thematic crowding | 1 | watchlist 与历史模型仍集中于 AI capex / storage / interconnect |
| **Total** | **7/14** | `elevated` |

Interpretation:

```text
flow_fragility_state: elevated
strategy_response: 可从全面防守转为修复观察，但不追高；候选必须有支撑、reclaim 或第二日确认。
```

## 4. 板块与主题领导力

| Theme / sector | Evidence | Action |
| --- | --- | --- |
| Broad indices | SPY +1.70%, DIA +1.82%, IWM +2.96% | 市场从 stress 修复到 elevated |
| Technology / XLK | XLK `183.21`, +3.73% | 技术修复强，但仍受利率和 AI capex 约束 |
| Semiconductors / SMH | SMH +6.75%, SOXX +8.39% | 强修复；等待第二日确认，不追 |
| AI compute | NVDA +2.22%, AMD +7.97%, AVGO +3.62%, INTC +9.27% | 反弹确认主题弹性；AMD 仍低于 492 风险线 |
| AI interconnect / optical | MRVL +11.13%; QCOM +6.15%; NOK +5.15% | MRVL 只 watch；边缘/网络只观察 |
| AI memory / storage | MU +11.66%, WDC +8.00%, STX +6.38% | 存储链最强之一；WDC/STX 仅 repair review |
| Cloud / AI factory | ORCL `184.10`, -8.53% | AI 订单强不等于股价可买；capex/融资压力被价格惩罚 |
| AI application / data owners | ADBE -6.25%, NOW -2.81%, CRM -2.36%; CRWD +6.76%, DDOG +2.90% | 应用层分化，必须单独看 ARR/ACV、客户、利润和 RS |
| Physical AI / robotics / space | TSLA +4.60%, RKLB +9.26%, RDW +14.93% | 高波动 watch/satellite only |
| Defensive / non-AI leaders | XLU +0.11%, XLP -0.26%, XLRE -0.16% | 风险偏好回升时防御落后 |

## 5. 实时热点新闻地图

| News item | Source/time | Tickers | Theme | Direction | Price confirms? | Thesis impact |
| --- | --- | --- | --- | --- | --- | --- |
| 美股期货 6 月 12 日盘前继续上涨，市场尝试延续 6 月 11 日强反弹 | Investopedia / IBD / MarketWatch, 2026-06-12 | SPY, QQQ, DIA | 市场结构 | 偏多 | 盘前确认，待收盘确认 | 支持 elevated repair，不支持 normal |
| 油价因美伊协议希望大跌，Brent/WTI 回落约 3%-5% | Guardian / MarketWatch / WSJ, 2026-06-12 | XLE, inflation, QQQ | 宏观/油价/地缘 | 对成长股偏多 | 是，期货偏强 | 降低地缘通胀压力，但协议未最终签署 |
| VIX 早盘降至约 `18.5` | Barron's, 2026-06-12 | SPY, QQQ | 市场结构 | 偏多 | 是 | 风险降级至 elevated，但 VIX/VIX3M 仍缺口 |
| Adobe Q2 超预期并上调全年展望，但因 AI freemium 短期 ARR 压力、CFO 离任、竞争担忧下跌 | WSJ / IBD / Barron's, 2026-06-11/12 | ADBE | AI 应用层 / 财报指引 | 基本面多、价格空 | 价格拒绝 | 应用层必须看收入质量、ARR 和管理层稳定，不因 AI 叙事买入 |
| Adobe CFO Dan Durn 将去 Marvell | WSJ / Barron's / IBD, 2026-06-11/12 | ADBE, MRVL | AI 应用层 vs AI 基建人才流 | MRVL 情绪偏多，ADBE 偏空 | MRVL 前日已强涨；ADBE 跌 | 对 MRVL 只是观察催化，不是追买理由 |
| Nvidia 据称准备向中国推出 Vera CPU | Investopedia, 2026-06-12 | NVDA, semis | AI compute / 出口限制 | 偏多 | 需后续价格和政策确认 | 支持 AI compute watch，不绕过风险门控 |
| 2026-06-12 20:31 本地实时公共/机构监控未验证新的 X、小红书、AQR、Citadel、GMO、Man post-window 条目；Citadel `Tokenomics` 为补录框架 | Local monitor, 2026-06-12 | AI basket | 机构 overlay | 中性 | n/a | 加入 token-cost elasticity，不构成交易信号 |

新闻纪律：新闻只能解释价格、触发观察或削弱/强化候选；不能绕过趋势、相对强度、恐慌门控、仓位集中和止损规则。

AI 应用层单独监控：`ADBE` 是今天最重要的应用层验证。它有业绩和指引，但价格下跌，说明市场关注 AI 收入转化、freemium 对 ARR 的短期压力、竞争和管理层变动。应用层不和 GPU、数据中心或 AI 基建混为一类；后续只看业绩验证、公司指引、客户案例、行业趋势和价格相对强度。

## 6. 当前持仓复核

真实账户：确认股票持仓为零，因此没有真实 stop-triggered position。下表用于 USD 20,000 模型/历史 replay 的策略语言，不代表真实持仓。

| Ticker | Role | AI class | Current action | Stop/reduce line | Trend/RS | Overlay impact | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MRVL | 真实账户已空仓；模型观察对象 | cyclical_supplier / bottleneck | 不追；等待 fresh setup | 旧真实 `<245/<235` 风险线因空仓失效；重入需新规则 | 收 `280.71`, +11.13%，强但已垂直反弹 | capex-cycle high; flow_fragility elevated | `watch only / no chase` |
| AMD | 历史模型风险复核；真实账户 watch-only | cyclical_supplier | 不加；若模型仍持有则优先 reduce-review | close `<492` 已触发，6/11 收 `488.45` 仍低于线 | 强反弹但未正式收复 492 | growth_duration_high; theme_overlap_high | `reduce-review` |
| WDC | 历史模型/观察 | cyclical_supplier | 不新买；若模型持有则防御持有并复核 | close `<500` 前日触发，6/11 收 `529.29` 已重回线上 | storage 强修复 | bottleneck watch; high cyclicality | `defensive hold / repair review` |
| STX | 历史模型/观察 | cyclical_supplier | 不新买；若模型持有则防御持有并复核 | close `<835` 前日触发，6/11 收 `868.09` 已重回线上 | storage 强修复 | high share price / small account sizing issue | `defensive hold / repair review` |

止损语言约束：`AMD` 未正式收复 `492`，不能写成普通持有。`WDC/STX` 已重新站上风险线，可以从 exit-review 降为 repair review，但这只是风险修复，不是新增买点。`MRVL` 已无真实持仓，强反弹带来机会成本，但不构成自动追买。

## 7. 候选股排序

今天没有立即可执行的新买入。市场门控已从 stress 改善，但 `trend_aligned_entry` 仍是 `cheap_but_unconfirmed`；没有技术价位基础的限价单不得写成买入建议。

| Rank | Ticker | Theme | AI class | Entry condition | Risk line | Max size | Reason |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| n/a | n/a | n/a | n/a | n/a | n/a | 0 | 缺少第二日确认、支撑/reclaim 技术价位和 VIX/VIX3M 完整确认 |

Watch-only ranking:

| Ticker | Reason rejected | Recheck trigger |
| --- | --- | --- |
| MRVL | 已 +11% 反弹，真实账户已空仓，追高不合规 | 回踩并守住 `267-270` 区域，或放量突破后回踩确认；同时 QQQ/SMH 不反转 |
| WDC / STX | storage 反弹强，但刚经历 risk-line whipsaw，且主题重叠 | 连续收在 `500/835` 上方并跑赢 SMH/QQQ；若买入必须给出 20/50 日线、前低或 VWAP 依据 |
| AMD | 仍低于 `492` 旧风险线 | 正式收复并守住 `492-500`，相对 QQQ 改善 |
| NVDA / AVGO | 质量较高但 AI capex crowding 仍在 | VIX 保持 <20、SMH/SOXX 延续、个股回踩不破 20 日趋势 |
| ORCL | AI factory 需求强但 capex、融资、自由现金流被价格惩罚 | 股价止跌并确认融资/现金流路径 |
| ADBE / NOW / CRM / SNOW / DDOG / CRWD / APP / PLTR | AI 应用层分化；ADBE 证明业绩好也可能被价格拒绝 | ARR/ACV、付费客户、利润率、公司指引与 RS 同步改善 |
| QCOM / NOK / INTC | edge/network/turnaround watch，仍需公司级验证 | 订单、利润率、设备周期/路线图与价格趋势确认 |
| RKLB / RDW / TSLA | 高波动 satellite watch only | 收入/订单/执行证据 + 趋势确认；小仓位上限 3%-5% |

## 8. 组合构建

```text
Active holdings count: real account 0; USD 20,000 model should target 0-4 until new setups confirm
Theme count: real account 0; watch themes 3, but do not rebuild all at once
Cash: model target 60%-70%; real account equity cash state remains 100% until user confirms otherwise
Largest position: none in real account; model single-name cap remains 15%, satellite 3%-5%
Theme overlap: high if MRVL/AMD/WDC/STX are all rebuilt; avoid same AI capex beta basket
Max new exposure allowed: framework 25%; today operational 0%-10% only after confirmed technical basis
```

集中持仓规则仍有效：目标 4-6 只股票、最多 8 只、2-3 个主题。但当前不是为了凑足持仓数而买入；正确动作是保留现金选择权，等待 `market repair + trend-aligned entry + technical price basis` 同时出现。

## 9. 执行清单

| Priority | Action | Ticker | Trigger | Size | Notes |
| ---: | --- | --- | --- | --- | --- |
| 1 | No immediate buy | 全部候选 | 缺少第二日确认与技术限价基础 | 0 | 新闻和盘前反弹不等于买点 |
| 2 | Reduce-review | AMD 模型/replay | 正式收盘仍低于 `492` | 不虚构成交 | 先处理 stop/reduce 语言，不写普通持有 |
| 3 | Repair monitor | WDC / STX 模型/replay | 连续收在 `500/835` 上方才可降级风险 | 不新买 | 仍需第二日确认 |
| 4 | Re-entry watch | MRVL | 回踩 `267-270` 守住或突破后回踩确认 | 0 today | 该区间来自真实卖出价与前次事件支撑观察，不是正式技术支撑；未确认前只 watch |
| 5 | Application-layer validation | ADBE and peers | ARR/ACV、客户、利润率和 RS 同步改善 | 0 | 应用层单独监控，不能借 AI 基建强势直接买 |
| 6 | Data follow-up | VIX/VIX3M | 获取同步 term structure | n/a | 当前是 risk gate 缺口 |

## 10. 策略反思

- 做对：昨天的高现金和不追买纪律保住了选择权；真实账户无持仓时，没有必要为了错过 MRVL 后续反弹而倒推追买。
- 漏项：MRVL 卖出后强反弹暴露了“获利退出后如何重入”的规则仍不精确，需要 future fresh setup，而不是凭情绪追回。
- 集中度：历史 MRVL/AMD/WDC/STX 组合仍高度暴露于 AI capex 和半导体/存储 beta；真实账户空仓使主题重叠风险暂时为零。
- 现金：现金帮助降低隔夜风险，但在强反弹日会牺牲收益；这是风险换收益，不是错误。
- 恐慌门控：从 stress 降为 elevated 是合理的；因 VIX/VIX3M 缺口和单日反弹，不应直接 normal。
- Institutional overlays：`flow_fragility=elevated` 和 `token_cost_elasticity` 提醒不要把 AI 使用增长直接等同于所有 AI 基建/应用股都可买。
- 假设变化：AI 基建长期需求仍在，但 ORCL/ADBE 共同说明市场更重视现金流、ARR 转化、融资成本和管理层稳定；AI 应用层继续 watch-only。

## 11. 记忆同步

```text
Daily detail file: domains/quant-strategy/memory/daily/2026-06-12-us-stock-premarket-strategy.md
Trade plan file: no separate trade plan; no executable order
Portfolio file: no new portfolio file; real account remains no confirmed equity holdings
Hypotheses updated: no
Decisions updated: no
References updated: no
Open todos: repair synchronized VIX/VIX3M source; define MRVL fresh re-entry setup; monitor AMD 492, WDC 500, STX 835; keep AI application layer separate
```

Sources used:

- Local memory/rules: `summary.md`, `decisions.md`, `daily-summaries.md`, recent 2026-06-11/2026-06-12 daily records, `market-fear-technical-framework.md`, `portfolio-concentration-rules.md`, `daily-market-monitoring-framework.md`, `us-stock-daily-strategy-report-template.md`, `institutional-overlays-daily-checklist.md`, `institutional-overlay-scorecard.md`, `ai-quality-capex-cycle-classification.md`, and `tools/README.md` Quote Workflow Smoke Test.
- Local realtime product: `domains/quant-strategy/memory/daily/2026-06-12-realtime-public-institutional-monitor.md`.
- Market data: Python quote workflow via `ResilientStockClient`, source `Tencent`, run 2026-06-12 20:40-20:45 Asia/Shanghai; Node path failed with source-level errors as recorded above.
- Public news checked 2026-06-12: Investopedia market-open briefing, IBD market trend/Adobe reports, WSJ Adobe and oil coverage snippets, MarketWatch futures/oil coverage, Guardian oil coverage, Barron's VIX/futures/Adobe snippets.
