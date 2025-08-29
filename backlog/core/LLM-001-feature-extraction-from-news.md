---
id: LLM-001
epic: llm_backlog
status: backlog
owner: team-llm
priority: high
estimate: 3sp
dependencies: [ING-002]
tags: [llm, features, news]
market: null
layer: Silver
last_updated: 2025-08-29
emit_metadata:
  source_id: news_rss
  layer: Silver
  input_path: data/bronze/news/
  notes: Extracted signals will be stored in Silver layer
---

# LLM-001: LLM extraction of game signals from news

- **Overview**: As a data scientist, I want LLMs to convert articles into structured game signals so that numeric models can consume high-signal context.
- **Value Proposition**: Transforms unstructured text about starters, injuries, and coach intent into quantitative features.

## Acceptance Criteria
- [ ] **JSON Schema Compliance**: Prompt outputs **JSON only** matching schema with fields: `qb_p_play`, `starter_snap_tier`, `coach_preseason_intensity`, `injury_risk_core`, `weather_penalty_pass`, `evidence` (quotes + URLs).
- [ ] **Temperature Control**: Temperature=0; responses validated against JSON schema; retry on invalid.
- [ ] **Data Persistence**: `data/gold/llm_signals.parquet` keyed by `game_id, as_of` with 100% valid JSON records.
- [ ] **Unknown Handling**: Unknowns represented as `null` or empty arrays; no hallucinated names.
- [ ] **Performance**: Process 100 articles in < 5 minutes with < 1% failure rate.
- [ ] **Evidence Quality**: 95% of evidence quotes match article text exactly.

## Technical Requirements
- [ ] System prompt enforcing JSON-only + abstention.
- [ ] pydantic schema; validator to drop/flag out-of-range values.
- [ ] Caching by (`cluster_id`, `schema_version`).
- [ ] Batch processing support for 100+ articles.
- [ ] Error handling for API failures and malformed responses.

## Implementation Plan
1. **Week 1**: Define schema and validator, implement basic extraction
2. **Week 2**: Add batch mode, caching, and error handling
3. **Week 3**: Integration testing, performance optimization, documentation

## Definition of Done
- [ ] 100% of outputs valid JSON; <1% manual correction rate.
- [ ] Spot-check: evidence quotes match article text exactly.
- [ ] Feature importances show non-zero lift in ablation (see EVAL-002).
- [ ] Unit tests pass on mocked articles with golden JSON.
- [ ] Integration test with real news data pipeline.

## Related Features
ING-001, ING-002, MOD-002, EVAL-002
