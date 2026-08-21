# 2026-08-12 组合快照

基于已完成的 2026-08-12 收盘：本地 Node Tencent structured quotes 的 `price` 与本地 Yahoo Chart completed daily bar 一致。现金和股数仅采用现有用户/券商确认的工作快照；没有新增订单或成交假设。

| 持仓 | 股数 | 收盘价 | 市值 | NAV 权重 | 风控状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 167.44 | 334.88 | 5.84% | completed-week defensive review / no add |
| MXL | 6 | 74.33 | 445.98 | 7.78% | completed-close reduce-review / no add |
| MRVL | 4 | 217.08 | 868.32 | 15.15% | completed-week defensive reduce-review / no add |
| QCOM | 2 | 163.07 | 326.14 | 5.69% | long-term hold / no add |

| 组合核对 | 数值 |
| --- | ---: |
| 工作现金 | USD 3,756.49 |
| 股票市值 | USD 1,975.32 |
| 工作 NAV | USD 5,731.81 |
| 现金比例 / 股票敞口 | 65.54% / 34.46% |
| 持仓数 / 有效主题数 | 4 / 1 |
| 最大单股 | MRVL 15.15% |

结论：4 个标的均暴露于同一 AI-capex/common-factor sleeve；`theme_overlap_high` 与 `sleeve_correlation_high` 持续。MRVL 略高于 normal 15% 单名上限，SMH 仍低于 MA50，MXL/MRVL 风险复核也未闭环，因此相关新增和摊低为 0%。本快照不是券商余额或成交回报。
