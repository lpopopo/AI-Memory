# 2026-07-14 美股盘后正式审计

运行时间：2026-07-15 09:37--09:40 Asia/Shanghai；审计对象为 2026-07-14 美股常规交易收盘。未登录券商、未提交订单、未虚构成交；真实持仓、现金、费用、FX 与结算以用户或券商回报为准。

## 1. 收盘数据与质量

先按 `tools/README.md` 运行本地 Node Quote Workflow smoke test。`StockService.fetchQuotes` 对 MRVL、AMD、WDC、STX、SPY、QQQ、SMH、SOXX、RSP、HYG、LQD、IWM 及实际持仓返回了完整的 `Tencent (Primary)` 结构化 quote objects；并使用同一客户端的 Yahoo Chart 日线补齐和交叉验证已完成的 2026-07-14 日线（含 ^VIX、^VIX3M）。没有把 Node 的传输失败或空数组误判为整体工作流不可用，也未使用裸 `python.exe`。

| 标的 | 正式收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL | 222.44 | +2.26% | Tencent Primary 与 Yahoo Chart completed daily bar 交叉确认；高 |
| AMD | 548.13 | +2.57% | 同上；高 |
| WDC | 563.32 | +1.40% | 同上；高 |
| STX | 878.31 | +2.05% | 同上；高 |
| SPY | 751.83 | +0.36% | 同上；高 |
| QQQ | 719.71 | +1.12% | 同上；高 |
| SMH / SOXX | 600.31 / 567.92 | +2.51% / +2.58% | 同上；高 |
| VIX / VIX3M | 16.50 / 19.30 | -3.85% / n/a | Yahoo Chart completed daily bar；中高 |
| RSP / SPY | 213.45 / 751.83 | -0.36% / +0.36% | 同上；高 |
| HYG / LQD | 79.68 / 107.21 | +0.20% / +0.23% | 同上；高 |
| IWM / SPY | 294.51 / 751.83 | +0.35% / +0.36% | 同上；高 |

数据时间：2026-07-15 09:37 Asia/Shanghai 查询；Yahoo 日线最后日期均为 2026-07-14。VIX/VIX3M 同日可用，故本轮不存在前次的期限结构日期错配。

## 2. 正式 Market Fear Gate

| 信号 | 结果 | 分数 |
| --- | ---: | ---: |
| VIX 水平 / 5 日变化 / VIX÷VIX3M | 16.50 / +2.29% / 0.855 | 1 / 0 / 0 |
| SPY、QQQ、SMH 63 日回撤 | -0.76% / -3.44% / -10.26% | 0 / 0 / 2 |
| SPY、QQQ 趋势 | 均在 MA50、MA200 上方 | 0 / 0 |
| IWM/SPY、RSP/SPY、HYG/LQD 21 日变化 | -0.51% / -0.01% / +1.53% | 0 / 0 / 0 |

**Fear Gate：normal 3/14**；风险乘数 **100%**，框架最大总股票敞口 **95%**，现金底线 **5%**，框架新买入上限 **50%**。

这只是市场层结论，不等于新增仓位授权。现有四个真实持仓仍为同一 AI-capex/半导体经济与资金流因子；趋势确认未完成、QCOM 已触发失败入场复核，因此实际新增或摊低上限仍为 **0%**。

## 3. 持仓 stop-trigger table

| 标的 | 状态 / 收盘 | 既有风险线 | 触发 / near-stop | 下一步 |
| --- | ---: | --- | --- | --- |
| GLW（2） | 187.64 | 加仓需收回 200--205 并守住 190；周收 `<166-167` 重验 | 日收仍低于 190；未触发周线风险线 | `defensive hold / no add` |
| MRVL（4） | 222.44 | 周收 `<223` 重验；加仓须 250--260 且权重 <12% | 周中低于 223；周线尚未完成 | `near-weekly-risk review / no add`；本周周收若 <223 则 `reduce-review`，不得因反弹追高 |
| MXL（6） | 92.59 | 周收 `<78` 重验；加仓须 97--100 且约 6% 权重 | 未触发周线；持仓仍超高风险卫星常态规模 | `defensive hold / reduce-review`，不摊低 |
| QCOM（2） | 178.10 | 185 观察线；completed close `<182` 失败入场复核 | **已触发 `<182`** | **`reduce-review`**；人工/券商核对后决定，非自动成交 |
| AMD（历史 replay/watch） | 548.13 | completed close `<492` | 未触发，距线 +11.4% | `repair watch / no buy`；若未来收盘 <492 必为 `reduce-review` |
| WDC（历史 replay/watch） | 563.32 | `<500` | 未触发，距线 +12.7% | `defensive watch / no buy` |
| STX（历史 replay/watch） | 878.31 | `<835` | 未触发，距线 +5.2% | `defensive watch / no add`；仍按存储共因子复核 |

GLW/MRVL/MXL 的旧短线建议从未提交，且已被 2026-07-10 的长期重分类替代；上表不是券商订单。

## 4. Institutional overlay scorecard 与相关风险复核

```text
flow_fragility_score: 6/14 -> medium（proxy-based；直接期权、CTA 与杠杆 ETF 流量未取得，未以缺失数据伪造确定性）
trend_aligned_entry_score: 1/5 -> trend_broken（真实 AI-capex sleeve）
AI_quality/capex_cycle: GLW diversified_supplier / medium；MRVL cyclical_supplier+bottleneck / high；MXL speculative_bottleneck / high；QCOM diversified_supplier+edge_inference / medium-high
factor_macro_flags: growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; long_term_bottom_unconfirmed
bottleneck_watch: optical/interconnect（GLW/MRVL/MXL）与 memory/storage（WDC/STX）均无足以授权新增的基本面或相对强度确认；7 月 14 日反弹仅改善当日价格，不构成底部确认。
action impact: 不追高、不新增、不摊低；QCOM 优先 reduce-review，MRVL 等待周线确认。
```

已执行组合级相关风险复核：四个真实持仓表面上分属光互连、组件和边缘推理，但都暴露于 AI-capex/半导体周期和拥挤交易。实际股票敞口 36.69% 虽低于 normal 的 95% 总上限，仍只有 **1 个有效广义主题**；MRVL 权重 15.00% 到达正常单股上限，MXL 9.36% 高于高风险卫星的 3--6% 常态。市场转为 normal 不能解除该共因子约束。

## 5. 组合与模型净值核对

真实账户工作快照沿用用户已确认的现金基准 USD 3,756.49：

| 项目 | 金额 / 比例 |
| --- | ---: |
| GLW 2、MXL 6、MRVL 4、QCOM 2 股票市值 | USD 2,176.78 |
| 工作 NAV | **USD 5,933.27** |
| 现金 / 股票敞口 | USD 3,756.49（63.31%）/ 36.69% |
| 持仓数 / 有效主题数 | 4 / 1 |
| 最大单股 | MRVL USD 889.76（15.00%） |

历史 institutional-replay 模型不是当前真实账户；按其冻结的旧模型份额（MRVL 8.0383、AMD 4.6083、WDC 3.6880、STX 2.2401）和 USD 12,323.96 现金占位，7 月 14 日基准模型 NAV 为 **USD 20,682.97**。overlay 无明确、已验证的自动成交假设，故 overlay NAV 与差额保持空白。

## 6. Replay 与记忆边界

已向迁移后的 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加 2026-07-14 已完成收盘行；原说明中的旧 `experiments/` 相对路径已迁移，不存在于当前工作区。没有预填未来日期。

本轮没有产生经过重复验证的稳定新规则，故不修改 `decisions.md`。没有真实订单或成交记录。
