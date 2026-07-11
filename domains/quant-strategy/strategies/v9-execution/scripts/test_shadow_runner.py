#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import pandas as pd

from run_v9_shadow import atomic_freeze, digest, visible_event_snapshot
from shadow_v9_engine import TamperAlarmException


class TestShadowRunner(unittest.TestCase):
    def mode_dir(self):
        return Path(tempfile.mkdtemp())

    def event(self, event_id="forward-test-event"):
        summary = "forward append test"
        return {"event_id": event_id, "source": "test", "author": "test", "post_id": event_id, "published_at": None, "first_seen_at": "2026-06-18T20:00:00+08:00", "content_summary": summary, "content_hash": hashlib.sha256(summary.encode()).hexdigest(), "theme": "test", "symbols": ["AMD"], "source_completeness": 20, "thesis_novelty": 10, "fundamental_validation": 10, "crowding_penalty": 5}

    def write_chain(self, mode, events):
        path = mode / "shared" / "event_append_log.jsonl"; path.parent.mkdir(parents=True)
        previous = ""; records = []
        for event in events:
            event_hash = digest({"previous_event_hash": previous, "event": event})
            records.append({"previous_event_hash": previous, "event_hash": event_hash, "event": event}); previous = event_hash
        path.write_text("\n".join(json.dumps(x) for x in records), encoding="utf-8")

    def test_append_event_is_visible_without_changing_baseline(self):
        mode = self.mode_dir(); self.write_chain(mode, [self.event()])
        snapshot, _, hashes = visible_event_snapshot(mode, pd.Timestamp("2026-06-18"))
        ids = {x["event_id"] for x in json.loads(snapshot.read_text(encoding="utf-8"))["events"]}
        self.assertIn("forward-test-event", ids); self.assertEqual(len(hashes), 1)

    def test_duplicate_baseline_event_raises_tamper_alarm(self):
        mode = self.mode_dir(); self.write_chain(mode, [self.event("kay-mrvl-three-layer-20260614")])
        with self.assertRaises(TamperAlarmException): visible_event_snapshot(mode, pd.Timestamp("2026-06-18"))

    def test_atomic_freeze_is_idempotent_and_rejects_change(self):
        path = self.mode_dir() / "x.json"
        self.assertEqual(atomic_freeze(path, {"a": 1}), "written")
        self.assertEqual(atomic_freeze(path, {"a": 1}), "unchanged")
        with self.assertRaises(TamperAlarmException): atomic_freeze(path, {"a": 2})


if __name__ == "__main__": unittest.main()
