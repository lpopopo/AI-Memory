"""Fail-closed source-health audit for V9 information-event authorization."""
from __future__ import annotations

import pandas as pd


REQUIRED_RECOVERY_SOURCES = ("x", "xiaohongshu")


def _healthy_status(value: object) -> bool:
    return str(value or "").lower().startswith("healthy")


def build_source_health_audit(raw: dict, as_of: str | pd.Timestamp) -> dict:
    """Explain whether live information capture may authorize new entries.

    Price-data health is intentionally irrelevant here. Recovery requires an
    explicit current interval plus timestamped evidence for every required
    information source; it is never inferred from a successful quote refresh.
    """
    as_of_date = pd.Timestamp(as_of).normalize()
    history = list(raw.get("source_health_history", []))
    normalized = []
    issues = []
    for index, row in enumerate(history):
        try:
            start = pd.Timestamp(row["start"]).normalize()
            end = pd.Timestamp(row["end"]).normalize() if row.get("end") else None
        except Exception as error:
            issues.append(f"invalid_interval_{index}:{error}")
            continue
        if end is not None and end < start:
            issues.append(f"reversed_interval_{index}")
        normalized.append({"start": start, "end": end, "status": str(row.get("status", "unknown"))})
    normalized.sort(key=lambda row: row["start"])
    for prior, current in zip(normalized, normalized[1:]):
        if prior["end"] is None or current["start"] <= prior["end"]:
            issues.append("overlapping_or_open_prior_interval")

    active = [row for row in normalized if row["start"] <= as_of_date and (row["end"] is None or as_of_date <= row["end"])]
    if len(active) != 1:
        issues.append("active_interval_missing_or_ambiguous")
    active_row = active[0] if len(active) == 1 else None

    evidence = raw.get("source_health_recovery_evidence")
    evidence_sources = evidence.get("sources", {}) if isinstance(evidence, dict) else {}
    evidence_as_of = None
    if isinstance(evidence, dict) and evidence.get("as_of"):
        try:
            evidence_as_of = pd.Timestamp(evidence["as_of"]).normalize()
        except Exception:
            issues.append("invalid_recovery_evidence_as_of")
    evidence_current = evidence_as_of is not None and evidence_as_of >= as_of_date
    healthy_sources = all(_healthy_status(evidence_sources.get(source)) for source in REQUIRED_RECOVERY_SOURCES)

    stored_status = str(raw.get("source_health", "unknown"))
    active_status = active_row["status"] if active_row else "unknown"
    blockers = []
    if not _healthy_status(stored_status):
        blockers.append("stored_source_health_not_healthy")
    if not _healthy_status(active_status):
        blockers.append("active_source_interval_not_healthy")
    if issues:
        blockers.append("source_health_history_invalid")
    if not evidence_current:
        blockers.append("current_recovery_evidence_missing")
    if not healthy_sources:
        blockers.append("required_live_sources_not_all_healthy")
    blockers = list(dict.fromkeys(blockers))
    allowed = not blockers
    return {
        "as_of": str(as_of_date.date()),
        "stored_status": stored_status,
        "active_interval": None if active_row is None else {
            "start": str(active_row["start"].date()),
            "end": str(active_row["end"].date()) if active_row["end"] is not None else None,
            "status": active_status,
        },
        "history_valid": not issues,
        "history_issues": issues,
        "recovery_evidence_as_of": str(evidence_as_of.date()) if evidence_as_of is not None else None,
        "required_recovery_sources": list(REQUIRED_RECOVERY_SOURCES),
        "new_information_entries_allowed": allowed,
        "blockers": blockers,
        "recovery_rule": "append a healthy_live interval and current timestamped coverage evidence; never rewrite the partial interval or infer recovery from price data",
    }


def filter_events_to_healthy_intervals(events: list, raw: dict) -> list:
    """Exclude events first observed inside partial or uncovered intervals."""
    intervals = []
    for row in raw.get("source_health_history", []):
        if not _healthy_status(row.get("status")):
            continue
        start = pd.Timestamp(row["start"]).normalize()
        end = pd.Timestamp(row["end"]).normalize() if row.get("end") else None
        intervals.append((start, end))
    eligible = []
    for event in events:
        observed = pd.Timestamp(event.effective_at).tz_localize(None).normalize()
        if any(start <= observed and (end is None or observed <= end) for start, end in intervals):
            eligible.append(event)
    return eligible
