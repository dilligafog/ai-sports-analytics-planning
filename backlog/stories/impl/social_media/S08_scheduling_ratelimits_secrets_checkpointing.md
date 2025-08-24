# Story S08 — Scheduling, Rate-Limits, Secrets & Checkpointing

**Last Updated:** 2025-08-24 13:59:19

## Overview
As an operator, I want resilient job scheduling with rate-limit handling and secure secrets so that social ingestion runs reliably.

## Value Proposition
Fewer failures, no credential leaks, predictable throughput.

## Acceptance Criteria
- Credentials loaded from `.env`/secret store; never logged.
- Exponential backoff and jitter on 429/5xx; per-provider QPS limits configurable.
- Per-handle, per-query checkpoint files; resumable runs.

## Technical Requirements
- Files:
  - `packages/data_pipeline/src/nfl_data_pipeline/utils/rate_limit.py`
  - `packages/data_pipeline/src/nfl_data_pipeline/utils/checkpoint.py`
- Update `busta` command help & examples.

## Implementation Plan
1. Implement rate-limit wrapper; integrate in providers.
2. Add secret loading & validation on startup.
3. Verify checkpoints via rerun tests.

## Definition of Done
- Chaos test (forced 429s) passes; checkpoints verified via rerun without refetching.

## Related Features
Provider ingestion (S02–S05); health checks (S09).
