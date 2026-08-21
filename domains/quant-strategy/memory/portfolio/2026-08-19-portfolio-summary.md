# 2026-08-19 组合快照

基于已完成的 2026-08-19 收盘：本地 Node Tencent structured `yesterdayClose`，并由本地 Yahoo Chart completed daily bar 核验。现金和股数只使用既有用户/券商确认的工作快照；没有新增订单或成交假设。

| 持仓 | 股数 | 收盘价 | 市值 | NAV 权重 | 风控状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 152.46 | 304.92 | 5.32% | reduce-review / defensive hold / no add |
| MXL | 6 | 66.43 | 398.58 | 6.95% | reduce-review / defensive hold / no add |
| MRVL | 4 | 237.27 | 949.08 | 16.56% | profit-protection / defensive hold / no add |
| QCOM | 2 | 161.91 | 323.82 | 5.65% | long-term hold / no add |

| 组合核对 | 数值 |
| --- | ---: |
| 工作现金 | USD 3,756.49 |
| 股票市值 | USD 1,976.40 |
| 工作 NAV | USD 5,732.89 |
| 现金比例 / 股票敞口 | 65.53% / 34.47% |
| 持仓数 / 有效主题数 | 4 / 1 |
| 最大单股 | MRVL 16.56% |

结论：四项持仓持续暴露于同一 AI-capex/common-factor sleeve，`theme_overlap_high` 与 `sleeve_correlation_high` 持续；MRVL 超过 normal 单名上限，GLW/MXL 风险线已触发，MRVL 的完成周复核尚未闭环。因此相关新增及摊低维持 `0%`。本快照不是券商余额或成交回报。
