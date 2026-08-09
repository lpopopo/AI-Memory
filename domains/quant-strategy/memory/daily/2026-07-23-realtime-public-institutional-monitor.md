# 2026-07-23 实时公开来源与机构研究监控

运行完成：2026-07-23 01:10 Asia/Shanghai。增量窗口：`2026-07-21T15:24:40.767Z` 至本次运行。起点取自上次成功监控产物，而非假设 24 小时窗口。全程只读公开页面；未读取 cookies、密码、本地存储、私信、通知或账户设置，未进行任何社媒互动、券商登录、下单或真实成交推断。

## 证据边界

- 浏览器可见核验：`@nvidia` 与 `@elonmusk` 页面给出稳定作者、status ID、正文和相对时间；下列 UTC 时间由 X snowflake ID 推导，并标明为推导时间。`@realDonaldTrump` 的可见时间线停留在 7 月 5 日及更早，覆盖不了本窗口；不能写作“没有新帖”。
- `@Kay2289123` 页面显示“hasn't posted”，与既往可见历史不一致，故仅记为当前匿名可见视图限制，不能据此判断账号无更新。
- 小红书作者页未渲染可读内容；因此运行降级检查器并已读取其 Markdown/JSON。公开 HTML 仅有未定时、无 URL/正文的标题候选，图片 `0/unknown`，不是本窗口笔记事实。
- 机构检查器已运行并读取 `work/institutional-research-latest.md/.json`。四家官方列表页均可读且候选详情已分开核验；没有窗口后的“稳定标题 + 日期 + 正文”详情页。

## 小红书追补核验（本轮重试）

| 平台/来源 | 账号 | ID / 可见时间 | 链接 | 类型与事实摘要 | 作者观点 | 策略映射 | 证据 | 待验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 | 美研芒格君 / Kay2289123 | `6a60140c000000001b01d1ab`; 页面显示“昨天 08:51 美国” | https://www.xiaohongshu.com/user/profile/632ea1e700000000230381cb/6a60140c000000001b01d1ab | 《开源模型越强，互联消耗越大，机会还在初期》；可见正文把 AI 互联分为 scale-up、scale-out、scale-across，并提出“电变光”位置由可插拔向 LPO/NPO/CPO 靠近。 | 认为光互联机会仍早期，但铜不会消失、光不会一次接管所有连接；要求按连接距离、客户采购、证据等级和利润归属区分公司。 | `AI bottleneck watch` 与 `AI_quality/capex_cycle` 的研究线索；`theme crowding` 仅作叙事温度观察。 | 高：公开作者/ID/标题/正文/页面可见时间；中：作者产业判断；低到中：具体订单/采购数字。 | 公司公告、财报、客户订单、产品量产/利润率和价格行为。 |

**轮播图核验：** 总数 `29`，`29/29` 已逐张视觉/OCR 读取。页面末端的评论区文字由平台限制遮挡，但不影响已可见的图文内容；无额外可交易结论。图片中的公司、订单或数值仍只属于作者陈述，除非另有官方公告、财报或客户确认，均不作为独立事实。

### 图片内容分析（作者观点与研究线索）

1. **技术分层。** 将互联按 `scale-up`（GPU/机柜内，当前铜、SerDes、retimer、AEC 为主）、`scale-out`（服务器集群，800G 已有规模、1.6T 处于收入/量产爬坡观察）和 `scale-across`（DCI，相干光、WDM、ROADM/EDFA）分开。页面强调它们是不同采购单，而非连续替代的“三代产品”。这是可复用的研究分类法，但非需求或盈利事实。
2. **系统瓶颈。** 第 6–10 张说明 GPU 利用率受内存与 GPU 间通信等待约束；铜与光取舍依赖距离、损耗、功耗、布线、维修和总成本，PAM4 提高每符号承载量但压缩裕量、提高 DSP/激光器/测试要求。属于技术解释，待用供应商规格和客户部署交叉确认。
3. **价值链。** 图中区分 PIC、EIC、DSP、激光器、封装/测试，并提醒“做光模块”不是单一生意。将 Astera Labs（电连接/CXL/智能线缆）与 Ayar Labs（封装内光 I/O）区分；将 Marvell、Credo、Broadcom、AAOI、Fabrinet、Ciena、Nokia、Lumentum、Coherent、Corning 等映射到不同层。该映射是研究索引，不能推导同质化的主题暴露或收入弹性。
4. **证据成熟度。** 图 11 和第 29 张给出从 demo、sample、qualification、volume order、production 到 revenue 的路线，并强调产品发布、送样、试产、订单、发货和收入不可互换。这个证据分级可用于 `AI_quality/capex_cycle` 与 `replay/backtest plan`，但尚未通过历史 replay 形成规则。
5. **图中需官方复核的具体主张。** 包括 ALAB、MRVL/Celestial、AVGO、AAOI、Ciena、Nokia、Lumentum、Coherent、AXT、IQE、Fabrinet、Corning/Meta 的收入、订单、投资、送样、量产和产能描述。作者自身也提示：投资、采购承诺、订单上限、初始出货和年化运行率不等同于已确认收入。

**策略映射（非交易建议）：** `AI bottleneck watch` 增加“互联位置/距离、客户认证、真实发货、200G/lane 良率、售价与毛利”五项核验字段；`theme crowding` 不因长文或公司清单评分；`portfolio concentration` 保持既有 AI-capex 共因子约束；不调整 `market fear gate`、`trend_aligned_entry` 或 `flow_fragility`。

## 已核验公开条目

| 平台/来源 | 账号 | ID / 时间 | 链接 | 类型与事实摘要 | 作者观点 | 策略映射 | 证据 | 待验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X | @nvidia | `2079715060197310935`; 2026-07-21 23:48:04Z（snowflake 推导） | https://x.com/nvidia/status/2079715060197310935 | SIGGRAPH 2026 主题演讲回放；神经渲染、world models 与机器人仿真。 | 产品/研发传播，非订单或业绩披露。 | `AI bottleneck watch`：物理 AI、仿真与 world-model 观察线索。 | 高：浏览器可见作者、正文、ID；中：投资传导。 | 采用、客户部署、营收/利润及相对强弱。 |
| X | @nvidia | `2079699527888404973`; 2026-07-21 22:46:21Z（推导） | https://x.com/nvidia/status/2079699527888404973 | Wistron 在得州 Fort Worth 开设首座美国工厂，页面称生产 Grace Blackwell compute boards、后续 Vera Rubin。 | 制造/供应链公告。 | `AI_quality/capex_cycle` 与 AI bottleneck watch：仅作为本土化制造线索。 | 高：公开帖子事实；中：供应链传导。 | 工厂产能、实际出货、客户与财报确认。 |
| X | @nvidia | `2079699529943699613`; 2026-07-21 22:46:21Z（推导） | https://x.com/nvidia/status/2079699529943699613 | 链接至 NVIDIA Blog 的 Wistron Fort Worth 制造厂介绍。 | 官方扩展材料入口。 | 与上项同一事件，避免重复计入独立催化剂。 | 高：帖子存在；中：商业含义。 | 详情页的产能、投产时间与订单证据。 |
| X | @nvidia | `2079633231629144565`; 2026-07-21 18:22:54Z（推导） | https://x.com/nvidia/status/2079633231629144565 | Spectrum-6 102.4Tb/s Ethernet switch 正进入多家 gigascale AI factories；帖文点名 CoreWeave、Microsoft、Nebius、SpaceXAI、Tesla 等为早期引入者。 | 官方产品/客户生态表述。 | `AI bottleneck watch`：网络互连是 AI 工厂瓶颈候选；`flow_fragility` 不因单帖调分。 | 高：作者/正文/ID；中低：部署与财务外溢。 | 各客户独立确认、部署规模、收入与供货节奏。 |
| X | @elonmusk | `2079758604656316619`; 2026-07-22 02:41:06Z（推导） | https://x.com/elonmusk/status/2079758604656316619 | 称 Grok Imagine 年内将制作完整《奥德赛》电影。 | 个人产品目标陈述。 | AI application/creative-tool 观察；不改变 `market fear gate`、集中度或 AI-capex 分类。 | 高：帖子事实；低：经营/经济含义。 | 产品能力、上线时点、用户与收入数据。 |

## 未核验证据与访问结论

- 小红书“美研芒格君”/Kay2289123：降级诊断仅见 AI、MRVL 光模块、存储、互连等标题候选；无单篇 URL、发布时间/编辑时间、正文、作者评论或轮播图，已读图片 `0/unknown`。这些只可作为低到中证据的主题拥挤度线索，不能当作当天笔记或基本面事实。
- X @Kay2289123：当前浏览器未提供可与既往历史一致的时间线，未核验本窗口 status；不得作“无更新”结论。
- X @realDonaldTrump：可见帖子均早于窗口；这是时间线覆盖缺口，非无帖结论；不更新政策/宏观事实。
- 降级检查器的三个 X profile 均为 HTTP 200 但正文长度为 0，不能覆盖上述浏览器可见内容，也不额外形成新 status 证据。

## 机构研究核验

| 机构 | 列表/详情可读性 | 窗口后高证据新增 | 结论 |
| --- | --- | ---: | --- |
| AQR | 列表可读；8 个候选逐项筛查，详情存在的稳定日期均早于窗口；`Total Portfolio Approach` 仅列表候选。 | 0 | 不提炼新的 `trend_aligned_entry` 或因子稳健性框架。 |
| Citadel Securities | 列表可读；候选详情已分开读取与日期过滤。 | 0 | 不提炼新的 `flow_fragility`/市场结构框架。 |
| GMO | 列表可读；8 个候选详情可读但均为窗口前已有条目。 | 0 | 不提炼新的 `AI_quality/capex_cycle` 框架。 |
| Man Institute | 列表可读；可读详情均为窗口前；另有若干日期不可验证候选。 | 0 | 日期不可验证候选只保留访问状态，不提炼新框架。 |

## 事实、推断与策略映射

**公开事实：** 本窗口浏览器可见 4 条 NVIDIA 原创 status 与 1 条 Elon Musk status；NVIDIA 内容涉及物理 AI/仿真、Wistron 美国制造与 Spectrum-6 互连生态。四家机构均无窗口后的官方-detail 高证据文章。

**我的推断（非事实）：** 制造地点、网络互连和仿真消息继续支持 AI 从训练向系统、网络与物理 AI 扩展的研究线索，但没有新增订单、可审计收入、毛利、市场价格或独立客户确认。因此它们不是新的需求确认，也不是单独的风险或趋势信号。

| 模块 | 本次处理 |
| --- | --- |
| market fear gate | 不变；必须依赖同期 VIX/VIX3M、广度、信用、指数/SMH completed-close 审计。 |
| trend_aligned_entry | 无新的 completed-close、均线或相对强弱证据；不触发。 |
| flow_fragility | 不因产品帖或机构零新增调分；需期权、ETF 流、广度和相关性数据。 |
| AI_quality/capex_cycle | 记录 Wistron/网络互连为供应链核验候选，尚不提高商业化等级。 |
| AI bottleneck watch | 增记 Spectrum-6、仿真/world models、本土制造为候选观察；待独立部署及财务验证。 |
| theme crowding | 小红书标题候选只提示存储/光互连叙事持续，证据不足以评分。 |
| factor_macro_exposure / portfolio concentration | 不变；现有 AI-capex 共因子与集中度约束优先。 |
| replay/backtest plan | 冻结 5 个高证据 status 时间戳；待补齐 1/5/20 日相对收益、SMH/QQQ、VIX/广度及独立基本面事件后再做非回填 replay。 |

## 记忆边界、缺口与后续开盘准备

- 未修改 `memory/decisions.md` 或 `memory/hypotheses.md`：单日社媒、单一机构观点或产品公告未达到历史 replay/重复验证门槛。
- 数据缺口：小红书单篇正文/评论/轮播图；@Kay 当前可用时间线；@realDonaldTrump 窗口覆盖；Wistron/Spectrum-6 的独立订单、出货、财务和价格数据；VIX3M、广度、信用和期权/ETF 流的同步读数。
- 需要用户确认的来源访问问题：若需严格核验小红书或 @Kay，请确认公开主页在浏览器中可稳定显示；不需要提供密码、cookies 或任何隐私数据。
- 后续开盘准备优先读取：`memory/daily/2026-07-21-post-close-audit.md`、本文件、`references/daily-market-monitoring-framework.md`、`references/institutional-overlays-daily-checklist.md` 和 `work/institutional-research-latest.md`。
