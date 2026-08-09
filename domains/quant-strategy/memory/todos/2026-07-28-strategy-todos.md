# 2026-07-28 策略待办

- [ ] 在 2026-07-28 美股常规交易收盘后补做正式审计；不得把本次 12:03 EDT Tencent `price` 写为收盘。
- [ ] 用本地 Node workflow 的可追溯 completed-close 字段复核 MRVL、AMD、WDC、STX、SPY、QQQ、SMH/SOXX、RSP、HYG/LQD、IWM/SPY；单独补齐可靠的 VIX/VIX3M 收盘数据。
- [ ] 优先核对 AMD `<492`、WDC `<500`、STX `<835` 是否在 completed close 触发；同时复核 GLW、MXL、MRVL 的既有 completed-week 风险线与 QCOM 长期持有/财报前不加仓条件。
- [ ] 仅在完成上述收盘核对后更新组合净值、正式 Fear Gate、overlay scorecard 和 replay ledger；不得假设经纪商订单或成交。
