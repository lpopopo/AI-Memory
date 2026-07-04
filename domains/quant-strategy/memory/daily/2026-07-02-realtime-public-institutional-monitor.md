# 2026-07-02 实时公开来源与机构研究监控

## 20:43-20:46 美国 6 月非农增量核验

### BLS 官方事实

- 发布时间：2026-07-02 08:30 ET（北京时间 20:30）；官方发布为 `THE EMPLOYMENT SITUATION - JUNE 2026`，公告号 `USDL-26-1125`。
- 非农就业：6 月季调后总非农就业增加 `57,000`；BLS 将其描述为变化不大，过去 12 个月月均增加 `36,000`。
- 失业率：`4.2%`，5 月为 `4.3%`；失业人数约 `709.4 万`。
- 劳动参与率：由 `61.8%` 降至 `61.5%`；就业人口比率由 `59.2%` 降至 `59.0%`。家庭调查就业人数减少 `50.7 万`，劳动力减少 `72.0 万`，因此失业率下降不能单独解释为劳动力市场走强。
- 工资与工时：私人非农平均时薪环比 `+0.3%`、同比 `+3.5%`，升至 `$37.64`；平均每周工时持平于 `34.3` 小时。
- 修正：4 月由 `+179,000` 下修至 `+148,000`，5 月由 `+172,000` 下修至 `+129,000`，两月合计下修 `74,000`。
- 行业：专业与商业服务 `+36,000`、社会援助 `+25,000`、医疗保健 `+22,000`；休闲与酒店业 `-61,000`。其他主要行业变化不大。
- 核验渠道：BLS 官方发布页和归档正文均可经只读文本代理读取；BLS Public Data API 的 `CES0000000001`、`LNS14000000`、`CES0500000003`、`CES0500000002`、`LNS11300000` 与公告一致。来源：[BLS June 2026 Employment Situation](https://www.bls.gov/news.release/archives/empsit_07022026.htm)。

### 我的推断与策略映射

- 数据组合是“企业新增就业弱、前值下修、家庭就业和参与率下降，但工资仍有韧性”。失业率下降主要伴随劳动力退出，不能按表面数字归类为全面就业改善。
- `factor_macro_exposure`：增长敏感资产面对就业减速；久期资产可能受降息预期支持，但 `3.5%` 工资增速意味着通胀约束没有消失。需要结合美债 2Y/10Y、美元、HYG/LQD 与联邦基金期货的发布后反应确认。
- `market fear gate`：该数据本身不改变 gate；需等待 VIX、期限结构、市场宽度与信用价差更新。不能因失业率低于上月便解除现有 `flow_fragility` 或持仓风险线。
- `AI_quality/capex_cycle`：就业减速会提高市场对 AI capex 自融资能力、信用支持和现金流兑现的敏感度；继续验证 `AI_cloud_credit_support`，不把宏观数据直接外推为单一 AI 标的方向。
- `replay/backtest plan`：记录发布时点，比较 30 分钟、收盘、1/5/20 日的 QQQ/SMH/IWM、2Y/10Y、DXY、HYG/LQD 和 AI-capex 篮子反应；拆分新增就业、前值修正、工资、参与率四类冲击。
- 本节只做宏观事实核验和策略条件映射，不生成直接买卖建议；市场一致预期尚未从独立可靠来源核验，因此不计算“高于/低于预期”的 surprise。

## 20:20-20:39 增量续跑（当前有效窗口）

### 运行边界

- 严格窗口：`2026-07-01T18:04:55.498Z` 至 2026-07-02 20:39（北京时间）；起点来自 `C:\Users\lp\.codex\automations\automation\memory.md` 的最近成功截止，没有使用 24 小时回退。
- 只读使用已登录 Chrome 核验公开页面；未读取 cookies、密码、本地存储、私信、通知隐私或账号设置，未关注、点赞、评论、转发、发帖、登录券商或提交订单。
- 本节是同日上一轮监控之后的增量结果。只做事实核验、证据分级、策略映射和记忆同步，不生成直接买卖建议，不记录或推断未确认真实成交。

### 结论摘要

#### 公开事实

1. 小红书 `美研芒格君 / Kay2289123` 新增非置顶笔记《存储之后的下个机会，聪明人已经开始关注》，ID `6a45e9690000000016027e78`，页面显示 `7小时前 美国`。标题、正文、作者置顶评论和 `32/32` 轮播均可读；32 张原图已逐张视觉/OCR复核，未读缺口 `0/32`。
2. `@Kay2289123` 窗口内新增三项可读内容：`2072513751262404612` 为作者对 META 组织、算力转售和自述减仓的解释；`2072542712205914491` 为小红书新笔记对应的完整 X 长帖；`2072554591506641280` 为作者回复，预告继续写光互连路线。作者所谓 META 经历、内部朋友信息、仓位和卖出 `80%` 均是自述，不是独立核验事实或真实账户成交。
3. `@nvidia` 窗口内发布 Isaac ROS 开源机器人平台帖子 `2072440109358600197`，以及 AI cloud 多租户 AI factory、收入分成和信用支持合作帖 `2072545807505527251`；配套链接回复分别为 `2072440113527664860`、`2072545810881839263`。官方帖子可核验，但没有披露伙伴、合同规模、信用承担结构、利用率或收入。
4. `@elonmusk` 窗口内转发 SpaceX 第 1000 台 Merlin 1D 发动机完成制造/验收 `2072464558732824680`，并转发第三方对 Tesla Supercharger 2026Q2 交付 2TWh 的陈述 `2072408701554897130`。前者是关联官方事实；后者仍需 Tesla 官方材料核验。
5. `@realDonaldTrump` 主页可读，但当前可见最新内容仍为 2026-06-21；严格窗口项目为 `0`。Kay `Articles` 最新仍是 6 月 30 日旧文，窗口新增 `0`；`Media` 最新仅对应本轮已记录的 `2072542712205914491`。
6. 机构检查器以同一严格窗口完成并读取 Markdown/JSON。AQR、Citadel Securities、GMO、Man Institute 各检查 8 个候选，四家 `post_window_verified=0`；全部列表页可读，AQR/GMO/Man 的 8 个详情均可读，Citadel 5 个稳定日期详情可读、3 个分类页日期不可验证。

#### 我的推断

- 新小红书笔记没有推翻既有 `capacity_relief_vs_bandwidth_relief`，而是把它扩成“内存税绕行生态”：HBF/CXL/预测分层主要缓解容量，PIM/PNM/光互连/3D 堆叠主要缓解搬运、带宽或距离；路线可以组合，不能按同一指标排名。
- 图片 29-31 的核心增量是 `memory_standard_power_shift`：当云厂商用长约、规格和接口定义需求，价值可能从单纯制造比特转向标准、控制器、封装/代工和软件。但这仍是作者框架，需以 JEDEC/OCP/CXL 官方标准、采购合同、产品量产和收入验证。
- NVIDIA 的收入分成与信用支持模式把 AI cloud 扩容从纯设备销售延伸到 `AI_cloud_credit_support`。这可能扩大算力覆盖，也可能把伙伴信用、利用率和残值风险部分传回 NVIDIA；应接入 `AI_credit_funding_fragility`，不是单向利好。
- Kay 的 META 减仓与“转向其他持仓”是注意力/轮动自述。它可进入 `theme crowding / flow_fragility`，不得写成已确认交易、公司内部事实或稳定规则。

### 已核验公开源项目

| 平台/来源 | 账号 | ID / 发布时间（北京时间） | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 | 美研芒格君 | `6a45e9690000000016027e78`；页面显示 `7小时前 美国` | https://www.xiaohongshu.com/explore/6a45e9690000000016027e78 | 新笔记；32 图 | 正文和图片拆分容量/带宽问题，覆盖 HBF、PIM/PNM、光互连、3D 堆叠、预测分层、CXL、SRAM，并讨论标准/接口和封装代工 | 内存紧张可能延续，绕开“内存税”的多路线会形成新生态 | `AI bottleneck watch`、`AI_quality/capex_cycle`、`portfolio concentration`、`replay/backtest plan` | 高：页面、正文、评论、`32/32` 原图；中：相对时间；低至中：产业数字/公司归因 | 绝对发布时间；AMD/MEXT、HBF、CMX、CXL、HBM4、代工/标准和产能数据的官方材料 |
| X | `@Kay2289123` | `2072513751262404612`；2026-07-02 10:52（最后编辑） | https://x.com/Kay2289123/status/2072513751262404612 | 编辑长帖 | 可见全文讨论 META 算力转售、组织与模型变现，并自述卖出 80% META | 认为 META 上行空间和管理逻辑变弱 | `flow_fragility`、`theme crowding`、`factor_macro_exposure` | 高：帖子/ID/正文/编辑时间；低：履历、内部信息、仓位与成交自述 | META 官方战略、capex、云业务合同、组织/人才事实；作者交易不可核验 |
| X | `@Kay2289123` | `2072542712205914491`；2026-07-02 12:47（最后编辑） | https://x.com/Kay2289123/status/2072542712205914491 | 长帖+旧 Article | 完整文字版对应小红书 32 图框架，列 HBF、近内存计算、光 HBM、3D 堆叠、分层/CXL、SRAM | 多路线分工形成绕开内存税的新曲线 | `AI bottleneck watch`、`AI_quality/capex_cycle` | 高：帖子全文/ID/编辑时间；产业传导中低 | 同上；作者“真金白银”陈述不进入账户记忆 |
| X 回复 | `@Kay2289123` | `2072554591506641280`；2026-07-02 13:34 | https://x.com/Kay2289123/status/2072554591506641280 | 作者回复 | 预告继续拆解突破内存墙的光互连路线和玩家 | 把光互连作为下一研究重点 | `theme crowding`、`AI bottleneck watch` | 高：回复存在/正文/时间；前瞻传导低 | 后续正文、官方产品/订单、估值与价格确认 |
| X | `@nvidia` | `2072440109358600197` / `2072440113527664860`；2026-07-02 06:00 | https://x.com/nvidia/status/2072440109358600197 | 官方原帖+链接回复 | Isaac ROS 被描述为面向移动机器人、操作系统和人形机器人的开源模块化 CUDA 加速平台 | 降低机器人开发门槛 | physical-AI watch、`AI_quality/capex_cycle` | 高：官方帖；商业传导低至中 | 开源采用、部署量、Jetson/软件收入、客户与单位经济 |
| X | `@nvidia` | `2072545807505527251` / `2072545810881839263`；2026-07-02 13:00 | https://x.com/nvidia/status/2072545807505527251 | 官方线程 | 声称与 AI clouds 通过收入分成和信用支持部署大规模多租户 AI factories | 从训练转向持续 Token 生产需要新商业模式 | `AI_quality/capex_cycle`、`flow_fragility`、`factor_macro_exposure` | 高：官方声明；财务传导中 | 合作伙伴、合同/担保结构、GPU 所有权、利用率、坏账/残值、收入确认和现金流 |
| X 转发 | `@elonmusk` / `@SpaceX` | `2072464558732824680`；2026-07-02 07:37 | https://x.com/SpaceX/status/2072464558732824680 | 关联官方转发 | SpaceX 称第 1000 台 Falcon 一级 Merlin 1D 发动机完成制造与验收测试 | 将复用与累计制造视为可靠性改进基础 | space / satellite infrastructure watch | 高：SpaceX 官方帖；上市标的传导低 | 生产/发射节奏、可靠性统计、成本、订单；不可外推 RKLB/RDW/TSLA |
| X 转发 | `@elonmusk` / `@XFreeze` | `2072408701554897130`；2026-07-02 03:55 | https://x.com/XFreeze/status/2072408701554897130 | 第三方帖子被转发 | 帖称 Tesla Supercharger 2026Q2 全球交付 2TWh 电量 | 将其视为网络规模扩张 | physical infrastructure / TSLA watch | 中：第三方可见且被转发；数字未独立核验 | Tesla 官方季度数据、站点/端口、利用率、收入、capex 和利润 |

### 机构研究核验

检查器命令：`institutional-research-checker.js --since 2026-07-01T18:04:55.498Z --max-items 8`；运行约 206 秒，成功写出并读取 `institutional-research-latest.md` 与 `.json`。

| 机构 | 列表页 | 详情页 | 窗口新增 | 本轮结论 |
| --- | --- | --- | ---: | --- |
| AQR | 可读 | 8/8 可读，稳定日期均早于窗口 | 0 | 不新增 `trend_aligned_entry` 框架 |
| Citadel Securities | 可读 | 5 个稳定日期详情可读；3 个分类页日期不可验证 | 0 | 来源可用；日期不可验证分类页不提炼框架 |
| GMO | 可读 | 8/8 可读，稳定日期均早于窗口 | 0 | 不新增 `AI_quality/capex_cycle` 框架 |
| Man Institute | 可读 | 8/8 可读，稳定日期均早于窗口 | 0 | 7 月 1 日 AI 债券文章已在上一轮处理，不重复提炼 |

### 策略映射

- `market fear gate`：本轮来源监控没有刷新 VIX、期限结构、宽度或信用；沿用最近正式 2026-07-02 post-close audit 的 `normal 2/14`，但不能用来源内容解除四持仓已触发风险线和 `flow_fragility 11/14 acute`。
- `trend_aligned_entry`：新笔记和 NVIDIA 帖不能替代 20/50 日趋势、相对强度和回撤质量；在急跌后的 AI-capex 篮子中仍是 `trend_broken / no new buy` 的证据背景。
- `flow_fragility`：Kay 的 META 减仓自述、存储/互连路线集中传播，以及 NVIDIA 信用支持模式均提示叙事、融资和主题相关性需要单独记录。
- `AI_quality/capex_cycle`：新增 `memory_standard_power_shift` 和 `AI_cloud_credit_support` 实验字段；区分制造比特、控制标准/接口、软件调度、封装代工及信用承担。
- `factor_macro_exposure`：收入分成/信用支持把 GPU 需求与 AI cloud 信用、残值和利用率绑定；需与 HYG/LQD、发行/融资条件和公司现金流一起验证。
- `AI bottleneck watch`：容量侧跟踪 HBF/CXL/分层/SRAM；带宽/搬运侧跟踪 PIM/PNM/光互连/3D；标准与封装侧跟踪 JEDEC/OCP/CXL、HBM4 base die 和代工渠道。
- `theme crowding`：小红书 119 条评论中大量追问“买哪个”，Kay 又预告光互连专栏，显示注意力正在从存储向“绕开内存税”路线扩散；这只用于拥挤度，不进入买入分数。
- `portfolio concentration`：GLW/MXL/DRAM/MU 与 SNDK/MRVL/ALAB/光互连/设备候选仍共享 AI-capex、内存墙和云厂商融资风险，不能按 ticker 数量视为分散。
- `replay/backtest plan`：记录小红书/X 同主题发布、Kay META 减仓自述和 NVIDIA AI-cloud 信用支持事件日，比较 1/5/20/60 日相对 QQQ/SMH/XSD/HYG/LQD、成交量、最大不利波动、信用/融资变化；拆分容量、带宽、标准/封装和信用四类因子。

### 数据缺口与需要用户确认的来源访问问题

1. 小红书本轮 `32/32` 图片均已读，轮播无缺口；但页面仅显示 `7小时前 美国`，没有绝对发布时间。无需用户提供登录信息。
2. 新笔记和 Kay X 帖含大量产业数字、公司归因、作者履历/人脉和交易自述；均未获公司公告、监管文件或券商记录独立确认。
3. NVIDIA 未披露 AI-cloud 收入分成/信用支持的伙伴、担保边界、GPU 所有权、利用率、残值与收入确认，当前只能建立实验字段。
4. Elon 转发的 Tesla 2TWh 数字来自第三方账号，尚未回到 Tesla 官方材料；纯视频帖 `2072445332315902174` 正文不可读，未做策略映射。
5. Trump 可见时间线仍停留在 6 月 21 日，只能说明当前 X 可见页无窗口项目，不能证明其他平台无新声明。
6. 当前无需要用户立即处理的来源登录问题；若后续页面出现验证码或登录失效，只需用户在 Chrome 中恢复页面，不应提供密码、cookie 或隐私数据。

### 后续开盘准备重点读取

1. `memory/daily/2026-07-02-realtime-public-institutional-monitor.md`（本文件，本节优先）
2. `memory/daily/2026-07-02-post-close-audit.md`
3. `memory/trades/2026-07-02-trade-plan.md`
4. `memory/portfolio/2026-07-02-portfolio-summary.md`
5. `memory/todos/2026-07-02-strategy-todos.md`
6. `references/realtime-public-source-tracker.md`
7. `references/institutional-market-research-framework.md`
8. `references/ai-quality-capex-cycle-classification.md`
9. `work/institutional-research-latest.md` 与 `work/institutional-research-latest.json`

### 记忆处置

- 已更新本文件、realtime tracker、H5/H8 假设和 daily summaries。
- `decisions.md` 不变：本轮为单日公开来源、公司宣传和作者观点，没有历史 replay 或反复验证支持升级为稳定规则。

## 运行边界

- 运行时间：2026-07-02 01:58-02:01（北京时间）。
- 严格窗口：`2026-06-30T15:50:24.313Z` 至 `2026-07-01T18:01:02.604Z`。起点采用自动化记忆中的最近成功截止，没有使用 24 小时回退。
- 范围：只读核验公开可见页面；未读取 cookies、密码、本地存储、私信、通知或账号设置；未关注、点赞、评论、转发、发帖、登录券商或提交订单。
- 本报告只做公开事实核验、证据分级、策略映射和记忆同步，不生成直接买卖建议，不记录或推断未确认真实成交。

## 结论摘要

### 公开事实

1. 小红书 `美研芒格君 / Kay2289123` 主页没有出现比既有 MU/存储笔记更晚的新非置顶笔记；旧 Cerebras 笔记 `6a41e1fd00000000170095e6` 的详情页在本轮首次读取时仍可见，显示 `编辑于 昨天 14:26 美国`、`26/26`，作者置顶评论明确说文章重新上线后修改了最后结论和部分内容。
2. `@Kay2289123` 窗口内可见互连三强拥挤度回顾、半导体设备 capex 研究方法、HBM/内存替代路线补充，以及对“Meta 出售算力等于行业过剩”的反驳。帖子存在、正文、ID 和时间为高证据；作者收益、持仓、Meta 内部交流和产业数字不是独立核验事实。
3. `@nvidia` 窗口内有美国 AI 五层产业叙事的官方线程，并转发 `@NVIDIAAI` 的通用运动控制器研究；均为产品/研究或政策叙事，没有订单、合同和收入规模。
4. `@elonmusk` 窗口内可见 Neuralink 穿硬脑膜电极植入原帖，并转发 xAI Memphis 投资、Grok Voice Agent Builder、Neuralink/Optimus 内容。只有 Neuralink 原帖可作为高证据的公开声明；被转发的第三方帖子仍需原始产品/监管/财务材料核验。
5. `@realDonaldTrump` 主页可读，当前可见最新内容仍为 2026-06-21 及更早；严格窗口内可核验项目为 `0`。
6. 机构检查器读取了 Markdown 与 JSON：AQR、Citadel Securities、GMO 均为 `post_window_verified=0`；Man Institute 有 1 篇 2026-07-01 官方详情页文章，标题、日期和正文稳定可读，可提炼为新的实验性信用融资框架。

### 我的推断

- Kay 的 Meta 帖提出有用的验证问题：单一公司、单一区域或单一 GPU 代际的闲置/转售，不能自动等于全行业结构性过剩。应把 `localized_capacity_mismatch` 与 `structural_compute_demand` 分开测量，但帖中的 Meta 内部交流、合同数字和“只是机构获利了结”仍属作者解释。
- 半导体设备帖子更适合作为 `equipment_capex_lead_lag` 假设：招聘、管理层问答和扩产公告可能早于收入确认；但作者自述重仓和 40% 收益只进入 `theme crowding`，不能成为候选分数。
- Man 的新文章强化 `AI_credit_funding_fragility`：AI 股权估值提供上行期权，债权人却承担建设延迟、成本超支、竞争和长期需求风险；没有稳定现金流业务作信用背书的 neocloud/data-center 纯标的更脆弱。
- NVIDIA/Elon 内容支持美国本土 AI 产业、physical AI 和开发工具的观察池，但当前证据主要是宣传或研发事实，不足以推导收入、估值或交易动作。

## 已核验公开源项目

| 平台/来源 | 账号 | ID / 页面可见时间（北京时间） | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 | 美研芒格君 | `6a41e1fd00000000170095e6`；页面显示“编辑于 昨天 14:26 美国” | https://www.xiaohongshu.com/explore/6a41e1fd00000000170095e6 | 旧笔记编辑更新 | 标题、正文、`26/26`、作者置顶评论可见；评论称重新上线后修改了最后结论和部分内容 | Cerebras 更像低延迟 decoder 专用加速器，不等于最佳生意；价格溢价、生态和利润分配仍是问题 | `AI_quality/capex_cycle`、`AI bottleneck watch` | 高：页面/正文/评论；中：相对编辑时间；低至中：编辑后图片证据 | 本轮编辑后轮播未重读；历史累计仅 `24/26` 原图复核，2 张缺口；绝对时间、技术/业务数字待官方材料 |
| X | `@Kay2289123` | `2071988672778678273`；2026-07-01 00:06 | https://x.com/Kay2289123/status/2071988672778678273 | 原帖+旧文引用 | 回顾 ALAB/CRDO/MRVL 三条互连研究，并自述收益和可能重新集中光互连 | “光进铜未必退”，互连长期持续需要 | `theme crowding`、`flow_fragility`、`portfolio concentration` | 高：帖子存在/正文；低：收益、持仓和归因自述 | 三家公司订单、客户集中、估值、相对强度；作者真实成交不可核验 |
| X | `@Kay2289123` | `2072022672603848988`；最后编辑 2026-07-01 02:21 | https://x.com/Kay2289123/status/2072022672603848988 | 原帖+图片 | 描述从 INTC/SpaceX 扩产、招聘和设备经验要求推演 AMAT/KLAC/LRCX/ASML 机会 | 设备“铲子”可能先于市场定价扩产 | `AI_quality/capex_cycle`、`AI bottleneck watch`、`replay/backtest plan` | 高：帖子事实；中低：招聘/扩产和未定价结论 | 官方 capex、招聘原文、订单/backlog、交付和收入确认；所谓 40% 收益不可核验 |
| X | `@Kay2289123` | `2072025126141673905`；最后编辑 2026-07-01 02:31 | https://x.com/Kay2289123/status/2072025126141673905 | 方法补充 | 可见正文强调不使用杠杆/期权、行业理解和仓位纪律，并提示冒名账号 | 行业理解只能提高概率，不能保证预测 | `theme crowding`、`portfolio concentration` | 高：帖子事实；低：个人执行纪律自述 | 不作为账户交易或稳定规则；需用实际 replay 验证方法有效性 |
| X | `@Kay2289123` | `2072037810123809108`；2026-07-01 03:21 | https://x.com/Kay2289123/status/2072037810123809108 | 原帖+第三方引用 | 引用 Blackwell/DeepSeek V4 软件优化和 Token 成本下降说法 | Token 越便宜，总需求可能越大 | `AI_quality/capex_cycle`、`replay/backtest plan` | 高：Kay 帖；中：第三方性能说法 | NVIDIA 原始基准、并发/延迟/功耗、实际客户成本与需求弹性 |
| X | `@Kay2289123` | `2072113252377694350`；2026-07-01 08:21 | https://x.com/Kay2289123/status/2072113252377694350 | 长文跟帖/路线摘要 | 将内存墙拆为容量与搬运，列出 HBF/SNDK、PIM/PNM、Optical HBM、3D stacking、CXL、预测分层和 SRAM | 多条路线互补而非互斥，SNDK 是其中一条替代路径 | `AI bottleneck watch`、`AI_quality/capex_cycle` | 高：帖子正文/ID/时间；产业映射中等 | 标准成熟度、客户认证、量产时间、可靠性、TCO、收入和毛利 |
| X | `@Kay2289123` | `2072148482916577703`；2026-07-01 10:41 | https://x.com/Kay2289123/status/2072148482916577703 | 原帖+旧长文引用 | 指向前述文章并强调 SNDK 路线 | SNDK 是关键替代路径 | `theme crowding`、`AI bottleneck watch` | 高：帖子事实；低至中：公司传导 | SNDK HBF/3D NAND 客户认证、capex、良率、量产和收入 |
| X | `@Kay2289123` | `2072359344705085763`；2026-07-02 00:39 | https://x.com/Kay2289123/status/2072359344705085763 | 原帖+2图 | 可见完整六段正文，反驳“Meta 卖算力=AI 全链过剩”，区分 neocloud 竞争与设备/互连/存储物理需求 | 更可能是局部供需错配而非结构性过剩 | `flow_fragility`、`AI_quality/capex_cycle`、`AI bottleneck watch` | 高：帖子正文；中低：引用数字和因果判断 | Bloomberg/Reuters 原文、Meta capex/合同原始披露、区域/代际利用率、租赁价格和下游实际订单 |
| X | `@Kay2289123` | `2072364009341464877`；最后编辑 2026-07-02 00:57 | https://x.com/Kay2289123/status/2072364009341464877 | 补充帖 | 引述 Meta 股东会说法，并称 Meta 一边租入、一边出租自有算力 | 算力紧缺和局部转售可同时存在；宏观数据仍是短期风险 | `factor_macro_exposure`、`flow_fragility` | 高：帖子存在/正文；低：朋友交流与机构获利解释 | Meta 官方纪要、租入/出租合同、利用率；“机构获利了结”不可验证 |
| X | `@nvidia` | `2072069361792413878`；2026-07-01 05:26 | https://x.com/NVIDIAAI/status/2072069361792413878 | NVIDIA 转发关联官方帖 | `@NVIDIAAI` 宣传可复用的 Generative Pretrained Controllers 运动控制研究 | 运动技能可 token 化并预训练复用 | `AI_quality/capex_cycle`、physical-AI watch | 中高：关联官方原帖；商业传导低 | 论文、基准、硬件、产品化、客户和收入 |
| X | `@nvidia` | `2072305047216521247`、`2072305070729748596`、`2072305076027179102`；2026-07-01 21:03 | https://x.com/nvidia/status/2072305047216521247 | 官方线程 | 以“AI 五层蛋糕”叙述美国新产业、生产率和就业，并链接 NVIDIA 页面 | AI 基建将推动美国再工业化 | `factor_macro_exposure`、AI domestic-capex watch | 高：官方帖；经济/收入传导低 | 五层定义、订单/合同、产能、生产率和就业统计 |
| X | `@elonmusk` | `2072034905299563005`；2026-07-01 03:09 | https://x.com/elonmusk/status/2072034905299563005 | 原帖+Neuralink 引用 | 声称 Neuralink 已实现穿硬脑膜电极植入，并强调安全性/操作简化 | 将其视为重大临床工程进展 | physical-AI/healthcare watch、`AI_quality/capex_cycle` | 高：公开声明；临床有效性中低 | 试验注册、样本、并发症、监管、商业化和财务贡献 |
| X 转发 | `@elonmusk` | `2072364825607569528`、`2072315431881453800`；2026-07-01 21:44 至 2026-07-02 01:00 | https://x.com/XFreeze/status/2072315431881453800 | 第三方/州长帖子被转发 | 可见 xAI Memphis 投资叙事和 Grok Voice Agent Builder beta 功能宣传 | 强调本地投资与低门槛语音 Agent | xAI capex watch、application/developer-tool watch | 中：转发/第三方可见；产品和投资数字未独立核验 | xAI 官方投资、用电/数据中心进度、产品文档、付费采用和收入 |

## 小红书逐图核验状态

- 主页：可读；置顶仍是旧介绍/MRVL，非置顶网格未显示新笔记。
- Cerebras 详情：本轮首次读取时标题、正文、作者评论和 `26/26` 可见，页面随后因访问令牌失效返回 `300031 当前笔记暂时无法浏览`。
- 图片计数：总数 `26`；本轮编辑后逐图重新读取 `0/26`；历史累计已读取 `24/26`，历史未读 `2/26`。由于文章明确发生编辑，不能假定历史图片与编辑后版本完全一致。
- 证据等级：页面存在/正文/作者评论为高；相对编辑时间为中；编辑后轮播为低，当前需用户在现有 Chrome 中重新打开该笔记后才能补齐。

## 机构研究核验

检查器命令：`institutional-research-checker.js --since 2026-06-30T15:50:24.313Z --max-items 8`。首次运行在 124 秒时超时且未写文件；重跑完成后已读取 `institutional-research-latest.md` 与 `.json`。

| 机构 | 列表页 | 详情页状态 | 窗口新增 | 结论 |
| --- | --- | --- | ---: | --- |
| AQR | 可读 | 8 个官方详情可读；稳定日期均早于窗口 | 0 | 不新增 `trend_aligned_entry` 框架 |
| Citadel Securities | 可读 | 5 个稳定日期详情可读；`1H 2026 Market Structure & Flows` 时间为 `2026-06-30T15:44:47Z`，比 cutoff 早 5 分 37 秒；3 个分类页日期不可验证 | 0 | 来源可用；不把近 cutoff 的旧文或分类页算新增 |
| GMO | 可读 | 7 个官方详情可读且早于窗口；`Diversifying Beyond 60/40...` 仅列表候选/详情未读成功 | 0 | 列表候选不提炼新框架 |
| Man Institute | 可读 | 8 个官方详情可读；7 月 1 日文章标题、日期和正文稳定 | 1 | 新增实验性 `AI_credit_funding_fragility` 框架 |

### Man 新框架：AI 债券融资脆弱性

- 官方文章：`The Hard Questions for AI Bonds Investors`，2026-07-01，https://www.man.com/insights/views-from-the-floor-2026-1-july 。
- 公开事实：文章区分有现金流业务支撑的综合发行人与没有等价 backstop 的 AI 纯标的；讨论 AI/超大规模云债券供给、长久期债券对建设/执行风险更敏感，以及大规模发行可能通过 substitution effect 推高信用补偿。
- 作者观点：股权投资者获得 AI 上行期权，债券投资者以固定票息承担建设延迟、成本超支、竞争和长期需求不确定性；大市值不应自动等同低信用风险。
- 我的策略映射：增加 `cashflow_backstop_separation`、`AI_credit_supply_pressure`、`credit_duration_mismatch` 三个实验字段；用于 `flow_fragility`、`factor_macro_exposure` 和 `AI_quality/capex_cycle`，不构成做空或卖出信号。
- 证据：高（官方域名详情页标题、日期、正文稳定）；策略传导为中，需要信用利差、发行规模、公司现金流和历史 replay 验证。

## 策略映射

- `market fear gate`：本轮来源监控没有完整刷新 VIX、期限结构、宽度、信用和正式收盘，不改变最近正式门槛。Kay 帖所称“市场等宏观数据”只是来源观点。
- `trend_aligned_entry`：设备/互连/存储的来源论点不能替代日 K、相对强度和回撤质量；7 月 1 日相关股票大幅下跌更要求先做价格确认。
- `flow_fragility`：同一来源反复展示 40%/170% 自述收益、重仓和“互连三强”会放大追涨注意力；Meta 传闻引发全链同步下跌也显示叙事驱动的相关性冲击。
- `AI_quality/capex_cycle`：新增 `localized_capacity_mismatch` 与 Man 的 `cashflow_backstop_separation`；区分局部闲置、结构性需求、capex 交付和现金流支撑。
- `factor_macro_exposure`：AI 债券供给、长久期信用、宏观数据和本土工业政策是新增风险维度，但没有当前利差/利率数据，暂不量化方向。
- `AI bottleneck watch`：继续分开测量容量、搬运、互连、存储层级与设备扩产；不能把 Meta 算力转售直接外推成设备/光互连/存储需求结论。
- `theme crowding`：互连、设备、内存替代三组内容均使用大涨/重仓叙事，主题温度高；注意力证据不等于基本面证据。
- `portfolio concentration`：现有 GLW/MXL/DRAM/MU 与 AMAT/KLAC/LRCX/ALAB/CRDO/MRVL 候选仍共享 AI-capex/半导体周期冲击，按 ticker 数量不能视为分散。
- `replay/backtest plan`：记录 Meta 传闻、Kay 反驳、设备 capex 帖和 Man AI 债券文章事件日；比较 1/5/20/60 日相对 QQQ/SMH/XSD/HYG/LQD 变化、最大不利波动、成交量和信用利差。

## 数据缺口与需要用户确认的来源访问问题

1. 小红书旧 Cerebras 笔记发生编辑，但本轮重新打开时返回 `300031 当前笔记暂时无法浏览`；需要用户在已登录 Chrome 中手动重新打开该笔记一次，后续才能补读编辑后 `26/26` 图片。无需提供密码、cookie 或其他隐私信息。
2. Cerebras 轮播历史累计已读 `24/26`，仍有 2 张原图缺口；本轮无法确认编辑是否改动图片。
3. Kay 对 Meta 朋友交流、租入/出租算力、作者持仓和收益均为自述，不能当作独立事实或真实成交。
4. NVIDIA/Elon 的若干转发是关联官方或第三方内容，需回到论文、产品文档、监管/临床和公司财务披露核验。
5. Trump 可见时间线停留在 6 月 21 日，只能说明 X 当前可见页无窗口项目，不能证明其他平台没有新声明。
6. Man 文章的策略传导缺少当前信用利差、发行定价和公司级偿债数据；本轮只建立监控字段。

## 后续开盘准备重点读取

1. `memory/daily/2026-07-02-realtime-public-institutional-monitor.md`（本文件）
2. `memory/daily/2026-07-02-details.md`
3. `memory/trades/2026-07-02-trade-plan.md`
4. `memory/portfolio/2026-07-02-portfolio-summary.md`
5. `memory/todos/2026-07-02-strategy-todos.md`
6. 最近正式 `memory/daily/*-post-close-audit.md`
7. `references/daily-market-monitoring-framework.md`
8. `references/institutional-market-research-framework.md`
9. `references/ai-quality-capex-cycle-classification.md`
10. `work/institutional-research-latest.md` 与 `work/institutional-research-latest.json`

## 记忆处置

- 已更新 realtime tracker、H5/H8 假设、机构研究框架和 daily summaries。
- `decisions.md` 不变：本轮新增均为单日公开来源或单篇机构观点，没有历史 replay 或反复验证支持升级为稳定规则。
