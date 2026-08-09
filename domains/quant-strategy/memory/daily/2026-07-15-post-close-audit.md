# 2026-07-15 美股盘后正式审计

运行时间：2026-07-16 Asia/Shanghai；审计对象为 2026-07-15 美股常规交易收盘。未登录券商、未提交订单、未假设成交；真实持仓、现金、费用、FX 与结算均以用户或券商回报为准。

## 收盘数据与质量

先按 `tools/README.md` 运行本地 Node Quote Workflow Smoke Test。`StockService.fetchQuotes()` 对 MRVL、AMD、WDC、STX、GLW、MXL、QCOM、SPY、QQQ、SMH、SOXX、VIX、RSP、HYG、LQD、IWM 均返回了非空、结构化的 `Tencent (Primary)` quote objects；Node 工作流可用。其内置 Yahoo Chart 日线备用交叉校验在本环境对全部标的返回 HTTP 404，因此不把该备用源失败写成工作流不可用。VIX3M 未返回；Cboe CSV 与浏览器可见快照也未能取得可验证数值。

| 标的 | 收盘/可靠盘后报价 | 日变动 | 来源与质量 |
| --- | ---: | ---: | --- |
| MRVL | 206.26 | -7.27% | Tencent (Primary)；中等（Yahoo 日线交叉校验 404） |
| AMD | 529.14 | -3.46% | Tencent (Primary)；中等 |
| WDC | 513.84 | -8.78% | Tencent (Primary)；中等 |
| STX | 828.30 | -5.69% | Tencent (Primary)；中等 |
| SPY / QQQ | 754.81 / 717.74 | +0.40% / -0.27% | Tencent (Primary)；中等 |
| SMH / SOXX | 590.77 / 555.27 | -1.59% / -2.23% | Tencent (Primary)；中等 |
| VIX / VIX3M | 21.67 / unavailable | 0.00% / n.a. | VIX：Tencent (Primary)，指数日内字段不完整、低中等；VIX3M：缺口 |
| RSP / SPY | 212.97 / 754.81 | -0.22% / +0.40% | Tencent (Primary)；中等 |
| HYG / LQD | 79.81 / 107.58 | +0.16% / +0.35% | Tencent (Primary)；中等 |
| IWM / SPY | 295.77 / 754.81 | +0.43% / +0.40% | Tencent (Primary)；中等 |

数据查询时间：本审计运行时（2026-07-16 Asia/Shanghai）；数据日为 2026-07-15 美国常规交易日。VIX3M、21 日相对比率和新的完整日线 MA/63 日回撤缺失，故以下门控为保守的、质量受限的正式工作状态，而非精确回测读数。

## Market Fear Gate

| 信号 | 结论 | 分数 |
| --- | --- | ---: |
| VIX 水平 | 21.67，处于 elevated 上沿 | 1 |
| 波动冲击 | 较 7 月 14 日已验证收盘 16.50 上升约 31.3%；不是完整 5 日读数，按保守临时压力项处理 | 2 |
| VIX/VIX3M | VIX3M 缺口，未伪造期限结构结论 | 0 |
| 半导体风险 | SMH/SOXX 显著弱于 SPY；7 月 14 日已验证 SMH 63 日回撤约 -10.26%，本日继续下跌 | 2 |
| 指数趋势、21 日宽度/信用 | 新完整日线 MA、21 日比率缺口；不计为利好 | 0 |

**Fear Gate：`elevated 5/14`（可得数据下限、保守判定）**。风险乘数 **70%**，框架最大总股票敞口 **75%**，现金底线 **25%**，框架新买入上限 **25%**。实际新买入/摊低上限仍为 **0%**：真实组合只有一个 AI-capex/半导体共因子，趋势入场破坏，且 QCOM 已触发 completed-close 风险线。

## Stop-trigger table

| 标的 | 收盘 | 既有风险线 | 触发 / near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（2） | 174.41 | 周收 `<166–167` 重验；加仓需重回 200–205 且守住 190 | 未触发；距周线风险约 4.5%，near-stop | `defensive hold / near-stop review / no add` |
| MXL（6） | 88.84 | 周收 `<78` 重验；加仓需 97–100 且约 6% 权重 | 未触发，距线约 +13.9% | `defensive hold / reduce-review / no add` |
| MRVL（4） | 206.26 | 周收 `<223` 重验；加仓需 250–260 且权重 <12% | 本周中已低于 223，周线尚未完成 | `near-weekly-risk review / no add`；若本周完成周收仍 `<223`，升为 `reduce-review`；事件反弹不得追高 |
| QCOM（2） | 177.98 | 185 观察线；completed close `<182` 为失败入场复核 | **仍触发** `<182` | **`reduce-review`**；下次人工/券商对账先核实持仓，非自动成交 |
| AMD（历史 replay/watch） | 529.14 | completed close `<492` | 未触发，距线 +7.5% | `repair watch / no buy`；若后续收盘 `<492`，必须 `reduce-review` |
| WDC（历史 replay/watch） | 513.84 | `<500` | 未触发，距线 +2.8%，near-stop | `defensive hold / near-stop review / no buy` |
| STX（历史 replay/watch） | 828.30 | `<835` | **触发** | `reduce-review`（replay 风险状态）；不推定真实账户持仓或成交 |

GLW、MRVL、MXL 的旧短线保护建议从未提交，且已被 2026-07-10 的长期重分类取代；表中不构成券商订单。

## Institutional overlay scorecard 与组合相关风险复核

```text
flow_fragility_score: 7/14 -> elevated（proxy-based）
  窄幅领导 2：SPY 上涨而 RSP 下跌；半导体/AI 集中度 2：SMH/SOXX 与相关持仓同步显著走弱；
  系统性/波控 1：前一日低 VIX 后出现急升；主题拥挤 2：真实四项均为 AI-capex 共因子。
  期权、CTA、买回窗口与杠杆 ETF 的直接数据缺失，未假定为事实。
trend_aligned_entry_score: 1/5 -> trend_broken（仅 market gate 尚允许有限风险；价格趋势、相对强度、回撤质量和催化剂价格确认均不足）
AI_quality/capex_cycle: GLW diversified_supplier / medium；MRVL cyclical_supplier+bottleneck / high；MXL speculative_bottleneck / high；QCOM diversified_supplier+edge inference / medium-high；本日价格为 rejected。
factor_macro_flags: growth_duration_high; volatility_shock; semiconductor_basket_unwind; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; long_term_bottom_unconfirmed
bottleneck_watch: 光互连与存储瓶颈叙事未获价格确认；不提升任何标的的行动等级。
action impact: 禁止追高、关联加仓和摊低；优先处理 QCOM 风险复核，MRVL 等待完成周线；WDC/STX 保持防御性复核。
```

已执行组合级相关风险复核：四个真实持仓表面分属光互连、组件与边缘推理，但均受 AI-capex、半导体估值与资金流冲击影响，故按 **一个有效主题** 管理。股票敞口低于 fear gate 总上限不构成放宽理由；关联新增仓位仍为 0%。

## 组合与模型净值核对

以用户确认的现金基准 USD 3,756.49 与上述可靠收盘报价计算：

| 项目 | 金额 / 比例 |
| --- | ---: |
| GLW 2 / MXL 6 / MRVL 4 / QCOM 2 股票市值 | USD 2,062.86 |
| 工作 NAV | **USD 5,819.35** |
| 现金 / 股票敞口 | USD 3,756.49（64.55%）/ USD 2,062.86（35.45%） |
| 持仓数 / 有效主题数 | 4 / 1 |
| 最大单股 | MRVL USD 825.04（14.18%） |

冻结的历史 institutional-replay 模型按 MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401 股与现金 USD 12,323.96 复算的基准 NAV 为 **USD 20,170.89**。overlay 没有已验证的自动成交假设，overlay NAV 与差额保持空白。

## Replay 与记忆边界

已向迁移后的 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加 2026-07-15 已完成收盘行；未预填未来日期。单日压力警报和一次 replay 不构成稳定规则，故 **未更新 `decisions.md`**。未记录任何真实订单或成交。
