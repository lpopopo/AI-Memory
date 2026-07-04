# 2026-07-01 Trade Plan

Run time: 2026-07-01 00:17 Asia/Shanghai. U.S. regular session intraday.

| Priority | Ticker | Action | Quantity | Price / trigger | Protection | State |
| ---: | --- | --- | ---: | --- | --- | --- |
| 0 | TTMI | Sell | 3 | Execute because completed close breached 188 | Do not average down | `mandatory exit` |
| 1 | XLI | Conditional limit buy after TTMI sale | 2 | Limit 183.00; no chase above 186.10 | Completed close below 178 -> exit review | `conditional` |
| 2 | GLW | Hold | 2 | No add at 257+ | Completed-close protection >=227 | `hold` |
| 3 | MXL | Hold | 6 | No add at 119+ | Completed-close protection >=104.30 | `hold` |
| 4 | DRAM | Hold | 4 | No add | Hard protection 70.50 | `hold` |
| 5 | MU | Hold | 1 | No add | Hard protection 1090; close-risk line 1100 | `hold` |

Sequence is mandatory: the XLI order is invalid until TTMI is sold. No brokerage action was performed by automation.
