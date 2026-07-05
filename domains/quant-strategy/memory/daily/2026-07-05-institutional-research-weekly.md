# 四大机构研究周度深度学习（2026-07-05）

## 运行与证据口径

- 周度窗口：`2026-06-14T10:08:33.531Z` 至 `2026-07-05T02:13:19.417Z`，基于最近可确认的 2026-06-14 周度学习完成时点；6/24-7/2 日度 monitor 用于去重，不替代周度窗口。
- 本地 checker：`institutional-research-checker.js --since 2026-06-14T10:08:33.531Z --max-items 8`，已读取 `work/institutional-research-latest.md` 与 `.json`。
- 证据规则：只有官方域名详情页具备稳定标题、日期和正文才提炼框架。列表/分类页日期不可验证时只保留候选。本报告不构成交易建议。

## 本周新增研究索引

| 来源 | 日期 | 标题与链接 | 主题 | 证据与处理 |
| --- | --- | --- | --- | --- |
| AQR | - | [Research Library](https://www.aqr.com/Insights/Research) | 趋势、因子、组合构建 | 列表及 8 个详情均可读；窗口后无新增。最近可核验候选为 2026-05-19，属窗口前。 |
| Citadel Securities | 2026-06-19 | [Fed Views: From Inertial to Adaptive Policy Making](https://www.citadelsecurities.com/news-and-insights/global-macro-strategy/fed-views-from-inertial-to-adaptive-policy-making/) | Fed 反应函数、曲线与波动期限结构 | 高：Reader 官方域名详情标题/日期/正文稳定；策略传导中等，待市场数据验证。 |
| Citadel Securities | 2026-06-20 | [Regime Change…but Not in Iran](https://www.citadelsecurities.com/news-and-insights/macro-thoughts/regime-changebut-not-in-iran/) | 自适应政策、AI 质量分化、能源风险 | 高：Reader 官方域名通道可读；观点性结论不视为事实或交易信号。 |
| Citadel Securities | 2026-06-27 | [Beware a Shifting Landscape](https://www.citadelsecurities.com/news-and-insights/macro-thoughts/beware-a-shifting-landscape/) | AI 先通胀后生产率、token/租赁成本、存储合约 | 高：官方详情可读；文中部分公司/宏观数字需回到一手数据验证。 |
| Citadel Securities | 2026-06-30 | [1H 2026 Market Structure & Flows](https://www.citadelsecurities.com/news-and-insights/global-market-intelligence/1h-2026-market-structure-flows/) | 集中度、被动资金、零日期权、杠杆与波动 | 高：官方详情含 20 项观察；平台数据外推至全市场的证据质量为中等。 |
| Citadel Securities | 2026-07-01 | [Cruel Summer for Fixed Income](https://www.citadelsecurities.com/news-and-insights/global-macro-strategy/cruel-summer-for-fixed-income/) | 政策预期、国债流、跨资产主成分 | 高：Reader 官方域名通道可读；预测命中率与方向判断需独立样本外复核。 |
| GMO | - | [Research Library](https://www.gmo.com/americas/research-library/) | 质量、估值、AI 周期、长期回报 | 列表及 8 个详情均可读；窗口后无新增。6/12 两篇详情均早于 cutoff，不重复提炼。 |
| Man Institute | 2026-06-17 | [SpaceX – To Infinity and Beyond?](https://www.man.com/insights/views-from-the-floor-2026-17-June) | AI 上市窗口、估值与 hyperscaler FCF | 高：官方详情稳定；已在 6/17 框架中入库，本周复核。 |
| Man Institute | 2026-06-23 | [The Strait of Uncertainty](https://www.man.com/insights/views-from-the-floor-2026-23-jun) | 能源物流、通胀与供应链恢复滞后 | 高：官方详情稳定；供应缺口和恢复时长属于作者/引用估计，需独立验证。 |
| Man Institute | 2026-07-01 | [The Hard Questions for AI Bonds Investors](https://www.man.com/insights/views-from-the-floor-2026-1-july) | AI 债券供给、现金流 backstop、期限错配 | 高：官方详情稳定；已在 7/2 monitor 入库，本周复核并去重。 |

Citadel 的 3 个分类/archive 页面虽可经 Reader 读取，但没有稳定发布日期，状态保留为 `date_unverified`，不据此提炼新框架。Citadel 不能标记为官网整体不可用：本轮列表和 5 个官方详情均通过 Reader 官方域名通道可读。

## 四家机构分别学到什么

### AQR

- 窗口后没有新增研究。既有 `trend_aligned_entry` 结论维持：便宜不是入场条件，回撤后的支撑、趋势和相对强度确认仍需先于加仓。
- 本轮没有新证据修改因子构建、组合约束或 `decisions.md`。

### Citadel Securities

- 最重要的新框架是把集中度、被动流、零日期权、杠杆 ETF、融资成本、隐含相关性和 `spot up / vol up` 视为联动系统。强趋势和脆弱结构可以同时存在，结构性买盘不等于低风险。
- `adaptive policy` 是待验证的宏观状态变量：更快的政策调整可能抬高短端与短期限尾部波动，同时降低长期失控风险。不能把它机械翻译成“利率永远更高”或股票卖出信号。
- AI capex 在生产率兑现前可能先表现为芯片、内存、电力、冷却、建设和人才的成本冲击；这把 AI 基建股票同时暴露于需求增长与输入通胀/融资压力。

### GMO

- 窗口后没有新增研究。继续保留既有质量与估值框架：区分自有现金流支持的平台、分散供应商、周期供应商、应用/数据所有者和纯叙事瓶颈；被动配置也可能漂移成昂贵美国成长+紧信用利差的单一风险包。
- 本轮没有新增 GMO 框架或假设。

### Man Institute

- AI 股权与债权需要分开：股权承接上行期权，债权以固定票息承担建设延迟、超支、竞争与技术期限风险；应识别实际产生 EBITDA/FCF 的业务，而不是用合并市值替代信用分析。
- SpaceX/大型 IPO 的资金吸收能力只能说明融资窗口，不足以证明整个 AI 产业的估值和商业回报健康；AI capex 占用经营现金流会把半导体强势与软件/应用变现分开。
- 能源物流恢复存在路径依赖；停火、通道重开或现货价格回落不必然即时消除运输、库存、保险与通胀风险。

## 对当前 AI 基建、应用、存储、光互连和市场风险的启发

- `market fear gate`：新增字段只做解释层。没有 VIX/VIX3M、宽度、信用和完成收盘趋势确认，不改变正式风险状态。
- `trend_aligned_entry`：零日期权、零售抄底和被动流支持不能替代个股/主题的支撑、reclaim 与相对强度。
- `flow_fragility`：AI/半导体若同时出现窄宽度、看涨期权集中、杠杆 ETF 扩张、spot-up-vol-up、低隐含相关性和融资价差上升，应提高放大风险等级，但不能单独做空。
- `AI_quality/capex_cycle`：基建与存储/光互连仍受物理瓶颈支持，但必须同步检查客户锁价、capex 吞噬 OCF、billable utilization、债务期限和现金流 backstop；应用层则必须证明收入/留存/单位经济，而非依赖基建支出外推。
- `factor_macro_exposure`：AI 组合可能同时是成长久期、输入通胀、半导体周期、外部融资和能源物流风险；ticker 数量不是风险分散。
- `bottleneck_watch`：把“容量短缺”拆为芯片/内存/电力/冷却/互连/物流，并记录瓶颈是否带来供应商收入、客户成本上升、替代路线或需求破坏。
- `portfolio concentration`：GLW/MXL/DRAM/MU/MRVL 等不同标签仍可能共享 AI-capex、半导体周期和拥挤流量冲击；本周研究不改变已有完成收盘退出/减仓规则，也不生成新买入建议。

## 可立即纳入日度监控

- 在现有 14 分 `flow_fragility` 分数外，单列可得性和数值：0DTE 占比/平均期权期限、半导体 call premium、倒挂 call skew 覆盖率、杠杆科技/半导体 ETF AUM、隐含相关性、半导体隐含波动、spot-up-vol-up 频率、融资价差代理。
- `factor_macro_exposure` 增加观察字段：`adaptive_policy_surprise`、`AI_input_cost_pressure`、`energy_logistics_lag`；缺失时写 `unavailable`，不能以主观评分补齐。
- AI 候选增加：OCF、CapEx、FCF、债务到期结构、债券/贷款利差、产生现金流的业务分部、已安装/已验收/可计费容量和利用率。

## 假设与回测改进

- H7 增加 `short_duration_leverage_density`、`spot_vol_correlation_shift`、`financing_capacity_pressure`，逐字段消融验证，不一次性改变交易规则。
- 新增 H11：自适应政策与 AI 物理输入成本可能在股票趋势破坏前改变因子暴露；若其不比 fear gate 和价格趋势提供增量预警，应拒绝该假设。
- 对 2022 成长久期压力、2024-2026 AI 集中行情及已知半导体反转事件做 point-in-time replay，比较 1/5/20/60 日 QQQ/SPY、SMH/QQQ、IGV/QQQ、HYG/LQD、收益率曲线和最大不利波动。
- 自动化应保存每个直接指标的 `value/source/as_of/availability`，避免把缺失期权或融资数据等同于低风险。

## 记忆库更新清单

- 新增本周周报：`memory/daily/2026-07-05-institutional-research-weekly.md`。
- 更新稳定参考：`references/institutional-market-research-framework.md`，加入结构性资金集中与短期限杠杆框架。
- 更新日度 checklist 与 backtest plan，加入直接市场结构诊断和增量消融指标。
- 更新 `memory/hypotheses.md`：扩展 H7，新增 H11。
- 更新 `memory/daily-summaries.md`。
- `memory/decisions.md` 不变：尚无历史 replay 或反复验证支持规则晋级。

## 下一步待验证事项

1. 为 0DTE、call skew、杠杆 ETF AUM、隐含相关性与融资价差寻找稳定、可追溯且 point-in-time 的公共数据源。
2. 建立 Citadel 6/19、6/20、6/27、6/30、7/1 与 Man 6/17、6/23、7/1 的事件表，冻结首次可见时间。
3. 先跑诊断与消融，再测试 elevated/acute 状态下减少新仓 25%-50% 是否改善回撤且不过度错失趋势赢家。
4. 独立核验机构文章引用的宏观、公司、债券发行和现金流数字；机构观点本身不能替代一手数据。
