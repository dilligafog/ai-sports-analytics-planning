# Story S02 — Twitter/X: Curated Accounts Ingestion

**Last Updated:** 2025-08-24 13:59:19

## Overview
As a data collector, I want to ingest posts from a curated list of NFL accounts on X so that beat writers and team announcements enter the news stream quickly.

## Value Proposition
High-signal, low-noise firehose from trusted voices; better injury/lineup detection.

## Acceptance Criteria
- Given valid X credentials, the job pulls latest posts for configured handles since last run.
- Configurable per-run max posts, lookback window, and `include_retweets` / `include_replies` toggles.
- Writes raw JSONL and normalized `SocialPost` to bronze; idempotent re-runs (no duplicates).
- Basic engagement fields recorded (like/repost/reply counts if available).

## Technical Requirements
- Files:
  - `packages/data_pipeline/src/nfl_data_pipeline/sources/social_x.py`
  - `config/social_sources.yaml` (`x.accounts`, `x.options`, rate-limit params)
- CLI: `busta pipeline collect social --provider x`
- Rate-limit/backoff & checkpointing (`state/social_x.json`).

## Implementation Plan
1. Add config loader for `x.accounts` (handles) and options.
2. Implement fetch loop with pagination + `since_id` checkpoint.
3. Map to `SocialPost`; persist raw & bronze; de-dup by provider id.
4. Add minimal unit tests with recorded fixtures.

## Definition of Done
- Dry-run against 3–5 public NFL accounts; sample rows visible in `busta pipeline report feeds`.
- State file advances across runs and prevents refetching.

## Related Features
Health checks; dedupe; entity linking; schema (S01).
