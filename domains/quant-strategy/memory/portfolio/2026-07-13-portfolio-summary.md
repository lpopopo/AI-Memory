# 2026-07-13 收盘组合摘要

运行时间：2026-07-14 23:41--23:45 Asia/Shanghai。使用 Yahoo Finance completed daily bars，并由本地 Node `Tencent (Primary)` quote workflow 的 `yesterdayClose` 对可比标的交叉；未登录券商，真实账户以用户/券商回报为准。

前提：用户已确认实际持仓为 GLW `2`、MXL `6`、MRVL `4`、QCOM `2`，DRAM 已卖出、无挂单；现金沿用已记录基准 `USD 3,756.49`。

| 持仓 | 股数 | 2026-07-13 收盘 | 市值 | NAV 权重 | 风险状态 |
| --- | ---: | ---: | ---: | ---: | --- |
| GLW | 2 | 183.11 | 366.22 | 6.21% | 失守约 190 支撑；defensive hold / no add |
| MXL | 6 | 89.30 | 535.80 | 9.09% | 高于卫星常态；defensive hold / reduce-review |
| MRVL | 4 | 217.53 | 870.12 | 14.76% | 暂低于 223 周线复核线；near-weekly-risk review |
| QCOM | 2 | 183.98 | 367.96 | 6.24% | 185 观察已触发、182 完成收盘失败线未触发 |

- 工作 NAV：`USD 5,896.59`
- 现金：`USD 3,756.49 / 63.71%`
- 股票敞口：`USD 2,140.10 / 36.29%`
- 活跃持仓：`4`；有效大主题：`1`（AI-capex / semiconductor common factor）
- 最大单股：MRVL `14.76%`；MXL `9.09%` 仍超过高风险卫星常态 `3%-6%`
- 正式 Fear Gate：`elevated 6/14`；框架新买入上限 `25%`，实际新买入上限 `0%`（趋势破坏与共同因子集中）

结论：现金与总股票敞口均符合 elevated 门控，但组合没有低相关第二主题，且四个持仓没有底部确认；不新增仓、不摊低，先复核 MRVL 周线和 QCOM 的 182 completed-close 失败线。
