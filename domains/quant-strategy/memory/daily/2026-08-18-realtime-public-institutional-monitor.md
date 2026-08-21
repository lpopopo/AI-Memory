# 2026-08-18 实时公开来源与机构研究监控

运行时间：`2026-08-18 22:51 Asia/Shanghai`。增量窗口暂取 `2026-08-11T14:49:11.778Z` 至本次运行结束：该起点为最后一次确认已刷新并完整读取的机构产物。仅收集公开、可见、只读页面与本地检查器输出；未读取 cookies、密码、本地存储、私信、通知或设置，未产生任何社交互动、券商登录、订单或成交操作。

## 证据状态与公开社媒

### 已核验项目

本轮没有满足“账号匹配 + 稳定 ID/链接 + 时间 + 正文”门槛的新增社媒项目，故没有可写入的 X 或小红书 verified item。

### 覆盖缺口与未核验证据

- Chrome 公开只读读取 `@Kay2289123`、`@nvidia`、`@elonmusk`、`@realDonaldTrump` 时，四个 profile 均只显示 `Loading…`；这只是页面访问缺口，不是无发帖或来源不可用结论。
- Chrome 对小红书目标页面仅呈现站点壳层、未呈现作者内容。其正确公开 profile 为 `https://www.xiaohongshu.com/user/profile/632ea1e700000000230381cb`；本次浏览器未能取得其可见笔记、评论或轮播。
- 浏览器对目标内容不可读后，运行并读取 `work/realtime-public-source-latest.md/.json`（运行时间 `2026-08-18T14:51:50.103Z`）。`@nvidia`、`@elonmusk` 与 `@realDonaldTrump` 的 Jina profile 均为 HTTP 200/空正文，未产生 status ID、时间或正文；这是低证据诊断，不能替代浏览器可见内容。
- 小红书公开 HTML/SSR 仅暴露题目候选，缺少稳定单篇 URL、发布时间、正文、作者评论与轮播。已读图片/总图片：`0/unknown`。其中“Token 算力工厂”“MRVL”“Credo/互联”等仅保留为低到中证据的主题温度候选，不可写成笔记事实或窗口内更新。

## 机构研究核验

已按要求执行 `institutional-research-checker.js --since 2026-08-11T14:49:11.778Z --max-items 8`，并读取 `work/institutional-research-latest.md/.json`。但二者仍内嵌 `2026-08-14T12:36:32.137Z` 的运行时间与 8 月 14 日文件更新时间，未被本次命令刷新。因此下表是**陈旧但已读的诊断与已验证历史事实**，不能据此断言 8 月 14 日之后没有新增。

| 机构 | 核验结论 | 详情页状态 / 策略映射 |
| --- | --- | --- |
| AQR Research | 陈旧产物显示列表页可读、8 个候选详情可读；0 篇窗口内 official-detail。 | 日期均已过滤为窗口前；不将该旧零值延伸为当前零新增。映射 `portfolio concentration`、`trend_aligned_entry` 的既有复核。 |
| Citadel Securities | 陈旧产物的官方详情页高证据核验文章：*August Checklist*，`2026-08-11T20:23:39Z`，链接：https://www.citadelsecurities.com/news-and-insights/global-market-intelligence/august-checklist/。 | 文章事实为高证据（稳定标题、日期、正文）；其“买方接力、盈利、估值压缩、仓位调整”是机构观点，映射 `flow_fragility` 的 replay 观察，非规则或市场事实。不能用陈旧清单判断此后新增。 |
| GMO Research Library | 陈旧产物显示列表页可读、3 个候选详情可读；0 篇窗口内 official-detail。 | 详情可读且日期均过滤为窗口前；维持 `AI_quality/capex_cycle` 的历史研究入口，不提炼新框架。 |
| Man Institute | 陈旧产物显示列表页可读、8 个候选详情可读；0 篇窗口内 official-detail。 | 详情页可读；日期不可验证候选仍只是候选，绝不写作“来源不可用”。维持 `factor_macro_exposure` / `flow_fragility` 的待刷新输入。 |

## 公开事实、推断与策略映射

- **公开事实：**本轮浏览器没有读取到目标账号的帖子正文；降级产物的三条 X profile 为空正文。小红书仅有无时间、无 URL、无正文题目候选。机构侧仅重读到上述已验证但陈旧产物中的 Citadel 官方文章。
- **我的推断：**小红书题目持续聚焦存储、光互联、MRVL/CRDO 等，最多提示 AI 基建叙事仍值得做拥挤度观察；它不证明订单、收入、价格、部署、供需或后续收益。
- **market fear gate / trend_aligned_entry：**未取得新的完成收盘、VIX/VIX3M、广度、信用或相对强弱输入，不重定级，沿用最近正式盘后审计。
- **flow_fragility：**Citadel 的已验证历史文章可作为 `citadel-august-checklist-2026-08-11` replay 标签；必须与完成收盘、波动期限结构、广度、信用和资金流代理共同检验，当前不评分。
- **AI_quality/capex_cycle / AI bottleneck watch / theme crowding：**Token、存储与互联题目只保留候选池；缺少公司公告、财报、订单、出货、利用率和毛利验证，不能改变 AI 分类、瓶颈层级或主题权重。
- **factor_macro_exposure / portfolio concentration：**没有新的可验证宏观事实。保留现有“一个有效 AI-capex sleeve”、主题重叠高及相关新增/摊低 `0%` 的既有风险记录；本报告不构成操作指令。
- **replay/backtest plan：**对 `citadel-august-checklist-2026-08-11`，在事件后 `1/5/20/60` 个完成交易日采集 SPY/QQQ/SMH、RSP/SPY、VIX/VIX3M、HYG/LQD、行业相对强弱及可用期权/资金流代理，检验其是否增加对 flow fragility 的解释力；单篇文章或单日社媒不得升级为规则。

## 数据缺口与开盘前读取

1. 需要确认 Chrome 是否能稳定结束 X 的 `Loading…` 状态，尤其是 Trump 的公开政策时间线。
2. 如有本窗口小红书单篇公开 URL，继续逐张读取笔记正文、作者评论与轮播；当前覆盖仍为 `0/unknown`。
3. 机构检查器需成功刷新 `work/institutional-research-latest.md/.json` 的运行时间，之后才可给出 AQR、Citadel、GMO、Man 的当前窗口计数。
4. 开盘前优先阅读：`memory/summary.md`、`memory/daily/2026-08-13-post-close-audit.md`、本文件、`references/realtime-public-source-tracker.md`、`references/institutional-overlays-daily-checklist.md` 与刷新后的 `work/institutional-research-latest.md`。

未更新 `decisions.md` 或 `hypotheses.md`：没有完成历史 replay 或重复验证的稳定规则。本报告不构成直接买卖建议，且不记录或推断订单、成交或账户状态。
