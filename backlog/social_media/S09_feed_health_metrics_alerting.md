# Story S09 — Feed Health, Metrics & Alerting for Social

**Last Updated:** 2025-08-24 13:59:19

## Overview
As an SRE, I want health metrics and dashboards for social ingestion so that I can detect stalls, auth failures, and surges.

## Value Proposition
Faster incident response; better capacity planning.

## Acceptance Criteria
- Extend `feed_health.py` to track: `last_success_ts`, `items_ingested`, `error_rate`, `avg_latency`, `rate_limit_hits`.
- CLI report shows social providers & top failing handles/queries.
- Optional webhook/email alert on stall > N minutes.

## Technical Requirements
- Files: `packages/data_pipeline/src/nfl_data_pipeline/sources/feed_health.py` (extend)
- Metrics dump: `data/ops/social_health/*.json`

## Implementation Plan
1. Add counters & timers around provider calls.
2. Update `busta pipeline report feeds` to include social section.
3. Write tests for failure detection and recovery logging.

## Definition of Done
- Demo report with at least one induced failure and one recovery; metrics visible in JSON dumps.

## Related Features
Scheduling (S08); provider ingestion (S02–S05).
