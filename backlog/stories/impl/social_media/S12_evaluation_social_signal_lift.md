# Story S12 — Evaluation: Does Social Improve Predictions?

**Last Updated:** 2025-08-24 13:59:19

## Overview
As a data scientist, I want to quantify the lift from social signals so that we know whether to keep investing.

## Value Proposition
Evidence-based prioritization.

## Acceptance Criteria
- Generate features: social sentiment, volume spikes, injury/transaction keyword counts by team/day.
- Backtest across historical weeks with/without social features; report delta in validation metrics.
- Clear go/no-go recommendation captured in markdown with charts.

## Technical Requirements
- Files: `packages/features/src/social_features.py`, `packages/models/notebooks/social_lift.ipynb`
- Inputs: bronze social posts + relevance tags; outputs: feature tables and evaluation report.

## Implementation Plan
1. Feature extraction jobs reading bronze social + relevance tags.
2. Re-train baseline ATS model with added features; compare performance (AUC/LogLoss/Calibration).
3. Document results and risks; include follow-up stories if lift is material.

## Definition of Done
- Markdown report with charts; clear summary of impact and recommendation committed at `docs/reports/social_lift.md`.

## Related Features
Relevance (S06); sentiment pipeline; modeling.
