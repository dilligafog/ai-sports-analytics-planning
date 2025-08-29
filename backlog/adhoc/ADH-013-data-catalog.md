---
id: ADH-013
title: Data Catalog
epic: adhoc
status: accepted
priority: medium
effort: TBD
branch_name: adh-013-data-catalog
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# Data Catalog

## Data Documentation Standard

### Required Metadata Fields
- **Source**: Origin of the data (e.g., API, scraping, manual collection)
- **Update Frequency**: How often the data is updated
- **Schema Version**: Version of the data structure
- **Dependencies**: Other datasets required for processing
- **Quality Checks**: Required validations
- **Business Rules**: Key transformations/rules applied
- **Retention Policy**: How long to keep historical data
- **Primary Keys**: Key fields for unique identification
- **Last Updated**: When the data was last processed
- **Data Owner**: Team/person responsible for the data
- **Usage**: What models/analysis use this data

### Layer Specific Requirements

#### Raw Layer
- Original schema documentation
- Source system details
- Data freshness requirements
- Raw data format (CSV, JSON, etc.)

#### Bronze Layer
- Normalization rules applied
- Field name mapping
- Data type standardization
- Initial quality metrics

#### Silver Layer
- Integration logic
- Business rules applied
- Data quality metrics
- Relationship documentation

#### Gold Layer
- Feature definitions
- Aggregation rules
- Model-specific transformations
- Performance metrics

## Current Data Inventory

### Raw Layer

#### Kaggle Data (/data/raw/kaggle)
- Source: Kaggle NFL datasets
- Schema: TBD
- Update Frequency: Manual
- Contains:
  - game_scores/
  - betting_data/
  - player_stats/
  - team_stats/
  - career_logs/
  - draft_data/
  - play_by_play/

#### News (/data/raw/news)
- Source: RSS Feeds
- Schema: TBD
- Update Frequency: Daily

#### Odds API (/data/raw/odds_api)
- Source: External Odds API
- Schema: TBD
- Update Frequency: Real-time during season

### Bronze Layer (/data/bronze)
Normalized versions of raw data:
- betting/
- career_logs/
- draft_data/
- game_scores/
- news/
- play_by_play/
- player_stats/
- plays/
- processed/
- team_stats/

### Silver Layer (/data/silver)
Integrated datasets:
- games.parquet
- plays.parquet

### Gold Layer (/data/gold)
Feature-engineered datasets:
- ats_labels.parquet
- game_features.parquet

## Action Items

1. Create detailed metadata documentation for each dataset:
   - [ ] Document raw data sources
   - [ ] Document bronze layer transformations
   - [ ] Document silver layer integrations
   - [ ] Document gold layer features

2. Implement automated metadata collection:
   - [ ] Schema validation
   - [ ] Row counts and update timestamps
   - [ ] Data quality metrics

3. Create data lineage documentation:
   - [ ] Map data flow between layers
   - [ ] Document dependencies
   - [ ] Track transformations

4. Establish monitoring:
   - [ ] Data freshness checks
   - [ ] Quality metric tracking
   - [ ] Pipeline status tracking
