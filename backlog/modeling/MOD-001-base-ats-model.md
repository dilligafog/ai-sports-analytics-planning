---
id: MOD-001
epic: llm_backlog
status: backlog
owner: modeling-team
priority: high
estimate: 5sp
dependencies: [ING-002]
tags: [modeling, ats]
market: ats
layer: Gold
last_updated: 2025-08-29
emit_metadata:
  source_id: base_ats_model
  layer: Gold
  input_path: data/gold/
  notes: Rebaseline ATS/ML/Total models with clean features
---

# MOD-001: Rebaseline ATS/ML/Total models with clean features

- **Overview**: As a data scientist, I want strong base models so that LLM signals can add lift on top of a solid foundation.
- **Value Proposition**: Good baselines ensure we don't attribute spurious gains to LLM features.

## Acceptance Criteria
- [ ] **Model Training**: Train baseline models for ATS, ML, and Totals using rolling features (last-5, last-10, season-to-date).
- [ ] **Cross-Validation**: Season/week grouped splits with log-loss/Brier reported and < 0.25 Brier score target.
- [ ] **Feature Store**: Schema stable and documented with 100% data completeness.
- [ ] **Performance**: Models achieve > 52% ATS accuracy on validation set.
- [ ] **Reproducibility**: Fixed seeds produce identical results across environments.

## Technical Requirements
- [ ] LightGBM/XGBoost with monotonic constraints where applicable.
- [ ] Leak checks (no future odds/stats leakage) with automated validation.
- [ ] Feature store under `data/gold/features.parquet` keyed by `game_id, team_id`.
- [ ] Model versioning and artifact storage in `models/baseline/`.
- [ ] GPU acceleration support for faster training.

## Implementation Plan
1. **Week 1-2**: Define feature set and labels per market, implement data pipeline
2. **Week 3**: Implement grouped CV and evaluation framework
3. **Week 4**: Store calibrated outputs for stacker input, documentation

## Definition of Done
- [ ] Reproducible training run with fixed seeds.
- [ ] Metrics recorded in `reports/metrics_baseline.md` with charts.
- [ ] Model artifacts versioned under `models/baseline/`.
- [ ] Feature importance analysis completed and documented.
- [ ] Integration tests pass with downstream stacker.

## Related Features
EVAL-001, MOD-002, MOD-003
