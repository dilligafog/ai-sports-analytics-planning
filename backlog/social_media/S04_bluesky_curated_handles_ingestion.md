# Story S04 — Bluesky: Curated Handles Ingestion

**Last Updated:** 2025-08-24 13:59:19

## Overview
As a data collector, I want to ingest Bluesky posts from specific handles so that we don’t miss reporters who migrated away from X.

## Value Proposition
Diversifies coverage; resilience against single-platform outages/policy changes.

## Acceptance Criteria
- Given Bluesky credentials or app-password, fetch latest posts from configured DIDs/handles.
- Raw & bronze written; idempotent with cursor checkpointing.
- Media URLs captured when present; links resolved where possible.

## Technical Requirements
- Files: `packages/data_pipeline/src/nfl_data_pipeline/sources/social_bluesky.py`
- Config: `bluesky.accounts` and `bluesky.options` in `config/social_sources.yaml`.
- Support REST feed endpoints; optional firehose toggle (future).

## Implementation Plan
1. Add client wrapper with pagination + cursor state.
2. Map payloads to `SocialPost` with link/media extraction.
3. Add fixtures + unit tests; ensure UTC normalization.

## Definition of Done
- Sample run over 3–5 NFL reporters; records visible in bronze; checkpoint persists.

## Related Features
Social schema (S01); health checks (S09).
