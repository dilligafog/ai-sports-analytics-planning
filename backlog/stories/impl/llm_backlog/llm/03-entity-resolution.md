---
id: LLM-003
epic: llm_backlog
status: draft
owner: team-llm
priority: medium
estimate: 2sp
dependencies: [ING-001]
tags: [llm, entity-resolution]
market: null
layer: Bronze
last_updated: 2025-08-24
emit_metadata:
  source_id: entity_resolver
  layer: Bronze
  input_path: data/bronze/news/
  notes: Map mentions to canonical team/player ids
---

# LLM-003: Entity resolution for teams and players

- **Overview**: As a data engineer, I want robust entity resolution so that names in text match our canonical IDs for teams and players.
- **Value Proposition**: Enables joins across news, odds, schedules, and stats without leaks or mismatches.

## Acceptance Criteria
- Dictionary-driven resolver supports aliases, abbreviations, and common misspellings.
- Resolver outputs `entity_id`, `confidence`, and `canonical_name`; abstains when <0.8 confidence.
- Stored lookups in `data/silver/entities.parquet`; unit tests cover 100+ variants.

## Technical Requirements
- Fuzzy matching (Jaro-Winkler), token set ratio, and abbreviation maps.
- Team code dictionary maintained under `config/teams.yml`.
- Player mapping seeded from public rosters; add-update pipeline.

## Implementation Plan
- Implement resolver with scoring and thresholds.
- Build test corpus of tricky aliases.
- Integrate into news pipeline and LLM features.

## Definition of Done
- Resolution accuracy ≥ 95% on test set.
- Unknowns correctly abstained and logged for review.

## Related Features
ING-002, LLM-001, MOD-002
