---
id: MOD-001
epic: llm_backlog
status: draft
owner: modeling-team
priority: high
estimate: 5sp
dependencies: [LLM-001, ING-002]
tags: [modeling, ats]
market: ats
layer: Gold
last_updated: 2025-08-24
emit_metadata:
  source_id: base_ats_model
  layer: Gold
  input_path: data/gold/
  notes: Rebaseline ATS/ML/Total models with clean features
---

# MOD-001: Rebaseline ATS/ML/Total models with clean features

- **Overview**: As a data scientist, I want strong base models so that LLM signals can add lift on top of a solid foundation.
- **Value Proposition**: Good baselines ensure we don’t attribute spurious gains to LLM features.

## Acceptance Criteria
- Train baseline models for ATS, ML, and Totals using rolling features (last-5, last-10, season-to-date).
- Cross-validation with season/week grouped splits; log-loss/Brier reported.
- Feature store schema stable and documented.

## Technical Requirements
- LightGBM/XGBoost with monotonic constraints where applicable.
- Leak checks (no future odds/stats leakage).
- Feature store under `data/gold/features.parquet` keyed by `game_id, team_id`.

## Implementation Plan
- Define feature set and labels per market.
- Implement grouped CV and evaluation.
- Store calibrated outputs for stacker input.

## Definition of Done
- Reproducible training run with fixed seeds.
- Metrics recorded in `reports/metrics_baseline.md`.
- Model artifacts versioned under `models/baseline/`.

## Related Features
EVAL-001, MOD-002
