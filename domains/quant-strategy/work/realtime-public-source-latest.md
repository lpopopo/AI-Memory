# Realtime Public Source Check

Run time: 2026-06-17T12:33:02.130Z (2026/06/17 20:33:02 Beijing)
Since: 2026-06-16T12:31:18.759Z (2026/06/16 20:31:18 Beijing)

## Summary

| Source | Status | New verified items | Dimension | Evidence | Note |
| --- | --- | ---: | --- | --- | --- |
| @nvidia | 未取得可采信新内容 | 0 | AI 算力/推理/产品路线 | 低 | 账号页可读，但没有抽取到可校验 status 链接；可能是 X 返回置顶/历史推荐或无链接摘要。 |
| @elonmusk | 未取得可采信新内容 | 0 | xAI/Tesla/SpaceX/AI 基建 | 低 | 账号页可读；已按 status 详情和 snowflake 时间筛选。 |
| @realDonaldTrump | 未取得可采信新内容 | 0 | 政策/关税/地缘风险 | 低 | 账号页可读；已按 status 详情和 snowflake 时间筛选。 |
| 美研芒格君 | visible_titles_raw_html_unverified_time | 0 | AI 产业链线索 | 低到中 | 原始公开 HTML/SSR 暴露可见笔记标题，但没有稳定单条笔记 URL、发布时间或正文；可用于主题温度和候选池，不可当作完整事实正文。 |

## @nvidia

账号页可读，但没有抽取到可校验 status 链接；可能是 X 返回置顶/历史推荐或无链接摘要。

Diagnostics:
- jina_profile: ok=true status=200 length=5062

## @elonmusk

账号页可读；已按 status 详情和 snowflake 时间筛选。

Diagnostics:
- jina_profile: ok=true status=200 length=3106
- jina_status id=1812258574049157405: ok=true status=200 length=2184
- jina_status id=1854026234339938528: ok=true status=200 length=2319
- jina_status id=1518677066325053441: ok=true status=200 length=2191
- jina_status id=1519495982723084290: ok=true status=200 length=2213
- jina_status id=1854201929519247803: ok=true status=200 length=2274

## @realDonaldTrump

账号页可读；已按 status 详情和 snowflake 时间筛选。

Diagnostics:
- jina_profile: ok=true status=200 length=8199
- jina_status id=2057968277062582378: ok=true status=200 length=2244
- jina_status id=2056827052851105947: ok=true status=200 length=2941
- jina_status id=2028505632123326484: ok=true status=200 length=0
- jina_status id=2027651077865157033: ok=true status=200 length=0
- jina_status id=2017417980594827718: ok=true status=200 length=0

## 美研芒格君

Visible title candidates without reliable time/body:
- [置顶] 40小时呕心沥血！MRVL光模块+AI推理布局解析
- [置顶] 一篇走心发文，为什么我们坚持做AI投资分享
- 深入拆解甲骨文, AI Token推理工厂的错配
- 耗时一周，深度拆解甲骨文ORCL的AI豪赌决心
- 好消息就是坏消息？从看懂AVGO到理解AI布局
- 迈威尔+50%, 不看懂怎么能安心？深入解读原
- MRVL? 一路恐高一路错过, 这次把握机会好吗
- 美光科技供应链深度挖掘, 下个产业机会流向
- 深入解读, 为什么英伟达财报下跌是一份大礼
- 深度拆解ALAB互联27年布局, 这次别踏空!
- 光模块存储板块狂热, 我们开始睡不好觉了！
- 诺基亚成光模块概念股？从无到有，最值钱
- CBRS+68%，下一个光模块？ 新机会深度解读
- NBIS CRWV深度解读，出现了难得的黄金坑？
- 27年的下个10倍投资机会，AI推理Token布局
- 光模块下投资还在早期，分享如何提前布局
- 耗时一周调研，带你彻底读懂 MRVL底层逻辑
- 光模块的投资才刚刚开始‼️现在入局还不晚
- 光模块下个机会？不是谁领先,而是相互看懂
- 从AAOI拆解光模块4层路线，下个标的是谁？

Diagnostics:
- raw_profile_html: ok=true status=200 length=833493
- jina_profile: ok=true status=200 length=0

Not investment advice.
