---
id: ADHOC-FIX-001
title: Feature Pipeline Fix for Future Game Predictions
type: ad-hoc
status: ready
priority: high
effort: medium
labels: [critical, pipeline, features, ensemble]
created: 2025-08-29
author: developer
dependencies: []
---

# ADHOC-FIX-001: Feature Pipeline Fix for Future Game Predictions

## 🎯 Story Overview

**Critical Issue**: Ensemble prediction system fails for future games because rolling features are all zero (no historical context calculated for upcoming games).

**Impact**: Despite having a sophisticated ensemble system with 83.6% training accuracy, predictions for future games return meaningless ~50/50 probabilities.

## 🚨 Problem Statement

### Current State
- ✅ Ensemble system trains successfully with historical data
- ✅ Models achieve excellent accuracy on historical games
- ❌ Future game predictions fail due to missing rolling averages
- ❌ Week 18 games have all rolling features = 0.0
- ❌ Data corruption ("False" team names)

### Root Cause
The feature engineering pipeline calculates rolling averages only for historical games. Future games need:
1. **Rolling averages calculated** from current season performance
2. **Team performance metrics** aggregated through the season
3. **Data quality validation** to prevent corruption

## 🔧 Technical Requirements

### 1. Rolling Feature Calculation for Future Games
- Calculate `home_roll3_pf_mean`, `home_roll5_pf_mean` etc. from 2025 season data
- Implement forward-looking feature engineering pipeline
- Handle edge cases (early season games with limited history)

### 2. Data Quality Validation
- Fix "False" team name corruption in Week 18 data
- Add validation for team names and data integrity
- Implement data quality checks in feature pipeline

### 3. Feature Pipeline Integration
- Ensure ensemble prediction pipeline uses properly calculated features
- Maintain consistency between training and prediction data sources
- Add logging and validation for feature quality

## 🎯 Success Criteria

### Primary Goals
- [ ] Week 18 games have meaningful rolling feature values (not all zeros)
- [ ] Ensemble predictions show realistic probabilities (not ~50/50)
- [ ] Data corruption issues resolved
- [ ] Feature calculation pipeline documented and tested

### Validation Tests
- [ ] `busta predict-ensemble 18` returns realistic predictions
- [ ] Rolling features have non-zero, sensible values
- [ ] Team names are valid NFL teams
- [ ] Confidence scores show meaningful variance

## 🛠️ Implementation Plan

### Phase 1: Data Investigation
1. Analyze current 2025 season data availability
2. Identify source of rolling feature calculations
3. Investigate "False" team name corruption

### Phase 2: Feature Engineering Fix
1. Implement rolling average calculation for future games
2. Update feature pipeline to handle forward-looking scenarios
3. Add data validation and quality checks

### Phase 3: Integration & Testing
1. Test ensemble predictions with fixed features
2. Validate prediction quality and realism
3. Document feature calculation process

## 📋 Technical Context

### Files Likely to Modify
- `packages/features/src/features/` - Feature engineering pipeline
- `data/gold/game_features.parquet` - Core feature data
- Feature calculation scripts and pipelines
- Data validation and quality checks

### Dependencies
- Existing ensemble system (completed)
- 2025 NFL season data
- Historical team performance data

## 🔄 Story Workflow

This is an **ADHOC** story created to address critical pipeline issues discovered during ensemble system testing. 

**Previous Context**: ENSEMBLE_SYSTEM story revealed feature pipeline gaps during end-to-end testing.

**Next Steps**: Fix feature calculation → Enable production ensemble predictions → Move to explainability phase.

---

**Priority**: HIGH - Blocks ensemble system from generating meaningful predictions
**Complexity**: MEDIUM - Feature engineering and data quality fixes
**Type**: ADHOC - Critical issue resolution
