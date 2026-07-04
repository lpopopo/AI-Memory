#!/usr/bin/env python3
"""Merge batch fetch results from _batch_fetch.json."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

def filter_images(urls):
    hi = [u for u in urls if "nd_dft_wlteh_webp" in u]
    return hi if hi else urls

batch = json.loads((BASE / "_batch_fetch.json").read_text(encoding="utf-8"))
data = json.loads((BASE / "posts-data.json").read_text(encoding="utf-8"))
prog_path = BASE / "_fetch_progress.json"
prog = json.loads(prog_path.read_text(encoding="utf-8")) if prog_path.exists() else {}

for post in batch:
    if post.get("error"):
        print(f"FAIL {post.get('noteId','?')[:8]}: {post['error']}")
        continue
    post["images"] = filter_images(post.get("images", []))
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
    prog[post["noteId"]] = post
    print(f"merged {post['noteId'][:8]} images={len(post['images'])}")

(BASE / "posts-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
prog_path.write_text(json.dumps(prog, ensure_ascii=False, indent=2), encoding="utf-8")
