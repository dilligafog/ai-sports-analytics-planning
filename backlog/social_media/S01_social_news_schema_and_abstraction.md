# Story S01 — Social News Schema & Abstraction

**Last Updated:** 2025-08-24 13:59:19

## Overview
As a data engineer, I want a unified social-news schema and source interface so that Twitter/X and Bluesky posts can flow through the same pipeline as RSS with minimal branching.

## Value Proposition
Reduces one-off logic, speeds integration of future sources, and simplifies downstream features (sentiment, entity linking, dedupe).

## Acceptance Criteria
- A new `SocialPost` domain model aligns with existing `NewsItem` fields where applicable: `id`, `published_at`, `url`, `source`, `author`, `text`, `language`, `engagement`, `entities`, `media`.
- Provider mappers for X and Bluesky populate this model; unit tests cover null/optional fields.
- Serialization supported to JSONL & Parquet; timestamps normalized to UTC; language codes normalized (ISO 639-1).
- Linting (ruff), typing (mypy) pass in CI.

## Technical Requirements
- Files:
  - `packages/data_pipeline/src/nfl_data_pipeline/sources/social_common.py` (interfaces, dataclasses or pydantic models)
  - `packages/data_pipeline/src/nfl_data_pipeline/transform/social_mapper.py` (provider→domain mappers)
  - `packages/data_pipeline/tests/test_social_schema.py`
- Storage layout:
  - Raw: `data/raw/social/{x|bluesky}/YYYY/MM/DD/*.jsonl`
  - Bronze (normalized): `data/bronze/social_posts/*.parquet`

## Implementation Plan
1. Define `SocialPost` with typed fields & validators (UTC coercion, ISO language codes, safe ints for counts).
2. Write shared helpers (emoji/hashtag normalization, URL expansion placeholder).
3. Create provider mappers returning `SocialPost` instances.
4. Wire bronze writer and add CI coverage.

## Definition of Done
- >90% test coverage on schema & mappers.
- `ruff`, `mypy` clean; docs added at `docs/ingestion/social.md`.
- Example JSONL→Parquet flow demonstrated with fixture payloads.

## Related Features
RSS `NewsItem` pipeline; sentiment; entity tagging; dedupe.
