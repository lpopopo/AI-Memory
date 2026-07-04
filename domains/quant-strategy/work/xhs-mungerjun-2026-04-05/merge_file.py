#!/usr/bin/env python3
"""Merge post JSON file into posts-data.json and save progress."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
path = Path(sys.argv[1])
post = json.loads(path.read_text(encoding="utf-8"))

# merge
import merge_fetched  # noqa - reuse logic
post["images"] = merge_fetched.filter_images(post.get("images", []))
data = json.loads((BASE / "posts-data.json").read_text(encoding="utf-8"))
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
(BASE / "posts-data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

# progress
prog_path = BASE / "_fetch_progress.json"
prog = json.loads(prog_path.read_text(encoding="utf-8")) if prog_path.exists() else {}
prog[post["noteId"]] = post
prog_path.write_text(json.dumps(prog, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"merged {post['noteId'][:8]} images={len(post['images'])}")
