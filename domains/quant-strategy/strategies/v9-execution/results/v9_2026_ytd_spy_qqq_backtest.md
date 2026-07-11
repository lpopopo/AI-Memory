# V9 2026YTD 回测：组合 vs SPY / QQQ

区间：`2026-01-02` 至 `2026-07-10`。引擎：当前 `v9-execution` + `V9Config` 默认（70% 指数核心 / 30% 个股）。
数据：`datasets/data_v9`。资讯：point-in-time 事件档案（不使用 retrospective backfill）。

| 模型 | 累计收益 | 最大回撤 | 年化Sharpe* | 资讯买入次数 |
| --- | ---: | ---: | ---: | ---: |
| buy_hold_SPY | 11.09% | -8.88% | 1.54 | 0 |
| buy_hold_QQQ | 18.61% | -11.72% | 1.67 | 0 |
| static_SPY_QQQ_50_50_daily | 14.86% | -10.30% | 1.64 | 0 |
| V8_equivalent_full_core | 10.38% | -7.00% | 1.34 | 0 |
| V9_index_core_70pct_cash_30pct | 7.28% | -4.96% | 1.33 | 0 |
| V9_current_70_30_point_in_time | 7.28% | -4.96% | 1.33 | 0 |

*样本不足一年，年化 Sharpe 不稳定。

## 读法

- `buy_hold_SPY` / `buy_hold_QQQ`：纯买入持有基准。
- `V8_equivalent_full_core`：100% 仓位跑 SPY/QQQ MA150/MA200（无个股）。
- `V9_index_core_70pct_cash_30pct`：现行天花板下仅指数核心、个股袖套空置为现金。
- `V9_current_70_30_point_in_time`：最新 V9 全规则；若资讯买入为 0，则收益应接近 core-70% 路径。

产物：`D:/code/AI-Memory/domains/quant-strategy/strategies/v9-execution/results/v9_2026_ytd_spy_qqq_backtest.json`
