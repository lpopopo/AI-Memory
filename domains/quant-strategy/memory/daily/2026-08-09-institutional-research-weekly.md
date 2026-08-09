# 2026-08-09 四大机构研究周报

运行完成：`2026-08-09 22:33 Asia/Shanghai`。本次使用上次周度成功检查器锚点 `2026-07-26T03:09:40.239Z`，并先运行并读取：

- `work/institutional-research-latest.md`
- `work/institutional-research-latest.json`

JSON 本轮含有未转义文本，无法被标准解析器读取；已按原始文本逐源核对，并与 Markdown 诊断和四个官方详情页交叉验证。该解析缺陷不改变已核验条目，但下次运行应修复检查器的 JSON 转义。

本记录只使用公开、只读材料；不含券商账户、凭证、订单、成交或未经验证的交易建议。

## 本周新增研究索引与核验状态

| 来源 | 核验结果 | 本窗口合格详情 | 证据与处理 |
| --- | --- | --- | --- |
| AQR Research | 本次 Reader 官方列表通道读取失败，且没有可核验候选详情 | 0 | 这是本窗口访问缺口，不能写成“无新增”或“来源不可用”；不从标题/搜索结果提炼框架。|
| Citadel Securities Market Insights | Reader 官方域名列表与 3 个稳定详情可读 | 3 | `August - After The Reset`、`From Forward Guidance to Market Guidance`（均 8/03）已由 8/04 日度续查入库；本周新增处理 8/05 的 `Traders on Defense`。三个 archive/tracker 候选为 `date_unverified` 或安全校验限制，只保留候选。|
| GMO Research Library | Reader 官方列表和 3 个候选详情可读 | 0 | 候选均早于窗口；列表/详情已核验，窗口后无新增。|
| Man Institute Market Views | Reader 官方列表与稳定日期详情可读 | 1 | 7/28 的 `The Yield Trap Hiding in Junior Bank Bonds` 为可用官方详情；其它无稳定日期候选仅记录、未提炼。|

## 分机构学习

### AQR：趋势、因子与组合构建

本轮没有新的可稳定核验详情；不改变既有“趋势/相对强度确认优先于机械抄底”的框架。AQR 本次是局部访问缺口，不是来源整体不可用结论。

### Citadel Securities：市场结构、流动性与资金流

- [Traders on Defense](https://www.citadelsecurities.com/news-and-insights/retail-detail/traders-on-defense/)（2026-08-05，官方域名 Reader 详情高证据）描述其平台在 7 月看到的零售期权防御转换：put premium 创纪录，活动由单股向指数/ETF 期权倾斜，且 8 月初出现现金股与期权的获利了结。其半导体、存储和软件的具体流量指标是平台专有事实，不能静默替换为价格指标。
- 8/03 的两篇 Citadel 详情已在 8/04 续查处理：它们保留 `flow_to_fundamentals_handoff_v2`、`market_guidance_reflexivity`、`AI_diffusion_cost_policy`、`social_license_permitting_bottleneck` 与 `product_complex_inflation_pass_through` 为实验字段。本周不重复升级。

可复用结论：把“参与度很高”与“在加风险还是转移风险”分开记录；指数平静或反弹本身不能证明 AI-capex 共同因子风险已解除。

### GMO：质量、估值与 AI 周期

官方列表和详情已核验但窗口后无新增。因此维持既有 `AI_quality/capex_cycle`、`expectation_gap_repricing` 与 `power_delivery_evidence` 梯度，不新增 GMO 框架。

### Man Institute：宏观、因子隐含暴露与回撤

- [The Yield Trap Hiding in Junior Bank Bonds](https://www.man.com/insights/views-from-the-floor-2026-28-July)（2026-07-28，官方域名 Reader 详情高证据）指出 AT1 的紧信用利差可同时伴随更长的有效久期、赎回延迟/负凸性和文件条款差异。它不是 AI 或股票方向判断；可复用的是“收益补偿压缩不等于风险下降”的结构化信用审查思路。

## 对当前量化策略的映射

| 模块 | 本周影响 |
| --- | --- |
| market fear gate | 不变；零售防御或复杂信用观察不能改写既有完成收盘波动率、广度、信用和趋势输入。|
| trend_aligned_entry | 不变；即使出现流动性/仓位“重置”叙事，仍要完成 support/reclaim、相对强度和盈利/指引确认。|
| flow_fragility | 新增诊断字段 `retail_risk_transfer`：`defensive` / `neutral` / `risk_seeking` / `unavailable`，必须记录来源和首次可见时间。|
| factor_macro_exposure | 新增诊断字段 `complex_credit_complacency`：利差补偿、久期/展期、负凸性和条款风险分开记录；没有点时专业数据则为 `unavailable`。|
| AI 质量、基建/应用、存储、光互连 | 零售对半导体/存储的防御转换强化了共同因子复核，而非公司订单、收入或瓶颈持续性的证明；原有 AI 质量、供电/许可与应用层单位成本框架不变。|
| portfolio concentration | 现有 AI-capex 单一有效 sleeve 约束不放宽；新字段只请求共同因子审查，不自动触发调仓。|

## 自动化与回测改进

1. 日度清单新增 `retail_risk_transfer` 和 `complex_credit_complacency`，专有平台数据须标 `source_only`，缺失不猜测。
2. 在 Overlay B 中冻结 2026-08-05 与 2026-07-28 事件行，分开测试原始来源与可公开复现代理；比较 1/5/20/60 日 QQQ/SPY、SMH/QQQ、RSP/SPY、HYG/LQD、VIX/VIX3M 和收益率变动，并报告 MAE、误报、错失赢家与现金拖累。
3. 先检查新增字段是否在 Fear Gate、趋势和已有 H7 流动性代理之外提供增量解释；若只是复述已发生价格变化，则拒绝晋升。

## 记忆库更新清单

- 更新 `references/institutional-market-research-framework.md`：增加两个可复用但实验性的字段合同。
- 更新 `references/institutional-overlays-daily-checklist.md` 与 `references/institutional-overlays-backtest-plan.md`。
- 更新 `memory/hypotheses.md` 的 H7/H11 证据与验证计划。
- 新增本周记录并追加 `memory/daily-summaries.md`。
- 未更新 `memory/decisions.md`：没有完成历史 replay 或重复验证的规则。

## 下一步待验证事项

- 为零售风险转移寻找公开、点时、可复现的期权期限、指数/ETF 对单股比重或资金流代理；不能用后验价格反推。
- 验证复杂信用补偿/结构变量是否能在 HYG/LQD、利率和 AI-capex 相对收益以外提供预警；若不能，保留为观察项。
- AQR 下次须重新尝试官方列表/详情通道；本轮不以访问失败推断其窗口内无新研究。

结论仅为研究与监控输入，不构成买卖建议。
