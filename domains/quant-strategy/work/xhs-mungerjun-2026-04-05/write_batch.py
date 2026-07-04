#!/usr/bin/env python3
"""Write CDP result string to _batch_fetch.json (dedupe by noteId)."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
raw = sys.stdin.read().strip()
if raw.startswith("{"):
    data = json.loads(raw)
    val = data.get("result", {}).get("value", raw)
else:
    val = raw
posts = json.loads(val)
seen = {}
for p in posts:
    nid = p.get("noteId")
    if nid and nid not in seen:
        seen[nid] = p
(BASE / "_batch_fetch.json").write_text(
    json.dumps(list(seen.values()), ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"saved {len(seen)} unique posts")
