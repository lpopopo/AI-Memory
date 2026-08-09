# 2026-07-23 实时公开来源与机构研究监控（20:36 Asia/Shanghai）

增量窗口：`2026-07-21T15:24:40.767Z` 至本次运行。起点沿用最近成功的 source-monitor 产物。全程仅读取公开可见页面；未读取 cookies、密码、本地存储、私信、通知或账户设置，未执行关注、互动、券商登录、订单或成交推断。

## 证据状态

- **浏览器可见高证据**：Chrome 读取了 @Kay2289123、@elonmusk 和小红书主页。@Kay 的窗口内帖文在页面上显示相对时间；其精确 UTC 时间以下按 X snowflake ID 推导，明确不是页面直接时间。
- **降级诊断**：`work/realtime-public-source-latest.md/.json` 已在本轮生成并读取。它为浏览器未呈现的 @nvidia 提供了 author-matched status 详情；小红书脚本结果仅有无 URL/时间/正文的标题候选，维持低到中证据，图片 `0/unknown`。
- **机构研究**：本轮已启动规定的 checker，但在 244 秒超时前未写出新的 MD/JSON；已读取的 `institutional-research-latest.md/.json` 时间仍为 2026-07-23 01:09，不能当作本窗口结论。不得据此声称四家机构本窗口“无新增”。

## 已核验公开条目

| 来源 | ID / 时间 | 链接 | 公开事实 | 作者观点/策略映射 | 证据与待验证 |
| --- | --- | --- | --- | --- | --- |
| X @Kay2289123 | `2080190120993698148`; 页面 5h，snowflake 推导约 2026-07-23 03:38Z | https://x.com/Kay2289123/status/2080190120993698148 | 作者讨论模型榜单之争，并以引用帖提出 token 使用量的说法。 | 作者把总 token 消耗视为更值得跟踪的 AI 变量；映射到 `AI_quality/capex_cycle` 的需求证据层级（使用量→商业化仍需拆分）。 | 高：公开作者、ID、可见正文；低：被引用的“60%”统计及其定义，须原始数据验证。 |
| X @Kay2289123 | `2080151391985914112`; 页面 7h，snowflake 推导约 2026-07-23 01:04Z | https://x.com/Kay2289123/status/2080151391985914112 | 作者称将把 TSM、GOOG 等财报作为下一阶段 AI Capex 与资金流的观察材料。 | 是研究计划，不是结果；映射 `AI_quality/capex_cycle`、`flow_fragility` 与 `factor_macro_exposure` 的后续财报核验清单。 | 高：作者帖存在；中：作者解释；待核验：各公司正式财报、指引、订单和价格行为。 |
| X @nvidia | `2080078677426241940`; 2026-07-22 23:52:57Z（snowflake） | https://x.com/i/status/2080078677426241940 | NVIDIA 宣传 LiveX 在 NBA Summer League 使用 NVIDIA AI 做实时互动、定制与商业化体验。 | 仅作为 Physical AI/垂直应用生态线索，映射 `AI bottleneck watch`；不代表 GPU 需求、收入或盈利确认。 | 中到高：Jina status 详情作者匹配；待核验：客户部署规模、合同、收入与毛利。 |
| X @elonmusk | `2080048685522837664`; 2026-07-22 21:53:46Z（snowflake） | https://x.com/elonmusk/status/2080048685522837664 | Elon 转发 Tesla Q2 2026 earnings call。 | 事件入口，映射 `factor_macro_exposure` / 高估值 AI 相关资产的财报日波动观察；不从帖文本身推导经营结论。 | 高：作者、ID、时间、正文；待核验：Tesla 官方财报、电话会全文、完成收盘价格反应。 |
| 小红书 美研芒格君/Kay2289123 | 主页可见既有笔记：`6a60140c000000001b01d1ab` 等；本轮未见稳定发布时间 | https://www.xiaohongshu.com/user/profile/632ea1e700000000230381cb | 主页可读、显示置顶与非置顶笔记卡片，但没有新笔记的可核验发布时间。 | 不据此断言新增；此前完整读过的互联笔记继续仅作 `AI bottleneck watch` 研究线索。 | 主页事实中证据；新增判断低证据。轮播本轮未进入单篇详情，`0/unknown`，无新增图片结论。 |

### 未独立计入的新旧/边界条目

降级 checker 还返回 NVIDIA `2079709298784088470` 与 `2079699527888404973`，均在窗口开始后不久，分别为 SIGGRAPH 活动/RTX PRO 6000 推广与 Wistron Fort Worth 生产 Grace Blackwell board 的官方表述。它们已在本日早先监控中记录，本轮不重复计入独立催化剂。`2079715060197310935` 作者与正文不足，只保留 related/repost 的中证据诊断，不提炼观点。

## 机构研究结论（本轮）

| 机构 | 列表/详情状态 | 本轮结论 |
| --- | --- | --- |
| AQR | 新 checker 未完成；旧输出不可覆盖本窗口 | 未形成新结论。 |
| Citadel Securities | 新 checker 未完成；旧输出不可覆盖本窗口 | 未形成新结论。 |
| GMO | 新 checker 未完成；旧输出不可覆盖本窗口 | 未形成新结论。 |
| Man Institute | 新 checker 未完成；旧输出不可覆盖本窗口 | 未形成新结论；旧输出中的 date-unverified 候选仍不得提炼框架。 |

## 策略映射（非交易建议）

- `market fear gate`、`trend_aligned_entry`：本轮没有完成收盘、波动率或趋势数据，不更新。
- `flow_fragility` / `factor_macro_exposure`：把 TSM、GOOG 与 Tesla 正式财报/电话会列为下一次核验入口；单条社媒不改变分数。
- `AI_quality/capex_cycle`：坚持“产品传播/活动 → 部署 → 客户订单 → 发货 → 收入/毛利”的证据分层；本轮只有前两层的线索。
- `AI bottleneck watch`：LiveX/Physical AI 为应用生态线索；不改变光互联、算力或存储的既有研究分类。
- `theme crowding` / `portfolio concentration`：不因来源提及或财报预期放松既有 AI-capex 共因子约束。
- `replay/backtest plan`：把此次“作者预告财报方向”的说法记录为时间戳事件，待收集 TSM/GOOG 完整财报、价格和行业 ETF 的完成日线后，才可做事件回放；不得作为事前规则。

## 数据缺口与后续开盘准备

1. Chrome 中 @nvidia 与 @realDonaldTrump 本轮未呈现文章；前者由降级 status 详情补充，后者仍是政策覆盖缺口，不能写成无新帖。
2. 小红书主页没有显示新卡片时间；请在需要确认“是否新增”时提供单篇公开链接，才能读取正文、评论及逐张轮播。
3. 机构 checker 本轮超时；下次应先成功重跑并读取新 `institutional-research-latest.md/.json`，再给 AQR、Citadel、GMO、Man 结论。
4. 开盘准备优先读取：本文件、`memory/daily/2026-07-22-post-close-audit.md`、`memory/summary.md`、`references/daily-market-monitoring-framework.md` 与正式财报/电话会原文。

未更新 `decisions.md` 或 `hypotheses.md`：本轮证据不构成经过历史 replay 或重复验证的稳定规则。
