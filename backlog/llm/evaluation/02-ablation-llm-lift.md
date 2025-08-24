---
id: EVAL-002
epic: llm_backlog
status: draft
owner: evaluation-team
priority: high
estimate: 3sp
dependencies: [EVAL-001]
tags: [evaluation, ablation]
market: null
layer: Analysis
last_updated: 2025-08-24
emit_metadata:
  source_id: ablation_studies
  layer: Analysis
  input_path: runs/ablation/
  notes: Ablation and lift measurement for LLM features
---

# EVAL-002: Ablation studies for LLM feature lift

- **Overview**: As a researcher, I want ablation experiments so that we know what LLM features actually help.
- **Value Proposition**: Prevents cost and complexity from unjustified features.

## Acceptance Criteria
- Run (Base), (Base+Market), (Base+Market+LLM minimal), (Base+Market+LLM full).
- Report per-market lift with confidence intervals.
- Keep features that pass a pre-agreed lift threshold and cost budget.

## Technical Requirements
- Bootstrap CIs; cost per 1k tokens tracked for each experiment.
- Config-driven feature toggles.
- Results written to `reports/ablation_llm.md`.

## Implementation Plan
- Add toggles and evaluator hooks.
- Run experiments on a past season sample.
- Summarize results and decide keep/drop list.

## Definition of Done
- Report published; keep/drop list committed.
- Pipeline uses only kept features by default.

## Related Features
LLM-001, MOD-002
