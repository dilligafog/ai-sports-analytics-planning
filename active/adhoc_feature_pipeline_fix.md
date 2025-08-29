# ADH-FPF: Feature Pipeline Fix for Live Predictions

## Background
The ensemble system implementation revealed critical issues with the feature pipeline for live predictions. While the ensemble training works perfectly with historical data, prediction generation fails for future games.

## Problem Statement
- **Zero Features Issue**: Week 18 games have all rolling features = 0.0
- **No Rolling Averages**: Future games lack historical rolling statistics
- **Data Corruption**: "False" team names in prediction data
- **Pipeline Disconnect**: Training uses historical features, prediction uses incomplete features

## Root Cause
The feature generation pipeline calculates rolling averages from completed games, but upcoming games don't have the necessary historical context for meaningful features.

## Acceptance Criteria

### 🎯 Core Features
- [ ] **Current Season Feature Calculator** - Generate rolling averages from 2025 season games completed so far
- [ ] **Future Game Feature Pipeline** - Create meaningful features for upcoming games using available data
- [ ] **Data Quality Validation** - Fix corrupted team names and validate data integrity
- [ ] **Feature Consistency** - Ensure training and prediction use same feature calculation methods

### 🔧 Technical Requirements
- [ ] **Rolling Average Calculator** - Update Week N games with stats from Weeks 1 through N-1
- [ ] **Team Season Stats** - Calculate current season statistics for each team
- [ ] **Feature Alignment** - Ensure 14 ensemble features are properly calculated for all games
- [ ] **Data Pipeline Integration** - Update gold layer feature generation for live data

### 📊 Quality & Testing
- [ ] **Feature Validation** - Verify all ensemble features are non-zero for current season games
- [ ] **Prediction Testing** - Confirm ensemble predictions work with properly calculated features
- [ ] **Data Integrity** - Fix team name corruption and validate all team mappings
- [ ] **End-to-End Testing** - Full pipeline test from raw data to ensemble predictions

## Success Metrics
- ✅ Ensemble models generate meaningful predictions (not ~50/50)
- ✅ All 14 ensemble features have realistic values for upcoming games
- ✅ No "False" or corrupted team names in prediction output
- ✅ Feature values consistent between training and prediction pipelines

## Technical Implementation

### Phase 1: Current Season Feature Calculation
- Update feature generation to use 2025 season games for rolling averages
- Calculate team performance metrics from completed games
- Ensure proper chronological ordering for rolling statistics

### Phase 2: Future Game Pipeline
- Create feature calculator for upcoming games using current season data
- Implement proper team performance context for predictions
- Validate feature ranges and distributions

### Phase 3: Integration & Testing
- Update ensemble CLI to use corrected features
- Test full pipeline from feature generation to ensemble predictions
- Validate prediction quality and model confidence

## Dependencies
- Requires access to 2025 season game results through current week
- Depends on gold layer data quality and team name standardization
- Needs ensemble system from previous story (ADH-005)

## Risk Assessment
- **Low Risk**: Feature calculation logic is straightforward
- **Medium Risk**: Data quality issues may require investigation
- **Validation**: Full end-to-end testing required before deployment

## Expected Outcome
A fully functional feature pipeline that enables the ensemble system to generate meaningful predictions for upcoming NFL games, with proper rolling averages calculated from the current season's completed games.

## Story Points
**8 points** - Complex data pipeline work with quality validation requirements

## Priority
**High** - Blocks ensemble system from being production-ready

## Labels
- `data-pipeline`
- `feature-engineering` 
- `ensemble-system`
- `bug-fix`
- `high-priority`
