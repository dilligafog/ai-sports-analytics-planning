---
id: LLM-017
epic: core
status: accepted
owner: qa-team
priority: high
estimate: 2sp
dependencies: []
tags:
- quality
- data
market: null
layer: Bronze
accepted_date: '2025-08-27'
completed_date: 2025-08-25
last_updated: 2025-08-25
implementation_notes: 'Data quality framework successfully implemented with pandera/Great
  Expectations.

  CI integration working as designed. Prerequisite for PREDICTIONS_OUTPUTS completed.

  '
emit_metadata:
  source_id: dq_checks
  layer: Bronze
  input_path: data/bronze/
  notes: Data quality checks on joins and keys
---

# QLT-001: Data quality checks on joins and keys ✅ ACCEPTED

- **Overview**: As a data engineer, I want quality checks on join keys so that mismatches are caught early.
- **Value Proposition**: Prevents silent data loss or duplication from mis-joins.

## Acceptance Criteria ✅ ALL MET
- ✅ Checks for duplicate `game_id` rows; one-to-one joins validated between schedules, odds, and features.
- ✅ Missing keys reported with counts and sample rows.
- ✅ CI gate fails if key error rate exceeds threshold.

## Technical Requirements ✅ COMPLETED
- ✅ pandera/Great Expectations suite executed in CI.
- ✅ Per-source completeness stats logged.

## Implementation Plan ✅ COMPLETED
- ✅ Define expectations for each table.
- ✅ Implement CI step.
- ✅ Create sample failing tests to verify gating.

## Definition of Done ✅ ACHIEVED
- ✅ Quality report produced for each run.
- ✅ CI blocks on violations as configured.

## Outcome Summary
Data quality framework successfully implemented and operational. This foundation enabled the completion of PREDICTIONS_OUTPUTS story by ensuring data integrity throughout the pipeline.

## Related Features
ING-*, MOD-*, PREDICTIONS_OUTPUTS (unblocked and completed)

## Impact
With data quality issues resolved, the pipeline is ready for:
1. ✅ Model training and predictions (PREDICTIONS_OUTPUTS story - COMPLETED)
2. Additional data source integration
3. Advanced feature engineering
