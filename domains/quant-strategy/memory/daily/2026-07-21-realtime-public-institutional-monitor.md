# 2026-07-21 实时公开来源与机构研究监控

运行完成：2026-07-21 23:25 Asia/Shanghai。增量窗口：`2026-07-20T13:48:57.576Z` 至 `2026-07-21T15:24:40.767Z`。起点取自最近成功写入的 7 月 20 日检查器产物。仅收集公开、只读内容；未读取浏览器隐私数据，未进行社媒互动、券商登录、下单或成交推断。

## 证据边界与访问状态

- Chrome 只读核验已连接；四个请求的 X 时间线仅呈现加载状态，未取得可引用正文、时间或 status ID。小红书可访问站点壳层，但目标作者主页未呈现内容。因此均为**浏览器访问缺口**，不是“没有更新”或“来源不可用”。
- 已运行并读取降级诊断 `work/realtime-public-source-latest.md/.json`。X 的作者匹配 status 详情可作高证据公开帖子事实，时间由 snowflake ID 推算。小红书仅有无 URL、时间、正文、评论和轮播图的标题候选，图片 `0/unknown`，只保留低至中证据主题线索。
- 已运行并读取 `work/institutional-research-latest.md/.json`；官方列表页和候选详情页分开核验，日期未验证项未当作新框架。

## 已核验条目

| 平台/来源 | 账号/机构 | ID / 时间 | 链接 | 类型与事实摘要 | 作者观点 | 策略映射 | 证据 | 待验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X（降级详情） | @nvidia | `2079221588705099788`；2026-07-20 23:07:11 北京 | https://x.com/i/status/2079221588705099788 | 官方帖：SIGGRAPH 2026 的图形、仿真、agentic/physical AI 与机器人公告。 | 产品/生态传播，不是订单、收入或利润披露。 | physical AI/仿真研究线索；不改 AI-capex 分类。 | 高：作者、正文；snowflake 时间 | 公司披露、客户部署、价格与相对强弱。 |
| X（降级详情） | @nvidia | `2079240931337965928`；2026-07-21 00:24:03 北京 | https://x.com/i/status/2079240931337965928 | 官方帖：Cosmos 3 Edge 边缘 GPU 世界模型公开可用，帖中称 40 亿参数 omni-model。 | 产品发布主张。 | 边缘推理/physical AI 线索；`AI_quality/capex_cycle` 不上调。 | 高 | 性能基准、商业化、客户采用与财务传导。 |
| X（降级详情） | @nvidia | `2079254592664301778`；2026-07-21 01:18:20 北京 | https://x.com/i/status/2079254592664301778 | 官方帖：DGX Station 上的 NemoClaw、Nemotron 3 Ultra、Omniverse 与 OpenShell 面向本地领域 agent 工作流。 | 产品栈/生态描述。 | 本地推理与软件栈线索；不能替代需求验证。 | 高 | 出货、定价、客户和独立行情确认。 |
| X（降级详情） | @elonmusk | `2079430412837757338`；2026-07-21 12:56:59 北京 | https://x.com/i/status/2079430412837757338 | 官方个人帖：推广 Grok Build。 | 极简宣传语，未含可核验经营/基础设施数据。 | xAI 应用层关注线索；不改宏观/集中度约束。 | 高（帖子事实）/低（经济含义） | 产品指标、融资/算力合同、独立市场数据。 |
| Man Institute | Man Group | 2026-07-20 16:00:00Z | https://www.man.com/insights/views-from-the-floor-2026-21-July | 官方详情页 *The VIX Isn't Worried, But Maybe It Should Be*，标题、日期、正文稳定可读。 | 讨论 VIX 所反映的风险定价。 | Fear Gate、`flow_fragility`、`factor_macro_exposure` 的风险复核输入，非独立信号。 | 高：官方详情页 | 当日 VIX/VIX3M、广度、信用、SMH 相对强弱与点时复核。 |

### 未核验证据

- 小红书“美研芒格君” / Kay2289123：公开 HTML 仍显示 MRVL/光模块、存储、AI 推理、ORCL、AVGO、ALAB、NBIS/CRWV 等标题候选，但无稳定单篇 URL、发布时间/编辑时间、正文、作者评论和轮播图；`0/unknown` 图。不得写为当日笔记、订单、收入、部署或价格事实。
- X @realDonaldTrump：降级检查器可读 profile 与若干详情，但没有落入窗口的可核验状态条目；不得写成“无新帖”。

## 机构研究核验结论

| 机构 | 列表/详情可读性 | 窗口后高证据新增 | 结论 |
| --- | --- | ---: | --- |
| AQR | 列表可读；8 个候选详情可读且均为窗口前/既有 | 0 | 无新 `trend_aligned_entry` 或因子稳健性框架。 |
| Citadel Securities | 列表可读；详情可读，archive 类候选另列日期不可验证 | 0 | 无新 `flow_fragility`/市场结构框架；列表候选不是研究结论。 |
| GMO | 列表可读；8 个候选详情可读且均为窗口前/既有 | 0 | 无新 `AI_quality/capex_cycle` 框架。 |
| Man Institute | 列表可读；1 篇窗口后官方详情，其余既有或日期不可验证 | 1 | 新文章仅作实验性风险复核输入；不升级交易规则。 |

## 事实、推断与策略映射

**公开事实：** 本窗口有 4 条匹配作者的 X status 详情（NVIDIA 3、Elon Musk 1）和 1 篇 Man Institute 官方详情文章。NVIDIA 均为产品/生态发布；Man 文章标题聚焦 VIX 风险定价。

**我的推断（非事实）：** 本地 agent、边缘世界模型和仿真仅延续 AI 从训练/云端向推理、边缘和物理 AI 扩展的观察线索；无订单、收入、毛利或客户部署新证据。Man 的 VIX 主题支持“不能只看低波动率”的复核纪律，不单独判定市场转弱或调整 Fear Gate。

| 模块 | 本次状态 |
| --- | --- |
| market fear gate | 不因一篇文章调整；须以独立 VIX、期限结构、广度、信用与指数数据审计。 |
| trend_aligned_entry | 未取得完成收盘、均线或相对强弱新确认；无触发。 |
| flow_fragility / theme crowding | 仅加入 Man 风险观察；无期权、ETF 流、隐含相关性或广度读数，状态不调分。 |
| AI_quality/capex_cycle / AI bottleneck watch | NVIDIA 讯号不等于商业兑现；仅登记边缘推理、仿真/physical AI、本地 agent 栈候选线索。 |
| factor_macro_exposure / portfolio concentration | 不变；既有 AI-capex 共同因子与集中度约束优先。 |
| replay/backtest plan | 冻结 5 个高证据时间戳，待补齐后续 1/5/20 日相对收益、VIX/广度与基本面事件，再做非回填 replay。 |

## 记忆边界、数据缺口与开盘准备

- 未修改 `memory/decisions.md` 或 `memory/hypotheses.md`：没有经重复或历史 replay 验证的稳定规则。
- 数据缺口：Chrome X 时间线、Kay 小红书单篇正文/评论/图片、真实订单/收入/部署、独立市场/期权/ETF 流、VIX3M 与广度/信用同步读数。
- 如需严格 Chrome 可见社媒核验，请用户确认 Chrome 内目标 X 页面和小红书作者主页可稳定加载；不需要提供密码、cookies 或隐私数据。
- 后续开盘准备优先读取：`memory/summary.md`、`memory/decisions.md`、`memory/daily/2026-07-20-post-close-audit.md`、`references/daily-market-monitoring-framework.md`、本文件和最新 Fear Gate 审计。
