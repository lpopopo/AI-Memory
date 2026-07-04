#!/usr/bin/env python3
"""Build extracted-batch-1.json from browser-extracted post data."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
queue = json.loads((BASE / "fetch-queue.json").read_text())

# Extracted post data from browser CDP (noteId -> fields)
POSTS = {}

POSTS["6a1691ba000000003601bcf5"] = {
    "noteId": "6a1691ba000000003601bcf5",
    "title": "美光科技供应链深度挖掘, 下个产业机会流向",
    "desc": "我们是来自美国硅谷的行业投研团队，成员来自斯坦福大学沃顿商学院，最近5天没发帖子，跟大家说句抱歉，团队成员心里有点小小失望，我们一直认真写帖子、用心写分享，坚持不误导、不知识收费（承诺了），但还是下掉不许分发，不需申诉\n\t\n《AMAT》《ASE白月光》《SNDK 供应链挖掘》《MRVL TPU8i 推理》《ANET》写好都没有发，担心审核员看得不舒服，担心写完也没人看到，担心认真排好的版被直接撤掉\n\t\n这次分享我们团队这半年来的深度分享，我们一直关注 HBM，但我们更关注 HBM 的上下游产业。如果不理解这句话什么意思，建议看看我们"三层思维框架"之前的帖子。\n\t\n道理很简单，不论是美光还是闪迪，上行趋势确实很明显，但是良率落地其实还没有跟上。下阶段需要做的是将良率搞上去，越高越好。这离不开它制造的锤子、钉子、水泥\n\t\n别怕这一长串代号，大家都退步了，就是你的机会\nASML、AMAT、LRCX、KLAC、\nHanmi、KLIC、FORM、TER、Advantest、\nTripod、Murata、Resonac、\nAMKR、ASX、\nUnimicron、Kinsus、Nan Ya、AT&S，\n\t\n要让 HBM 上最细的图案被印出来 ASML；\n制作工艺中的19 个材料工程的机器 AMAT；\n要让晶圆上的洞和膜雕到原子级 LRCX；\n要让坏砖在堆塔前就被挑出来 KLAC。\n\t\n要让 12 层 DRAM 精准压成千层塔，靠 Hanmi\n要让每颗 HBM 像答考卷一样被秒级筛过，靠 FORM；\n要让 GPU 大脑通过最严的判卷，靠 TER 和 Advantest。\n\t\n要让千层塔的胶水、水泥、绝缘膜不掉链子,，靠 Tripod、Murata、Resonac；\n要让 HBM 和 GPU 住进同一个封装大房间, 靠 TSM, AMKR 和 ASX；\n要让这颗 AI 大脑稳稳坐在地基上, 靠 Unimicron、Kinsus、Nan Ya、AT&S。\n\t\n而站在最中间收尾、就叫美光，MU。\n\t\n希望这篇文章对你有帮助，转发给朋友，让他别再只盯着美光了。也欢迎大家对文章点赞、收藏、友好评论，这是对我们的最大鼓励\n\t\n我们不懂投资，不懂股票，无法提出建议，投资需谨慎，我们只做行业的深度调研，下篇想看什么，你在关心什么？还有什么是我漏掉的？评论区交流分享，大家一起交流学习\n\t\n#战略性新兴产业 #多元化投资  #半导体  #AMA #TSM #MU",
    "tags": ["#战略性新兴产业", "#多元化投资", "#半导体", "#AMA", "#TSM", "#MU"],
    "carouselTotal": "23",
    "images": [
        "https://sns-webpic-qc.xhscdn.com/202607041551/93167fc8ee2b320256fc47169527c06d/spectrum/1040g0k0320lnf4klli405opek7jov0ebciqahjg!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/fcbc4f3311c230063d4ccdbe356827fe/spectrum/1040g0k0320lnf4g8lk005opek7jov0ebajdmj9o!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/033b8dd54426c0de7a094ee6e7ada125/spectrum/1040g0k0320lnf4g8lk0g5opek7jov0ebt8v9tc0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/2f06a4e00ae6d4e5abca68b01c6975dc/spectrum/1040g0k0320lnf4g8lk105opek7jov0eb5rgu1k8!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/94a7e9c839cffc4c487e104f01a48267/spectrum/1040g0k0320lnf4g8lk1g5opek7jov0eb3de175o!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/ecd8ad2ae703b05b0adc285c0892bf4a/spectrum/1040g0k0320lnf4g8lk205opek7jov0eb5qii5a8!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/81092a7f86aa6e79638078508bfb5f79/spectrum/1040g0k0320lnf4g8lk2g5opek7jov0eb8buiaho!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/8d5e84952bd8ac131aba1766106839b2/spectrum/1040g0k0320lnf4g8lk305opek7jov0eb59fu4o0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/4e31255743039763c4bd3a05f7a5d264/spectrum/1040g0k0320lnf4g8lk3g5opek7jov0eblndtquo!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/c9b9da08c8be973e982850fa673bb4b8/spectrum/1040g0k0320lnf4g8lk405opek7jov0ebvjog9eo!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/4bd11157fd18099a1dc9ddb72a696a85/spectrum/1040g0k0320lnf4g8lk4g5opek7jov0ebpvrdn20!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/b7e19629b58a32f99eb5782250a154fc/spectrum/1040g0k0320lnf4g8lk505opek7jov0eb2sei4o0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/cdfd8d7a7c230ecac4fb19aa1545a7c7/spectrum/1040g0k0320lnf4g8lk5g5opek7jov0eb0skik1o!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/cca3277cfbfae8834775549cbc74efec/spectrum/1040g0k0320lnf4g95k005opek7jov0ebc1tdtfo!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/d26d1f2bd9678c502826639a64d0865a/spectrum/1040g0k0320lnf4g95k0g5opek7jov0ebufca42g!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/41424bf72f2bb42844b68db5e4c65a08/spectrum/1040g0k0320lnf4klli005opek7jov0ebgd53cu0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/91ab2d06a9922f4372de138ed95a8202/spectrum/1040g0k0320lnf4klli0g5opek7jov0eb29ffl5o!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/881571abcd02975888cd45b35c6d34a0/spectrum/1040g0k0320lnf4klli105opek7jov0ebr0l5ec0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/aa883478e247eadc994c82bb005b4600/spectrum/1040g0k0320lnf4klli1g5opek7jov0eb14ge27g!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/42549f25fa981fcd0e949345614ea535/spectrum/1040g0k0320lnf4klli205opek7jov0ebp2732io!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/9b0fba6b214948b753e23255b0d55b78/spectrum/1040g0k0320lnf4klli2g5opek7jov0ebhf1ourg!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/0855e01bb8211b9ede446048c3020072/spectrum/1040g0k0320lnf4klli305opek7jov0ebispg8f8!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041551/c56eab8689542c3fd97c9ebb5d7a7100/spectrum/1040g0k0320lnf4klli3g5opek7jov0eb8735ad0!nd_dft_wlteh_webp_3",
    ],
}

# Load remaining posts from companion data file if present
_data_file = BASE / "_extracted_data.json"
if _data_file.exists():
    extra = json.loads(_data_file.read_text())
    POSTS.update(extra)

results = []
for q in queue[:10]:
    if q.get("skip"):
        continue
    nid = q["noteId"]
    if nid not in POSTS:
        raise KeyError(f"Missing extracted data for {nid}")
    post = dict(POSTS[nid])
    post["date"] = q["date"]
    post["url"] = q["url"]
    results.append(post)

out = BASE / "extracted-batch-1.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(results)} posts to {out.name}")
