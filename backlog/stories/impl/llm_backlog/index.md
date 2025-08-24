---
id: LLM-BACKLOG
epic: llm_backlog
status: draft
owner: team-llm
priority: medium
estimate: null
dependencies: []
tags: [llm, backlog]
market: null
layer: null
last_updated: 2025-08-24
---

# NFL Predictions — LLM-Augmented Backlog
_Generated on 2025-08-24_

This page lists the epic-level backlog for LLM-augmented features and infra. Each story should follow the repository story template at `docs/stories/_template.md` (front-matter + sections) so tooling can parse and surface metadata automatically.

**Status**: 29 total stories across 7 functional areas (3 completed, 5 new stories added based on gap analysis)

## Table of Contents
- [ING-001: Expand and standardize News RSS sources](ingestion/01-news-rss-sources.md)
- [ING-002: Article deduplication & enrichment pipeline](ingestion/02-article-dedup-enrich.md)
- [ING-003: Odds API integration (moneyline, spread, totals, props)](ingestion/03-odds-api-integration.md)
- [ING-004: PFR weekly schedule & team stats scraper](ingestion/04-pfr-scraper-week.md)
- [ING-005: Content quality scoring and filtering](ingestion/05-content-quality-filtering.md)
- [LLM-001: LLM extraction of game signals from news](llm/01-feature-extraction-from-news.md)
- [LLM-002: Evidence citation & traceability for LLM outputs](llm/02-evidence-citation-and-traceability.md)
- [LLM-003: Entity resolution for teams and players](llm/03-entity-resolution.md)
- [LLM-004: Regime-change detection from weekly summaries](llm/04-regime-change-detection.md)
- [LLM-005: Injury override & starter availability signal](llm/05-injury-override-signal.md)
- [LLM-006: Batch processing optimization for LLM features](llm/06-batch-processing-optimization.md)
- [MOD-001: Rebaseline ATS/ML/Total models with clean features](modeling/01-base-ats-model.md)
- [MOD-002: Meta-model stacker with LLM-aware weighting](modeling/02-stacker-meta-model.md)
- [MOD-003: Probability calibration & reliability curves](modeling/03-probability-calibration.md)
- [MOD-004: Abstention and do-not-bet logic](modeling/04-abstention-logic.md)
- [MOD-005: Feature store schema & lineage](modeling/05-feature-store-schema.md)
- [MOD-006: Production model calibration monitoring](modeling/06-calibration-monitoring.md)
- [EXP-001: Grounded explanation cards for picks](explain/01-llm-grounded-explanations.md)
- [UI-001: Landing page with daily games & confidence](ui/01-landing-page-cards.md)
- [UI-002: Game detail page with rationale and signals](ui/02-game-detail-page.md)
- [INF-001: Configuration standards (YAML + pydantic)](infra/01-config-standards-yaml.md)
- [INF-002: Task runner integration (busta/CLI from repo root)](infra/02-task-runner-busta.md)
- [INF-003: Caching & TTL for time-sensitive signals](infra/03-caching-ttl.md)
- [INF-004: Secrets management & key rotation](infra/04-secrets-management.md)
- [INF-005: LLM provider failover and model versioning](infra/05-llm-provider-failover.md)
- [EVAL-001: Offline evaluation harness & metrics tracking](evaluation/01-offline-eval-metrics.md)
- [EVAL-002: Ablation studies for LLM feature lift](evaluation/02-ablation-llm-lift.md)
- [QLT-001: Data quality checks on joins and keys](quality/01-data-quality-checks.md)
- [QLT-002: Structured logging & lightweight monitoring](quality/02-logging-and-monitoring.md)
- [QLT-003: Feature store monitoring and drift detection](quality/03-feature-monitoring-drift.md)

## How to use this backlog

- Each story under this epic should include YAML front-matter and the standard sections from `docs/stories/_template.md`.
- Use the `busta` CLI for all runnable validation steps (see template). Examples below show common commands.

## Epic-level acceptance criteria

- Stories have machine-readable front-matter (id, owner, status, priority, estimate, tags, market, layer).
- Each story includes clear acceptance criteria and a done checklist.
- How-to-run steps use `busta` commands where applicable.
- **Phase-based delivery**: 29 stories organized into 4 phases (Foundation → Core → Enhancement → Experience)
- **Gap coverage**: Critical gaps identified and addressed with 5 new stories
- **Strategic alignment**: Implementation plan documented in `docs/proposals/LLM_BACKLOG_STRATEGIC_PLAN.md`

## Example busta commands (CLI-first)

```bash
# Run feature generation for moneyline (example)
busta features --market moneyline

# Run a pipeline step
busta pipeline data normalize-bronze

# Build/deploy web assets (epic-level docs or demo pages)
busta build-web
```

## Story template

Create new stories using `docs/stories/_template.md`. Stories missing required front-matter may be skipped by automation.

## Related issues / PRs

- (link to related issues or PRs here)

