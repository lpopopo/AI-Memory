#!/usr/bin/env python3
"""Build Apr-May fetch queue from profile URLs and manifest."""

import datetime
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
URLS = json.loads((BASE / "profile-urls-with-token.json").read_text(encoding="utf-8"))
MANIFEST = json.loads((BASE / "apr-may-manifest.json").read_text(encoding="utf-8"))

url_map = {p["id"]: p["href"] for p in URLS["posts"]}
already = {"69f82e40", "6a192fd5"}

queue = []
for item in MANIFEST:
    short = item["id"][:8]
    entry = {
        "id": item["id"],
        "title": item["title"],
        "publishedDate": item["publishedDate"],
        "href": url_map.get(item["id"]),
        "action": "copy" if short in already else "fetch",
    }
    queue.append(entry)

(BASE / "fetch-queue.json").write_text(
    json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8"
)
need = sum(1 for q in queue if q["action"] == "fetch")
print(f"queue: {len(queue)} posts, fetch: {need}, copy: {len(queue)-need}")
