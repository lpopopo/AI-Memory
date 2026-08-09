# 2026-07-23 收盘组合摘要

审计于 2026-07-24 19:56 Asia/Shanghai 完成。股票/ETF 收盘为本地 Node quote workflow 的结构化 `Tencent (Primary).yesterdayClose`；运行时 7/24 美股盘中，该字段代表 7/23 completed close。真实账户以用户或券商回报为准，未假设订单或成交。

| 持仓 | 股数 | 2026-07-23 收盘 | 市值 | NAV 权重 | 风险状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 154.06 | 308.12 | 5.33% | defensive hold / completed-week reduce-review / no add |
| MXL | 6 | 86.80 | 520.80 | 9.01% | defensive hold / reduce-review / no add |
| MRVL | 4 | 210.99 | 843.96 | 14.60% | defensive hold / completed-week reduce-review / no add |
| QCOM | 2 | 175.63 | 351.26 | 6.08% | reduce-review；收盘仍低于 182 |

- 工作 NAV：**USD 5,780.63**；现金 USD 3,756.49（**64.98%**）；股票 USD 2,024.14（**35.02%**）。
- 持仓数 4；有效广义主题数 1（AI-capex / semiconductor common factor）。
- 最大单股 MRVL 14.60%，低于正常 15% 上限，但现有共因子与风险复核禁止加仓。
- Fear Gate 为 `normal 3/14`，框架新买入上限 50%；账户实际新增/摊低仍为 **0%**，因为 `trend_broken`、`theme_overlap_high`、`sleeve_correlation_high` 与未闭环风险复核。
