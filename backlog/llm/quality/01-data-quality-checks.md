---
id: QLT-001
epic: llm_backlog
status: draft
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
  notes: Data quality checks with smart CI integration
---

# QLT-001: Data quality checks on joins and keys

- **Overview**: As a data engineer, I want quality checks on join keys so that mismatches are caught early.
- **Value Proposition**: Prevents silent data loss or duplication from mis-joins.

## Acceptance Criteria
- **Smart CI Integration**: CI checks only run when data is actually available
- **Data Detection**: CI automatically detects if data directories/files exist before attempting validation
- **Local/Production Focus**: Primary quality checks run in local development and production environments
- **CI Code Validation**: CI validates data quality check code itself (unit tests, syntax, imports)
- **Sample Data Testing**: CI uses small sample datasets for testing validation logic
- Missing keys reported with counts and sample rows when data is present

## Technical Requirements
- **Conditional CI**: `if [ -d "data/bronze" ]; then run_quality_checks; else echo "No data - skipping"; fi`
- **Sample Data**: Include small test datasets in repo for CI validation of check logic
- **Unit Tests**: Test data quality functions with mock/sample data in CI
- **Production Integration**: Full quality checks run during actual data pipeline execution
- **Environment Detection**: Detect if running in CI vs local/production environment

## Implementation Plan
1. **Create quality check framework** with environment detection
2. **Add sample test data** (small files) to repo for CI testing
3. **Implement conditional CI step** that checks for data availability first
4. **Write unit tests** for quality check functions using sample data
5. **Integrate with production pipeline** for full data validation

## Definition of Done
- **CI passes** when no data is present (doesn't fail on missing data)
- **CI validates** quality check code using sample data
- **Production quality checks** run when actual data pipeline executes
- **Unit tests** verify quality check logic works correctly
- **Documentation** explains when/where quality checks run

## Related Features
ING-*, MOD-*
