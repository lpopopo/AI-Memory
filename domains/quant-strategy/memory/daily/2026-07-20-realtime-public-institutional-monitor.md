# 2026-07-20 实时公开来源与机构研究监控

运行时间：2026-07-20 21:48 Asia/Shanghai。增量窗口：`2026-07-19T03:34:43.000Z` 至本次运行；起点取自最近一次已写入的机构检查器产物（`work/institutional-research-latest.*`）。仅收集公开、只读信息；未读取浏览器私密数据，未进行社媒互动、券商登录、下单或成交推断。

## 证据边界

- 已优先尝试 Chrome 公开页面，但扩展连接返回 `Browser is not available: extension`，故未取得浏览器可见时间线、笔记正文或轮播图。
- 依任务约定运行并读取降级诊断 `work/realtime-public-source-latest.md/.json`。该诊断不覆盖浏览器可见证据：X 三个 profile 均 HTTP 200 但正文长度为 0；小红书仅取得无稳定 URL/时间/正文的标题候选，轮播图已读 `0/unknown`。
- 机构检查器在 `2026-07-20T13:48:35.952Z` 完成，已读取 `work/institutional-research-latest.md/.json`。仅 official-domain detail page 同时有稳定标题、日期、正文才计入高证据新增。

## 已核验来源条目

本窗口没有满足“来源、ID、可见时间、链接及正文”条件的新增社媒条目，也没有窗口后 official-detail 高证据机构文章。因此无可登记的 `verified source item`。

### 未核验证据与访问状态

| 平台/来源 | 账号/机构 | ID/时间/链接状态 | 可见内容 | 证据 | 不可得出的结论 |
| --- | --- | --- | --- | --- | --- |
| X | @Kay2289123 | Chrome 不可连接；降级检查器未覆盖此账号 | 无本窗口可读 status | 访问缺口 | 不得写为无更新或账号不可用 |
| X | @nvidia | profile `https://x.com/nvidia`；HTTP 200、正文 0 | 无 status ID、时间、正文 | 低（诊断） | 不得写为无新帖 |
| X | @elonmusk | profile `https://x.com/elonmusk`；HTTP 200、正文 0 | 无 status ID、时间、正文 | 低（诊断） | 不得写为无新帖 |
| X | @realDonaldTrump | profile `https://x.com/realDonaldTrump`；HTTP 200、正文 0 | 无 status ID、时间、正文 | 低（诊断） | 不得写为无新帖 |
| 小红书 | 美研芒格君 / Kay2289123 | 无稳定 note URL、发布时间、编辑时间或正文 | 原始公开 HTML 的标题候选仍围绕 MRVL、光模块、存储、AI 推理、ORCL、AVGO、ALAB、NBIS/CRWV；图片 `0/unknown` | 低至中（主题线索） | 标题不能证明笔记为本窗口新增，亦不能证明订单、收入、部署或价格事实 |

## 机构研究核验

| 机构 | 列表页/详情页 | 窗口后高证据新增 | 结论 |
| --- | --- | ---: | --- |
| AQR | 列表可读；8 个候选详情可读并可核验日期 | 0 | 无新增 `trend_aligned_entry` 或因子稳健性框架 |
| Citadel Securities | 列表可读；8 个候选详情可读；部分 archive 候选日期不可验证 | 0 | 无新增 `flow_fragility` 或市场结构框架；7/14 的 *After the Reset* 为窗口前既有文章 |
| GMO | 列表可读；8 个候选详情可读并可核验日期 | 0 | 无新增 `AI_quality/capex_cycle`、估值或质量框架 |
| Man Institute | 列表可读；8 个候选详情可读；部分候选 `date_unverified` | 0 | 无新增 `factor_macro_exposure`、`flow_fragility` 或 AI 瓶颈框架；7/14 的 *Chips Down, Then What?* 为窗口前既有文章 |

## 事实、推断与策略映射

**公开事实：** 本窗口机构四源经列表、详情与日期过滤后，高证据新增均为 0；社媒端没有可引用的新增正文条目。

**我的推断（非事实）：** 小红书可见标题持续涉及存储、光互连与推理，最多只能作为既有叙事的拥挤度复核线索；没有独立资金流、订单、客户、毛利率、价格或收盘确认，不能强化主题判断。

| 模块 | 本次状态 |
| --- | --- |
| market fear gate | 未取得 VIX、广度、信用或指数新证据；不因本监控调整 |
| trend_aligned_entry | 未取得完成日线、均线或相对强弱确认；不触发新增/加仓判断 |
| flow_fragility / theme crowding | 仅低至中证据标题线索；不调整评分，维持以独立期权、广度、ETF 流和价格数据复核 |
| AI_quality/capex_cycle / AI bottleneck watch | 存储、光互连、CXL/推理仅保留在待验证清单；需公司原始资料、客户/订单、盈利和独立行情验证 |
| factor_macro_exposure / portfolio concentration | 现有 AI-capex 共因子与集中度约束不变 |
| replay/backtest plan | 本窗口无新增合格点时事件；不回填、不重标。继续使用既有机构文章和已验证社媒条目的冻结时间戳进行回放 |

## 数据缺口与开盘准备

- 需要用户确认的访问问题：如需严格社媒核验，请确认 Chrome 扩展可重新连接并可稳定打开 X 与小红书的公开页面；无需登录、无需互动。
- 数据缺口：@Kay2289123 与三条 X 时间线；小红书单篇 URL/时间/正文/作者评论/轮播图；独立行情、期权、CTA、杠杆 ETF、订单和基本面数据。
- 后续开盘准备优先读取：`memory/summary.md`、`memory/decisions.md`、最近 post-close audit、`references/daily-market-monitoring-framework.md`、本文件，以及独立行情/Fear Gate 审计。

## 记忆边界

未修改 `decisions.md` 或 `hypotheses.md`：单日新闻、标题候选和单篇机构观点均未经过历史 replay 或重复验证，不构成稳定交易规则，也不构成直接买卖建议。
