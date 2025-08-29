---
id: MOD-002
epic: llm_backlog
status: backlog
owner: modeling-team
priority: medium
estimate: 4sp
dependencies: [MOD-001]
tags: [modeling, stacking]
market: null
layer: Gold
last_updated: 2025-08-29
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
- [ ] **Input Integration**: Successfully blend base model probs, market implied probs, and LLM signals.
- [ ] **Output Quality**: Calibrated probabilities for ATS/ML/Total with weights logged per game.
- [ ] **Performance Improvement**: Ablation shows ≥ 2% Brier reduction vs baseline models.
- [ ] **Explainability**: Per-game breakdown shows contributing inputs and their weights.
- [ ] **Robustness**: Handles missing LLM signals gracefully with fallback weights.

## Technical Requirements
- [ ] Logistic regression or shallow GBM; optional LLM advisory for weight priors.
- [ ] Isotonic/Platt calibration over validation folds with confidence intervals.
- [ ] Explainability: SHAP-like summary or weight table per prediction.
- [ ] Model versioning and A/B testing framework.
- [ ] Automated retraining pipeline.

## Implementation Plan
1. **Week 1**: Implement stacker fit/predict API with basic blending
2. **Week 2**: Add LLM signal integration and weight optimization
3. **Week 3**: Implement explainability features and comprehensive testing
4. **Week 4**: Performance optimization and production deployment

## Definition of Done
- [ ] Ablation report written to `reports/ablation_stacker.md` with charts.
- [ ] Per-game logs include component weights and final probabilities.
- [ ] Model achieves target 2%+ Brier improvement in production.
- [ ] Integration tests pass with all upstream dependencies.
- [ ] Documentation covers model interpretation and maintenance.

## Related Features
LLM-001, EVAL-002, MOD-001, MOD-003
