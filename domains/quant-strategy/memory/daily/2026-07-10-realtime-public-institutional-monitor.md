# 2026-07-10 实时公开来源与机构研究监控

运行时间：2026-07-10 20:45 Asia/Shanghai。严格窗口：`2026-07-09T12:40:17.691Z` 至本次运行。窗口起点来自 automation memory 中 2026-07-09 20:40 Asia/Shanghai 的成功 rerun；未采用 24 小时假设。

本报告只做公开信息核验、证据分级、策略映射和记忆同步；不生成直接买卖建议，不登录券商，不提交订单，不记录或推断未确认真实成交。

## 访问方法与边界

- 已按要求读取根 `README.md`、memory architecture、quant-strategy summary / decisions / hypotheses / daily-summaries、最近 daily、指定 references 和 `tools/README.md`。
- Chrome 公开页面读取尝试：小红书主页读取两次均在浏览器控制层超时；一次批量 X/Xiaohongshu 读取也超时并重置运行时。未读取 cookies、密码、本地存储、私信、通知、账号设置；未关注、点赞、评论、转发或发帖。
- 已运行公开源降级诊断：`node domains/quant-strategy/tools/realtime-public-source-checker.js --since 2026-07-09T12:40:17.691Z --out domains/quant-strategy/work/realtime-public-source-latest.md`。结果只作为低到中证据，不覆盖此前 Chrome 可见内容。
- 已运行机构 checker：`node domains/quant-strategy/tools/institutional-research-checker.js --since 2026-07-09T12:40:17.691Z --max-items 8 --out domains/quant-strategy/work/institutional-research-latest.md`。该工具调用在 300 秒边界超时，但已写出 Markdown/JSON；已读取两份产物。
- 额外官方网页核验发现 Man Group official-domain detail page `H2 Technology Outlook - Still Dancing, But Moving Closer to the Door?`，日期 `10 July 2026`，正文可读，因此作为本轮唯一高证据机构新项。

## 结论摘要

### 公开事实

1. 小红书 `美研芒格君 / Kay2289123`：Chrome 未能稳定读取主页或详情页；降级 checker 的 raw HTML/SSR 暴露 20 条标题候选，但无稳定单篇 URL、发布时间、正文、作者评论或轮播图。本轮图片读取为 `0/unknown`；历史 `6a45e9690000000016027e78` 的 `32/32` 图片证据不被覆盖。
2. X `@Kay2289123`、`@nvidia`、`@elonmusk`、`@realDonaldTrump`：本轮 Chrome 读取未完成；Jina profile 均为 `ok=true` 但 `length=0`。没有本窗口内可采信的新 status ID、发布时间、链接或正文摘要。不得复用上一轮已记录的 2026-07-07/08 status 作为本轮新证据。
3. AQR：本地 checker 的 Reader list 通道失败，候选数 `0`；官方 Research 页面经网页核验可读，最新可见研究仍早于本窗口，例如 `The Wrapper Illusion...` 为 2026-06-15、`Total Portfolio Approach` 为 2026-05-19。结论是“本轮 Reader 通道失败且未发现窗口内详情页”，不是“来源不可用”。
4. Citadel Securities：本地 checker 的 Reader list 通道失败，候选数 `0`；官方 Market Insights 列表页经网页核验可读，最新可见候选包括 `AI-merican Exceptionalism`、`Cruel Summer for Fixed Income`、`1H 2026 Market Structure & Flows` 等，但均为窗口前内容或列表候选。本轮无 post-window official detail framework。
5. GMO：列表页、8 个候选详情页可读；全部为窗口前内容，`post-window verified=0`。无新 `AI_quality/capex_cycle` 框架。
6. Man Group / Man Institute：checker 的 market views 通道读到 8 个候选但均为窗口前或 date-unverified；额外 official-domain detail page 核验到 `H2 Technology Outlook - Still Dancing, But Moving Closer to the Door?`，日期 `10 July 2026`，正文可读，是本轮唯一高证据新机构项目。

### 我的推断

- 本轮社媒端没有新增中高证据 verified event；小红书标题候选只能说明主题温度仍集中在 AI 硬件、光互联、存储、云工厂、MRVL/ORCL/AVGO/ALAB/CBRS/NBIS/CRWV 等方向，不能作为完整 source item。
- Man Group 新文强化了现有 H7/H8/H11：AI 交易正在从“宽主题 beta”转向层级轮动和赢家/输家分化；半导体估值与下游软件现金流之间存在结构分歧；OpenAI/Anthropic 等私有 AI 实体与云厂商 backlog/承诺高度相关，可能形成集中对手方风险；中国模型和半导体成本效率需要纳入 AI 竞争格局；未来 IPO 与 lock-up 释放可能成为 2027 压力点。
- 这些推断是机构观点到策略监控字段的映射，不是买卖信号。必须等待价格、财报、官方 capex/backlog、客户集中度、信用/IPO 数据和 replay 验证。

### 未核验证据

- 小红书 20 条标题候选没有时间、URL、正文、评论、图片，因此只保留为低到中证据主题温度。
- X 四个账号本轮没有可读 status 详情；不能推断“无发帖”，只能记录“本轮访问通道未取得可采信正文”。
- Man Group 新文中的 cloud backlog、私有 AI 承诺、IPO 规模、中国模型效率、供应链采购变化等为机构作者观点和引用数据，需要回到公司 filings、S&P Global / Visible Alpha、OpenRouter、IPO lock-up 数据和官方财报验证。

## Verified source item table

| 平台/来源 | 账号或机构 | ID / 时间 | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 raw HTML/SSR | 美研芒格君 / Kay2289123 | 无稳定单篇时间 | `https://www.xiaohongshu.com/user/profile/632ea1e700000000230381cb` | 主页标题候选 | 暴露 20 条标题候选；无窗口内新发确认；无正文/URL/时间/图片 | 无可提炼作者正文 | 仅作 AI-capex / optical / memory / cloud-factory 主题温度观察 | 低到中 | 单篇 URL、发布时间、正文、评论、轮播图 |
| X | `@Kay2289123` | 无 | `https://x.com/Kay2289123` | profile/checker 访问 | Chrome 未完成，Jina profile 空 | 无 | 不新增事件 | 低 | 已登录 Chrome 时间线或单帖详情 |
| X | `@nvidia` | 无 | `https://x.com/nvidia` | profile/checker 访问 | Chrome 未完成，Jina profile 空；网页搜索只显示旧/泛化 profile snippet | 无 | 不新增官方产品/生态事件 | 低 | Chrome 可见 profile 或单帖详情 |
| X | `@elonmusk` | 无 | `https://x.com/elonmusk` | profile/checker 访问 | Chrome 未完成，Jina profile 空；搜索结果主要指向旧 Grok 4.5 项 | 无 | 不新增 xAI/Tesla/SpaceX 事件 | 低 | Chrome 可见 profile 或单帖详情 |
| X | `@realDonaldTrump` | 无 | `https://x.com/realDonaldTrump` | profile/checker 访问 | Chrome 未完成，Jina profile 空；无窗口内可读政策正文 | 无 | 不做关税、财政、产业政策映射 | 低 | 可读政策正文或官方文字稿 |
| 机构 | AQR Research | checker run `2026-07-10T12:37:07Z` | `https://www.aqr.com/Insights/Research` | official list + checker | checker Reader list 失败；官方列表页可读，最新可见内容早于窗口 | 无新框架 | 不新增 `trend_aligned_entry` 字段 | 中：列表页可读；低：checker 通道失败 | 下轮继续核验 list/detail 标题、日期、正文 |
| 机构 | Citadel Securities | checker run `2026-07-10T12:37:07Z` | `https://www.citadelsecurities.com/news-and-insights/category/market-insights/` | official list + checker | checker Reader list 失败；官方列表页可读，最新可见候选为窗口前 | 无新框架 | 不新增 `flow_fragility` 字段 | 中：列表页可读；低：checker 通道失败 | 详情页日期与正文；避免把列表候选当新框架 |
| 机构 | GMO Research Library | 8 candidates, all pre-window | `https://www.gmo.com/americas/research-library/` | official checker | 列表和详情可读；`post-window verified=0` | 无新框架 | 不新增 `AI_quality/capex_cycle` 字段 | 高：列表/详情状态 | 下轮继续过滤窗口内新详情 |
| 机构 | Man Group | `10 July 2026` | `https://www.man.com/insights/h2-2026-technology-outlook` | official-domain detail article | 标题、日期、正文可读；文章讨论 AI 交易成熟、半导体周期、私有 AI/cloud backlog 集中、中国效率竞争、IPO/lock-up 压力 | 技术投资需要从宽主题转向更选择性的价值链定位；不宜离场但应靠近出口 | 新增监控字段：`AI_stack_selectivity_rotation`、`semiconductor_peak_margin_trap`、`private_AI_customer_concentration`、`China_AI_efficiency_competition`、`AI_IPO_lockup_pressure` | 高：官方页面/日期/正文；中：策略传导 | 公司 filings、cloud backlog、OpenAI/Anthropic 承诺、OpenRouter、IPO lock-up、1/5/20/60 日 replay |

## 策略映射

- `market fear gate`：本轮 source monitor 不刷新价格或 VIX，沿用 2026-07-09 post-close 的 `normal 2/14`；但真实账户仍被 GLW/DRAM/MXL/MRVL unresolved-stop veto 和 AI-capex common-factor correlation 约束，实际新买入上限仍为 `0%`。
- `trend_aligned_entry`：社媒无新增可验证 catalyst；Man 新文反而强调从宽主题转向选择性分层，强化“不能只因 AI 硬件热度或回调就买入”，仍需 20/50 日趋势、相对强度和止损闭环。
- `flow_fragility`：Man 新文把半导体 rally、私有 AI 承诺、IPO/lock-up 和资本循环放在同一风险结构内，支持维持 `elevated / near-acute` 观察；不构成单独看空信号。
- `AI_quality/capex_cycle`：新增实验字段 `semiconductor_peak_margin_trap`、`private_AI_customer_concentration`、`China_AI_efficiency_competition`、`AI_stack_selectivity_rotation`。用于区分平台/供应商/软件/应用层，不提升任何 ticker 的核心角色。
- `factor_macro_exposure`：新增 `AI_IPO_lockup_pressure` 与 `tech_value_chain_rotation`，映射到成长久期、流动性窗口、VC 资本回收和 2027 潜在供给压力。
- `AI bottleneck watch`：继续跟踪 GPU -> memory -> optics -> wafer capacity 的瓶颈轮动，但要把“短期瓶颈”与“可持续企业 ROI/软件现金流”分开。
- `theme crowding`：小红书标题候选和 Man 新文都指向同一结论：AI 硬件主题仍拥挤，ticker 多样化不等于因子分散。
- `portfolio concentration`：不改变真实持仓记忆，不记录任何成交；公开来源不能解除 GLW/DRAM/MXL/MRVL stop closure 与 XLI 状态确认问题。
- `replay/backtest plan`：冻结 Man `2026-07-10` article event，比较 1/5/20/60 日 QQQ/SMH/XSD/HYG/LQD、半导体设备、存储、光互联、软件/网络安全、云基础设施、IPO/新股篮子的收益、成交量和最大不利波动。检验这些字段是否比现有 fear gate / flow fragility 更早识别 AI 硬件拥挤风险。

## 机构研究核验结论

| 机构 | 列表页 | 详情页 | 窗口新增 | 结论 |
| --- | --- | --- | ---: | --- |
| AQR | checker Reader 失败；官方网页可读 | 未取得窗口内新详情 | 0 | 不可写来源不可用；无新 `trend_aligned_entry` 框架 |
| Citadel Securities | checker Reader 失败；官方网页可读 | 未取得窗口内新详情；列表候选多为窗口前 | 0 | 不可写来源不可用；无新 `flow_fragility` 框架 |
| GMO | checker 可读 | 8 个候选详情可读，均窗口前 | 0 | 无新 `AI_quality/capex_cycle` 框架 |
| Man Group | checker 可读但漏掉本项；官方网页补核验成功 | `H2 Technology Outlook` 有稳定标题、日期、正文 | 1 | 新增实验监控字段；不升级为稳定规则 |

`decisions.md` 不更新：本轮新增是单篇机构观点和访问诊断，不具备历史 replay 或反复验证的稳定规则证据。

## 数据缺口与需要用户确认的访问问题

1. 小红书 Chrome 读取连续超时；详情页、编辑时间、作者评论、轮播图均未复核。本轮图片证据 `0/unknown`。
2. X 四个账号本轮没有可读 timeline 或 status 详情；需要用户确认已登录 Chrome 中 X 是否可手动打开这些主页/单帖。
3. AQR、Citadel checker Reader list 本轮失败，但官方网页可读；下轮需要继续区分 Reader 通道失败、官方列表可读、详情可读、详情被挡、仅列表候选、日期不可验证。
4. Man Group 新文中的数值和判断需要独立验证，不应直接进入公司质量分或仓位角色。

## 后续开盘准备重点读取

1. `memory/daily/2026-07-09-post-close-audit.md`
2. `memory/daily/2026-07-09-details.md`
3. `memory/daily/2026-07-10-realtime-public-institutional-monitor.md`
4. `memory/portfolio/2026-07-09-portfolio-summary.md`
5. `memory/todos/2026-07-09-strategy-todos.md`
6. `references/realtime-public-source-tracker.md`
7. `references/institutional-market-research-framework.md`
8. `references/institutional-overlays-daily-checklist.md`
9. `references/ai-quality-capex-cycle-classification.md`
10. `work/realtime-public-source-latest.md` / `.json`
11. `work/institutional-research-latest.md` / `.json`

## 20:50 Chrome 访问恢复补记

本补记复用同一严格窗口，且仅提高旧内容的浏览器可见证据，不把窗口前内容重新计为新增事件。

| 平台/来源 | 账号或机构 | ID / 页面可见时间 | 链接 | 类型 | 公开事实摘要 | 作者观点 / 策略映射 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 | 美研芒格君 / Kay2289123 | `6a45e9690000000016027e78`; `07-02 美国`; 轮播 `1/32` | `https://www.xiaohongshu.com/explore/6a45e9690000000016027e78` | 旧笔记详情 | Chrome 可见标题、完整可见正文、作者置顶评论和 32 页轮播总数；首图已视觉核验。 | 文中把 AI 存储压力拆为容量与带宽，并列出 HBF、近内存计算/光 HBM、软件冷热分层/CXL 等路线。这是作者观点，只维持既有 `AI bottleneck watch` / `AI_quality/capex_cycle` 的历史研究语境。 | 高：页面标题/正文/评论/日期/轮播计数；历史全图证据仍为 `32/32`。 | 本次只视觉复核首图；不将历史 32 页重新计数，也不据此生成交易信号。 |
| X | `@Kay2289123` | status `2074172593175957904`; `Last edited 12:44 AM · Jul 7, 2026` | `https://x.com/Kay2289123/status/2074172593175957904` | 旧长帖详情 | Chrome 可见完整正文、引用 CNBC/SemiAnalysis 说明和最后编辑时间。 | 帖子将 Kyber 延后、Oberon/Rubin、pluggable/LPO/CPO 路径映射到光互联观察；该叙述与作者 ticker 含义仍须以 NVIDIA、供应链和财报材料独立核验。 | 高：可见状态详情及编辑时间；中：技术/市场传导。 | 该帖早于本轮严格窗口；Kay 主页新加载超时，不能据此推断此后没有新帖。 |

浏览器边界：只读取公开可见页面；未读取 cookies、密码、本地存储、私信、通知或账户设置，未执行关注、点赞、评论、转发或发帖操作。`decisions.md` 不更新。

## 21:25 实时资讯重试

- 严格增量窗口：`2026-07-10T12:45:00Z` 至 `2026-07-10T13:25:49.273Z`。Chrome 已确认 `https://x.com/Kay2289123` 主页处于打开状态，但时间线可见内容导出连续中断；这不是来源不可用结论。
- 降级诊断产物：[realtime-public-source-retry-latest.md](../../work/realtime-public-source-retry-latest.md) 与同名 JSON。`@nvidia` profile 和 status `2075311533190455594`、`2075293913213018544` 可读，但工具按 status 详情与 snowflake 时间筛选后，严格窗口内 verified item 为 `0`。`@elonmusk`、`@realDonaldTrump` 的 Reader profile 为空。
- 小红书 raw HTML/SSR 仍只给出 20 条既有标题候选；缺少稳定单篇 URL、发布时间、正文和图片，证据为低到中，不构成实时资讯或作者观点提炼。
- 策略映射：`market fear gate`、`trend_aligned_entry`、`flow_fragility`、`AI_quality/capex_cycle`、`AI bottleneck watch`、`theme crowding`、`portfolio concentration` 与 `replay/backtest plan` 均不新增事件。`decisions.md`、假设字段、交易、订单和成交记录均不更新。
