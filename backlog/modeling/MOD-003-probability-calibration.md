---
id: MOD-003
epic: llm_backlog
status: draft
owner: modeling-team
priority: medium
estimate: 3sp
dependencies: [MOD-001]
tags: [modeling, calibration]
market: null
layer: Gold
last_updated: 2025-08-24
emit_metadata:
  source_id: calibration
  layer: Gold
  input_path: models/calibration/
  notes: Probability calibration & reliability curves
---

# MOD-003: Probability calibration & reliability curves

- **Overview**: As a quant, I want calibrated probabilities so that our 60% means 60% in the long run.
- **Value Proposition**: Calibration improves bankroll management and trust in the system.

## Acceptance Criteria
- Reliability plots for ATS/ML/Total created for baseline and stacker.
- Isotonic regression selected unless sample size too small (fallback to Platt).
- Calibration error reported and tracked over time.

## Technical Requirements
- Bin-based reliability and Brier decomposition.
- Store calibration maps with model metadata.
- Unit tests for calibration functions.

## Implementation Plan
- Implement calibration utilities.
- Integrate into training and inference pipelines.
- Generate plots and tables in `reports/`.

## Definition of Done
- Plots and metrics present; CI test covers calibration edge cases.
- Inference applies correct calibration map for model version.

## Related Features
MOD-001, MOD-002, EVAL-001
