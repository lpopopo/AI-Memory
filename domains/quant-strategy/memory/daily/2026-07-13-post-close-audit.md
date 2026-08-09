# 2026-07-13 美股盘后正式审计

运行时间：2026-07-14 23:41--23:45 Asia/Shanghai。审计对象为 2026-07-13 美股常规交易收盘；运行时 2026-07-14 美东仍在盘中，因此没有把即时行情写成收盘。未登录券商、未提交订单、未虚构成交；真实持仓、现金、费用、FX 与结算以用户或券商回报为准。

## 1. 数据、正式收盘与质量

先按 `tools/README.md` 运行本地 Node Quote Workflow smoke test。`StockService.fetchQuotes` 对 MRVL、AMD、SPY、QQQ、SMH 及扩展标的返回了结构化 `Tencent (Primary)` objects；运行时的 `price` 为 7 月 14 日美东盘中价，故本审计只取其 `yesterdayClose` 作为 7 月 13 日收盘交叉核验。随后使用 Codex 项目 `.venv` 的 `download_v9_data.py` 刷新 Yahoo Finance/yfinance 已完成日线（下载时间 `2026-07-14T15:43:25Z`）；以下主表以该 completed daily bar 为准。二者对可比标的收盘一致。Tencent 的 VIX `21.67` 为停滞占位，不使用。

| 标的 | 2026-07-13 收盘 | 日变动 | 来源 / 质量 |
| --- | ---: | ---: | --- |
| MRVL | 217.53 | -7.75% | Yahoo Finance completed daily bar + Tencent yesterdayClose；高 |
| AMD | 534.39 | -4.21% | 同上；高 |
| WDC | 555.55 | -4.64% | 同上；高 |
| STX | 860.66 | -5.46% | 同上；高 |
| SPY | 749.17 | -0.77% | 同上；高 |
| QQQ | 711.74 | -1.90% | 同上；高 |
| SMH | 585.62 | -4.16% | 同上；高 |
| SOXX | 553.61 | n/a | Tencent `yesterdayClose` 结构化对象；中高（本轮无日线交叉） |
| VIX | 17.16 | +14.17% | Yahoo Finance completed daily bar；高 |
| VIX3M | 18.57（2026-07-10 最后有效） | n/a | Yahoo Finance；日期错配、低一档质量。V9 诊断以前值前向填充，得到约 0.924 的 VIX/VIX3M，仅作保守辅助。 |
| RSP | 214.23 | -0.03% | Yahoo Finance + Tencent 交叉；高 |
| HYG / LQD | 79.52 / 106.96 | -0.24% / -0.47% | Yahoo Finance + Tencent 交叉；高 |
| IWM | 293.48 | -0.85% | Yahoo Finance + Tencent 交叉；高 |

- 21 日相对代理：`RSP/SPY +0.57%`、`HYG/LQD +1.30%`、`IWM/SPY +0.74%`，均未触发框架的宽度/信用恶化扣分。
- 收盘结构：SPY 仍在 MA50/MA200 上方；QQQ 低于 MA50、但高于 MA150/MA200；SMH 低于 MA20/MA50 且较 63 日高点回撤 `-12.45%`。半导体跌幅显著大于 SPY/QQQ，不能将指数的温和回撤误读为 AI-capex 风险解除。

## 2. 正式 Market Fear Gate

V9 已完成的日线诊断为 **`elevated 6/14`**：VIX 水平 `17.16` 计 1 分；5 日 VIX 变化 `+10.21%` 计 0；期限结构近似 `0.924` 计 0（日期错配）；SPY 63 日回撤 `-1.12%` 计 0，QQQ `-4.51%` 计 1，SMH `-12.45%` 计 3；QQQ 低于 MA50 计 1；三项宽度/信用代理均为 0。

| 项目 | 数值 |
| --- | ---: |
| 风险乘数 | 70% |
| 最大总股票敞口 | 75% |
| 现金底线 | 25% |
| 框架最大新买入敞口 | 25% |
| 实际新买入上限 | **0%** |

实际新买入上限为 0%，原因不是旧的 unresolved-stop veto（已于 7 月 12 日由用户确认解除），而是活跃仓均属同一 AI-capex 共同因子、`flow_fragility=elevated`、`theme_overlap_high`、趋势入场为 `trend_broken`，且没有任何持仓满足长期底部确认。不得借事件反弹、盘中跳升或 AMD 的单日价格行为追高。

## 3. Stop-trigger table

GLW/MRVL/MXL 的 7 月 10 日未提交短线 stop-market 建议已被用户的长期重分类取代；下表不把它们写成券商订单。周线风险线必须等本周完整周线收盘确认。

| 标的 | 范围 | 收盘 | 既有风险 / 减仓线 | 是否触发 | near-stop | 下一步状态 |
| --- | --- | ---: | --- | --- | --- | --- |
| GLW | 活跃 2 股 | 183.11 | 加仓需收在 `200-205` 上并守住约 `190`；周线 `<166-167` 重验 | 硬周线未触发；日收盘已失守 190 支撑 | 否（距周线线约 9.8%） | `defensive hold / no add`；停止底部积累，周线失守再重验长期逻辑 |
| MRVL | 活跃 4 股 | 217.53 | 不加仓，除非权重约 12% 以下且收在 `250-260`；周线 `<223` 重验 | 周线尚未完成；周一日收盘暂低于 223 | 是 / 暂时穿线 | `near-weekly-risk review / no add`；若本周周收仍 `<223`，转 `reduce-review`，禁止因反弹追高 |
| MXL | 活跃 6 股 | 89.30 | 不加仓，除非约 6% 权重、业绩确认且收在 `97-100`；周线 `<78` 重验 | 否；但低于 MA20/MA50 | 否（距周线线约 14.5%） | `defensive hold / reduce-review`；高风险卫星仍超常态规模，不摊低 |
| QCOM | 活跃 2 股 | 183.98 | `185` 下方升级观察；completed close `<182` 失败入场复核 | 185 观察线已触发；182 失败线未触发 | 是（距 182 约 1.1%） | `near-stop review / hold-watch only`；若下一完成收盘 `<182`，进入 `reduce-review` |
| AMD | 非活跃观察 / 历史模型 | 534.39 | completed close `<492` | 否 | 否（高约 8.6%） | `repair watch / no buy`；若后续收盘 `<492`，必须 `reduce-review` |
| WDC | 非活跃观察 / 历史模型 | 555.55 | `<500` | 否 | 否（高约 11.1%） | `defensive watch / no buy`；深回撤未修复 |
| STX | 非活跃观察 / 历史模型 | 860.66 | `<835` | 否 | 是（高约 3.1%） | `near-stop review / no add`；不将单日反弹当作买入授权 |

## 4. Institutional overlay scorecard

```text
flow_fragility_score: 8/14 -> elevated（proxy-based；直接期权/CTA/杠杆 ETF 流数据本轮不可得，不以缺失数据伪造确定性）
  市场领导窄化 1/2；半导体/AI 共同因子集中且同步下跌 2/2；
  spot-down + VIX 上行的脆弱性代理 1/2；系统化去风险代理 1/2；
  buyback 转换风险 1/2；hedging 0/2；主题拥挤 2/2。
trend_aligned_entry_score: 1/5 -> trend_broken（活跃 AI-capex sleeve）
  Fear Gate 仅勉强允许受限暴露；四个活跃仓均无 MA/支撑 reclaim、无相对强度确认、无已确认新催化。
AI_quality/capex_cycle:
  GLW diversified_supplier / medium；MRVL cyclical_supplier + bottleneck / high；
  MXL speculative_bottleneck / high；QCOM diversified_supplier / edge inference / medium-high。
factor_macro_flags:
  growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high;
  semiconductor_basket_unwind; long_term_bottom_unconfirmed。
bottleneck_watch:
  optical/interconnect（GLW/MRVL/MXL）与 memory/storage（WDC/STX）均未出现经验证的基本面改善；
  7 月 13 日同步走弱仅加强风险复核，不构成新增仓理由。
action impact:
  禁止新买入/摊低；先看共同因子总暴露与周线风险，再等至少两次 completed-close 的底部确认。
```

已执行组合级相关风险复核：四个活跃 ticker 虽有光互联、组件和 edge-inference 标签，但经济敏感性仍集中于 AI-capex/半导体。股票敞口仅 `36.29%`，低于 elevated 的 75% 上限，不能抵消「单一有效主题」的相关风险；MRVL 已接近 15% 正常单股上限，MXL `9.09%` 仍高于高风险卫星常态 3%-6%。因此不以任何单名的盘中反弹放松约束。

## 5. 真实账户工作估值与模型组合核对

工作估值沿用用户确认的现金基准 `USD 3,756.49`，不假设 7 月 10 日后有新成交。

| 持仓 | 股数 | 收盘 | 市值 | NAV 权重 | 状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 183.11 | 366.22 | 6.21% | defensive long-term hold / no add |
| MXL | 6 | 89.30 | 535.80 | 9.09% | oversized satellite / reduce-review |
| MRVL | 4 | 217.53 | 870.12 | 14.76% | near-weekly-risk review / no add |
| QCOM | 2 | 183.98 | 367.96 | 6.24% | near-stop review / hold-watch |

- 工作 NAV：`USD 5,896.59`；股票市值：`USD 2,140.10 / 36.29%`；现金：`USD 3,756.49 / 63.71%`。
- 活跃持仓数 `4`；名义标签可分两类，但有效大主题 `1`（AI-capex/semiconductor common factor）；最大单股 MRVL `14.76%`。
- 历史 replay 固定股数篮子（非真实账户）按本轮收盘为 `USD 20,511.99`，其中股票 `39.92%`；它不代表真实账户，也没有假定 overlay 成交。

正式 shadow forward 已按 runbook 仅前进已完成的 `2026-07-13`：`v8_base`、`v9_a`、`v9_e`、`passive_50_50` 的期初/当前 NAV 均为 `1.0000`、现金 `100%`、无信息仓盈亏；审计通过、无 tamper alarm。它们仅生成下一交易日的模型 V8 再平衡待执行项（`v8_base/passive_50_50` 各 SPY/QQQ 50%，`v9_a/v9_e` 各 35%），且 `authorizes_trade=false`；不是实盘订单或成交。Rule E 仍只有 `18/50` 可靠 PIT 事件，不能统计晋升。

## 6. Replay 与记忆处理

- `institutional-overlay-replay-protocol.md` 的首个 replay 窗口限于 2026-06-05 事件及随后四个完成交易日；2026-07-13 不属于该窗口，且目标 replay ledger 在当前仓库不存在，故未创建或追加非适用行，更未预填未来日期。
- 已写入本审计、组合快照和待办，并向 daily summary 追加简要记录。
- `decisions.md` 未更新：本轮只有单日收盘、日期错配的 VIX3M 与既有规则的执行，不构成经过验证的稳定新规则。

非投资建议。
