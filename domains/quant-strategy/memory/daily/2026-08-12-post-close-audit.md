# 2026-08-12 美股盘后正式审计

审计完成于 `2026-08-13 20:06 Asia/Shanghai`。本记录只使用 2026-08-12 已完成的美股常规交易收盘；未登录券商、未提交订单、未虚构成交。真实账户的仓位、订单与成交均以用户或券商回报为准。

## 收盘数据、来源与质量

首先按 `tools/README.md` 运行 Node Quote Workflow Smoke Test（`MRVL/AMD/SPY/QQQ/SMH`），随后扩展至持仓、指数、波动率和广度/信用代理。两次调用均返回非空的 `Tencent (Primary)` 结构化 quote objects，故本地报价工作流可用；其内部链路仍为 Tencent -> Yahoo Chart -> Sina，且 Node 具有 `node:https -> PowerShell WebClient -> fetch` 传输兜底。随后以同一客户端的 Yahoo Chart 6 个月日线交叉核验权益/ETF 的 8/12 completed bar。Tencent 的 VIX `21.67` 为陈旧值且 VIX3M 未返回，均未采用；改以 Cboe 官方 daily-price CSV 的同步收盘值。

| 标的 | 8/12 收盘 | 日变动 | 来源 / 数据质量 |
| --- | ---: | ---: | --- |
| MRVL / AMD | 217.08 / 482.93 | +2.25% / +1.82% | Tencent Primary `price` + 本地 Yahoo Chart completed bar / 中高 |
| WDC / STX | 454.10 / 878.21 | +3.69% / +7.03% | 同上 / 中高 |
| SPY / QQQ | 772.49 / 723.70 | +0.25% / +0.73% | 同上 / 中高 |
| SMH / SOXX | 584.83 / 546.61 | +2.08% / +2.32% | 同上 / 中高 |
| VIX / VIX3M | 14.55 / 18.53 | -4.78% / -2.01% | Cboe official daily-price CSV / 高 |
| RSP / SPY | 221.08 / 772.49 | +0.18% / +0.25% | Tencent Primary + Yahoo Chart / 中高 |
| HYG / LQD | 79.61 / 106.12 | +0.13% / +0.12% | 同上 / 中高 |
| IWM / SPY | 302.71 / 772.49 | +0.57% / +0.25% | 同上 / 中高 |

技术与代理复核：SPY 位于 MA20/MA50 `753.19/748.12` 上方，距 63 日高点 `-0.10%`；QQQ 位于 `701.03/713.49` 上方，距高点 `-3.01%`。SMH 位于 MA20 `561.53` 上方，但仍低于 MA50 `593.35`、距 63 日高点 `-12.57%`，其 21 日相对 QQQ 变化为 `-3.12%`。VIX 五日变化 `-3.96%`，VIX/VIX3M 为 `0.785`，期限结构正常。21 日 RSP/SPY、HYG/LQD、IWM/SPY 相对变化分别为 `+0.80%/+0.94%/+0.04%`，未触发宽度或信用恶化阈值。

当天没有独立的 8/12 策略建议、执行清单或盘中复盘文件；最近的真实账户执行资料仍是 7/10 的历史计划和已确认 DRAM 卖出，不能替代新的订单或成交事实。

## 市场恐慌门控

正式判定：**normal 4/14**。VIX 低于 16、期限结构正常、SPY/QQQ 趋势完整且广度/信用代理健康；SMH 的深度回撤、低于 MA50 与相对 QQQ 走弱保留扣分。

- 风险乘数：**100%**
- 现金底线：**5%**
- 框架新买入上限：**50%**（最大股票敞口 95%）
- 实际 AI-capex 相关新增/摊低上限：**0%**。四项真实持仓仍是一条共同因子 sleeve，SMH 未重回 MA50，且 GLW/MXL/MRVL 风险复核未闭环；`normal` 不是相关加仓授权。

## Stop-trigger table

| 标的 | 8/12 收盘 | 既有风险线 / 条件 | 触发或 near-stop | 下一步状态 |
| --- | ---: | --- | --- | --- |
| GLW（真实 2 股） | 167.44 | completed-week `<166-167` 复核带 | 周内反弹至带上方；尚非完成周收盘，不能宣布解除 | defensive hold / completed-week review / no add |
| MXL（真实 6 股） | 74.33 | completed-close `<78` | 已触发，低于线 4.71% | reduce-review / defensive hold / no add |
| MRVL（真实 4 股） | 217.08 | completed-week `<223`；利润保护与长期底部复核 | 仍低于复核带 2.65% | defensive hold / completed-week reduce-review / no add；禁止因事件反弹自动追高 |
| QCOM（真实 2 股） | 163.07 | 7/27 长期覆盖；未来加仓须收复约 182、两次收盘不创新低和 sleeve 容量 | 覆盖有效，新增条件未满足 | long-term hold / no add / post-earnings review |
| AMD（replay/watch，非真实持仓） | 482.93 | completed-close `<492` | **已触发，低于线 1.84%** | **reduce-review / no buy** |
| WDC（replay/watch，非真实持仓） | 454.10 | `<500` | **已触发，低于线 9.18%** | **reduce-review / no buy** |
| STX（replay/watch，非真实持仓） | 878.21 | `<835` | 当日重回线以上 5.17%，但仍低于 MA50 且存储链未修复 | defensive hold / near-stop review / no buy |

AMD、WDC、STX 仅用于 replay/watch，本表不推断真实账户持仓、订单或成交。

## Institutional overlay scorecard 与组合级复核

- `flow_fragility_score: 5/14 -> medium (proxy-based)`：宽度与信用代理改善，VIX 回落；但 SMH/SOXX 仍低于 MA50、21 日相对 QQQ 走弱、存储链仍处深回撤，期权、单股隐含相关、杠杆 ETF 流量与 CTA 数据不可得，未强行记为零。
- `trend_aligned_entry_score: 1/5 -> trend_broken`：Fear Gate 允许敞口得 1 分，但 SMH 尚未重回 MA50、相对强度仍弱，未取得可验证的确认催化或有序回撤后的趋势重建。
- `AI_quality/capex_cycle`：GLW 为 diversified supplier / medium；QCOM 为 diversified supplier + edge inference / medium-high；MRVL、AMD、WDC、STX 为 cyclical supplier / high；MXL 为 speculative bottleneck / high。单日反弹不改变分类。
- `factor_macro_flags`：`growth_duration_high; theme_overlap_high; sleeve_correlation_high; AI_capex_cycle_high; semiconductor_trend_broken; unresolved_MXL_risk_review; storage_drawdown`。
- `bottleneck_watch`：光互连、定制芯片与存储仍共享 AI-capex 周期；STX 的单日修复尚不足以证明存储链修复，WDC 仍在风险线下。
- `action impact`：`theme_overlap_high` 与 `sleeve_correlation_high` 已触发组合级相关风险复核，即使 flow fragility 仅为 medium。GLW/MXL/MRVL/QCOM 仍按一条有效 sleeve 管理；SMH 重回 MA50、相对强度修复且风险复核闭环前，相关新增/摊低维持 **0%**。

## 模型组合净值核对

采用已确认工作现金 USD `3,756.49` 与真实持仓 GLW `2`、MXL `6`、MRVL `4`、QCOM `2` 标记；未假设新委托、成交、费用或 FX 变动。

| 项目 | 数值 |
| --- | ---: |
| 股票市值 | USD 1,975.32 |
| 工作 NAV | USD 5,731.81 |
| 现金 / 股票敞口 | USD 3,756.49 / 65.54%；USD 1,975.32 / 34.46% |
| 持仓数量 / 有效主题数量 | 4 / 1（AI-capex / semiconductor common factor） |
| 最大单股 | MRVL USD 868.32 / 15.15% |

现金高于 normal 的 5% 底线。MRVL 略高于 normal 15% 单名上限，故本轮维持不加仓与完成周复核；不由此推断真实卖单。冻结 institutional-replay baseline（MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`、现金 USD `12,323.96`）按本收盘标记为 **USD 19,936.40**；overlay NAV 和差额留空，因为没有可验证的 overlay 执行假设。

## Replay、记忆边界与后续

已向 `strategies/research-archive/2026-06-08-institutional-overlay-replay/replay-ledger-template.csv` 追加一条已完成的 2026-08-12 收盘行，未预填未来日期。单日价格、replay 或警报不足以升级为稳定规则，故不更新 `memory/decisions.md`。
