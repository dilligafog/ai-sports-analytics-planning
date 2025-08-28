---
id: LLM-005
epic: llm_backlog
status: draft
owner: team-llm
priority: high
estimate: 2sp
dependencies: []
tags: [llm, injuries]
market: null
layer: Silver
last_updated: 2025-08-27
emit_metadata:
  source_id: injury_override
  layer: Silver
  input_path: data/silver/injuries/
  notes: Overrides or supplements official injury feeds with LLM signal
---

# LLM-005: Injury override & starter availability signal

- **Overview**: As a handicapper, I want a quantified probability of key starters playing so that preseason and injury-heavy weeks are modeled correctly.
- **Value Proposition**: Starter availability is the single biggest preseason lever; quantifying it improves predictions and bet selection.

## Acceptance Criteria
- For QB/RB/WR1/WR2/TE1/LT/EDGE1/CB1 positions, compute `p_play` and `snap_tier`.
- Signal TTL is 24h unless refreshed by newer news.
- Models can query `p_play` by player/team and adjust expected efficiency.

## Technical Requirements
- Derive from LLM outputs with schema validation and hysteresis (don’t flip-flop on tiny news).
- Persist player-level signals under `data/gold/player_availability.parquet`.
- Feature functions map player-level to team-level effects.

## Implementation Plan
- Add position taxonomy and mapping to starters.
- Implement hysteresis and TTL logic.
- Join into feature store for predictions.

## Definition of Done
- Historical audit shows fewer false-start assumptions vs baseline.
- Models with this signal outperform in preseason backtests.

## Related Features
LLM-001, MOD-001, MOD-002
