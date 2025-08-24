---
id: EVAL-001
epic: llm_backlog
status: draft
owner: evaluation-team
priority: high
estimate: 3sp
dependencies: []
tags: [evaluation, metrics]
market: null
layer: Analysis
last_updated: 2025-08-24
emit_metadata:
  source_id: offline_eval
  layer: Analysis
  input_path: runs/
  notes: Offline harness and metrics tracking
---

# EVAL-001: Offline evaluation harness & metrics tracking

- **Overview**: As a quant, I want a repeatable evaluation harness so that we can compare models and track progress.
- **Value Proposition**: Objective measurement prevents regressions.

## Acceptance Criteria
- Compute log-loss, Brier, AUC, and calibration error per market and time period.
- Produce time-series of metrics; store under `reports/metrics_history.parquet`.
- Simple HTML/MD report summarizing latest runs.

## Technical Requirements
- Grouped CV by season/week; robust splits.
- Plot reliability and lift curves (matplotlib).
- Seed handling for reproducibility.

## Implementation Plan
- Implement evaluator module.
- Add report generator.
- Store artifacts and wire into CI.

## Definition of Done
- Baseline metrics recorded and versioned.
- CI fails on metric regressions beyond thresholds.

## Related Features
MOD-001, MOD-002, MOD-003
