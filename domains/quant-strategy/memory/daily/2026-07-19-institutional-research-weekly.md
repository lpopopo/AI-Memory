# 四大机构研究周度深度学习 — 2026-07-19

## 范围与证据方法

- 周度窗口：`2026-07-12T02:05:31.859Z`（上次成功周度 checker 完成时间）至本次运行。
- 已按要求运行 `institutional-research-checker.js --since 2026-07-12T02:05:31.859Z --max-items 8`，生成并读取 `work/institutional-research-latest.md` 与 `work/institutional-research-latest.json`。后者存在解析错误（正文中的未转义字符），因此以已生成 Markdown 表、原始 JSON 文本和官方详情页逐项核验；这不改变 checker 的来源诊断。
- checker 完成时间：`2026-07-19T03:34:43.198Z`。四家官方列表均由 Reader 官方域名通道可读，候选详情也逐项读取并按日期过滤。Citadel 不是“官网不可用”。

## 本周新增研究索引

| 来源 | 详情页核验结果 | 本窗口稳定正文文章 | 主题与证据质量 |
| --- | --- | --- | --- |
| AQR | 列表与 8 个详情可读 | 无新增 | 高：列表/详情日期过滤完成；不把“无新增”写成未核验 |
| Citadel Securities | Reader 官方域名列表与详情可读；3 个 archive 页仅 `date_unverified` | [After the Reset: Time to Focus on Fundamentals](https://www.citadelsecurities.com/news-and-insights/global-market-intelligence/after-the-reset/)（页面显示 2026-07-13） | 高：标题、日期、正文稳定；市场结构、零售/仓位、行业内风险定位、盈利窗口 |
| GMO | 列表与详情可读 | [Targeting Outcomes](https://www.gmo.com/americas/research-library/targeting-outcomes_insights/)、[Mid-Year Update: Equity Dislocation Strategy](https://www.gmo.com/americas/research-library/mid-year-update-equity-dislocation-strategy_marketcommentary/)、[Japan Equities](https://www.gmo.com/americas/research-library/japan-equities_insights/)（均 2026-07-15） | 高：标题、日期、正文稳定；其中仅 Equity Dislocation 直接补充 US AI 质量/估值框架 |
| Man Institute | 列表与详情可读；另有 3 篇候选 `date_unverified`，未被当作本周新增研究 | [Chips Down, Then What?](https://www.man.com/insights/views-from-the-floor-2026-14-july)（页面显示 2026-07-14） | 高：标题、日期、正文稳定；AI stack 选择性、存储供给、杠杆/集中度、私有模型公司与中国竞争 |

## 四家机构分别学到什么

### AQR

- 本窗口列表与详情均已核验、无新增。既有原则不变：反对把“更便宜”直接等同于入场，趋势、相对强弱和风险门槛仍优先于抄底叙事。
- 本轮不因旧文重复更新框架、假设或决策。

### Citadel Securities

- 市场可从仓位/机械流主导切换至盈利与基本面主导，但该判断要拆成：零售需求、技术仓位、领导宽度、融资条件、估值和随后盈利兑现六项，而不是一个乐观/悲观标签。
- 宽基指数平静并不排除半导体、动量和单名对冲集中的横截面压力。对 AI-capex 共因子组合，这是“集中度/追高”检查，而非自动 Fear Gate 升级。
- 日度可纳入：`risk_localisation` 和 `flow_to_fundamentals_handoff` 字段；缺少可复现的期权、融资或零售数据时必须记为 `unavailable`。

### GMO

- `Mid-Year Update` 的直接启发是：AI disruption 下，高估值/完美预期公司可能因微小落差重估；相反，普通预期中的便宜公司对上行意外更敏感。适合将“预期差”与估值、指引和业绩后价格反应一起研究，而不是用静态 value/growth 标签。
- 该文的动态轮换强调暴露会随估值变化而改变，支持现有 AI_quality/capex_cycle 与 portfolio concentration 的“按证据复核”方法；不构成多空建议。
- `Targeting Outcomes` 与 `Japan Equities` 的正文及日期已核验，但前者是 EM 债券的目标收益/基准暴露讨论，后者是日本结构改革，未直接新增 US AI 交易框架；仅记录为 outcome-based exposure governance 的旁证。

### Man Institute

- AI 交易从“持有整个主题”向跨 stack 选择转变：GPU、存储、光互连、晶圆产能、基础设施和最终应用不应被视作同一个方向因子。已有 `AI_stack_selectivity_rotation` 继续有效。
- 新文提示需核验存储紧张是否缓和、私有模型公司承诺与云端收入/backlog 的错配、以及中国芯片/开源模型成本竞争。它们是待验证的质量、现金流和脆弱性字段，不是对存储、光互连或应用层的买卖结论。
- 对本组合的含义是优先降低 AI-capex 共因子误判：当前 trend/Fear Gate/持仓集中度控制优先，关注指标不能替代完成收盘确认。

## 映射、自动化与回测

- **立即日度观察：** `systemic_market_stress` 对 `cross_sectional_risk_localisation` 的区分；`flow_to_fundamentals_handoff`；业绩/指引后的价格确认；存储供需、客户集中度、AI capex 的现金流/融资回补。均为监控字段，缺数据则 `unavailable`。
- **未验证假设：** 已追加到 H7/H8 的 `expectation_gap_repricing` 与风险定位字段，要求冻结首次可见时间并进行回放。
- **稳定参考框架：** 更新 `references/institutional-market-research-framework.md`、日度 checklist 和 Overlay B 回测计划，明确“系统性”与“横截面”风险不能互相替代。
- **回测任务：** 在 2026-07-13/15 事件标签上，比较 QQQ/SPY、SMH/QQQ、RSP/SPY、HYG/LQD 及存储、光互连、设备、云和软件篮子的 1/5/20/60 日表现、MAE、误拦截、现金拖累；先诊断，后评估是否有增量价值。

## 记忆库更新与边界

- 已更新 institutional framework、daily checklist、backtest plan 与 `hypotheses.md`；已追加 `daily-summaries.md`。`decisions.md` 未改。
- 无券商隐私、账户凭证、真实订单或成交写入；机构观点未被转化为交易建议。
- 下一步：收集可复现的横截面期权/融资/宽度代理，并以已完成收盘和 PIT 时间戳验证新增字段是否优于现有 Fear Gate、趋势和 concentration 规则。
