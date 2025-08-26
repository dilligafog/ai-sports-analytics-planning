---
id: NFL_PLAYER_INJURY_DATA_INTEGRATION
epic: ingestion
status: in_progress
owner: implementation-team
priority: high
estimate: 5
dependencies: []
tags: [injury, data]
market: null
layer: Bronze
last_updated: 2025-08-25
implementation_notes: |
  Phase 1 COMPLETED: Foundation built with injury_data.py, injury_features.py, CLI integration
  Phase 2 IN PROGRESS: Data sources integration and enhancement
  Current: 11,764 Kaggle records + ESPN RSS configured + odds API ready
emit_metadata:
  source_id: injury_provider
  layer: Bronze
  input_path: data/raw/kaggle/play_by_play/injuries.csv
  notes: Multi-source injury aggregation with ML-ready features
---

# User Story: NFL Player Injury Data Integration

## Overview
**As a** betting analyst  
**I want** comprehensive player injury data integrated into our system  
**So that** I can assess the impact of injuries on game outcomes and betting lines

## Value Proposition
Injuries significantly impact game outcomes and betting lines. Integrating detailed player injury data allows for more accurate predictions and provides critical context for betting decisions.

## Acceptance Criteria
- System collects injury data from reliable sources (official NFL injury reports, third-party APIs)
- Data includes injury type, severity, player position, and expected return timeline
- Information is standardized and integrated into machine learning features
- Historical injury data is available for backtesting
- UI shows relevant injury information for upcoming games
- LLM can reference injury data when generating betting narratives

## Technical Requirements
- Implement data collection from injury report sources
- Create schema for injury data storage
- Develop feature engineering for injury impact (team strength adjustments)
- Integrate injury data into ML pipelines
- Expose injury data to UI and LLM components

## Implementation Plan
### ✅ Phase 1: Foundation (COMPLETED)
- ✅ Data Collection Module: `injury_data.py` - Multi-source injury data aggregation
- ✅ Feature Engineering: `injury_features.py` - Position-weighted impact scoring
- ✅ CLI Integration: `busta injuries collect|features|analyze` commands
- ✅ Data Schema: Standardized injury report structure with severity levels
- ✅ Infrastructure: 11,764 Kaggle records + ESPN RSS + odds API ready

### 🔄 Phase 2: Data Sources Enhancement (IN PROGRESS)
**Immediate Priority**: Integrate `nfl_data_py` package
- **`nfl.import_injuries(years)`** - Official NFL injury reports with standardized format
- **`nfl.import_depth_charts(years)`** - Player availability and starting status
- **`nfl.import_weekly_rosters(years)`** - Real-time roster changes and player status
- **Benefits**: Reliable, structured data from nflverse ecosystem (384⭐ on GitHub)
- **Installation**: `pip install nfl_data_py`

**Additional Source Research** (Implementation team investigating):
- SportsData.io NFL API - Premium injury reports with real-time updates
- Fantasy Sports APIs - Injury impact on player availability  
- Social Media Monitoring - Early injury news detection
- Team Beat Reporter Feeds - Local injury intelligence
- Medical Data Providers - Injury severity and recovery timelines

### 📊 Phase 3: ML Feature Engineering (DESIGNED)
- Position Impact Weights: QB (1.0), WR1 (0.8), LT (0.8), etc.
- Severity Multipliers: Out (1.0), Doubtful (0.8), Questionable (0.4)
- Team-Level Features: Total injury impact, offense/defense splits
- Game-Level Features: Injury advantage differentials

### 🎯 Phase 4: Integration Points (PLANNED)
- Gold Layer: `data/gold/injuries/` for ML-ready features
- Prediction Models: Injury impact in moneyline/ATS/OU predictions
- UI Dashboard: Key injury information display
- LLM Narratives: Injury context in betting explanations

## Definition of Done
- ✅ **Foundation Built**: injury_data.py, injury_features.py, CLI commands operational
- ✅ **Existing Data**: 11,764 Kaggle injury records integrated
- 🔄 **Enhanced Sources**: nfl_data_py integration for official NFL injury/depth/roster data
- 🔄 **ML Features**: Position-weighted injury impact features in gold layer
- 🔄 **Model Integration**: Injury features accessible to prediction models
- ⏳ **UI Integration**: Relevant injury information displayed for games
- ⏳ **LLM Enhancement**: Narratives include injury context and impact analysis

## Current Status & Next Steps
**Implementation Team Progress**: Solid foundation complete, now enhancing data sources
**Planning Recommendation**: Prioritize `nfl_data_py` integration - direct fit for current architecture
**Expected Impact**: 
- Betting accuracy improvement through injury-aware predictions
- Line movement detection for value betting opportunities
- Risk management for high injury uncertainty games
- Enhanced user experience with transparent injury context

## Related Features
- Data Source Integration Framework (will enhance)
- Feature Engineering (being enhanced)
- Predictions & Outputs (will be enhanced)
- **LLM-005**: Injury override & starter availability signal (blocked by this story)

## Research Notes for Implementation Team
**High-Priority Integration**: The `nfl_data_py` package provides exactly what you need:
```python
# Perfect fit for your current architecture
import nfl_data_py as nfl

# Official NFL injury reports (standardized format)
injury_data = nfl.import_injuries([2024, 2025]) 

# Depth charts (starter status, availability)
depth_charts = nfl.import_depth_charts([2024, 2025])

# Weekly rosters (real-time player status)
rosters = nfl.import_weekly_rosters([2024, 2025])
```

**Why This Package**: 
- 384⭐ GitHub, actively maintained by nflverse ecosystem
- Pandas DataFrames - fits your existing data pipeline
- Official NFL data source - reliable and consistent
- Complements your existing 11K+ Kaggle records perfectly
- Enables the blocked LLM-005 story for starter availability signals
