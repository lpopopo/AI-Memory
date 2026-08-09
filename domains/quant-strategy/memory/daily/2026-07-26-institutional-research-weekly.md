# 四大机构研究周度深度学习 — 2026-07-26

## 范围、增量窗口与证据方法

- 周度窗口：`2026-07-19T03:34:43.198Z`（上次成功周度 checker 完成时间）至本次运行。
- 已按要求运行 `institutional-research-checker.js --since 2026-07-19T03:34:43.198Z --max-items 8`；初次调用在写出结果后因外层等待超时返回，但产物已生成。已读取并核对 `work/institutional-research-latest.md` 与 `work/institutional-research-latest.json`。checker 运行时间为 `2026-07-26T03:09:40.239Z`。
- 资料通道：四家列表页与候选官方详情页均由 Reader 官方域名通道读取并逐项日期过滤。仅有稳定标题、日期和正文的 official-domain detail 才用于下述框架提炼。
- 证据边界：机构文章是高证据的“文章存在与作者论述”，向本策略的传导仍需点时数据和历史 replay；下列内容不是买卖建议。

## 本周新增研究索引

| 来源 | 核验结论 | 窗口后稳定正文 | 主题与证据质量 |
| --- | --- | --- | --- |
| AQR Research | 列表与 8 个详情均可读、日期已过滤；窗口后无新增。 | 无。 | 高：不是“未核验”。既有趋势/相对强弱优先于抄底的框架不重复升级。 |
| Citadel Securities Market Insights | Reader 官方域名列表与详情通道可读；窗口后无新增。3 个 archive 页面为 `date_unverified`，不是来源不可用。 | 无。 | 高：列表/详情已核验；保留既有 flow-fragility、风险定位与基本面交接框架。 |
| GMO Research Library | 列表与详情可读；3 篇窗口后 official-detail 可用。 | [The Electricity Tipping Point & the Next Energy Boom](https://www.gmo.com/americas/research-library/the-electricity-tipping-point--the-next-energy-boom_insights/)、[Targeting Outcomes](https://www.gmo.com/americas/research-library/targeting-outcomes_insights/)、[Mid-Year Update: Equity Dislocation Strategy](https://www.gmo.com/americas/research-library/mid-year-update-equity-dislocation-strategy_marketcommentary/)（均显示 2026-07-23）。 | 高：标题、日期、正文稳定。首篇与 AI 物理约束相关；第三篇补充期望差/动态轮动；第二篇是 EMD 结果导向配置，未新增 US AI 框架。 |
| Man Institute Market Views | 列表与详情可读；1 篇窗口后 official-detail 可用。另有 3 篇 `date_unverified` 候选，只作访问/日期限制记录。 | [The VIX Isn't Worried, But Maybe It Should Be](https://www.man.com/insights/views-from-the-floor-2026-21-July)（显示 2026-07-21）。 | 高：标题、日期、正文稳定；低波动、低相关/紧信用与集中 AI 领导并存的背离诊断。 |

## 四家机构分别学到什么

### AQR：趋势、因子与组合构建

- 本窗口列表/详情已核验、无新增。既有可复用原则保持：价格更低不是入场确认；`trend_aligned_entry` 仍需要完成收盘的趋势/相对强弱与 Fear Gate 共识。
- 未因旧文重复更新假设、框架或决策。

### Citadel Securities：市场结构、流动性与仓位

- 本窗口无新增，且不是官网不可用：Reader 官方域名的列表和详情均可读。`A More Fragile World`（7 月 18 日）在窗口前；三个 archive 仅日期不可验证。
- 既有 `flow_fragility`、`systemic_market_stress` 对 `cross_sectional_risk_localisation` 的区分继续有效。本周不把没有点时选择权、融资或零售数据的叙事硬填入评分。

### GMO：质量、估值与 AI/电力资本开支周期

- `The Electricity Tipping Point` 把 AI 数据中心放在更宽的电力需求再加速之中：发电、并网、输配电、储能、冷却和资源投入是不同环节；文章同时明确 AI 不是全部需求来源。因此，电力主题不能直接等同于单一 AI 公司订单或盈利确认。
- `Mid-Year Update: Equity Dislocation Strategy` 的可复用点是“期望差 + 动态轮动”：高增长不必然抵消过高的隐含预期，低预期资产也需实际向上意外来重估。对策略而言只形成 `expectation_gap_repricing` 的点时回放字段，不产生静态 value/growth 标签或方向判断。
- `Targeting Outcomes` 是新且高证据的 EMD 配置讨论，但与当前 US AI 股策略没有直接的新框架；仅作为明确目标与基准暴露分离的旁证。

### Man Institute：宏观、隐含暴露与回撤

- `The VIX Isn't Worried, But Maybe It Should Be` 指出在 AI/大盘科技领导集中、油价/利率/重大财报与政策事件临近时，VIX 的低位、低相关与低信用补偿可能共同反映“表面平静”。这是风险复核输入，不是预测，也不等于 VIX 低就应减仓。
- 将其定义为 `complacency_divergence`：必须同时保存波动率、集中度、信用/相关性或期权证据及事件日历；任一缺失即记录 `unavailable`，防止低 VIX 单因子化。

## 对 AI 基建/应用/存储/光互连与市场风险的映射

| 策略层 | 可立即纳入日度监控的观察项 | 未验证/回测边界 |
| --- | --- | --- |
| market fear gate | 继续使用既有完成收盘的 VIX、广度、信用与趋势输入。 | `complacency_divergence` 不可单独升降 Fear Gate。 |
| trend_aligned_entry | 当流动性背离或 AI-capex 共因子集中时，仍只允许既有的 support/reclaim + 相对强弱确认。 | 不能从机构观点或电力需求叙事直接生成入场。 |
| flow_fragility | 记录 `complacency_divergence = present/absent/unavailable`，并拆分 VIX、集中度、信用/相关性、期权和事件日历的可得性。 | 与既有 H7 流动性评分对比，不以低 VIX 单独触发。 |
| AI_quality/capex_cycle | 记录 `power_delivery_evidence = source_only/independently_confirmed/unavailable`，并标明发电、并网、输配电、储能、冷却、采购、利用率、收入和毛利所处阶段。 | 公告、产品或机构叙事仅 `source_only`；需独立规划/采购/运营/财务证据才可确认。 |
| bottleneck_watch | AI 基建、存储与光互连均需把“电力交付/并网”与“芯片、内存、光学供给”分开记录，防止把总需求误当成公司兑现。 | 需验证具体供应商的订单、出货、ASP、毛利与客户集中度。 |
| portfolio concentration | 低波动与领导集中共存时复核共同 AI-capex 因子、而非把多个 ticker 误当分散。 | 仅在现有集中度/趋势规则已触发时讨论规模影响。 |

## 自动化与回测改进

1. 在日度 overlay 记录中新增 `complacency_divergence` 的组件级字段和可得性；不得用当天之后的波动率、相关性或信用数据回填。
2. 把 2026-07-21 冻结为 H7 事件行：分别测试低 VIX 单独标签、完整联合标签和原 flow-fragility 基线，报告 1/5/20/60 日 QQQ/SPY、SMH/QQQ、RSP/SPY、HYG/LQD、MAE、误拦截与现金拖累。
3. 把 2026-07-23 冻结为 H8 事件行。电力交付只在 `independently_confirmed` 样本中评估相对选择与缺口风险；`source_only` 保持诊断样本，不能视为已实现需求。
4. `expectation_gap_repricing` 需要逐期冻结估值、业绩/指引意外和完成收盘反应，并与既有 Fear Gate、趋势、capex-cycle 分类进行增量检验。

## 记忆库更新清单

- 更新 `references/institutional-market-research-framework.md`：加入 `complacency_divergence`、`power_delivery_evidence` 与证据阶梯。
- 更新 `references/institutional-overlays-daily-checklist.md`：增加日度字段与不替代 Fear Gate 的约束。
- 更新 `references/institutional-overlays-backtest-plan.md`：为 Overlay B/C 增加点时标签、对照组与度量。
- 更新 `memory/hypotheses.md` 的 H7/H8 证据与验证任务。
- 新增本周记录并追加 `memory/daily-summaries.md`；未更新 `memory/decisions.md`。

## 下一步待验证事项

- 补齐可公开复现的 VIX 期限结构、隐含相关性/偏度、信用补偿和集中度的同期快照，先验证联合背离是否优于既有 H7。
- 对电力/并网交付使用独立来源交叉验证；区分项目宣布、设备采购、投运、利用率、收入与毛利。
- 在累计足够独立样本前，所有本周字段均为观察、假设和回测输入，不改变稳定决策或生成交易建议。
