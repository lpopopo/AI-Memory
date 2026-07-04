#!/usr/bin/env python3
"""Merge extracted post data with queue and write extracted-batch-1.json."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
queue = json.loads((BASE / "fetch-queue.json").read_text())

# Load base data (post 1) and append remaining from MCP extraction
posts = json.loads((BASE / "_extracted_data.json").read_text())

# Posts 2-9 from browser CDP extraction
posts.update(json.loads((BASE / "_extracted_rest.json").read_text()))

results = []
for q in queue[:10]:
    if q.get("skip"):
        continue
    nid = q["noteId"]
    if nid not in posts:
        raise KeyError(f"Missing {nid}")
    item = dict(posts[nid])
    item["date"] = q["date"]
    item["url"] = q["url"]
    results.append(item)

out = BASE / "extracted-batch-1.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(results)} posts")
