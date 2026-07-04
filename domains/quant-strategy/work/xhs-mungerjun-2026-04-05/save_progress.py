#!/usr/bin/env python3
"""Append fetched post to _fetch_progress.json from stdin JSON."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
PROGRESS = BASE / "_fetch_progress.json"

post = json.loads(sys.stdin.read())
prog = {}
if PROGRESS.exists():
    prog = json.loads(PROGRESS.read_text(encoding="utf-8"))
nid = post.get("noteId", "")
if nid:
    prog[nid] = post
    PROGRESS.write_text(json.dumps(prog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"progress saved {nid[:8]}")
