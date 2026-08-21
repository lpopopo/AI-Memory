# 2026-08-20 实时公开来源与机构研究监控

运行完成：`2026-08-20 23:56 Asia/Shanghai`。增量窗口为 `2026-08-11T14:49:11.778Z` 至运行结束，起点取自最后一次已刷新且完整读回的机构检查产物。仅收集公开可见、只读页面与本地检查器输出；未读取 cookies、密码、本地存储、私信、通知或设置，未互动、未登录券商、未提交订单，也未记录或推断成交。

## 证据口径

- **公开事实**：浏览器可见的账号、状态 ID、正文与页面相对时间；或 official-domain detail page 的稳定标题、日期和正文。
- **我的推断**：只用于研究映射，绝不等同于订单、收入、出货、部署、价格或交易事实。
- X 本轮在部分页面只提供相对时间；下表保留页面可见时间，未将其伪装为精确发布时间。

## 公开社媒核验

| 平台/来源 | 账号 / ID / 页面可见时间 | 类型与事实摘要 | 作者观点 / 策略映射 | 证据强度与待验证 |
| --- | --- | --- | --- | --- |
| X | `@nvidia` / `2089804526970642920` / `Aug 19` | 官方帖：RTX Spark 将创作工作流、本地 AI 工具与 RTX 游戏集成在一台 PC。链接：https://x.com/nvidia/status/2089804526970642920 | 既有边缘/本地推理产品观察；映射 `AI_quality/capex_cycle`，不证明销量、ASP、出货、收入或股价影响。 | **高（帖子事实）**：浏览器可见官方账号、ID、正文、日期和视频占位；媒体内容未读。该项已于前轮入库，本轮无可见窗口内新 NVIDIA 帖。 |
| X | `@nvidia` / `2089331953585607127` / `Aug 17` | 官方帖称 SB Energy 位于 Ohio 的 PORTS-Pike Technology Campus 将由 NVIDIA 作为独家 AI compute infrastructure provider，并引用 land/power/shell 为 AI factories 的关键资源。链接：https://x.com/nvidia/status/2089331953585607127 | 既有 `AI bottleneck watch` 线索：电力、土地和机房壳体；须由项目方、合同、监管或财报资料独立验证。 | **高（帖子事实）**：浏览器可见官方账号、ID、正文与日期；“独家”、规模、交付、利用率与可归因收入均待核验。已于前轮入库。 |
| X | `@elonmusk` / `2090398269318758570` / `4 hours ago`（置顶） | 作者发文“Grok @Bot can earn you money”，并转引第三方关于自动化召回流失用户的自述。链接：https://x.com/elonmusk/status/2090398269318758570 | 仅为作者转帖/产品关注线索；可放入 `AI_quality/capex_cycle` 的应用层待证伪观察，不进入主题评分，也不确认产品能力、客户结果、收入或任何标的影响。 | **高（帖子事实）**；转引所称结果、图片及产品实际功能未核验。 |
| X | `@Kay2289123` | 公开 profile 仅显示 `Loading posts by @Kay2289123`，未见可记录的窗口内正文、ID或时间。 | 无。 | **访问缺口**，不是无更新结论。 |
| X | `@realDonaldTrump` | 公开 profile 仅显示 `Loading posts by @realDonaldTrump`，未见可记录的窗口内正文、ID或时间。 | 无。 | **访问缺口**，不是无更新或无政策风险结论。 |
| 小红书 | 美研芒格君 / `Kay2289123` / 主页可见 | 主页可见账号、置顶内容及最新非置顶卡片仍为既有笔记 `6a7149a300000000060051d7`《如果你也在找下一阶段的AI主线标的，看MRVL》；主页未给出稳定发表/编辑时间，本轮未打开单篇正文、作者评论或轮播。 | 只保留既有 AI 互联/存储主题温度背景；不得写成窗口内新笔记或公司事实。 | **中（主页身份与卡片）/ 单篇未核验**。轮播覆盖 `0/unknown`，无新增图像核验。 |

## 机构研究核验

已执行规定命令：`node ...institutional-research-checker.js --since 2026-08-11T14:49:11.778Z --max-items 8 --out ...institutional-research-latest.md`；该次进程约四分钟仍未输出，已停止，未覆盖现有文件。随后已读取 `work/institutional-research-latest.md` 与 `.json`：二者文件时间和内嵌运行时间均为 `2026-08-19T14:36:33.117Z`，因此下表是**已读的、仍有效的历史窗口诊断**，不是 8 月 20 日的刷新计数。

| 机构 | 列表/详情页状态（已读产物） | 结论与证据边界 | 策略映射 |
| --- | --- | --- | --- |
| AQR Research | 列表可读，8 个候选详情可读、日期稳定。 | 旧产物中本窗口 0 篇 official-detail 高证据；不得外推为本次运行后零新增。 | 不改变 `trend_aligned_entry` 或 `portfolio concentration`。 |
| Citadel Securities | 列表可读，8 个候选详情已读。 | 旧产物高证据确认 *August Checklist*（8/12）、*Back to Cloud (Nine?)*（8/17）和 *High Touch, Rewired*（8/17）；详情页稳定标题、日期和正文。 | 前者仅为 `flow_fragility` replay 标签；*Back to Cloud (Nine?)* 的“云、推理、分发可见回报”仅作 `AI_quality/capex_cycle` 实验观察，需以 hyperscaler 财报、利用率、capex、毛利与相对强弱复核。 |
| GMO Research Library | 列表可读，3 个候选详情可读且日期稳定。 | 旧产物中 0 篇窗口内 official-detail；不能据此判断当前时点。 | 不改变 `factor_macro_exposure` 或 AI-capex 框架。 |
| Man Institute | 列表可读，8 个详情已读。 | 旧产物中 0 篇稳定日期的窗口内 official-detail；若干详情可读但日期不可验证，保留候选。 | 不因日期缺失或动态加载而称来源不可用；不提炼新 `flow_fragility` / `factor_macro_exposure` 框架。 |

## 综合映射：事实、推断与控制项

- **market fear gate / trend_aligned_entry：**本轮没有完成收盘、广度、信用、VIX 期限结构或相对强弱的新输入；沿用 `2026-08-18-post-close-audit.md`，不重定级。
- **flow_fragility：**没有新鲜机构刷新；Citadel 三文继续只是 replay 标签，不能单独证明市场状态。
- **AI_quality / capex_cycle / AI bottleneck watch：**NVIDIA 既有 Ohio 帖保留“电力、土地、机房壳体”待核验维度；Elon 转帖仅提供应用叙事，不构成产品变现事实。
- **factor_macro_exposure：**无新增、稳定日期的 AQR/GMO/Man 研究输入；不改变判断。
- **theme crowding / portfolio concentration：**小红书既有 MRVL 卡片和本轮社媒不构成新增公司基本面证据。维持最近正式审计的单一 AI-capex sleeve、主题重叠高和相关新增/摊低 `0%` 约束；本报告不构成操作指令。
- **replay/backtest plan：**延续 `citadel-back-to-cloud-nine-2026-08-17`：事件后 `1/5/20/60` 个完成交易日对照 QQQ/SMH、云/推理相关篮子、RSP/SPY、VIX/VIX3M、HYG/LQD 及可用 capex/利用率代理。Elon 新帖仅保留 `grok-bot-application-claim-2026-08-20` 的低优先级应用层事件标签；先验证产品能力与可量化指标，跨样本有效后才可讨论规则变更。

## 数据缺口与开盘准备

1. Kay 与 Trump 的 Chrome 公开时间线仍停在 Loading；请确保登录会话/页面加载稳定后再补读，不能推断无更新。
2. 小红书最新非置顶单篇的公开时间、正文、作者评论和轮播未读，图片覆盖仍为 `0/unknown`。
3. 机构检查器本轮未刷新；下一次先检查 `work/institutional-research-latest.md/.json` 的文件与内嵌运行时间，再使用 AQR/Citadel/GMO/Man 计数。
4. 开盘前重点读取：`memory/summary.md`、`memory/daily/2026-08-18-post-close-audit.md`、本文件、`references/realtime-public-source-tracker.md`、`references/institutional-overlays-daily-checklist.md` 与 `work/institutional-research-latest.md`。

未更新 `decisions.md` 或 `hypotheses.md`：没有完成历史 replay 或重复验证的稳定规则。本报告不构成直接买卖建议，也不记录或推断订单、成交或账户状态。
