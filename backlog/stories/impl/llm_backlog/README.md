# LLM Backlog — Epic README

Purpose
- Short summary: coordinate LLM-related stories (ingest, features, infra, evaluation, UI) and provide common commands and milestones.

Goals
- Produce reliable, auditable LLM signals for model inputs.
- Provide evidence-citation and traceability for any LLM-derived features.
- Integrate signals into the existing 9-layer pipeline (Raw → Bronze → Silver → ...).

Milestones
- M1: Ingestion & enrichment (RSS, dedup, odds API) — ING-001..ING-003
- M2: LLM feature extraction + entity resolution — LLM-001..LLM-003
- M3: Evaluation and modeling lift studies — EVAL-001..MOD-003
- **M4: Social media expansion** — See `docs/stories/social_media/` (Phase 5)

Common busta commands

```bash
# Run ingestion normalization
busta pipeline data normalize-bronze

# Generate features for moneyline
busta features --market moneyline

# Run a quick local evaluation harness (example)
busta train --market moneyline
```

Where to start
- Review `docs/stories/_template.md` and add or update stories under this folder using the front-matter.
- Ensure each story includes `emit_metadata` when it has a data source.

Automation notes
- CI tooling will parse the YAML front-matter to surface status and owners; keep fields consistent.
