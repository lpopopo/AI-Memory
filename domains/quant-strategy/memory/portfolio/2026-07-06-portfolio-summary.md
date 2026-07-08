# 2026-07-06 组合摘要

审计对象：2026-07-06 美股常规交易收盘。运行时间：2026-07-07 08:02 Asia/Shanghai。数据来自本地 Node quote workflow 的 Tencent 结构化对象、Yahoo completed daily bars 和 Cboe/Yahoo 波动率核验。真实账户以用户/券商回报为准。

## 真实账户工作估算

假设：2026-07-03 工作现金 `USD 2,875.69`；用户确认 MU `1 @ USD 1,010.00` 已卖出，估算卖出费 `USD 1.00`，因此现金增加约 `USD 1,009.00`；GLW、DRAM、MXL、MRVL 未收到后续成交回报；XLI 状态未知且未计入。

| 持仓 | 股数 | 收盘 | 市值 | NAV 权重 | 分类 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 194.80 | 389.60 | 6.38% | `triggered exit/reduce`; below 227 |
| DRAM | 4 | 64.76 | 259.04 | 4.24% | `triggered exit`; below 70.50 |
| MXL | 6 | 95.68 | 574.08 | 9.40% | `triggered reduce/exit`; below 113.38 |
| MRVL | 4 | 249.27 | 997.08 | 16.33% | `triggered exit/reduce-review`; below 260 |

- 估算股票市值：`USD 2,219.80`。
- 估算现金：`USD 3,884.69 / 63.63%`。
- 估算 NAV：`USD 6,104.49`。
- 股票敞口：`USD 2,219.80 / 36.37%`。
- 持仓数量：`4`。
- 名义主题数量：`2`；有效大主题数量：`1`，AI capex。
- 最大单股：MRVL `16.33%`。

已关闭：MU `1` 已由用户确认在 2026-07-06 以 `USD 1,010.00` 卖出，估算净现金增加 `USD 1,009.00`。该成交降低了单名和记忆/半导体风险，但没有解除其余 completed-close stops。

## 退休历史模型 / replay 口径

该口径只用于 institutional overlay replay，不代表真实账户。固定股数 MRVL `8.0383`、AMD `4.6083`、WDC `3.6880`、STX `2.2401`，现金占位 `USD 12,323.96`。

| 标的 | 股数 | 收盘 | 市值 | 状态 |
| --- | ---: | ---: | ---: | --- |
| MRVL | 8.0383 | 249.27 | 2,003.71 | below 260; reduce-review / model exit trigger |
| AMD | 4.6083 | 552.05 | 2,544.01 | above 492; repair watch |
| WDC | 3.6880 | 577.46 | 2,129.67 | above 500; defensive watch |
| STX | 2.2401 | 868.26 | 1,944.99 | near 835; defensive near-stop review |

- 历史模型股票市值：`USD 8,622.38`。
- 历史模型 NAV：`USD 20,946.34`。
- 历史模型现金比例：`58.84%`。
- 历史模型股票敞口：`41.16%`。
- 历史模型最大单股：AMD `12.15%`。

## 风险状态

Market Fear Gate 为 `normal 2/14`，但真实账户实际新买入上限为 `0%`，因为 GLW、DRAM、MXL、MRVL 均仍处于未解决 completed-close 风险状态，且活跃股票敞口全部属于同一 AI-capex 篮子。

精确现金、费用、FX、税费、结算、XLI 状态和剩余止损成交必须以用户/券商回报为准。
