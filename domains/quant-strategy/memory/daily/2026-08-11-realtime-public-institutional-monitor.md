# 2026-08-11 实时公开来源与机构研究监控

运行时间：2026-08-11 22:49 Asia/Shanghai。增量窗口：`2026-08-06T13:17:14.178Z` 至本次运行；起点取自最近一次已成功刷新并读取的机构检查器产物。

本记录仅含公开、只读资料。未读取 cookies、密码、本地存储、私信、通知或设置；未进行任何社交互动、券商登录、下单、成交记录或账户状态推断。

## 证据与访问状态

- Chrome：按公开只读方式连接并尝试读取 `@Kay2289123`，页面加载/可见 DOM 连续超时且浏览器连接重置，未得到正文快照。因此所有指定 X 账号和小红书均为本轮**浏览器可见访问缺口**，不是“没有更新”或“来源不可用”。
- 降级诊断：按工具说明运行并读取 `work/realtime-public-source-latest.md/.json`。`@nvidia`、`@elonmusk`、`@realDonaldTrump` 的 Jina profile 均为 HTTP 200 但正文长度 0；没有 URL、时间、正文同时齐备的新 status，故没有可记录的 verified social item。
- 小红书“美研芒格君”/Kay2289123：原始公开主页可返回，只有无稳定单篇 URL、发布时间、正文、作者评论或轮播图的标题候选；本轮图片已读 `0/unknown`。其只能作为低到中证据的主题热度线索，不作为笔记事实或新内容确认。

## 已核验机构来源

| 平台/来源 | 机构 | ID / 日期 | 链接 | 类型 | 公开事实摘要 | 作者观点 / 策略映射 | 证据 | 待验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 官方详情页 | AQR Research | 2026-08-11；`Ten Lessons on Managing Concentrated Wealth` | https://www.aqr.com/Insights/Research/Tax-Aware-Investing/Ten-Lessons-on-Managing-Concentrated-Wealth | 研究文章 | 官方域名详情页含稳定标题、日期和正文；文章讨论集中财富/集中持仓的差异化风险管理。 | 只映射为 `portfolio concentration` 的研究复核：集中敞口需按风险、约束与目标单独审查，不能把“长期持有理由”当作相关性或流动性风险已消失。不得据此改变仓位或规则。 | 高：官方详情页可读，标题、日期、正文均稳定。 | 未来用公开可复现的组合浓度、相关性和回撤数据完成 replay；文章不提供当前标的的价格或收益确认。 |

机构检查器已刷新并读取 Markdown/JSON：AQR `1/8` 篇窗口内 official-detail 高证据文章；Citadel Securities `0/8`、GMO `0/3`、Man Institute `0/8`。后三者的列表页与候选详情页按日期过滤完成；“0”仅表示本次检查器抓取并核验的候选中没有窗口内、稳定日期的官方详情文章，不把列表候选或日期不可验证条目提炼为新框架。

## 事实、推断与策略映射

- **公开事实：** 本轮仅确认上述 AQR 文章。社媒检查未获得满足 ID/URL/时间/正文要求的新条目。
- **我的推断：** AQR 的集中风险讨论支持继续把当前 AI-capex 暴露作为一个有效主题 sleeve 做相关性复核；这不是关于个别公司的订单、收入、估值或未来价格的判断。
- **未核验证据：** 小红书标题候选、全部未能加载的 X 正文、Trump 的窗口内政策内容，以及任何由社媒引出的供应链、订单、收入或部署结论。
- **market fear gate / trend_aligned_entry：** 不重定级；本轮没有完成收盘价、波动率、广度或相对强度输入。
- **flow_fragility / factor_macro_exposure：** 不重算；AQR 条目只提示集中风险审查，不替代流动性、信用或宏观因子数据。
- **AI_quality/capex_cycle / AI bottleneck watch / theme crowding：** 无新官方 detail 证据；小红书标题线索不升级。
- **portfolio concentration：** 维持既有“一个有效 AI-capex sleeve、相关新增/摊低 0%”的约束；本记录不形成操作建议。
- **replay/backtest plan：** 对 AQR 2026-08-11 条目建立候选事件行：在 `1/5/20/60` 个完成交易日比较 QQQ/SPY、SMH/QQQ、RSP/SPY、HYG/LQD、VIX/VIX3M，并测试其是否为既有集中度/相关性字段带来增量解释；未完成 replay 前不更新 `decisions.md`。

## 数据缺口与后续开盘准备

1. Chrome 可见社媒页面持续超时；请在 Chrome 保持登录、网络稳定且目标页可打开后再触发补读。小红书如出现稳定新笔记 URL，需逐条读取正文、作者评论和全部轮播图。
2. `@realDonaldTrump` 的窗口内公开政策覆盖未完成，不能解释为没有更新。
3. 开盘准备优先读取：`memory/summary.md`、`memory/daily/2026-08-10-post-close-audit.md`、本文件、`references/realtime-public-source-tracker.md`、`references/institutional-overlays-daily-checklist.md`。

未修改 `decisions.md` 或 `hypotheses.md`：没有经历史 replay 或反复验证的稳定新规则。本记录不构成买卖建议。
