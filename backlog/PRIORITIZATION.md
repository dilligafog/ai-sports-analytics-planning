# Story Prioritization List

**Purpose**: Prioritized task list for coding agents to select next work items  
**Last Updated**: 2025-08-24  
**Total Stories**: 50  

## Quick Start for Implementation Agents

1. **Pick the first available story** from the "Ready to Start" section below
2. **Verify dependencies** are completed before beginning work
3. **Reference the story ID** in all commits and PRs (format: `feat(STORY-ID): description`)
4. **Update this planning repo** when work begins and completes
5. **Report outcomes** including lessons learned and follow-up needs

## Story Selection Criteria

Stories are prioritized by:
- **🚫 No blocking dependencies** (ready to start immediately)
- **🔥 High business impact** (pick accuracy, user confidence)
- **⚡ Foundation components** (unblock future work)
- **📊 Clear scope** (well-defined acceptance criteria)

---

## Ready to Start (No Dependencies)

### 🔥 High Priority - Start These First

**1. INF-004** - INF-004: Secrets management & key rotation
- **File**: `backlog/llm/infra/04-secrets-management.md`
- **Owner**: infra-team
- **Estimate**: 2sp
- **Epic**: llm_backlog
- **Tags**: secrets, security

**2. EVAL-002** - EVAL-002: Ablation studies for LLM feature lift
- **File**: `backlog/llm/evaluation/02-ablation-llm-lift.md`
- **Owner**: evaluation-team
- **Estimate**: 2sp
- **Epic**: llm_backlog
- **Tags**: evaluation, ablation

**3. ING-001** - ING-001: Expand and standardize News RSS sources
- **File**: `backlog/llm/ingestion/01-news-rss-sources.md`
- **Owner**: team-data
- **Estimate**: 2sp
- **Epic**: llm_backlog
- **Tags**: ingestion, rss

**4. ING-003** - ING-003: Odds API integration (moneyline, spread, totals, props)
- **File**: `backlog/llm/ingestion/03-odds-api-integration.md`
- **Owner**: team-data
- **Estimate**: 2sp
- **Epic**: llm_backlog
- **Tags**: ingestion, odds

**5. MOD-005** - MOD-005: Feature store schema & lineage
- **File**: `backlog/llm/modeling/05-feature-store-schema.md`
- **Owner**: feature-store-team
- **Estimate**: 4sp
- **Epic**: llm_backlog
- **Tags**: feature-store, schema

**6. MODEL_TRAINING_EVALUATION** - User Story: Model Training & Evaluation
- **File**: `backlog/models/MODEL_TRAINING_EVALUATION.md`
- **Owner**: TBD
- **Estimate**: Not specified
- **Epic**: modeling
- **Tags**: modeling, evaluation

**7. NFL_PLAYER_INJURY_DATA_INTEGRATION** - User Story: NFL Player Injury Data Integration
- **File**: `backlog/models/NFL_PLAYER_INJURY_DATA_INTEGRATION.md`
- **Owner**: TBD
- **Estimate**: Not specified
- **Epic**: ingestion
- **Tags**: injury, data

**8. PREDICTIONS_OUTPUTS** - User Story: Predictions & Outputs
- **File**: `backlog/models/PREDICTIONS_OUTPUTS.md`
- **Owner**: TBD
- **Estimate**: Not specified
- **Epic**: predictions
- **Tags**: outputs, infra

**9. QLT-001** - QLT-001: Data quality checks on joins and keys
- **File**: `backlog/llm/quality/01-data-quality-checks.md`
- **Owner**: qa-team
- **Estimate**: 2sp
- **Epic**: llm_backlog
- **Tags**: quality, data

### 📋 Medium Priority - Next in Queue

**13. ADVANCED_NFL_STATISTICS_INTEGRATION** - User Story: Advanced NFL Statistics Integration
- **File**: `backlog/models/ADVANCED_NFL_STATISTICS_INTEGRATION.md`
- **Owner**: TBD
- **Estimate**: Not specified
- **Epic**: analytics

**14. AI_GENERATED_SALES_PITCH** - User Story: AI-Generated Sales Pitch
- **File**: `backlog/ui/AI_GENERATED_SALES_PITCH.md`
- **Owner**: TBD
- **Estimate**: Not specified
- **Epic**: ui_explainability

**15. DATA_SOURCE_INTEGRATION_FRAMEWORK** - User Story: Data Source Integration Framework
- **File**: `backlog/infrastructure/DATA_SOURCE_INTEGRATION_FRAMEWORK.md`
- **Owner**: TBD
- **Estimate**: Not specified
- **Epic**: infra

**16. INF-001** - INF-001: Configuration standards (YAML + pydantic)
- **File**: `backlog/llm/infra/01-config-standards-yaml.md`
- **Owner**: infra-team
- **Estimate**: 2sp
- **Epic**: llm_backlog

**17. INF-003** - INF-003: Caching & TTL for time-sensitive signals
- **File**: `backlog/llm/infra/03-caching-ttl.md`
- **Owner**: infra-team
- **Estimate**: 2sp
- **Epic**: llm_backlog

**18. ING-004** - ING-004: PFR weekly schedule & team stats scraper
- **File**: `backlog/llm/ingestion/04-pfr-scraper-week.md`
- **Owner**: team-data
- **Estimate**: 2sp
- **Epic**: llm_backlog

**19. PUBLIC_BETTING_DATA_INTEGRATION** - User Story: Public Betting Data Integration
- **File**: `backlog/models/PUBLIC_BETTING_DATA_INTEGRATION.md`
- **Owner**: TBD
- **Estimate**: Not specified
- **Epic**: ingestion

**20. QLT-002** - QLT-002: Structured logging & lightweight monitoring
- **File**: `backlog/llm/quality/02-logging-and-monitoring.md`
- **Owner**: qa-team
- **Estimate**: 2sp
- **Epic**: llm_backlog

**21. SCHEDULING_AUTOMATION** - User Story: Scheduling & Automation
- **File**: `backlog/infrastructure/SCHEDULING_AUTOMATION.md`
- **Owner**: TBD
- **Estimate**: Not specified
- **Epic**: infra

### 📝 Low Priority - Future Work

**22. KAGGLE_DATA_UTILIZATION** - User Story: Kaggle Data Utilization
- **File**: `backlog/models/KAGGLE_DATA_UTILIZATION.md`
- **Owner**: TBD
- **Estimate**: Not specified

**23. WEATHER_DATA_INTEGRATION** - User Story: Weather Data Integration
- **File**: `backlog/models/WEATHER_DATA_INTEGRATION.md`
- **Owner**: TBD
- **Estimate**: Not specified

### ❓ Priority Needs Review

**24. S** - Story S03 — Twitter/X: Keyword & List Search
- **File**: `backlog/social_media/S03_x_keyword_and_list_search.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**25. S** - Story S12 — Evaluation: Does Social Improve Predictions?
- **File**: `backlog/social_media/S12_evaluation_social_signal_lift.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**26. S** - Story S04 — Bluesky: Curated Handles Ingestion
- **File**: `backlog/social_media/S04_bluesky_curated_handles_ingestion.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**27. S** - Story S06 — Relevance Filter & Entity Linking for Social
- **File**: `backlog/social_media/S06_relevance_filter_and_entity_linking.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**28. S** - Story S01 — Social News Schema & Abstraction
- **File**: `backlog/social_media/S01_social_news_schema_and_abstraction.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**29. S** - Story S07 — De-duplication & Cross-Post Collapsing
- **File**: `backlog/social_media/S07_dedup_and_crosspost_collapsing.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**30. S** - Story S09 — Feed Health, Metrics & Alerting for Social
- **File**: `backlog/social_media/S09_feed_health_metrics_alerting.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**31. S** - Story S05 — Bluesky: Keyword/Graph Search
- **File**: `backlog/social_media/S05_bluesky_keyword_and_graph_search.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**32. S** - Story S02 — Twitter/X: Curated Accounts Ingestion
- **File**: `backlog/social_media/S02_x_curated_accounts_ingestion.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**33. S** - Story S10 — Compliance, Config Gating & Kill-Switch
- **File**: `backlog/social_media/S10_compliance_config_gating_killswitch.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**34. S** - Story S11 — UI/CLI Surfacing & Source Configuration
- **File**: `backlog/social_media/S11_ui_cli_source_configuration.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

**35. S** - Story S08 — Scheduling, Rate-Limits, Secrets & Checkpointing
- **File**: `backlog/social_media/S08_scheduling_ratelimits_secrets_checkpointing.md`
- **Owner**: TBD
- **Note**: Priority needs to be assigned

---

## Blocked by Dependencies

These stories require other work to be completed first:

**INF-005** - INF-005: LLM provider failover and model versioning (high)
- **Dependencies**: LLM-001
- **File**: `backlog/llm/infra/05-llm-provider-failover.md`

**ING-002** - ING-002: Article deduplication & enrichment pipeline (high)
- **Dependencies**: ING-001
- **File**: `backlog/llm/ingestion/02-article-dedup-enrich.md`

**LLM-001** - LLM-001: LLM extraction of game signals from news (high)
- **Dependencies**: ING-001, ING-002
- **File**: `backlog/llm/llm/01-feature-extraction-from-news.md`

**LLM-002** - LLM-002: Evidence citation & traceability for LLM outputs (high)
- **Dependencies**: LLM-001
- **File**: `backlog/llm/llm/02-evidence-citation-and-traceability.md`

**LLM-005** - LLM-005: Injury override & starter availability signal (high)
- **Dependencies**: NFL_PLAYER_INJURY_DATA_INTEGRATION
- **File**: `backlog/llm/llm/05-injury-override-signal.md`

**MOD-001** - MOD-001: Rebaseline ATS/ML/Total models with clean features (high)
- **Dependencies**: LLM-001, ING-002
- **File**: `backlog/llm/modeling/01-base-ats-model.md`

**MOD-006** - MOD-006: Production model calibration monitoring (high)
- **Dependencies**: MOD-001, MOD-002
- **File**: `backlog/llm/modeling/06-calibration-monitoring.md`

**QLT-003** - QLT-003: Feature store monitoring and drift detection (high)
- **Dependencies**: MOD-005
- **File**: `backlog/llm/quality/03-feature-monitoring-drift.md`

**EXP-001** - EXP-001: Grounded explanation cards for picks (medium)
- **Dependencies**: LLM-002
- **File**: `backlog/llm/explain/01-llm-grounded-explanations.md`

**ING-005** - ING-005: Content quality scoring and filtering (medium)
- **Dependencies**: ING-001, ING-002
- **File**: `backlog/llm/ingestion/05-content-quality-filtering.md`

**LLM-003** - LLM-003: Entity resolution for teams and players (medium)
- **Dependencies**: ING-001
- **File**: `backlog/llm/llm/03-entity-resolution.md`

**LLM-004** - LLM-004: Regime-change detection from weekly summaries (medium)
- **Dependencies**: LLM-001, LLM-003
- **File**: `backlog/llm/llm/04-regime-change-detection.md`

**LLM-006** - LLM-006: Batch processing optimization for LLM features (medium)
- **Dependencies**: LLM-001, INF-003
- **File**: `backlog/llm/llm/06-batch-processing-optimization.md`

**MOD-002** - MOD-002: Meta-model stacker with LLM-aware weighting (medium)
- **Dependencies**: MOD-001
- **File**: `backlog/llm/modeling/02-stacker-meta-model.md`

**MOD-003** - MOD-003: Probability calibration & reliability curves (medium)
- **Dependencies**: MOD-001
- **File**: `backlog/llm/modeling/03-probability-calibration.md`

**MOD-004** - MOD-004: Abstention and do-not-bet logic (medium)
- **Dependencies**: MOD-003
- **File**: `backlog/llm/modeling/04-abstention-logic.md`

**UI-001** - UI-001: Landing page with daily games & confidence (medium)
- **Dependencies**: LLM-001
- **File**: `backlog/llm/ui/01-landing-page-cards.md`

**UI-002** - UI-002: Game detail page with rationale and signals (medium)
- **Dependencies**: LLM-002, UI-001
- **File**: `backlog/llm/ui/02-game-detail-page.md`

---

## Strategic Context

### Current Focus Areas
1. **Pick Accuracy** - Model improvements and data quality (14 stories)
2. **LLM Pipeline** - News ingestion and feature extraction (30 stories)  
3. **Infrastructure** - Platform reliability and automation (8 stories)
4. **Social Media** - Twitter/X and Bluesky integration (12 stories)

### Implementation Notes
- **Story Format**: Some stories use YAML frontmatter, others use simple markdown
- **Cross-Repo Links**: Reference implementation repo in commits: `github.com/dilligafog/ai-sports-analytics`
- **Estimates**: Stories with estimates use story points (sp) or days (d)
- **Status Tracking**: Update story status in planning repo when work progresses

### Automation
This file is auto-generated from story metadata. To regenerate:
```bash
python3 scripts/regenerate_prioritization.py
```

**Last Generated**: 2025-08-24 20:20:43
