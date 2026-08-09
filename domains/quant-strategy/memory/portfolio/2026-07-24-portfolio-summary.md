# 2026-07-24 收盘组合摘要

审计于 2026-07-25 11:35 Asia/Shanghai 完成。股票收盘取本地 Node quote workflow 的结构化 `Tencent (Primary).price`；因 7/24 已完成，`price` 是正式收盘字段。真实账户仍以用户或券商回报为准，未假设订单或成交。

| 持仓 | 股数 | 2026-07-24 收盘 | 市值 | NAV 权重 | 风险状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 146.65 | 293.30 | 5.25% | defensive hold / completed-week reduce-review / no add |
| MXL | 6 | 71.59 | 429.54 | 7.68% | reduce-review / defensive hold / no add（`<78`） |
| MRVL | 4 | 194.23 | 776.92 | 13.90% | defensive hold / completed-week reduce-review / no add |
| QCOM | 2 | 166.97 | 333.94 | 5.97% | reduce-review（completed close `<182`） |

- 工作 NAV：**USD 5,590.19**；现金 USD 3,756.49（**67.20%**）；股票 USD 1,833.70（**32.80%**）。
- 持仓数 4；有效广义主题数 1（AI-capex / semiconductor common factor）；最大单股 MRVL 13.90%。
- Fear Gate 为 `elevated 5/14`：框架新买上限 25%，但账户实际新增/摊低为 **0%**，因为 `trend_broken`、`theme_overlap_high`、`sleeve_correlation_high` 与未闭环风险复核。
