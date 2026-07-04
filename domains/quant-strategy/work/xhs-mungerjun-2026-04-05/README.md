# 美研芒格君 2026年4-5月帖子归档

博主: [美研芒格君](https://www.xiaohongshu.com/user/profile/632ea1e700000000230381cb)

## 范围

2026-04-01 ~ 2026-05-31，共 **31 篇**（见 `apr-may-manifest.json`）

## 目录结构

```
xhs-mungerjun-2026-04-05/
├── apr-may-manifest.json      # 31篇帖子清单+日期
├── fetch-queue.json           # 抓取队列（含 token 链接）
├── profile-urls-with-token.json
├── posts-data.json            # 全部帖子元数据
├── _fetch_progress.json       # 增量抓取进度（每篇抓取后更新）
├── download_posts.py          # 下载轮播图
├── merge_fetched.py           # 合并单篇抓取结果
├── merge_batch.py             # 合并批量抓取结果
└── xhs-{noteId前8位}/         # 每篇帖子目录
    ├── content.md
    ├── image-urls.json
    └── 01.webp ...
```

## 同步进度（2026-07-04 更新）

| 状态 | 数量 |
|------|------|
| 4–5 月总计 | 31 篇 |
| **已完整同步（正文+轮播图+本地 webp）** | **28 篇** |
| 仅有正文（无轮播图） | 3 篇 |
| 抓取失败 | 0 篇 |

### 无轮播图（3 篇，非抓取失败）

| noteId | 标题 | 原因 |
|--------|------|------|
| `69eed82d` | 200小时调研，光模块美股深度调研挖掘 | 视频帖，仅有正文 |
| `69f7d227` | 对不起，光模块LITE的分析我们团队尽力了 | 纯文字说明帖 |
| `6a082024` | 一篇走心发文，为什么我们坚持做AI投资分享 | 纯文字帖（正文引用图3/图5但无 spectrum 轮播） |

### 已完整同步（28 篇）

全部见 `download-summary.json`。含 Apr 28–May 29 共 28 篇图文帖，轮播图已下载至各 `xhs-{id}/` 目录。

## 使用方法

```bash
# 从 posts-data.json 下载/更新本地 content.md + webp
python3 download_posts.py

# 合并浏览器抓取的单篇 JSON（stdin）
python3 merge_fetched.py < post.json

# 合并 _batch_fetch.json 批量结果
python3 merge_batch.py
```

从博主主页**点击封面图**打开帖子后提取内容（避免直链触发安全限制）。
