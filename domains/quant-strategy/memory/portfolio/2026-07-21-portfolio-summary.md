# 2026-07-21 收盘组合摘要

审计于 2026-07-23 01:04–01:15 Asia/Shanghai 完成。股票/ETF 价格来自本地 Node quote workflow 的结构化 `Tencent (Primary).yesterdayClose`（运行时为 7/22 美东盘中，故该字段代表 7/21 completed close）。真实账户以用户或券商回报为准；未假设订单或成交。

| 持仓 | 股数 | 2026-07-21 收盘 | 市值 | NAV 权重 | 风险状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 162.41 | 324.82 | 5.62% | defensive hold / completed-week reduce-review / no add |
| MXL | 6 | 86.06 | 516.36 | 8.94% | defensive hold / reduce-review / no add |
| MRVL | 4 | 207.96 | 831.84 | 14.40% | defensive hold / completed-week reduce-review / no add |
| QCOM | 2 | 173.50 | 347.00 | 6.01% | reduce-review；收盘仍低于 182 |

- 工作 NAV：**USD 5,776.51**；现金 USD 3,756.49（**65.03%**）；股票 USD 2,020.02（**34.97%**）。
- 持仓数 4；有效广义主题数 1（AI-capex / semiconductor common factor）。
- 最大单股 MRVL 14.40%，低于常规 15% 上限，但不授权加仓。
- Fear Gate：`normal 3/14`，框架新买入上限 50%；实际新增/摊低仍为 **0%**，因为相关共同因子、`trend_broken`、`theme_overlap_high`、`sleeve_correlation_high` 与未闭环风险复核。
