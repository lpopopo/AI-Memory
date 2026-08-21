# 2026-08-13 组合快照

基于已完成的 2026-08-13 收盘：本地 Node Tencent structured quotes 的 `yesterdayClose` 与本地 Yahoo Chart completed daily bar 一致。现金和股数仅使用现有用户/券商确认的工作快照；没有新增订单或成交假设。

| 持仓 | 股数 | 收盘价 | 市值 | NAV 权重 | 风控状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 158.54 | 317.08 | 5.51% | completed-week defensive review / no add |
| MXL | 6 | 76.65 | 459.90 | 8.00% | completed-close reduce-review / no add |
| MRVL | 4 | 222.18 | 888.72 | 15.45% | completed-week defensive reduce-review / no add |
| QCOM | 2 | 164.79 | 329.58 | 5.73% | long-term hold / no add |

| 组合核对 | 数值 |
| --- | ---: |
| 工作现金 | USD 3,756.49 |
| 股票市值 | USD 1,995.28 |
| 工作 NAV | USD 5,751.77 |
| 现金比例 / 股票敞口 | 65.31% / 34.69% |
| 持仓数 / 有效主题数 | 4 / 1 |
| 最大单股 | MRVL 15.45% |

结论：四个标的均暴露于同一 AI-capex/common-factor sleeve，`theme_overlap_high` 与 `sleeve_correlation_high` 持续。MRVL 略高于 normal 15% 单名上限；SMH 仍低于 MA50，且 MXL/MRVL 的风险复核未闭环。因此相关新增及摊低为 `0%`。本快照不是券商余额或成交回报。
