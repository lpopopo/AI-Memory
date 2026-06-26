# 2026-06-24 实时公开来源与机构研究监控

运行时间：2026-06-24 20:31-20:45 Asia/Shanghai。

严格监控窗口：`2026-06-23T12:31:57.485Z` 至本次运行结束。窗口来源为自动化提供的上次成功运行时间（北京时间 `2026-06-23 20:31:57`），未使用 24 小时回退假设。

范围：只读核验公开信息、证据分级、策略映射和记忆同步。未登录券商、未提交订单、未记录或推断未确认真实成交；本文不构成买卖建议。

## 1. 执行摘要

- 严格窗口内新增可核验公开内容为 1 项：小红书账号“美研芒格君 / Kay2289123”的 CRDO / 铜光互联笔记。
- 笔记正文、作者、ID、相对编辑时间、作者评论和 24 张轮播图均通过已登录 Chrome 可见页面核验；图片读取为 `24/24`，未读缺口为 `0`。
- X 的 `@Kay2289123`、`@nvidia`、`@elonmusk`、`@realDonaldTrump` 页面在 Chrome 持续停留在加载或隐私扩展错误状态。降级检查器对后三个账号也只返回零长度 profile，未形成任何窗口后 verified status。`@Kay2289123` 不在本地检查器覆盖范围内，因此不能用脚本补证。
- AQR、Citadel Securities、GMO、Man Institute 的官方域名列表/详情检查与日期过滤完成，四源严格窗口后新增均为 `0`。Citadel 的部分分类页仍存在 `date_unverified` 或 `detail_blocked_no_date`，但其可读详情页和列表渠道正常，不能标为来源整体不可用。
- 本次不新增机构研究框架，不更新 `decisions.md`。CRDO 内容只补充 H5 的待验证路径与 replay 设计。

## 2. 已核验公开来源项

| 平台/来源 | 账号/机构 | ID | 页面可见时间 | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 | 美研芒格君 / `Kay2289123` | `6a3b5e5c0000000015027e00` | 页面于约 2026-06-24 20:37 北京时间显示“编辑于 8 小时前 美国”；只有相对时间 | https://www.xiaohongshu.com/explore/6a3b5e5c0000000015027e00 | 非置顶笔记；24 图轮播 | 正文把 AI 数据中心互联分为标准/平台、互联芯片、物理器件和 hyperscaler/neocloud 资本开支层；CRDO 被描述为以 SerDes、AEC/retimer 做短距 scale-out 互联，并通过光 DSP、硅光 PIC、ZeroFlap 模块扩展到光互联。作者评论区主要补充群组运营与合规说明，没有新的可量化行业事实。 | 核心判断是未来 2-3 年铜 AEC 不会被光完全替代，铜短距与光长距会共存；CRDO 当前现金流主要来自 AEC，光业务是高增长但尚未充分量产的远期期权；真正风险不是“铜或光二选一”，而是光业务量产、客户采用、毛利和交付节奏能否兑现。 | 将 CRDO 的研究拆成 `current_AEC_cashflow` 与 `optical_optionality` 两条证据链；在 AI bottleneck watch 中区分 scale-up / scale-out / scale-across；把光 DSP、PIC、外部激光器数量、ZeroFlap、客户决定权与 hyperscaler capex 作为后续验证字段。该内容不能覆盖 2026-06-23 市场恐慌门槛恶化、趋势破坏和主题拥挤结论。 | 页面存在/作者/标题/正文/评论/24 图为高；相对发布时间为中；图片中的公司数据、电话会转述和行业预测为中低，需一手资料复核 | CRDO 10-K/10-Q 中员工、收入、客户集中度、AEC 占比；FY27 光收入指引；DustPhotonics/Hyperlume/CoMira 并购金额与产品路线；光 DSP/PIC/ZeroFlap 收入与毛利；AEC 速率/距离数据；CPO 占比；hyperscaler 采用与订单；价格趋势、估值、流动性和主题拥挤 |

### 24 图视觉核验摘要

- 已读图片：`24`
- 总图片：`24`
- 未读缺口：`0`
- 图片层证据：高（浏览器页面暴露 24 个原始轮播资产并逐张视觉读取）
- 内容层证据：作者研究摘要，不等同于公司公告或审计数据

主要图片内容：

1. CRDO 被定位为完整连接方案商，核心底座是 SerDes。
2. AEC/retimer 用于短距 scale-out，作者强调 5-7 米、可靠性和 link-flap 管理。
3. scale-across 偏长距光；scale-up 当前几乎无 CRDO 收入；scale-out 是主要战场。
4. CPO 被描述为较远期，而不是立即替代 AEC。
5. 光业务拆为光 DSP、硅光 PIC、ZeroFlap 模块；作者把收购与光模块量产视为 FY27 增长的主要不确定性。
6. 作者明确承认客户集中、光业务尚未大规模量产、远期预期已被市场提前计价等风险。

## 3. X 账号核验

| 账号 | Chrome 可见状态 | 降级检查器 | 窗口后 verified item | 证据结论 |
| --- | --- | --- | ---: | --- |
| `@Kay2289123` | profile 持续 Loading / 无可读 timeline | 本地检查器不覆盖该账号 | 0 | 低；不得从小红书图片中的 X 截图推断 status ID、时间或正文 |
| `@nvidia` | profile 持续 Loading | Jina profile `200` 但长度 `0` | 0 | 低 |
| `@elonmusk` | 页面显示 privacy-related extension 错误或 Loading | Jina profile `200` 但长度 `0` | 0 | 低 |
| `@realDonaldTrump` | profile 持续 Loading | Jina profile `200` 但长度 `0` | 0 | 低 |

没有复用历史 status ID，也没有把无法核验的 profile 当作“没有发帖”的事实。结论仅是本次未取得可采信的新 status。

## 4. 机构研究源核验

本地检查器命令：

```powershell
node D:\code\AI-Memory\domains\quant-strategy\tools\institutional-research-checker.js --since 2026-06-23T12:31:57.485Z --max-items 8 --out D:\code\AI-Memory\domains\quant-strategy\work\institutional-research-latest.md
```

已读取：

- `work/institutional-research-latest.md`
- `work/institutional-research-latest.json`

注意：JSON 文件存在历史编码/转义瑕疵，PowerShell `ConvertFrom-Json` 不能完整解析；本次以同一次运行生成的 Markdown、文件时间和原始 JSON 文本交叉核对，不把解析失败误判为来源不可用。

| 来源 | 列表页 | 详情页 | 严格窗口后新增 | 结论 |
| --- | --- | --- | ---: | --- |
| AQR Research | Reader 可读 | 8 个详情候选可读并日期过滤 | 0 | 最新检查项均为窗口前/既有内容；不新增 `trend_aligned_entry` 框架 |
| Citadel Securities | Reader 列表可读 | 多个官方详情页可读；另有分类页 `date_unverified` 和 `detail_blocked_no_date` | 0 | 不能写“来源不可用”；窗口后没有稳定标题、日期和正文的新详情项 |
| GMO Research Library | Reader 列表可读 | 8 个详情候选可读并日期过滤 | 0 | 最新稳定项为窗口前/既有内容；不新增 AI quality/valuation 框架 |
| Man Institute Market Views | Reader 列表可读 | 8 个详情候选可读并日期过滤 | 0 | `The Strait of Uncertainty` 日期为 2026-06-23，但早于严格 cutoff；不作为本次新增 |

## 5. 公开事实、作者观点、我的推断

### 公开事实

- 小红书主页在本次读取时显示上述 CRDO 笔记为最新非置顶内容。
- 单篇页面可见标题、作者、笔记 ID、正文、相对编辑时间、评论和 `1/24` 轮播标识。
- 24 个原始轮播图均已读取。
- 机构检查器对四源的严格窗口后 verified count 均为 0。

### 作者观点或二手整理

- 铜 AEC 在未来 2-3 年仍有稳定地盘，光不会立即全面替代铜。
- CRDO 可由 AEC 现金流向光 DSP/PIC/模块扩展。
- FY27 光业务可能成为主要增长引擎。
- CPO 在未来三年占比可能仍较低。

这些属于作者对公司披露、投行会议和行业资料的整理，未在本次逐项回到公司一手资料核验。

### 我的策略推断

- 对 CRDO 不能使用单一“铜将被光替代”或“光增长即 CRDO 必胜”的叙事，应拆为当前收入质量、客户集中、铜产品生命周期、光产品量产、毛利和估值六个独立问题。
- `current_AEC_cashflow` 与 `optical_optionality` 可成为 H5 的候选排序字段，但只有公司一手数据和价格确认同时满足时，才可能进入量化候选排名。
- 2026-06-23 AI/半导体主题急跌后，新增内容首先提高的是研究优先级，不是仓位优先级。

## 6. 策略映射

| 维度 | 本次映射 |
| --- | --- |
| `market fear gate` | 不改变 2026-06-23 post-close 的 `elevated 5/14`。单篇行业笔记不能降低现金底线或解除风险门槛。 |
| `trend_aligned_entry` | CRDO 仅加入验证队列；必须等待日线趋势、相对 QQQ/SMH/互联同业的 RS、支持/收复和成交量确认。 |
| `flow_fragility` | 光互联/AEC/AI 网络仍是拥挤主题。作者提到暴涨暴跌和远期故事被提前计价，支持继续维持高拥挤警报。 |
| `AI_quality/capex_cycle` | CRDO 暂维持 `speculative_bottleneck / interconnect_transmission`；AEC 有收入基础，但客户集中、远期光量产和 capex 依赖阻止其仅凭叙事升级为核心。 |
| `factor_macro_exposure` | 增加 `theme_overlap_high`、`growth_duration_high` 和 `AI_capex_cashflow_pressure` 的研究注释；不新增稳定 flag。 |
| `AI bottleneck watch` | 新增三层字段：`scale_up`、`scale_out`、`scale_across`；重点跟踪 AEC/retimer、光 DSP、硅光 PIC、外部激光器、CPO 和 link reliability。 |
| `theme crowding` | 内容热度与最新主页曝光说明 CRDO/MRVL/光互联叙事仍活跃；只作为拥挤温度，不作为价格反转证据。 |
| `portfolio concentration` | 当前实盘已有 MRVL/GLW/TTMI 的 AI 基建重叠暴露；CRDO 不得因同主题研究更新而绕过集中度约束。 |
| `replay/backtest plan` | 在 H5 replay 中增加：AEC 当前收入占比、光业务收入占比、客户集中度、capex 增速、CRDO/QQQ/SMH 相对强弱、主题回撤后 5/20/60 日表现，以及“纯铜现金流”与“光期权”分层标签。 |

## 7. 记忆更新

- 创建本文件。
- 更新 `references/realtime-public-source-tracker.md`，加入 2026-06-24 浏览器与降级检查结论。
- 更新 `memory/hypotheses.md` 的 H5，加入 CRDO 双路径与验证字段。
- 向 `memory/daily-summaries.md` 追加 2026-06-24 摘要。
- `memory/decisions.md` 未更新：单篇社媒内容和单日机构“无新增”不能升级为稳定规则。
- `references/institutional-market-research-framework.md` 未更新：没有窗口后 official-domain detail page 新框架。

## 8. 数据缺口与后续重点

数据缺口：

- X 四个账号未取得可读最新 timeline/status；`@Kay2289123` 也没有脚本补证。
- 小红书只显示相对编辑时间，缺少稳定绝对发布时间。
- CRDO 图片中的多数公司数字和电话会引文尚未回到 10-K、10-Q、财报电话会或官方产品资料逐项核验。
- 机构 JSON 存在编码/转义问题，虽不影响 Markdown 结论，但应修复 checker 的 JSON 合法性。

需要用户确认的来源访问问题：

- Chrome 的 X 页面提示隐私相关扩展可能影响加载。若用户希望恢复 X 高证据核验，需要在用户侧确认是否允许调整/暂时停用导致冲突的隐私扩展；本次未自行修改扩展。

后续开盘准备重点读取：

- `memory/daily/2026-06-23-post-close-audit.md`
- `memory/daily/2026-06-24-realtime-public-institutional-monitor.md`
- `memory/portfolio/2026-06-23-portfolio-summary.md`
- `memory/todos/2026-06-23-strategy-todos.md`
- `work/realtime-public-source-latest.md`
- `work/institutional-research-latest.md`

## 9. 2026-06-24 22:49 X 浏览器复核修正

用户要求重新检查 X 后，已登录 Chrome 的 X 页面恢复正常。以下浏览器可见结果替代本文件第 3 节中“X 未取得可读内容”的初次结论。所有操作保持只读；未查看 cookies、密码、本地存储、私信、通知内容或账号设置，未关注、点赞、评论、转发或发帖。

严格窗口仍为 `2026-06-23T12:31:57.485Z` 之后。

### 9.1 `@Kay2289123`

| Status / Article ID | 北京时间 | 链接 | 类型 | 可见事实摘要 | 作者观点与策略映射 | 证据 |
| --- | --- | --- | --- | --- | --- | --- |
| `2069511714509635621` | 2026-06-24 04:03:37 | https://x.com/Kay2289123/status/2069511714509635621 | 原创帖，引用既有 MRVL 长文 | 作者把 NVIDIA 后续多机架 scale-up 路线与 MRVL 的定制 ASIC、硅光、光 DSP、CPO、交换芯片及 Celestial AI 资产相联系；同时把 ALAB 定位为机架内关键连接组件商，把 CRDO 定位为 hyperscaler/OEM 选择的 AEC、机柜间铜/光和 Ethernet scale-out 受益方。 | `AI bottleneck watch`：要求严格区分 MRVL/ALAB/CRDO 在 scale-up、机架内连接和 scale-out 的角色。属于作者产业链判断，不是已确认订单或 NVIDIA 供应关系。 | 高：status ID、作者、时间、完整正文；中低：产业链传导和未来架构份额 |
| `2069521725470175721` | 2026-06-24 04:43:23；页面显示 edited | https://x.com/Kay2289123/status/2069521725470175721 | 原创持仓说明 | 作者公开称其 MRVL 个人投资组合分为长期正股、波段正股和基于大额正股的 covered call / sell put 三层，并明确称未全部卖出 MRVL。 | 仅记录为作者自述，不视为经纪商核验成交，也不映射为用户账户动作。对策略只提供 `source_positioning/crowding` 温度；期权结构不可复制为稳定规则。 | 高：公开页面自述；低：真实持仓规模、成本、成交和持续状态 |
| `2069666239044317581` | 2026-06-24 14:17:38 | https://x.com/Kay2289123/status/2069666239044317581 | X Article：CRDO 深度分析 | X 长文与小红书 24 图内容一致但提供更完整正文：CRDO FY26 收入、AEC 驱动、客户集中、scale-out 现有收入、scale-up 期权、光 DSP/PIC/ZeroFlap 路线、光收入目标、并购、估值和风险清单。文末明确称发稿时不持有 CRDO。 | 延续 `current_AEC_cashflow` / `optical_optionality` 两条证据链；新增可测试风险字段：单一客户收入/应收占比、RPO、库存、股权稀释、GAAP/调整利润差异、光收入/毛利兑现。作者给出的价格区间和操作纪律不进入稳定策略。 | 高：Article ID、时间、完整正文；中低：财务数字和引文尚待公司一手资料逐项复核 |
| `2069669280178987314` | 2026-06-24 14:29:43 | https://x.com/Kay2289123/status/2069669280178987314 | CRDO Article 引用补充 | 作者自述曾两次关注并卖出 CRDO，核心总结为“光前进，铜未必后退；长期光机会大于铜”，并强调管理层光收入增长预期仍需持续跟踪。 | `theme crowding` 与 `source_positioning`；不能推断当前持仓或形成买卖建议。 | 高：公开正文/时间；低：历史成交无法独立核验 |
| `2069670049863119067` | 2026-06-24 14:32:47 | https://x.com/Kay2289123/status/2069670049863119067 | 置顶自我介绍 | 作者说明研究范围覆盖算力、互联、存储，并称 X 仅此账号、无付费服务。 | 来源身份与研究范围说明；不构成公司或市场事实。 | 高：页面存在/正文；低：个人背景声明未独立验证 |
| `2069674006215811089` | 2026-06-24 14:48:30 | https://x.com/Kay2289123/status/2069674006215811089 | X Article：CoreWeave | 长文把 CRWV 定位为重资产 GPU 工厂/租赁商：需求和订单强，但折旧、利息与 CapEx 令净亏损扩大。作者提出四个观察指标：CapEx/收入、利息/收入、扣折旧后的营业利润率、经营现金流对 CapEx 的覆盖。 | `AI_quality/capex_cycle`：新增 `neocloud_financing_fragility` 日常观察字段；高订单不等同于高自由现金流，需同时核验客户集中、电力、债务成本、设备利用率和 CapEx 放缓。单篇文章不升级为稳定规则。 | 高：Article ID、时间、完整正文；中低：文中财务数据和远期估值需 SEC/公司资料复核 |

### 9.2 `@nvidia`

以下均为 `@nvidia` 官方原创，严格窗口后可见：

| Status ID | UTC / 北京时间 | 链接 | 事实摘要 | 策略映射 | 证据 |
| --- | --- | --- | --- | --- | --- |
| `2069435311126417814` | 2026-06-23 15:00:01Z / 23:00:01 | https://x.com/nvidia/status/2069435311126417814 | NVIDIA 在 DTW Ignite 推广电信运营的全天候 AI agents，覆盖数据、模型、仿真和安全运行时；列出 Amdocs、NTT DATA、ServiceNow、TCS、SoftBank、Keysight、Samsung Research 等伙伴。 | telecom agentic AI / edge-network operations watch；对 NOK/QCOM 等只作产业链观察，不能直接传导。 | 高：官方 status |
| `2069450408737517660` | 2026-06-23 16:00:00Z / 2026-06-24 00:00:00 | https://x.com/nvidia/status/2069450408737517660 | NVIDIA Agent Toolkit 汇集开放 Nemotron 模型、工具、skills 与安全运行时，用于企业领域专用 agents。 | AI application/data-owner 与 inference runtime；需要企业采用、收入和成本证据。 | 高：官方 status |
| `2069480608749817922` | 2026-06-23 18:00:00Z / 02:00:00 | https://x.com/nvidia/status/2069480608749817922 | NVIDIA 称其平台覆盖 TOP500 的 81%、新增系统的 89%，并宣称训练/推理吞吐及 Green500 能效领先。 | AI compute/platform strength；数字属于官方营销口径，需 TOP500/MLPerf 等独立数据核验。 | 高：官方 status；中：投资传导 |
| `2069480612688220668` | 2026-06-23 18:00:01Z / 02:00:01 | https://x.com/nvidia/status/2069480612688220668 | 上述超级计算内容的官方博客链接补充。 | 同上，不单独增加策略权重。 | 高 |
| `2069525909724418344` | 2026-06-23 21:00:01Z / 05:00:01 | https://x.com/nvidia/status/2069525909724418344 | NVIDIA 称其对 NAIRR pilot 的 AI 基础设施贡献已支持 700 多个美国研究项目，使用 DGX 参考架构提供资源。 | AI infrastructure public/research demand；不等同于商业收入或订单。 | 高：官方 status |
| `2069525913264423355` | 2026-06-23 21:00:02Z / 05:00:02 | https://x.com/nvidia/status/2069525913264423355 | NAIRR 官方博客链接补充。 | 同上。 | 高 |

### 9.3 `@elonmusk`

| Status ID | 北京时间 | 链接 | 类型/摘要 | 策略映射 | 证据 |
| --- | --- | --- | --- | --- | --- |
| `2069445014787129590` | 2026-06-23 23:38:34 | https://x.com/elonmusk/status/2069445014787129590 | 置顶原创，讨论 DOGE 对资金接收方进行联系信息核验并否认停止经验证的医疗资助。 | 政策/政治内容；本次未发现可直接映射到美股 AI 组合的可靠新增催化。 | 高：公开正文；低：相关政策事实需政府文件验证 |
| `2069690741295861935` | 2026-06-24 15:55:00 | https://x.com/elonmusk/status/2069690741295861935 | 原创短帖“Try Grok”，引用用户称 Grok 优于 Google。 | xAI/Grok 消费与搜索采用温度；缺少用户、收入、留存或搜索份额数据，不形成策略信号。 | 高：status；低：商业传导 |
| `2069660314870899007` | 2026-06-24 13:54:06 | https://x.com/XFreeze/status/2069660314870899007 | Elon 转发 X Freeze 的 Grok Build v0.2.64 更新，涉及目录/分支显示、worktree agents、recap 等开发工具功能。 | agentic coding / developer workflow adoption watch；这是第三方原帖被 Elon 转发，不是 `@elonmusk` 原创产品声明。 | 中高：转发事实；中低：产品采用 |

其余可见转发主要是政治/文化内容，未映射进量化策略。

### 9.4 `@realDonaldTrump`

- Profile、Posts 和 Media 页面可读。
- 可见最新原创/置顶内容为 2026-06-21，早于严格窗口。
- 严格窗口后可见 verified item：`0`。
- 因此本次没有新增关税、贸易、科技监管、能源或地缘政策映射。

### 9.5 修正后的策略结论

- X 新内容增加了研究证据，不改变 2026-06-23 post-close 的 `market fear gate=elevated`、`flow_fragility=acute` 和同主题新买入阻断。
- CRDO X Article 强化“现有 AEC 现金流 + 光业务兑现风险”框架，但其价格区间、历史交易和主观操作纪律不进入 `decisions.md`。
- CoreWeave Article 增加 `neocloud_financing_fragility`：订单、收入增长和 EBITDA 必须与折旧、利息、CapEx、客户集中和 OCF-CapEx 缺口同时看。
- NVIDIA 官方内容支持 compute、agent toolkit、telecom agents 和公共科研基础设施需求仍活跃，但属于产品/生态事实，不是自动买入信号。
- Elon 的 Grok/Grok Build 更新只进入应用层和开发工具采用观察池。
- 未记录或推断任何用户真实成交；作者持仓声明与用户账户完全分离。
