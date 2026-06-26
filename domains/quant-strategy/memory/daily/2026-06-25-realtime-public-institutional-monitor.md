# 2026-06-25 实时公开来源与机构研究监控

运行时间：2026-06-25 20:33-21:29 Asia/Shanghai。

严格监控窗口：`2026-06-24T12:30:49.954Z` 至本次运行结束。窗口采用自动化提供的上次运行时间；对 2026-06-24 22:49 已写入的 X 项目按 status ID 去重。

范围：只读核验公开信息、证据分级、策略映射和记忆同步。未读取 cookies、密码、本地存储、私信、通知隐私或账号设置；未关注、点赞、评论、转发或发帖；未登录券商、未提交订单、未记录或推断未确认真实成交。本文不构成买卖建议。

## 1. 执行摘要

- 小红书账号“美研芒格君 / Kay2289123”出现一篇严格窗口后的新非置顶笔记：`MU先别眼红, 5+4逻辑全面梳理搞懂存储产业`，ID `6a3caa1a000000001700a95a`。正文、相对时间、作者评论和全部 `21/21` 轮播图均通过已登录 Chrome 可见页面核验，未读图片缺口为 `0`。
- `@Kay2289123` 新增可核验内容集中在 Cerebras / `CBRS`、MU 存储周期、MRVL CXL 内存池与作者 MRVL 长期持仓观点。Cerebras 长文提供了可测试的 `latency_vs_throughput_cost`、客户集中、数据中心 capex、毛利恢复和订单兑现字段，但其财务数字和公司引文仍需 SEC、公司财报和官方资料复核。
- `@nvidia` 新增官方内容覆盖生物医药 AI 基础设施、海浪能源数字孪生、广告营销 agentic workflow、Jetson 边缘零售，以及一项 `@NVIDIARobotics` 转发。它们支持 AI 应用/physical AI/edge AI 的需求观察，不构成自动交易信号。
- `@elonmusk` 的策略相关新增为一条 AI 监管机构名称玩笑/提议和一条 Starlink 哈萨克斯坦铁路部署转发；其余主要是政治/文化转发。`@realDonaldTrump` 页面可读，但最新可见主帖仍为 2026-06-21，严格窗口后 verified item 为 `0`。
- AQR、Citadel Securities、GMO、Man Institute 四源均完成列表和最多 8 个详情候选的核验，严格窗口后 official-domain verified framework 均为 `0`。Citadel 的列表与多个详情页可读；两个详情页受安全校验阻挡，若干分类页日期不可验证，不能写成来源整体不可用。
- 本次不更新 `decisions.md`，不新增直接买卖建议。只更新 H5 的存储层级、推理延迟/吞吐成本和 CXL 内存效率验证字段。

## 2. 已核验公开来源项

### 2.1 小红书

| 平台/来源 | 账号 | 笔记 ID | 页面可见时间 | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 | 美研芒格君 / `Kay2289123` | `6a3caa1a000000001700a95a` | 2026-06-25 约 20:37 北京时间显示“8小时前 美国”；精确绝对时间未暴露 | https://www.xiaohongshu.com/explore/6a3caa1a000000001700a95a | 非置顶笔记；21 图轮播 | 正文与图片用书桌/书架比喻拆分 SRAM、HBM、DDR、NAND/SSD、HDD，并按 AI 数据中心、手机、汽车/自动驾驶、机器人/边缘 AI、游戏显卡等场景解释速度、容量、持久性、功耗和可靠性差异。作者评论补充其后续关注具身 AI/物理 AI，并称 HBM 趋势“挺长，但不是永远”。 | 核心观点不是笼统“看好存储”，而是先识别存储层级和应用场景；AI 数据中心会同时拉动 HBM、DDR、企业 SSD 和 HDD，端侧/车载/边缘设备更看重低功耗、可靠性和本地推理。 | 为 `AI bottleneck watch` 增加 `memory_hierarchy_demand_map`；把存储候选按 HBM、DDR、NAND/SSD、HDD、CXL/offload、edge-memory 分层。内容热度提高研究优先级，但不能替代价格、周期、供需、毛利和集中度检查。 | 页面、作者、ID、正文、评论、`21/21` 图片为高；相对时间为中；行业供需、价格、份额和公司传导为中低 | MU/SK hynix/Samsung HBM 与 DRAM 供需、DDR5 价格持续性、企业 SSD 容量与价格、HDD nearline 排期、NAND/SSD 控制器与厂商份额、edge/auto memory 单车价值、周期库存、资本开支、毛利和价格趋势 |

轮播核验：

- 已读图片：`21`
- 总图片：`21`
- 未读缺口：`0`
- 图片层证据：高
- 内容层证据：作者科普与行业推断，不等同于公司公告或审计数据

### 2.2 X：`@Kay2289123`

| Status / Article ID | 发布时间（北京时间） | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `2069958412872638784`；伴随引用帖 `2069958893997040125` | 2026-06-25 09:38:38；伴随帖 09:40:32 | https://x.com/Kay2289123/status/2069958412872638784 | X Article：Cerebras / `CBRS` 财报与商业模式 | 长文讨论 wafer-scale SRAM 推理架构、低延迟与 GPU 高并发吞吐的差异、毛利率下滑、数据中心供给、客户集中、OpenAI 订单/融资关系、竞争、估值和解禁风险。 | Cerebras 技术护城河真实但专业化，强项是低延迟，弱项是高并发单位成本、客户集中、数据中心 capex、远期订单兑现和 NVIDIA 生态竞争。 | 新增 `latency_vs_throughput_cost`、`inference_specialization_risk`、`customer_financing_concentration` 和 `datacenter_capacity_margin_bridge` 观察字段；`CBRS` 仅进入高波动 speculative inference watch，不按作者价格区间形成规则。 | 高：Article ID、作者、完整正文、时间；中低：财务数字、客户/产品引文和估值情景尚未回到一手资料 | 10-Q/招股书客户占比、G42/MBZUAI 关联、OpenAI 合同/贷款/认股权证、750MW 交付、AWS Trainium 分工、云与硬件收入、毛利、OCF/CapEx、锁定产能、解禁/Form 4、实际 tokens/s 与单位成本 |
| `2069907461730087236` | 2026-06-25 06:16:10；页面显示 edited | https://x.com/Kay2289123/status/2069907461730087236 | 原创 MU / 存储周期帖 | 页面可见作者称 MU 财报“双超预期”并盘后上涨，重申短期缺算力、长期缺存储、持续需要更快互联，并引用“multi-decade memory demand cycle”。 | 存储与互联仍是长期主线，但作者同时提醒不要在“半场开香槟”。 | 作为 `theme crowding` 和 memory-cycle 研究温度；财报数据、盘后涨幅和管理层引文必须独立复核，不能在价格急涨后转化为追涨信号。 | 高：status/作者/时间/正文；中低：财报数字和投资传导 | MU 正式财报、指引、HBM/DRAM/NAND 分部、毛利、供给扩张、库存、客户、价格、盘后与常规时段价格确认 |
| `2069864998801961428`；引用官方 `@MarvellTech` `2069839931871261080` | 2026-06-25 03:27:26；官方引用帖 03:47:50 前后页面可见 | https://x.com/Kay2289123/status/2069864998801961428 | 原创帖引用 Marvell 官方 CXL 内容 | 作者称 DDR5 价格上涨使 MRVL 的 Structera CXL、廉价内存、2:1 硬件压缩和 DDR4 再利用具备节省成本的意义；官方引用帖称服务器 DDR5 每 GB 成本和价格明显上升。 | “Micron 卖稀缺，Marvell 卖节省”，互联和内存池可提高算力/存储利用率。 | 增加 `memory_capacity_efficiency`、`CXL_latency_tax`、`compression_realized_ratio` 和 `cold_vs_hot_data_fit` 字段；不能只看节省内存成本，必须核验延迟、软件采用、工作负载和真实 TCO。 | 高：Kay status、官方引用存在与正文；中低：价格数字、压缩比和大规模采用 | Marvell 官方产品资料、DDR5 价格来源、CXL 延迟、压缩比、客户部署、软件生态、收入/毛利、与光内存池/竞品的差异 |
| `2069844080474071194` | 2026-06-25 02:04:19 | https://x.com/Kay2289123/status/2069844080474071194 | 原创持仓/长期观点说明 | 作者公开称持有 MRVL 三年，并以需求、业绩和 NVIDIA 合作为继续判断的核心问题。 | 心态和纪律比短期聪明重要，长期互联需求未变。 | 只记录为作者自述和 `source_positioning/crowding`；不验证真实持仓，不映射为用户账户动作，也不能覆盖用户已确认的 MRVL 止损执行。 | 高：公开页面自述；低：真实持仓规模、成本、交易和供应关系 | 作者持仓不可独立核验；MRVL/NVIDIA 合作范围、订单、收入、利润、估值和价格趋势需一手验证 |

### 2.3 X：`@nvidia`

| Status ID | 发布时间（北京时间） | 链接 | 类型/事实摘要 | 策略映射 | 证据 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- |
| `2069990854589333805`；引用 `@nvidianewsroom` `2069956130365718649` | 2026-06-25 11:47:32；引用帖 09:29:34 | https://x.com/nvidia/status/2069990854589333805 | 官方原创引用 BIO2026 医药 AI 讨论，强调安全、可扩展 AI 基础设施对发现流程的重要性 | healthcare AI / research infrastructure watch；不等于商业收入 | 高：官方页面；中低：投资传导 | 客户部署、药物发现效率、收入、合作范围与真实生产使用 |
| `2069888296684073414` / `2069888298617630762` | 2026-06-25 05:00:01 | https://x.com/nvidia/status/2069888296684073414 | 官方原创及博客伴随帖：Eco Wave Power 使用 Omniverse 数字孪生和加速计算模拟海浪能源条件 | energy digital twin / industrial AI / power infrastructure watch | 高：官方内容；中低：规模和收入传导 | 项目规模、商业部署、Omniverse 使用深度、收入和能源经济性 |
| `2069873195499352248` / `2069873200020795545` | 2026-06-25 04:00:00 | https://x.com/nvidia/status/2069873195499352248 | 官方原创及博客伴随帖：广告营销合作伙伴使用 NVIDIA full-stack AI 做因果分析、安全 agentic workflow 和实时竞价 | application/data-owner 与 inference workflow watch | 高：官方内容；中低：商业采用 | 付费客户、推理量、收入、成本、竞价改善和合作伙伴实际依赖 |
| `2069842996082708907` / `2069842999899468129` | 2026-06-25 02:00:00 | https://x.com/nvidia/status/2069842996082708907 | 官方原创及播客伴随帖：Instacart Caper Carts 使用 Jetson/edge AI 在真实杂货店识别商品 | edge AI / retail physical AI / Jetson deployment watch | 高：官方内容；中：投资传导 | 部署台数、单位经济、识别准确率、Jetson 收入与客户扩张 |
| `2069860852963143745` | 2026-06-25 03:10:58 | https://x.com/NVIDIARobotics/status/2069860852963143745 | `@nvidia` 转发 `@NVIDIARobotics`：Cosmos 3 Nano 后训练 policy model 在 MolmoSpaces 榜单排名声明 | robotics / physical AI model watch；明确为关联账号转发，不是 `@nvidia` 原创 | 中高：转发与关联账号正文；中低：榜单和商业传导 | 榜单方法、复现、真实机器人部署、收入和生态采用 |

### 2.4 X：`@elonmusk`

| Status ID | 发布时间（北京时间） | 链接 | 类型/事实摘要 | 策略映射 | 证据 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- |
| `2070042592012570970` | 2026-06-25 15:13:08 | https://x.com/elonmusk/status/2070042592012570970 | 置顶原创，提出/调侃 AI 行业监管机构名称 | 仅作为 `AI_policy_sentiment` 低权重观察，不能当作正式政策 | 高：status；低：政策传导 | 是否存在正式监管提案、法案、机构文件或行政行动 |
| `2070049375347159552` | 2026-06-25 15:40:05 | https://x.com/elonmusk/status/2070049375347159552 | 原创引用外援政治帖，询问遗漏国家 | 政治/财政观点；本次不形成美股 AI 组合可靠催化 | 高：status；低：事实和市场传导 | 原帖数字、政府预算和政策文件 |
| `2070036268260450796` | 2026-06-25 14:48:00 | https://x.com/cb_doge/status/2070036268260450796 | Elon 转发 DogeDesigner，称哈萨克斯坦铁路将为约 900 节车厢部署 Starlink | Starlink / satellite connectivity adoption watch；属于第三方原帖被转发 | 中高：转发事实；中低：部署和收入 | KTZ/Starlink 官方公告、合同、上线时间、收入和覆盖范围 |

### 2.5 X：`@realDonaldTrump`

- Profile、Posts 和 Media 页面可读。
- 最新可见主帖/置顶为 2026-06-21，早于严格窗口。
- 严格窗口后 verified item：`0`。
- 本次没有新增关税、贸易、科技监管、能源或地缘政策映射。

## 3. 机构研究源核验

本地检查器命令：

```powershell
node D:\code\AI-Memory\domains\quant-strategy\tools\institutional-research-checker.js --since 2026-06-24T12:30:49.954Z --max-items 8 --out D:\code\AI-Memory\domains\quant-strategy\work\institutional-research-latest.md
```

已读取并交叉核对：

- `work/institutional-research-latest.md`
- `work/institutional-research-latest.json`

本次 JSON 可由 PowerShell `ConvertFrom-Json` 成功解析。

| 来源 | 列表页 | 详情页 | 严格窗口后新增 | 结论 |
| --- | --- | --- | ---: | --- |
| AQR Research | Reader 可读 | 8 个详情候选可读并日期过滤 | 0 | 最新稳定详情均为窗口前/既有；不新增 `trend_aligned_entry` 框架 |
| Citadel Securities | Reader 列表可读 | 多个详情页可读；`regime-changebut-not-in-iran` 与 `the-frontier-is-not-for-everyone` 为 `detail_blocked_no_date`；若干分类页 `date_unverified` | 0 | 来源不是整体不可用；没有窗口后稳定标题、日期和正文的新详情项 |
| GMO Research Library | Reader 列表可读 | 8 个详情候选可读并日期过滤 | 0 | 最新稳定详情为窗口前/既有；不新增 AI quality/valuation 框架 |
| Man Institute Market Views | Reader 列表可读 | 8 个详情候选可读并日期过滤 | 0 | 2026-06-23 `The Strait of Uncertainty` 早于 cutoff；不作为本次新增 |

没有 official-domain detail page 同时满足窗口后、稳定标题、日期和正文，因此不更新 `institutional-market-research-framework.md`。

## 4. 公开事实、作者观点、我的推断

### 公开事实

- 小红书主页显示 `6a3caa1a000000001700a95a` 为最新非置顶笔记；详情页可见正文、相对时间、作者评论和 `1/21` 轮播标识。
- 21 个轮播原图均已读取。
- X status/Article 页暴露上述 ID、作者、正文和页面时间；时间同时按 X snowflake 校准。
- 机构检查器四源严格窗口后 verified count 均为 0。

### 作者观点或二手整理

- AI 数据中心会同时拉动 HBM、DDR、SSD/NAND 和 HDD，而端侧/车载/边缘 AI 的存储需求结构不同。
- MU/存储进入长期需求周期，MRVL CXL/压缩可以降低内存成本。
- Cerebras 的低延迟推理有真实价值，但客户集中、毛利、capex、订单兑现和单位成本是主要风险。
- NVIDIA 官方内容显示 AI 应用正在向医药、能源数字孪生、广告、零售边缘和机器人扩展。

这些内容中涉及财务数字、市场份额、性能、价格、订单和供应关系的部分，未在本次逐项回到 SEC、财报、合同或独立 benchmark 核验。

### 我的策略推断

- “存储”不应作为单一主题字段，应拆成 `SRAM/HBM/DDR/NAND-SSD/HDD/CXL-offload/edge-memory`，并按应用场景匹配收入和周期证据。
- 推理芯片不能只比较 token 速度，应同时记录单用户延迟、总吞吐、并发、能耗、单位 token 成本、软件生态和资本开支。
- MU/storage 内容与价格急涨的同步提高了 `theme crowding`，首先应提高追涨门槛，而不是提高仓位优先级。
- 作者长期持仓叙述不得覆盖用户账户的止损纪律或已确认 MRVL 平仓事实。

## 5. 策略映射

| 维度 | 本次映射 |
| --- | --- |
| `market fear gate` | 本监控不刷新市场行情，沿用 2026-06-24 正式收盘 `normal 3/14`；单篇社媒或官方产品帖不能改变门控。 |
| `trend_aligned_entry` | MU/storage、MRVL CXL、CBRS 只进入验证队列；急涨或高估值下必须等待价格趋势、相对强度、支撑/收复和成交量确认。 |
| `flow_fragility` | 沿用 `9/14 elevated`。存储盘后急涨、社媒热度和同主题扩散提高 crowding 警惕，但不是新的量化分数。 |
| `AI_quality/capex_cycle` | `CBRS` 暂列 speculative inference accelerator：技术差异化高，但客户集中、capex、毛利和远期订单风险高。存储链继续区分 HBM/DRAM/NAND/HDD 周期与平台/控制器/互联卖铲者。 |
| `factor_macro_exposure` | 维持 `theme_overlap_high`、`growth_duration_high`、`AI_capex_cashflow_pressure`；Elon AI 监管帖只作低权重政策情绪，不新增正式 flag。 |
| `AI bottleneck watch` | 新增 `memory_hierarchy_demand_map`、`latency_vs_throughput_cost`、`CXL_memory_efficiency`、`edge_memory_reliability` 四组字段。 |
| `theme crowding` | MU/storage 的内容热度与盘后叙述显示主题温度上升；需防止把结构性需求与短期供给缺口、价格垂直上涨混为一谈。 |
| `portfolio concentration` | 当前确认持仓 GLW/TTMI 已是同一 AI 基建/互联主题；本次内容不得为 MRVL、MU、SNDK、WDC、STX、CBRS 等绕过集中度约束。 |
| `replay/backtest plan` | 对存储主题增加 HBM/DDR/NAND/HDD 层级标签、库存/价格/毛利/CapEx、价格跳空后 5/20/60 日表现；对推理芯片增加 latency、throughput、unit cost、customer concentration、OCF-CapEx 和毛利恢复字段。 |

## 6. 记忆更新

- 创建本文件。
- 更新 `references/realtime-public-source-tracker.md`。
- 更新 `memory/hypotheses.md` 的 H5 验证字段。
- 向 `memory/daily-summaries.md` 追加一条简洁总结。
- `memory/decisions.md` 未更新。
- `references/institutional-market-research-framework.md` 未更新。

## 7. 数据缺口、需要确认的问题与后续重点

数据缺口：

- 小红书只暴露“8小时前”，没有稳定绝对发布时间。
- 小红书和 Kay X 中的 MU、DDR5、HBM、HDD、CBRS、MRVL 财务/价格/性能/订单数字尚未逐项回到公司一手资料核验。
- `@nvidia` 的产品/生态帖缺少商业收入、部署规模和单位经济数据。
- Elon 转发的 Starlink 铁路部署尚未取得 KTZ/Starlink 一手合同或公告。
- Citadel 两个候选详情页仍受安全校验阻挡，日期和正文不可验证。

需要用户确认的来源访问问题：

- 本次已登录 Chrome 可读取主要账号，不需要调整隐私扩展。
- 若用户希望未来把 Citadel 受阻详情候选升级为高证据，需要可读的 official-domain detail page 或官方 PDF；当前不建议仅凭列表候选提炼框架。

后续开盘准备重点读取：

- `memory/daily/2026-06-24-post-close-audit.md`
- `memory/daily/2026-06-25-realtime-public-institutional-monitor.md`
- `memory/portfolio/2026-06-24-portfolio-summary.md`
- `memory/todos/2026-06-24-strategy-todos.md`
- `memory/trades/2026-06-25-real-mrvl-sell.md`
- `work/institutional-research-latest.md`
- `work/institutional-research-latest.json`
