import unittest

import pandas as pd

from v9_source_health import build_source_health_audit, filter_events_to_healthy_intervals


class SourceHealthAuditTests(unittest.TestCase):
    def test_partial_live_remains_fail_closed(self):
        raw = {
            "source_health": "partial",
            "source_health_history": [{"start": "2026-06-27", "end": None, "status": "partial_live"}],
        }
        audit = build_source_health_audit(raw, "2026-08-07")
        self.assertFalse(audit["new_information_entries_allowed"])
        self.assertIn("active_source_interval_not_healthy", audit["blockers"])

    def test_status_text_alone_cannot_claim_recovery(self):
        raw = {
            "source_health": "healthy",
            "source_health_history": [{"start": "2026-08-01", "end": None, "status": "healthy_live"}],
        }
        audit = build_source_health_audit(raw, "2026-08-07")
        self.assertFalse(audit["new_information_entries_allowed"])
        self.assertIn("current_recovery_evidence_missing", audit["blockers"])

    def test_current_evidence_for_all_sources_allows_recovery(self):
        raw = {
            "source_health": "healthy",
            "source_health_history": [{"start": "2026-08-01", "end": None, "status": "healthy_live"}],
            "source_health_recovery_evidence": {
                "as_of": "2026-08-07",
                "sources": {"x": "healthy", "xiaohongshu": "healthy"},
            },
        }
        audit = build_source_health_audit(raw, "2026-08-07")
        self.assertTrue(audit["new_information_entries_allowed"])
        self.assertEqual(audit["blockers"], [])

    def test_overlapping_intervals_are_rejected(self):
        raw = {
            "source_health": "healthy",
            "source_health_history": [
                {"start": "2026-06-27", "end": None, "status": "partial_live"},
                {"start": "2026-08-01", "end": None, "status": "healthy_live"},
            ],
            "source_health_recovery_evidence": {
                "as_of": "2026-08-07",
                "sources": {"x": "healthy", "xiaohongshu": "healthy"},
            },
        }
        audit = build_source_health_audit(raw, "2026-08-07")
        self.assertFalse(audit["new_information_entries_allowed"])
        self.assertIn("source_health_history_invalid", audit["blockers"])

    def test_events_observed_during_partial_interval_never_become_eligible(self):
        class Event:
            def __init__(self, effective_at):
                self.effective_at = pd.Timestamp(effective_at)

        raw = {
            "source_health_history": [
                {"start": "2026-05-29", "end": "2026-06-26", "status": "healthy_archived"},
                {"start": "2026-06-27", "end": "2026-08-02", "status": "partial_live"},
                {"start": "2026-08-03", "end": None, "status": "healthy_live"},
            ]
        }
        events = [Event("2026-06-20"), Event("2026-07-15"), Event("2026-08-04")]
        eligible = filter_events_to_healthy_intervals(events, raw)
        self.assertEqual([event.effective_at.date().isoformat() for event in eligible], ["2026-06-20", "2026-08-04"])


if __name__ == "__main__":
    unittest.main()
