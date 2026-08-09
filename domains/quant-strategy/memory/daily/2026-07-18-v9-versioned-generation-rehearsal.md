# 2026-07-18 V9 版本化候选链演练

## 结论

本轮完成的是运行与验证架构优化，不是参数寻优。V9 的 MA150/MA200、70/30 上限、Fear Gate、止损和 Rule E 阈值均未改变。

新增不可覆盖的 `results/shadow_portfolio/generations/<generation-id>` 布局。每个 generation 拥有独立的 frozen、forward、dry-run 与 validation 证据；已有 generation ID 不得复用。只有在干净工作区生成且 manifest 为 `forward_eligible=true` 的 generation 才能初始化正式账户。

## 数据与演练

- 刷新 46 个标的，完成日线数据截至 `2026-07-17`。
- 创建候选 generation：`v9-opt-20260718-r1`。
- 冻结代码哈希：`51954c7c9cadae9c2254540ab136b8854bace0176004d81c0cc0fd044a93ab34`。
- 隔离演练日期：`2026-07-15`、`2026-07-16`、`2026-07-17`，三日均成功完成。
- 候选是在脏工作区生成，故 `forward_eligible=false`、`formal_initialized=false`，证据等级仅为 `engineering-only`。
- 启动审计没有代码哈希不一致，但正确阻止了正式启动：manifest 不合格且没有四个正式 genesis。

## 三日结果解读

截至 `2026-07-17`：

- V8/full-core 与 passive 账户 NAV 均为 `0.980047308`，约 `-1.995%`。
- V9 A 与 V9 E NAV 均为 `0.986003766`，约 `-1.400%`；现金约 `29.88%`。
- V9 A 与 V9 E 完全一致，Rule E 增量 alpha 为 `0`，无股票持仓、无待执行订单、无观察名单候选。
- V9 相对 full-core 少跌约 0.60 个百分点，来源是固定 30% 现金缓冲，而不是 Rule E 选股贡献。
- Fear Gate 为 `elevated 8`，VIX `18.77`、VIX/VIX3M 约 `1.011`、SMH 63 日回撤约 `-16.80%`、QQQ 位于 MA50 下方；`authorizes_trade=false`。

因此，当前只能确认防守结构在这三日窗口降低了回撤，不能确认半导体或 Rule E 已形成可交易转向，也不能声称信息 alpha。

## 验证

- 完整回归：`48/48` 通过。
- `git diff --check` 无空白错误，仅有现存换行格式提示。
- 版本化路径、generation ID 校验、不可覆盖、安全审计与隔离前向链均纳入测试。

## 下一步

先整理并提交当前策略、监控与验证变更；随后从干净提交创建一个全新的 formal generation，并从冻结后的第一个真实完成交易日开始连续记录。不得把 `2026-07-13` 至 `2026-07-17` 的缺失日期回填为前向证据。Rule E 晋级仍需至少 `50` 条可靠 PIT 事件和持续前向样本；当前为 `18/50`。
