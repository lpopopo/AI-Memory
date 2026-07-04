#!/usr/bin/env python3
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
queue = json.loads((BASE / "fetch-queue.json").read_text())
queue_map = {q["noteId"]: q for q in queue}

# Raw extracted data from browser (noteId -> data)
RAW = json.loads((BASE / "_raw_extracted.json").read_text())

results = []
for q in queue[:10]:
    if q.get("skip"):
        continue
    data = RAW[q["noteId"]]
    data["date"] = q["date"]
    data["url"] = q["url"]
    results.append(data)

out = BASE / "extracted-batch-1.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Saved {len(results)} posts to {out.name}")
