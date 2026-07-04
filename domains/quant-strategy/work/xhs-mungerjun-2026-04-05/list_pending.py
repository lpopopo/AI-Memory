#!/usr/bin/env python3
"""Fetch one post via noteId prefix - run merge after saving _last_fetch.json from browser."""
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent

def pending():
    data = json.loads((BASE / "posts-data.json").read_text(encoding="utf-8"))
    return [p for p in data["posts"] if not p.get("images")]

if __name__ == "__main__":
    for p in pending():
        print(p["noteId"][:8], "|", p["title"][:50])
