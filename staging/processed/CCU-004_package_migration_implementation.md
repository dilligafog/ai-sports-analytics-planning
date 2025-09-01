---
id: CCU-004
title: Implement Package-by-Package Config Migration
epic: infrastructure
status: backlog
priority: high
estimate: "8sp"
dependencies: [CCU-003]
labels: [code-cleanup, migration, high-risk]
created: 2025-09-01
author: planning-agent
owner: ""
layer: null
---

# CCU-004: Implement Package-by-Package Config Migration

## Story Overview
**Story ID**: CCU-004
**Epic**: Code Clean Up - Migration Implementation
**Priority**: HIGH
**Effort**: Medium (1-2 weeks)
**Type**: Implementation
**Status**: Ready

## Background
Following the human decision in HUM-CDR-015, we need to implement the package-by-package migration strategy from config.py to config_v2.py. The analysis in CDR-005 series identified 26 affected files organized in logical packages.

## Acceptance Criteria
- [ ] Core config package migrated and validated
- [ ] Data pipeline packages migrated and validated
- [ ] Models packages migrated and validated
- [ ] Scripts and utilities migrated and validated
- [ ] All migrations follow dependency order from CDR-005 analysis
- [ ] Package-specific smoke tests pass for each migrated package
- [ ] Dual repo sync validation completed

## Implementation Plan
1. **Core config package** (foundational dependencies)
2. **Data pipeline packages** (dependent on core)
3. **Models packages** (dependent on pipeline)
4. **Scripts and utilities** (least dependencies)

## Technical Details
- Follow the migration pattern established in CDR-008 (backtesting pilot)
- Update imports: `from nfl_data_pipeline.config import create_settings` → `from nfl_data_pipeline.config_v2 import create_settings`
- Update variable naming: `settings` → `config`
- Preserve compatibility patterns for gradual migration
- Add REFACTOR_AUDIT logging as per HUM-CDR-016

## Risk Assessment
- **Medium Risk**: Affects multiple packages but isolated by package boundaries
- **Mitigation**: Package-by-package approach allows rollback per package
- **Validation**: Dual repo safety net and smoke tests per package</content>
<parameter name="filePath">/home/bustabook/ai-sports-analytics-planning/proposals/CDR-stories/CDR-MIG-001_package_migration_implementation.md
