---
id: MOD-005
epic: llm_backlog
status: draft
owner: feature-store-team
priority: high
estimate: 4sp
dependencies: []
tags: [feature-store, schema]
market: null
layer: Gold
last_updated: 2025-08-24
emit_metadata:
  source_id: feature_store_schema
  layer: Gold
  input_path: data/gold/
  notes: Feature store schema & lineage
---

# MOD-005: Feature store schema & lineage

- **Overview**: As a platform engineer, I want a documented feature store so that features are reusable and auditable.
- **Value Proposition**: Prevents one-off features and speeds iteration.

## Acceptance Criteria
- Schema includes sources: numeric, market, and LLM-derived features.
- Lineage tracked from raw → silver → gold with versioning.
- Data dictionary produced under `docs/feature_store.md`.

## Technical Requirements
- Use Parquet + Delta-like partitioning by date/week where useful.
- Add `as_of` timestamps and TTLs for time-sensitive LLM features.
- Great Expectations or pandera checks for critical columns.

## Implementation Plan
- Design table(s) and write loaders.
- Implement validation checks and CI step.
- Document dictionary and sample queries.

## Definition of Done
- Validation passes on full pipeline run.
- Docs up to date; joins work across sources.

## Related Features
ING-*, LLM-*, MOD-*
