#!/usr/bin/env python3
"""Merge a fetched post JSON into posts-data.json."""

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA = BASE / "posts-data.json"


def filter_images(urls):
    hi = [u for u in urls if "nd_dft_wlteh_webp" in u]
    return hi if hi else urls


def main():
    post = json.loads(sys.stdin.read())
    post["images"] = filter_images(post.get("images", []))
    data = json.loads(DATA.read_text(encoding="utf-8"))
    for i, p in enumerate(data["posts"]):
        if p["noteId"] == post["noteId"]:
            post.setdefault("publishedDate", p.get("publishedDate"))
            post.setdefault("position", p.get("position"))
            post["url"] = f"https://www.xiaohongshu.com/explore/{post['noteId']}"
            post.pop("status", None)
            data["posts"][i] = {**p, **post}
            break
    else:
        post["url"] = f"https://www.xiaohongshu.com/explore/{post['noteId']}"
        data["posts"].append(post)
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"merged {post['noteId'][:8]} images={len(post['images'])}")

if __name__ == "__main__":
    main()
