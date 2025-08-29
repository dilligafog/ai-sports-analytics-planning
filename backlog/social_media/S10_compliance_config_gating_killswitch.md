# Story S10 — Compliance, Config Gating & Kill-Switch

**Last Updated:** 2025-08-24 13:59:19

## Overview
As a product owner, I want compliance toggles and a global kill-switch so we can quickly disable a provider if policies or access change.

## Value Proposition
Risk reduction; easier ops during platform policy shifts.

## Acceptance Criteria
- Config flags: `enable_x`, `enable_bluesky`, and `social_read_only` mode.
- `busta pipeline collect social` respects flags; kill-switch halts fetch but keeps transforms/test stubs.
- Audit log of enable/disable events.

## Technical Requirements
- Files: `packages/data_pipeline/src/nfl_data_pipeline/config/settings.py` (flags)
- Audit: `data/ops/audit/social_flags.log`

## Implementation Plan
1. Add flags & wiring to providers.
2. Write simple audit appender and test toggling.
3. Document ops runbook in `docs/ingestion/social.md`.

## Definition of Done
- Toggling flags changes behavior without code changes; covered by integration tests.

## Related Features
Scheduling (S08); provider ingestion (S02–S05).
