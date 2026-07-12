# 四大机构研究周度深度学习（2026-07-12）

## 运行与证据口径

- 检索窗口：`2026-07-05T02:13:19.417Z` 至 `2026-07-12T02:05:31.859Z`；起点为上次周度研究 checker 完成时间。
- 已运行并读取 `institutional-research-checker.js --since 2026-07-05T02:13:19.417Z --max-items 8` 的 Markdown 与 JSON 产物：`work/institutional-research-latest.md`、`work/institutional-research-latest.json`。
- 提炼门槛：仅 official-domain detail 页面同时具备稳定标题、日期和正文时才提炼新框架。机构观点是研究输入，不是交易建议；未经 point-in-time replay 的规则不进入 `decisions.md`。

## 本周新增研究索引

| 来源 | 核验状态 | 窗口后新增 | 处理 |
| --- | --- | --- | --- |
| AQR Research | Reader 官方域名列表、8 个候选详情均可读；日期已核验 | 0 | 列表/详情已核验，窗口后无新增；维持趋势优先于抄底、因子与组合约束框架。 |
| Citadel Securities Market Insights | Reader 官方域名列表、8 个候选详情均可读；3 个 archive 页面日期不可验证 | 0 | 列表/详情已核验，窗口后无新增；不得将 archive 候选或通道问题写成官网整体不可用。 |
| GMO Research Library | Reader 官方域名列表、8 个候选详情均可读；日期已核验 | 0 | 列表/详情已核验，窗口后无新增；维持质量、估值与 capex-cycle 分类。 |
| Man Institute Market Views | Reader 官方域名列表、8 个候选详情可读；其中 1 篇日期与正文稳定 | 1 | 新增高证据文章并只作为观察/假设/回测输入。 |

### 新增可提炼文章

- Man Group，2026-07-07，[Could 'Super El Niño' Scorch AI Too?](https://www.man.com/insights/views-from-the-floor-2026-7-july)。文章将气候波动描述为可能的复合输入冲击：热浪/干旱可同时推高制冷负荷、加剧水资源和电网约束，并经 LNG、化肥、农产品、铜/铝和物流传导。AI 数据中心的电力与冷却水需求使其与这些约束相互叠加。证据质量：高（官方详情标题、日期、正文可读）；对股票策略的传导质量：中等，须独立事件数据与回放验证。

## 四家机构分别学到什么

- **AQR：** 本周无新增。继续使用既有结论：估值回落不是入场条件；`trend_aligned_entry` 仍需完成收盘的趋势/相对强度/支撑收复确认。组合构建必须先看共同风险，不能由单一主题热度替代约束。
- **Citadel Securities：** 本周无新增。其官方域名 Reader 通道可读，既有市场结构结论仍是流动性、被动资金、零日期权、杠杆 ETF 与隐含相关性共同决定脆弱性；只用于 `flow_fragility` 诊断，不作为单独做空或卖出信号。
- **GMO：** 本周无新增。继续区分平台/多元供应商、周期供应商、应用/数据所有者和叙事型瓶颈；以现金流、客户集中度、资本开支周期、估值与实际 AI 变现质量约束候选排序。
- **Man Institute：** 新增“气候—资源—AI 输入”框架。重点不是预测天气，而是在已被独立数据确认的电力、水、LNG/物流或关键材料约束出现时，检查 AI 基建、存储与光互连是否共享成本和供给冲击。

## 对当前策略的映射

- **可立即纳入日度监控：** 在 `factor_macro_exposure` 下增加 `climate_resource_input_stress`，仅允许 `low/elevated/high/unavailable`，并必须保存 `source/as_of`。`elevated/high` 只触发共同因子复核；不能自行改变 market fear gate 或生成买卖指令。
- **AI 基建/存储/光互连：** 同时检查电力、冷却/水、LNG/物流、铜/铝等输入约束，和客户 capex、可计费利用率、OCF/FCF、融资期限、相对强度。它们常为同一 AI-capex 因子，而不是独立分散。
- **AI 应用：** 气候输入压力不能外推为应用层受益或受损；仍以收入、留存、单位经济和价格确认作为主证据。
- **市场风险：** `market fear gate`、完成收盘趋势和既有集中度上限优先。`flow_fragility`、`AI_input_cost_pressure`、`energy_logistics_lag` 与新字段只提供解释和候选假设。

## 自动化与回测改进

1. 日度记录新增字段必须保存 `value/source/as_of/availability`；无独立证据时固定为 `unavailable`，不可主观补分。
2. 建立独立核验的电网/水资源/LNG/物流/关键材料约束事件表，冻结 first-visible 时间，禁止以后验天气结果回填事件。
3. 在 Overlay F 中比较“Fear Gate + trend + flow fragility”基线与新增诊断；仅在已验证的约束、`flow_fragility >= elevated` 或主题重叠高、且趋势未确认时，研究 25%-50% 新增仓降幅。
4. 以 QQQ/SPY、SMH/QQQ、存储、光互连、能源/电力、工业金属、VIX/VIX3M、HYG/LQD 和收益率的 1/5/20/60 日表现、MAE、错失赢家率、回撤、现金拖累与换手为结果指标。

## 记忆库更新清单

- 更新 `references/institutional-market-research-framework.md`：加入 Man 的气候—资源—AI 输入压力框架。
- 更新 `references/institutional-overlays-daily-checklist.md`：加入有来源/时点约束的日度诊断字段。
- 更新 `references/institutional-overlays-backtest-plan.md`：新增 Overlay F。
- 更新 `memory/hypotheses.md`：新增 H14；未更新 `decisions.md`。
- 本文件为阶段性周报；不记录账户、凭证或真实交易信息。

## 下一步待验证事项

1. 为 H14 选取可追溯且独立的约束事件，而非只使用机构观点或天气叙事。
2. 检验 H14 是否提供 Fear Gate、趋势、`flow_fragility`、H11 输入压力字段之外的增量预警；没有增量即拒绝。
3. 下一周继续以本次 checker 完成时间 `2026-07-12T02:05:31.859Z` 为默认起点，并保留四类访问诊断。
