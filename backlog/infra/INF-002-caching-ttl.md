---
id: INF-003
epic: llm_backlog
status: draft
owner: infra-team
priority: medium
estimate: 2sp
dependencies: []
tags: [caching, ttl]
market: null
layer: Infra
last_updated: 2025-08-24
emit_metadata:
  source_id: cache_policy
  layer: Infra
  input_path: null
  notes: Caching and TTL for time-sensitive signals
---

# INF-003: Caching & TTL for time-sensitive signals

- **Overview**: As a platform engineer, I want caching and expirations so that stale news doesn’t leak into predictions.
- **Value Proposition**: Controls cost and correctness for LLM and news retrieval.

## Acceptance Criteria
- LLM feature cache keyed by `cluster_id` with 24h TTL (configurable).
- News fetch cache with ETag/Last-Modified; odds cache 60s.
- Monitoring warns when signals exceed TTL during inference.

## Technical Requirements
- Cache to disk with metadata index; purge cron/task.
- TTL enforcement in feature loader; warnings bubble to reports.
- Configurable via `config/runtime.yml`.

## Implementation Plan
- Implement cache layer and TTL checks.
- Add monitoring hooks to inference.
- Write tests for expiry and refresh behavior.

## Definition of Done
- Expired entries are refreshed automatically.
- No inference run uses signals older than TTL.

## Related Features
LLM-001, ING-001
