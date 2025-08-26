---
id: QLT-001
epic: llm_backlog
status: completed
owner: qa-team
priority: high
estimate: 2sp
dependencies: []
tags: [quality, data]
market: null
layer: Bronze
last_updated: 2025-08-25
emit_metadata:
  source_id: dq_checks
  layer: Bronze
  input_path: data/bronze/
  notes: Data quality checks on joins and keys
---

# QLT-001: Data quality checks on joins and keys ✅ COMPLETED

- **Overview**: As a data engineer, I want quality checks on join keys so that mismatches are caught early.
- **Value Proposition**: Prevents silent data loss or duplication from mis-joins.

## Acceptance Criteria
- Checks for duplicate `game_id` rows; one-to-one joins validated between schedules, odds, and features.
- Missing keys reported with counts and sample rows.
- CI gate fails if key error rate exceeds threshold.

## Technical Requirements
- pandera/Great Expectations suite executed in CI.
- Per-source completeness stats logged.

## Implementation Plan
- Define expectations for each table.
- Implement CI step.
- Create sample failing tests to verify gating.

## Definition of Done
- Quality report produced for each run.
- CI blocks on violations as configured.

## Related Features
ING-*, MOD-*, PREDICTIONS_OUTPUTS (unblocked)

## Next Steps
With data quality issues resolved, the pipeline is ready for:
1. Model training and predictions (PREDICTIONS_OUTPUTS story)
2. Additional data source integration
3. Advanced feature engineering
