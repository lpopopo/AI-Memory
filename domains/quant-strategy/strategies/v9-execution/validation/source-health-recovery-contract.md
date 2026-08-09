# V9 Source-Health Recovery Contract

`source_health=partial` blocks new information-driven entries. It does not
block index-core risk management or review of existing positions.

Recovery is fail-closed and must never be inferred from a successful price
download. To restore `healthy`:

1. Close the existing `partial_live` interval without deleting or shortening
   its historical coverage gap.
2. Append a new `healthy_live` interval beginning on the first genuinely
   covered observation date.
3. Add `source_health_recovery_evidence` with an `as_of` date and explicit
   `healthy` status for both `x` and `xiaohongshu`.
4. Preserve real `first_seen_at` timestamps. Items discovered during the gap
   remain observations and cannot be backdated into point-in-time evidence.
5. Run the source-health tests and create a new versioned forward generation
   before using recovered events in formal execution.

Example schema:

```json
{
  "source_health": "healthy",
  "source_health_recovery_evidence": {
    "as_of": "YYYY-MM-DD",
    "sources": {
      "x": "healthy",
      "xiaohongshu": "healthy"
    }
  }
}
```

Changing only the top-level status is insufficient and remains blocked.
