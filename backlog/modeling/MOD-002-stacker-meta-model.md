---
id: MOD-002
epic: llm_backlog
status: draft
owner: modeling-team
priority: medium
estimate: 5sp
dependencies: [MOD-001]
tags: [modeling, stacking]
market: null
layer: Gold
last_updated: 2025-08-24
emit_metadata:
  source_id: stacker_model
  layer: Gold
  input_path: models/
  notes: Meta-model stacker with LLM-aware weighting
---

# MOD-002: Meta-model stacker with LLM-aware weighting

- **Overview**: As a modeler, I want a stacker to blend base models with market info and LLM signals so that predictions adapt to context.
- **Value Proposition**: Combines numeric strength with text-derived situational awareness.

## Acceptance Criteria
- Inputs: base model probs, market implied probs, selected LLM signals.
- Outputs calibrated probabilities for ATS/ML/Total; weights logged per game.
- Ablation shows improvement vs baselines ≥ 2% Brier reduction.

## Technical Requirements
- Logistic regression or shallow GBM; optional LLM advisory that outputs weight priors.
- Isotonic/Platt calibration over validation folds.
- Explainability: per-game breakdown of contributing inputs.

## Implementation Plan
- Implement stacker fit/predict API.
- Join features; run CV with and without LLM signals.
- Persist calibrated outputs; add SHAP-like summary or weight table.

## Definition of Done
- Ablation report written to `reports/ablation_stacker.md`.
- Per-game logs include component weights and final prob.

## Related Features
LLM-001, EVAL-002, MOD-001
