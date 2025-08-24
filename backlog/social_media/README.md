# Social Media Sources — User Stories

**Generated:** 2025-08-24 13:59:19  
**Refined:** 2025-08-24 (Updated for current architecture)

This collection contains 12 ready-to-implement user stories for adding Twitter/X and Bluesky as social news sources to the NFL Predictions project.

## Architecture Alignment

These stories align with our current **9-layer data architecture**:
- **Raw Layer**: JSON social posts from APIs
- **Bronze Layer**: Normalized `SocialPost` schema 
- **Silver Layer**: Deduplicated, entity-linked posts
- **Gold Layer**: Relevance-filtered, ML-ready features

## Story Overview

### Foundation (S01-S02)
- **S01**: Core `SocialPost` schema and provider abstraction
- **S02**: Twitter/X curated account ingestion

### Data Collection (S03-S05)  
- **S03**: Twitter/X keyword and list search
- **S04**: Bluesky curated handles ingestion
- **S05**: Bluesky keyword and graph search

### Processing Pipeline (S06-S08)
- **S06**: Relevance filtering and entity linking
- **S07**: Deduplication and cross-platform post collapsing
- **S08**: Scheduling, rate limits, and checkpointing

### Operations (S09-S11)
- **S09**: Feed health metrics and alerting
- **S10**: Compliance, configuration gating, and kill switches
- **S11**: UI/CLI for source configuration

### Evaluation (S12)
- **S12**: Measuring social signal lift in predictions

## Integration with Current System

### CLI Integration
Stories integrate with our `busta` CLI pattern:
```bash
busta pipeline collect social --provider x
busta pipeline collect social --provider bluesky
busta features --include-social  # Future enhancement
```

### Configuration
Extends our existing YAML config system:
- `config/social_sources.yaml` - Social platform configuration
- `config/entities.yaml` - NFL entity recognition

### Storage Layout
Follows our established data lake structure:
```
data/
├── raw/social/{x|bluesky}/YYYY/MM/DD/*.jsonl
├── bronze/social_posts/*.parquet  
├── silver/social_posts_processed/*.parquet
└── gold/social_features/*.parquet
```

## Implementation Priority

**Phase 1** (Foundation): S01, S02, S06  
**Phase 2** (Expansion): S03, S04, S08  
**Phase 3** (Operations): S07, S09, S10, S11  
**Phase 4** (Evaluation): S05, S12

## Next Steps

1. **Review and approve** stories in this PR
2. **Create tracking issues** for each story
3. **Begin implementation** with Phase 1 stories
4. **Update project backlog** with social media roadmap
