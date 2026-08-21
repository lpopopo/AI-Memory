# 2026-08-18 组合快照

基于已完成的 2026-08-18 收盘：本地 Node Tencent structured `yesterdayClose`，并由本地 Yahoo Chart completed daily bar 核验。现金和股数仅使用现有用户/券商确认的工作快照；没有新增订单或成交假设。

| 持仓 | 股数 | 收盘价 | 市值 | NAV 权重 | 风控状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 159.90 | 319.80 | 5.61% | reduce-review / defensive hold / no add |
| MXL | 6 | 72.63 | 435.78 | 7.65% | reduce-review / defensive hold / no add |
| MRVL | 4 | 216.00 | 864.00 | 15.17% | completed-week reduce-review / no add |
| QCOM | 2 | 160.19 | 320.38 | 5.62% | long-term hold / no add |

| 组合核对 | 数值 |
| --- | ---: |
| 工作现金 | USD 3,756.49 |
| 股票市值 | USD 1,939.96 |
| 工作 NAV | USD 5,696.45 |
| 现金比例 / 股票敞口 | 65.94% / 34.06% |
| 持仓数 / 有效主题数 | 4 / 1 |
| 最大单股 | MRVL 15.17% |

结论：四项持仓仍暴露于同一 AI-capex/common-factor sleeve，`theme_overlap_high` 与 `sleeve_correlation_high` 持续。MRVL 略超 normal 15% 单名上限，GLW、MXL、MRVL 的既有风险复核均未闭环；因此相关新增及摊低维持 `0%`。本快照不是券商余额或成交回报。
