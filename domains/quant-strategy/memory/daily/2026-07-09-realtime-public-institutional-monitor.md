# 2026-07-09 实时公开来源与机构研究监控

运行时间：2026-07-09 03:20 Asia/Shanghai。  
严格窗口：`2026-07-07T12:31:24.086Z` 至本次运行。起点来自自动化消息中的 last run；`references/realtime-public-source-tracker.md` 最近完整记录停在 2026-07-07 20:39 Beijing，二者基本衔接。  
本报告只做公开信息核验、证据分级、策略映射和记忆同步；不生成直接买卖建议，不登录券商，不提交订单，不记录或推断未确认真实成交。

## 方法与访问边界

- 已读取根 `README.md`、memory architecture、quant-strategy summary/decisions/hypotheses/daily-summaries、最近 daily、指定 references 和 tools README。
- Chrome 只读读取公开可见页面：小红书 `美研芒格君 / Kay2289123` 主页、X `@Kay2289123`、`@nvidia`、`@elonmusk`、`@realDonaldTrump`。未读取 cookies、密码、本地存储、私信、通知、账号设置；未关注、点赞、评论、转发或发帖。
- 按要求运行并读取机构检查器：
  `node D:\code\AI-Memory\domains\quant-strategy\tools\institutional-research-checker.js --since 2026-07-07T12:31:24.086Z --max-items 8 --out D:\code\AI-Memory\domains\quant-strategy\work\institutional-research-latest.md`
- 因小红书详情页回流到 explore、X Jina 通道为空，额外运行 `realtime-public-source-checker.js` 作为降级诊断；脚本结果只作为低到中证据，不覆盖 Chrome 可见内容。

## 结论摘要

### 公开事实

1. 小红书主页可见：账号 `美研芒格君`，小红书号 `Kay2289123`，前两篇仍为置顶笔记；最新非置顶仍是旧笔记 `存储之后的下个机会，聪明人已经开始关注`，ID `6a45e9690000000016027e78`。主页未显示严格窗口内新笔记。直接打开该旧笔记本轮回流到 explore，未能复核正文、作者评论或轮播图。
2. X `@Kay2289123` 严格窗口内可见新增多条帖子：OpenAI/GPT 5.6 token 消耗推断、MRVL 单日大跌后的基本面复盘、DeepSeek 自研芯片与定制算力、作者自述现金/持仓纪律、以及 07/07 AI 硬件恐慌链条拆解。作者自述收益、持仓、买卖点和线下分享均不记录为确认成交。
3. X `@nvidia` 可见官方窗口内帖子：LangChain/NemoClaw deep agents blueprint、SIGGRAPH 2026 AI in Production Day、AI 医疗知识普及案例、NVIDIA Vera CPU/agentic AI CPU 瓶颈。均为官方生态/产品叙事，高证据用于“帖子存在和可见正文”，但不是订单、收入、毛利或利用率证据。
4. X `@elonmusk` 可见窗口内 xAI/Grok 4.5 相关发布与转发，强调 coding/agents、速度、token efficiency、成本和 Cursor/Vercel 接入。策略相关性限于 AI 应用层与推理需求观察；未验证付费用户、token 成本、推理毛利或算力采购。
5. X `@realDonaldTrump` 主页最新可见仍为 2026-07-05 白宫活动置顶和 2026-07-02 视频；没有严格窗口内可读政策正文，因此不提炼关税、财政、产业政策或地缘风险新框架。
6. AQR、Citadel Securities、GMO、Man Institute 本轮机构检查器均为 `post-window verified = 0`。列表页与多数详情页可读或日期可过滤；不能写为官网不可用。没有 official-domain detail page 在窗口内同时具备稳定标题、日期和正文，因此不新增机构框架。

### 我的推断

- Kay 的新帖把 AI-capex 争议从“是否过剩”进一步拆成 `token_intensity_from_better_models`、`custom_compute_co_design`、`AI_hardware_deleveraging_chain` 和 `MRVL_valuation_path_compression`。这些是候选监控字段，不是买入信号。
- OpenAI/GPT 5.6 与 Grok 4.5 的可见叙事共同指向“更强模型可能带来更长推理链、更高工具调用、更低单位成本和更多 agent 工作流”，但需要官方产品页、真实使用量、付费转化、token 成本和云端部署位置验证。
- NVIDIA 的 LangChain/NemoClaw、Vera CPU 与 AI 医疗/创意生产帖强化 `agentic_AI_inference_stack` 与 `CPU_GPU_utilization_bottleneck` 观察，但没有足够证据提高任何单一 ticker 的质量分或核心角色。
- MRVL/ALAB/CRDO/MU/DRAM/GLW/MXL 等仍属于同一 AI-capex/半导体/存储/互联共同因子；Kay 的“逢恐慌找错误逻辑”观点只能进入 replay 与 crowding，不解除实际账户 unresolved-stop veto。

### 未核验证据

- Kay 对 OpenAI GPT 5.6 “内测体验”、MRVL 官方公告/指引、DeepSeek 自研芯片、Meta compute、Samsung/Micron 读法、个人持仓和收益的描述均需原始来源或公司文件复核。
- 小红书旧笔记 `6a45e9690000000016027e78` 本轮图片读取为 `0/32`；总图数沿用历史记录 `32`，未读缺口 `32`。历史 2026-07-02 `32/32` 图像证据不被本轮覆盖。
- `@realDonaldTrump` 视频内容未分析；不能从视频卡片或空正文推断政策方向。

## 已核验公开源项目

| 平台/来源 | 账号或机构 | ID / 时间 | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 | 美研芒格君 / Kay2289123 | `6a45e9690000000016027e78`，旧最新非置顶 | https://www.xiaohongshu.com/explore/6a45e9690000000016027e78 | 主页复核 | 主页仍显示该旧笔记为最新非置顶；置顶两篇仍在前列；未见窗口内新笔记 | 存储之后继续关注新 AI 瓶颈 | 保留旧 `memory_standard_power_shift` 字段；不新增 | 中：主页可见；低：详情/图片本轮失败 | 正文、评论、编辑时间、`32/32` 图片重新逐张核验 |
| X | `@Kay2289123` | `2074755111679877351` / `2026-07-08T07:19:00Z` | https://x.com/Kay2289123/status/2074755111679877351 | 帖子 / quote OpenAI | 可见正文称 GPT 5.6 更长推理链、更多工具调用、更多 token 消耗；引用 OpenAI 发布预告 | 更强模型可能带来企业利润与数据中心/AI factory token 消耗催化 | `token_intensity_from_better_models`、AI factory watch | 高：页面 ID/时间/正文可见；中低：产品和部署传导 | OpenAI 原帖/产品页、发布时间、部署厂商、企业付费和 token 用量 |
| X | `@Kay2289123` | `2074583043361386771` / `2026-07-07T19:55:16Z` | https://x.com/Kay2289123/status/2074583043361386771 | MRVL 长帖 | 讨论 MRVL 单日跌超 9%、高位回撤、公司公告、CFO 交接时重申 Q2 指引、AI 硬件链去风险 | 认为公司路径未变，市场从远期叙事转向下季收入/毛利验证 | `MRVL_valuation_path_compression`、`AI_hardware_deleveraging_chain` | 高：帖子可见；中低：公告解读需核对 | MRVL 官网公告、Q2 guidance、订单/客户/毛利证据 |
| X | `@Kay2289123` | `2074541184098398705` / `2026-07-07T17:08:56Z` | https://x.com/Kay2289123/status/2074541184098398705 | 帖子 / quote Reuters | 引用 Reuters 关于 DeepSeek 自研 AI 芯片的报道；作者认为 token 需求、定制算力和 co-design 仍在增加 | 定制芯片“铲子”可能有机会 | `custom_compute_co_design`、`AI bottleneck watch` | 高：X 帖可见；中：Reuters quote 可见；传导中低 | Reuters 原文、DeepSeek/供应商官方确认、工艺/存储/互联需求 |
| X | `@Kay2289123` | `2074538840405246067` / `2026-07-07T16:59:37Z` | https://x.com/Kay2289123/status/2074538840405246067 | 自述持仓/纪律帖 | 作者自述 MRVL/MU 多年投资、约 40% 现金、近期利用逻辑错误加仓/快进快出 | 强调耐心、现金和产业理解；减少公开买点 | 只进入 `theme crowding` 和行为观察；不记录为成交 | 高：页面可见；低：持仓/收益自述 | 不记录真实成交；需 broker 或第三方证据才可作为交易事实 |
| X | `@Kay2289123` | `2074528471225892956` / `2026-07-07T16:18:25Z` | https://x.com/Kay2289123/status/2074528471225892956 | 市场恐慌长帖 | 拆解 07/07 AI 硬件恐慌：Meta compute、Samsung/MU、SOX、MRVL/GLW/AMD/INTC 同步去风险 | 认为是拥挤 AI 硬件 trade 集中降杠杆，不是单公司基本面崩坏 | `AI_hardware_deleveraging_chain`、`flow_fragility`、replay | 高：页面可见；中低：市场因果链需数据验证 | 1/5/20/60 日 replay、成交量、SOXX/SMH/相关个股 MAE |
| X | `@nvidia` | `2074872091388903774` / `2026-07-08T15:03:50Z` | https://x.com/nvidia/status/2074872091388903774 | 官方帖 / LangChain quote | NVIDIA 与 LangChain 的 NemoClaw Deep Agents Blueprint，强调企业可控可定制 agent stack、性能和低推理成本 | 推广 open agent systems | `agentic_AI_inference_stack`、software efficiency watch | 高：官方页面可见；中低：商业传导 | NVIDIA/LangChain 博客、benchmark、客户部署、推理收入 |
| X | `@nvidia` | `2074584281662300649` / `2026-07-07T20:00:11Z` | https://x.com/nvidia/status/2074584281662300649 | 官方帖 | SIGGRAPH 2026 AI in Production Day，生成式/agentic AI 进入影视、动画、叙事和生产流程 | AI 创意生产生态推广 | AI application workflow watch | 高：官方页面可见；低到中：投资传导 | 会议信息、客户案例、软件收入/算力需求 |
| X | `@nvidia` | `2074554037509185674` / `2026-07-07T18:00:00Z` | https://x.com/nvidia/status/2074554037509185674 | 官方帖 | AI 医疗知识普及案例，称技术每年影响 2000 万生命 | AI for global healthcare | `AI_for_good_healthcare_access` | 高：官方页面可见；中低：商业传导 | 案例原文、部署规模、收入/合作方、GPU/云使用量 |
| X | `@nvidia` | `2074510027897844105` / `2026-07-07T15:05:07Z` | https://x.com/nvidia/status/2074510027897844105 | 官方帖 | NVIDIA Vera CPU，强调 agentic AI 顺序推理、工具调用和 CPU 瓶颈会影响 GPU 利用率 | CPU 单线程/规模化对 agentic loop 重要 | `CPU_GPU_utilization_bottleneck`、AI factory efficiency | 高：官方页面可见；中：产品传导需验证 | Vera benchmarks、OEM/云部署、GPU 利用率和收入影响 |
| X | `@elonmusk` | `2074740539874775163` / `2026-07-08T06:21:06Z` | https://x.com/elonmusk/status/2074740539874775163 | 原帖 | 称 Grok 4.5 将向公众开放，定位为更快、更 token-efficient、更低成本的 Opus-class 模型 | xAI 模型效率和成本竞争 | `xAI_agent_model_cost_efficiency` | 高：页面可见；中低：商业传导 | xAI 官方页、定价、使用量、推理成本、基础设施采购 |
| X | `@elonmusk` / SpaceXAI / Cursor / Vercel | `2074932046632267901` 等 / `2026-07-08T17:33-19:02Z` | https://x.com/elonmusk | 转发/短帖 | Grok 4.5 面向 coding/agents，Cursor/Vercel 接入，称速度和成本效率领先 | 强调 real-world usefulness 而非 benchmark | AI application monetization、agent coding workflow | 中高：profile 可见；部分为转发 | SpaceXAI/xAI 原文、Cursor/Vercel 产品页、付费使用和留存 |
| X | `@realDonaldTrump` | 无窗口内新政策正文 | https://x.com/realDonaldTrump | profile 复核 | 最新可见仍为 2026-07-05 白宫活动置顶和 2026-07-02 视频；窗口内无可读政策正文 | 无 | 不做宏观政策映射 | 中：profile 可见；低：政策正文不足 | 官方文字稿、白宫政策文件、关税/财政/产业政策正文 |
| 机构 | AQR / Citadel / GMO / Man | checker run `2026-07-08T19:08:17Z` | `work/institutional-research-latest.md/.json` | 本地 checker | 四家 `post-window verified=0`；AQR/Citadel/GMO/Man 列表页和多数详情页可读或日期过滤 | 无新框架 | 保留既有 overlays | 高：列表/详情状态；无新增 | 下一轮继续核对 official detail page 的标题/日期/正文 |

## 策略映射

- `market fear gate`：本次公开源监控不刷新 VIX/VIX3M、信用、宽度或正式收盘趋势。继续沿用 2026-07-07 post-close audit：Market Fear Gate `elevated 5/14`，真实账户 unresolved-stop veto 下实际新买入上限仍为 `0%`。
- `trend_aligned_entry`：Kay/NVIDIA/Elon 的叙事不能替代 20/50 日趋势、相对强度、回撤质量和已解决 stop 状态。当前 AI-capex sleeve 仍按 `trend_broken / risk-handle first` 处理。
- `flow_fragility`：Kay 7/7 恐慌链条与作者自述“40% cash / 利用逻辑错误”强化 crowding 行为证据；AI hardware 去杠杆链条进入 replay，不进入买入分数。
- `AI_quality/capex_cycle`：新增未验证字段 `token_intensity_from_better_models`、`custom_compute_co_design`、`MRVL_valuation_path_compression`、`agentic_AI_inference_stack`、`CPU_GPU_utilization_bottleneck`、`xAI_agent_model_cost_efficiency`。这些需要官方和财务/使用量数据验证。
- `factor_macro_exposure`：Trump 无新政策正文；NVIDIA/Elon/OpenAI 相关项偏产品/生态，不形成利率、关税、财政或地缘方向信号。
- `AI bottleneck watch`：继续拆分 token demand、custom silicon、memory/storage、interconnect、CPU bottleneck、agent workflow 和 AI factory deployment；不把“算力需求”单向映射到任何 ticker。
- `theme crowding`：MRVL/ALAB/CRDO/MU/DRAM/GLW/MXL/NVDA/AMD/INTC/半导体设备链仍共享 AI-capex 与半导体周期风险；ticker 增多不等于风险分散。
- `portfolio concentration`：不更改真实持仓记忆，不新增或推断任何成交。公开源仅辅助后续开盘前核验，不能解除 GLW/DRAM/MXL/MRVL unresolved-stop veto。
- `replay/backtest plan`：将 Kay `2074528471225892956`、`2074583043361386771`、`2074541184098398705`、NVIDIA `2074872091388903774`、`2074510027897844105`、Elon/Grok 4.5 相关项按 first-visible time 冻结，比较 1/5/20/60 日 QQQ/SMH/XSD/HYG/LQD、MRVL/ALAB/CRDO/MU/DRAM/GLW/MXL/NVDA/AMD/INTC/ORCL/CRWV/NBIS 的收益、成交量和最大不利波动。

## 机构研究核验结论

| 机构 | 列表页 | 详情页 | 窗口新增 | 结论 |
| --- | --- | --- | ---: | --- |
| AQR | 可读 | 8 个候选详情可读，稳定日期均早于窗口 | 0 | 无新 `trend_aligned_entry` 框架 |
| Citadel Securities | 可读 | `AI-merican Exceptionalism`、`Cruel Summer for Fixed Income` 等详情可读但均早于窗口；部分 archive/category 为 `date_unverified` | 0 | 不能标记不可用；无新 `flow_fragility` 框架 |
| GMO | 可读 | 多数详情可读；1 个 PE letter 详情失败但为旧候选 | 0 | 无新 `AI_quality/capex_cycle` 框架 |
| Man Institute | 可读 | 7 月 7 日 `Could 'Super El Nino' Scorch AI Too?` 的稳定日期为 `2026-07-06T16:00:00Z`，早于本窗口；其他均旧或 date_unverified | 0 | 无新 `factor_macro_exposure` 框架 |

`decisions.md` 不更新：本轮新增均为单日公开源、作者观点、官方生态/产品宣传或无窗口新增机构结果；没有历史 replay 或反复验证支持稳定规则升级。

## 数据缺口与需要用户确认的访问问题

1. 小红书详情页本轮回流 explore，无法读取 `6a45e9690000000016027e78` 正文/评论/编辑时间/轮播；当前已读图片 `0/32`，未读缺口 `32`。
2. X 页面使用 Chrome 可见文本和自动翻译；若需要精确中文原文，应逐条点 `Show original` 或保存单帖详情页后复核。
3. Kay 关于 OpenAI、DeepSeek、MRVL、Meta、Samsung/Micron、个人收益和买卖点的内容均未被独立确认。
4. Trump 仅有视频/活动卡片，没有窗口内可读政策正文；不能用于政策映射。
5. 机构源虽可读，但没有窗口内新 official-domain detail page；下一轮仍需继续区分列表页可读、详情页可读、详情页被挡、仅列表候选、日期不可验证。

## 后续开盘准备重点读取

1. `memory/daily/2026-07-07-post-close-audit.md`
2. `memory/daily/2026-07-09-realtime-public-institutional-monitor.md`
3. `memory/daily/2026-07-07-details.md`
4. `memory/portfolio/2026-07-07-portfolio-summary.md`
5. `memory/todos/2026-07-07-strategy-todos.md`
6. `references/realtime-public-source-tracker.md`
7. `references/institutional-market-research-framework.md`
8. `references/institutional-overlays-daily-checklist.md`
9. `references/ai-quality-capex-cycle-classification.md`
10. `work/realtime-public-source-latest.md`、`work/realtime-public-source-latest.json`、`work/institutional-research-latest.md`、`work/institutional-research-latest.json`
---

## 2026-07-09 20:40 Asia/Shanghai rerun

本段是同日增量复核。严格窗口采用自动化消息给出的 last run：`2026-07-08T19:03:32.307Z` 至 `2026-07-09T12:40:17.691Z`。本轮只做公开信息核验、证据分级、策略映射和记忆同步；不生成直接买卖建议，不登录券商，不提交订单，不记录或推断未确认真实成交。

### 访问方法与边界

- 已按任务要求重新读取根 README、memory architecture、quant-strategy summary / decisions / hypotheses / daily-summaries、最近 daily、指定 references 和 tools README。
- 尝试使用已登录 Chrome 读取小红书主页；页面连续两次在读取层超时，未读取 cookies、密码、本地存储、私信、通知或账号设置，也未关注、点赞、评论、转发或发帖。该结果记录为访问缺口，不等同于来源不可用。
- 按要求运行机构检查器：`node D:\code\AI-Memory\domains\quant-strategy\tools\institutional-research-checker.js --since 2026-07-08T19:03:32.307Z --max-items 8 --out D:\code\AI-Memory\domains\quant-strategy\work\institutional-research-latest.md`。第一次 120 秒超时，第二次 300 秒窗口成功写出 Markdown 和 JSON。
- 因 Chrome/X 公开页未能稳定读取时间线，运行 `realtime-public-source-checker.js` 作为降级诊断。脚本结果中 X Jina profile 均为空；小红书仅暴露标题候选、无稳定 URL/时间/正文，因此只按低到中证据处理，不覆盖此前 Chrome 可见内容。

### 公开事实

1. 小红书账号 `美研芒格君 / Kay2289123`：降级 checker 的 raw HTML/SSR 暴露 20 条可见标题候选；前两条仍为置顶样式，第三条仍是旧的“存储之后的下一个机会...”标题。没有稳定单篇 URL、发布时间、正文、作者评论或图片可读证据。本轮图片读取为 `0/未知总数`；历史 `6a45e9690000000016027e78` 的 `32/32` 图片证据不被本轮覆盖。
2. X `@Kay2289123`：本轮没有取得严格窗口内可采信新 status。Chrome 读取未完成，X 公开直接页为空，Jina profile 为空；不得复用上轮已记录的 2026-07-07/08 status 当作本轮新证据。
3. X `@nvidia`、`@elonmusk`、`@realDonaldTrump`：Jina profile 均返回 `ok=true` 但 `length=0`；公开直接页也没有正文行可读。本轮没有新增可验证 status ID、发布时间和正文摘要。
4. AQR、Citadel Securities、GMO、Man Institute：机构检查器在精确窗口内均为 `post-window verified = 0`，每家检查 8 个候选。列表页可读，多个详情页可读或日期可过滤；这不是“来源不可用”。没有窗口内同时具备 official-domain 稳定标题、日期和正文的新详情页，因此不提炼新机构框架。

### 我的推断

- 本轮公开社媒信息质量低于 2026-07-09 03:20 监控：没有新的中高证据 X status 或小红书详情页。策略层面只能写“无新增 verified event”，不能新增候选字段或覆盖 H5/H6/H8。
- 小红书 raw HTML 标题候选显示主题热度仍集中在 AI 主线、MRVL、存储、光互联、ORCL token factory、AVGO、ALAB、CBRS、NBIS/CRWV 等，但因缺少时间、URL 和正文，只能作为低到中证据的主题温度观察。
- 机构研究源的最新可读候选仍落在窗口前：AQR 最新列表项为 2026-05/03 及更早；Citadel 最新候选包括 2026-07-05 `AI-merican Exceptionalism` 但早于本窗口；GMO 最新候选为 2026-06-12；Man 最新候选为 2026-07-07 且早于本窗口。没有稳定新框架。

### 未核验证据

- 小红书标题候选没有正文、发布时间、单篇 URL、作者评论和轮播图，不能作为完整 source item。
- X 四个账号没有本轮可读 status 详情；不能推断“无发帖”，只能记录“本轮访问通道未取得可采信新内容”。
- 机构检查器输出存在部分中文编码显示问题，但 JSON 字段、URL、日期状态和 `post-window verified` 计数可读；结论以 JSON/Markdown 结构字段为准。

### Verified source item table

本轮严格窗口内没有新的中高证据 verified social source item。低到中证据项目如下：

| 平台/来源 | 账号或机构 | ID/时间 | 链接 | 类型 | 事实摘要 | 作者观点 | 策略推断 | 证据强度 | 待验证事项 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 小红书 raw HTML/SSR | 美研芒格君 / Kay2289123 | 无稳定单篇时间 | `https://www.xiaohongshu.com/user/profile/632ea1e700000000230381cb` | 主页标题候选 | 暴露 20 条标题候选，无法确认窗口内新发；第三条仍类似旧“存储之后的下一个机会...”主题 | 不提炼 | 仅做 AI-capex / optical / memory / cloud-factory 主题温度观察 | 低到中 | 单篇 URL、发布时间、正文、评论、轮播图 |
| X | @Kay2289123 | 无 | `https://x.com/Kay2289123` | profile/checker 访问 | 本轮未取得可读 status 详情 | 无 | 不新增事件 | 低 | 已登录 Chrome 时间线或单帖详情 |
| X | @nvidia | 无 | `https://x.com/nvidia` | profile/checker 访问 | Jina profile 为空，直接公开页无正文行 | 无 | 不新增官方产品/生态事件 | 低 | Chrome 可见 profile 或单帖详情 |
| X | @elonmusk | 无 | `https://x.com/elonmusk` | profile/checker 访问 | Jina profile 为空，直接公开页无正文行 | 无 | 不新增 xAI/Tesla/SpaceX 事件 | 低 | Chrome 可见 profile 或单帖详情 |
| X | @realDonaldTrump | 无 | `https://x.com/realDonaldTrump` | profile/checker 访问 | Jina profile 为空，直接公开页无正文行 | 无 | 不新增政策映射 | 低 | 可读政策正文或官方文本稿 |
| 机构 | AQR / Citadel / GMO / Man | checker run `2026-07-09T12:40:17.691Z` | `work/institutional-research-latest.md/.json` | official-domain checker | 四家 `post-window verified=0`；列表页和多数详情页可读/可日期过滤 | 无新框架 | 保留既有 overlays | 高：来源状态；无新增：框架 | 下轮继续核对 official detail page 的标题/日期/正文 |

### 策略映射

- `market fear gate`：本轮 source monitor 不刷新价格或 VIX，沿用 2026-07-08 post-close audit 的 `elevated 5/14` 与真实账户 `unresolved-stop veto`。公开来源没有解除新买入上限 `0%` 的证据。
- `trend_aligned_entry`：没有新的 price-confirmed catalyst；AI-capex sleeve 仍按 `trend_broken / risk-handle first` 处理。
- `flow_fragility`：没有新增 Citadel post-window 框架；沿用已有 `acute` 风险语境。小红书低证据标题只能提示主题热度仍集中，不能提高或降低分数。
- `AI_quality/capex_cycle`：没有新增 official-domain 详情页或公司事实；不新增质量分、核心角色或 capex-cycle 字段。
- `factor_macro_exposure`：Trump/X 无新政策正文；机构源无新宏观框架。维持既有 growth-duration、AI-capex-cycle 和 theme-overlap 风险标签。
- `AI bottleneck watch`：继续跟踪 optical/interconnect、memory/storage、cloud-factory、custom silicon、agentic inference，但本轮无新 verified event。
- `theme crowding`：低证据标题候选仍偏 AI 硬件/光互联/存储/云工厂，支持“主题拥挤需观察”，不支持买卖或规则升级。
- `portfolio concentration`：不改变真实持仓记忆，不记录任何成交；GLW/DRAM/MXL/MRVL stop closure 和 XLI 状态仍需用户/券商确认。
- `replay/backtest plan`：本轮无新增高证据事件行；后续 replay 应优先冻结前一轮 2026-07-07/08 已验证 Kay/NVIDIA/Elon rows，而不是把本轮低证据标题候选加入事件表。

### 机构研究核验结论

| 机构 | 列表页 | 详情页 | 窗口新增 | 结论 |
| --- | --- | --- | ---: | --- |
| AQR | 可读 | 8 个候选详情可读，均早于窗口 | 0 | 无新 `trend_aligned_entry` 框架 |
| Citadel Securities | 可读 | 2026-07-05、07-01、06-30 等详情可读但均早于窗口；若干 archive/category 日期不可验证 | 0 | 来源可读但无新 `flow_fragility` 框架 |
| GMO | 可读 | 8 个候选详情可读，最新为 2026-06-12，均早于窗口 | 0 | 无新 `AI_quality/capex_cycle` 框架 |
| Man Institute | 可读 | 2026-07-07、07-01 等详情可读但均早于窗口；一项 date_unverified | 0 | 无新 `factor_macro_exposure` 框架 |

`decisions.md` 不更新：本轮没有历史 replay、反复验证或稳定规则证据。

### 数据缺口与用户确认

1. Chrome 读取小红书主页连续超时，详情页和轮播图未复核；本轮图片证据为 `0/未知总数`。
2. X 四个账号本轮没有可读时间线或 status 详情；需要用户确认已登录 Chrome 的 X 页面是否可正常手动打开。
3. 小红书 raw HTML 标题候选存在编码问题且缺少单篇 URL/时间/正文，不可作为高证据事件。
4. 机构检查器已成功，但部分中文说明编码异常；后续如要做机构周报，建议直接读取 JSON 的结构字段和官方详情 URL。

### 后续开盘准备重点读取

1. `memory/daily/2026-07-08-post-close-audit.md`
2. `memory/daily/2026-07-09-realtime-public-institutional-monitor.md`
3. `memory/portfolio/2026-07-08-portfolio-summary.md`
4. `memory/todos/2026-07-08-strategy-todos.md`
5. `references/realtime-public-source-tracker.md`
6. `references/institutional-overlays-daily-checklist.md`
7. `references/ai-quality-capex-cycle-classification.md`
8. `work/realtime-public-source-latest.md` / `.json`
9. `work/institutional-research-latest.md` / `.json`

