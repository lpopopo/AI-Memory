# 2026-07-27 实时公开来源与机构研究监控

运行完成：2026-07-27 21:00 Asia/Shanghai。增量窗口：`2026-07-24T12:37:24.596Z` 至本次运行；起点取自 automation memory 中上次完整机构检查的成功写入时间。全程只读公开页面/公开 Reader 输出；未读取 cookies、密码、本地存储、私信、通知或设置，未进行任何社媒互动、券商登录、订单或成交推断。

## 证据边界与访问状态

- Chrome 扩展连接可用，但尝试读取 `@Kay2289123` 可见 DOM 两次均在页面快照生成前超时。因此四个 X 账号与小红书均没有形成新的**浏览器可见**事实；这是覆盖缺口，不能写成无更新。
- 按降级规则，已运行并读取 `work/realtime-public-source-latest.md/.json`。其中含稳定 status URL、正文、作者匹配与 snowflake 推导时间的 X 条目，记为**中证据**（脚本/Reader 详情，非本轮 Chrome 可见复核）；无 URL、时间或正文的小红书标题候选只记低到中证据。
- 已运行并读取 `work/institutional-research-latest.md/.json`。机构的列表页可读、详情可读、窗口前内容和日期不可核验候选均单独标识，未把访问限制误写为来源不可用。

## 已核验公开条目

| 平台/来源 | 账号 | ID / 时间（UTC，snowflake 推导） | 链接 | 类型与事实摘要 | 作者观点/策略映射 | 证据 | 待验证 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| X（降级 Reader） | @nvidia | `2081666629264449730`; 2026-07-27 09:02:54 | https://x.com/i/status/2081666629264449730 | 宣布 Open Secure AI Alliance，称将与行业伙伴开源开发软件与 agent 安全工具。 | `AI bottleneck watch`：AI agent 安全/工具链线索；不构成部署或收入。 | 中：URL、正文、作者匹配和推导时间齐全；非本轮 Chrome 可见。 | 联盟成员、产品采用、可审计商业化。 |
| X（降级 Reader） | @nvidia | `2081142850994229468`; 2026-07-25 22:21:36 | https://x.com/i/status/2081142850994229468 | 宣传首尔大学 NVIDIA AI Technology Center。 | 区域研发生态线索；不调整 `AI_quality/capex_cycle`。 | 中 | 实际设施、投资与产出。 |
| X（降级 Reader） | @nvidia | `2080887168793190587`; 2026-07-25 05:25:36 | https://x.com/i/status/2080887168793190587 | 称 NAVER、NVIDIA、Brookfield 扩展韩国国家 AI factory 基建，并提及 NAVER 部署 DSX。 | `AI_quality/capex_cycle` / `AI bottleneck watch`：仅为官方项目陈述，须按公告→订单→交付→收入分层。 | 中 | 三方正式公告、合同规模、交付与财报。 |
| X（降级 Reader） | @nvidia | `2080886765146321314`; 2026-07-25 05:24:00 | https://x.com/i/status/2080886765146321314 | 称 SK Group 与 NVIDIA 推动 AI factories 和下一代 HBM 合作，帖文含 2GW DSX AI Factory 陈述。 | AI 基建与内存供应链候选；不提高商业化等级。 | 中 | SK/NVIDIA 官方公告、资本开支、量产与收入。 |
| X（降级 Reader） | @nvidia | `2080833379197477226`; 2026-07-25 01:51:52 | https://x.com/i/status/2080833379197477226 | K-AI 愿景宣传，涉及芯片、前沿 AI、physical AI、机器人与 AI factories。 | 叙事/主题温度，不能计为订单、需求或趋势信号。 | 中 | 独立项目和财务证据。 |
| X（降级 Reader） | @elonmusk | `2081627240777895998`; 2026-07-27 06:26:23 | https://x.com/i/status/2081627240777895998 | “I will not forget about Mars”。 | 无可操作的市场映射。 | 中 | 无。 |
| X（降级 Reader） | @elonmusk | `2081624723432124681`; 2026-07-27 06:16:23 | https://x.com/i/status/2081624723432124681 | 与媒体关系的个人表述。 | 无。 | 中 | 无。 |
| X（降级 Reader） | @elonmusk | `2081622225023611265`; 2026-07-27 06:06:27 | https://x.com/i/status/2081622225023611265 | 发布名为 SPACELESS 的视频内容。 | 无法推导 xAI/Tesla/SpaceX 经营事实。 | 中 | 产品归属、上线与指标。 |
| X（降级 Reader） | @elonmusk | `2081616755823186385`; 2026-07-27 05:44:43 | https://x.com/i/status/2081616755823186385 | “Grok Imagine”视频帖。 | AI 应用/创作工具研究线索；不调整市场或组合模块。 | 中 | 产品能力、用户、收入。 |

### 未核验证据与覆盖缺口

- 小红书“美研芒格君”/Kay2289123：降级输出只有标题候选，无稳定新笔记 URL、发布时间/编辑时间、正文、作者评论或轮播；已读图片 `0/unknown`。只能作为光互联、存储等主题温度线索，不能认定为本窗口新增事实。
- X `@Kay2289123`：Chrome 页面未生成可读快照，未取得本窗口 status；不能据此认定无更新。
- X `@realDonaldTrump`：降级 profile 可读，但筛得 status 均早于窗口；由于 Chrome 覆盖失败，政策/宏观来源仍为未完成覆盖，而非无新帖结论。
- `@elonmusk` 的一个 related/repost 条目作者为 `@brivael`，不计为目标账号的独立事实。

## 机构研究核验

| 机构 | 列表/详情状态 | 窗口后 official-detail 高证据 | 结论 |
| --- | --- | --- | --- |
| AQR | 列表可读；8 个候选均读取详情并按日期过滤。 | 1 | [An Interview with Nathan Sosner: Perspectives on Concentrated Wealth](https://www.aqr.com/Insights/Research/Journal-Article/An-Interview-with-Nathan-Sosner-Perspectives-on-Concentrated-Wealth)，`2026-07-26T16:00:00Z`。文章讨论集中财富/集中持股下的分散化、税务成本与波动对长期复利的影响。高证据仅限官方标题、日期、正文及其框架；对本组合仅强化既有 `portfolio concentration` 审核，不形成交易规则。 |
| Citadel Securities | 列表可读；已读 8 个候选详情。 | 0 | 5 篇为窗口前；3 个归档候选无稳定日期，保留为低证据访问状态，不提炼 `flow_fragility` 框架。 |
| GMO | 列表可读；已读 8 个候选详情。 | 0 | 全部为窗口前/既有项；不新增 `AI_quality/capex_cycle` 框架。 |
| Man Institute | 列表可读；已读 8 个候选详情。 | 0 | 5 篇窗口前；3 个候选日期不可核验，不能从中提炼 `factor_macro_exposure` 或 AI 框架。 |

## 事实、推断与策略映射（非交易建议）

**公开事实：** 降级 Reader 可定位到 NVIDIA 五条窗口内官方 status，主题为 AI 安全联盟、韩国研发中心与 AI factory/内存基础设施；Elon Musk 四条作者匹配 status 主要是 Mars、媒体观点和 Grok Imagine 内容。AQR 有一篇窗口后、官方详情页标题/日期/正文稳定的集中持股研究。

**我的推断：** 韩国 AI factory/HBM 叙事与既有 AI-capex 研究主线一致，但当前证据停在官方传播或项目陈述层；尚无独立订单、实际发货、收入、毛利、价格行为或客户验证。AQR 对集中持股的讨论与现有共同因子审查方向一致，但单篇机构文章不是新规则的验证。

| 模块 | 本次处理 |
| --- | --- |
| market fear gate / trend_aligned_entry | 不变；本次没有 completed-close、VIX、广度、信用或趋势证据。 |
| flow_fragility / factor_macro_exposure | 不因单篇 AQR 或社媒调整；Trump 政策覆盖仍缺口。 |
| AI_quality/capex_cycle | 对 AI factory、DSX、HBM 维持“官方陈述→合同/订单→交付→收入”分层。 |
| AI bottleneck watch | 新增 AI agent security、AI factory 与 HBM 的待核验入口。 |
| theme crowding / portfolio concentration | 不放松现有 AI-capex 共因子与集中度约束；AQR 文章只作复核背景。 |
| replay/backtest plan | 冻结本次 status 时间戳；未来仅在补齐公告/财报与 1/5/20 日价格、SMH/QQQ、VIX/广度后做非回填 replay。 |

未更新 `memory/decisions.md` 或 `memory/hypotheses.md`：本次均为单日公开内容/单篇机构观点，未满足历史 replay 或重复验证门槛。

## 开盘前重点与数据缺口

1. 数据缺口：Chrome 公开可见的 @Kay/@nvidia/@elonmusk/@realDonaldTrump 时间线、小红书单篇正文/评论/轮播（`0/unknown`）、韩国项目的订单/交付/财务证据，以及同步宏观与价格数据。
2. 如需严格验证小红书新笔记或 @Kay，请确认 Chrome 中对应**公开页面**可稳定显示，或提供公开单篇链接；不需要提供密码、cookie 或其他隐私数据。
3. 开盘准备优先读取：[本监控](2026-07-27-realtime-public-institutional-monitor.md)、[最新机构输出](../../work/institutional-research-latest.md)、[7/24 盘后审计](2026-07-24-post-close-audit.md)、[领域摘要](../summary.md)、[日度市场框架](../../references/daily-market-monitoring-framework.md) 与 [机构 overlay checklist](../../references/institutional-overlays-daily-checklist.md)。
