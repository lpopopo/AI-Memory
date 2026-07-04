#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

def p(note_id, title, desc, tags, carousel_total, images):
    return {
        "noteId": note_id,
        "title": title,
        "desc": desc,
        "tags": tags,
        "carouselTotal": carousel_total,
        "images": images,
    }

POSTS = {}

POSTS["6a0fa1bc000000003601f820"] = p(
    "6a0fa1bc000000003601f820",
    "深入解读, 为什么英伟达财报下跌是一份大礼",
    "们是来自美国硅谷的投研团队，团队成员来自于斯坦福大学、沃顿商学院\n\t\n5月20日，英伟达发布财报，盘后下跌 ～2%。我们深入研究了英伟达几十篇华尔街投行的研报、卖方报告、财报和电话会议逐字稿\n\t\n先说结论，长期来看，NVIDIA 的网络业务和 CPU 业务还没有在财报里的数字中完全体现。以年为维度来看，存在不少的上行空间\n\t\n审核员请注意，请仔细审核，这篇是行业分析，认真创作不易，不要再无端下架了 \n\t\n财报后 LITE+11%, COHR+5%, MRVL+3%, ALAB+4%, CRWV+6%,  英伟达早就不能单点来看了，要把它放到一个复杂的 AI 基础架构的知识图谱上来看，牵一发而动全身，他们的关系，我们已经在之前的文章中分析过。\n\t\n这次财报信息增量不少，除了 GPU 之外，网络服务同比增加了 199%，再联想起英伟达对 GLW、LITE、COHR、MRVL 的投资，你应该不会感到惊讶\n\t\n背后其实有个更大的叙事，不管是 GPU 还是自研推理芯片，英伟达的互联都能分上一杯羹。此外，英伟达推出Vera CPU 系列，专注 Agent 推理和 Token 成本，带给了英伟达整体营收可见度之外的纯增量\n\t\n我们惊讶地发现，在网络和 CPU 上，增量价值还没有被完全定价。华尔街只有在报表上看到了之后，才会真的计入市场的价格，形成群体共识，领先贪婪的机构半步，take risk是散户的优势\n\t\n英伟达并不会会一帆风顺，情绪、算法迭代、宏观经济，都会将英伟达挫伤。前途可能是波折的\n\t\n我们并不知道明天、下周的价格，我们只看年维度。本文仅仅作为行业分析，不唱票，不推荐，没有任何建议或者财经诱导。请审核员注意\n\t\n各位英伟达的股东们，你们怎么看？\n\t\n你觉得英伟达是一份被低估的大礼，还是完全 price in？欢迎在评论区留下你的观点想法？\n\t\n如果对你有帮助，欢迎点赞、收藏、评论、转发，一键三连是对我们最好的鼓励\n\t\n#howto投资 #光模块 #半导体 #NVDA #MRVL #ALAB #CRWV #金融投资 #投资需谨慎 #投资",
    ["#howto投资", "#光模块", "#半导体", "#NVDA", "#MRVL", "#ALAB", "#CRWV", "#金融投资", "#投资需谨慎", "#投资"],
    "20",
    [
        "https://sns-webpic-qc.xhscdn.com/202607041552/1ccff901925b4e16579c5ddf5db2e7c1/spectrum/1040g34o320eualqblk5g5opek7jov0ebrdesqh8!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/3296ecbebc276349060943d01efa1fef/spectrum/1040g0k0320eualndlk005opek7jov0eb3j5s8k8!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/4be17cff6c1306ccef024cc191c65f35/spectrum/1040g0k0320eualndlk0g5opek7jov0eb5jih9ag!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/5023b75f7d705bed72b6a700f91f02ed/spectrum/1040g0k0320eualndlk105opek7jov0ebr3erls8!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/3a66bcddb67af1a551ab4abec3c88aea/spectrum/1040g0k0320eualndlk1g5opek7jov0ebtoglfu0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/ec328157612185a848a12a72adfed7c0/spectrum/1040g0k0320eualndlk205opek7jov0eb4uq9hio!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/9749e64952f8bb590de8172ba2f10695/spectrum/1040g0k0320eualndlk2g5opek7jov0eb8bcl15g!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/650b4a21e72d44e7e063852c45a8e35a/spectrum/1040g0k0320eualndlk305opek7jov0eb7g9o4o0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/456c739ca54c55aa870cb476b1de869d/spectrum/1040g0k0320eualndlk3g5opek7jov0ebh0hmhug!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/5e7645df935476115c77229fa1026b6c/spectrum/1040g0k0320eualndlk405opek7jov0ebirhdcao!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/51e560be68ff21dd2908cc3a31fee5e5/spectrum/1040g0k0320eualndlk4g5opek7jov0ebpfq9up8!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/db1025bb97276df7bad169d23e560be8/spectrum/1040g0k0320eualndlk505opek7jov0eb3ba7n08!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/8719eefb012e7c67b243bc0d693f6a78/spectrum/1040g0k0320eualndlk5g5opek7jov0ebl9uqdmo!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/34bf6b3e821757ac923bf47677c3a7a3/spectrum/1040g0k0320eualndlk605opek7jov0ebhqa87c0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/ddea84e9dea07a245de7c2cc62e565cf/spectrum/1040g0k0320eualndlk6g5opek7jov0eb91vidjo!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/b30083464e65db21be898a38139dca52/spectrum/1040g34o320eualqblk305opek7jov0ebc07dis8!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/f9adb67065f7b903518db9ef623087b2/spectrum/1040g34o320eualqblk3g5opek7jov0eb8edr8q0!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/d723581c7e61e28cf5ba67a0a30e2430/spectrum/1040g34o320eualqblk405opek7jov0eb3cnjrpg!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/9eb93a2f271a14933469a884927e0b1c/spectrum/1040g34o320eualqblk4g5opek7jov0ebpjo0tng!nd_dft_wlteh_webp_3",
        "https://sns-webpic-qc.xhscdn.com/202607041552/055e62a74276dbef769efa44ce04cb3a/spectrum/1040g34o320eualqblk505opek7jov0ebjqbe4d0!nd_dft_wlteh_webp_3",
    ],
)

# Additional posts loaded from companion module
from posts_rest import POSTS_REST  # noqa: E402

POSTS.update(POSTS_REST)

(BASE / "_extracted_rest.json").write_text(json.dumps(POSTS, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(POSTS)} posts to _extracted_rest.json")
