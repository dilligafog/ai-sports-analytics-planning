---
id: LLM-004
epic: llm_backlog
status: draft
owner: team-llm
priority: medium
estimate: 3sp
dependencies: [LLM-001, LLM-003]
tags: [llm, regime-detection]
market: null
layer: Gold
last_updated: 2025-08-24
emit_metadata:
  source_id: regime_detector
  layer: Gold
  input_path: data/silver/llm_signals/
  notes: Weekly summaries and regime-change flags
---

# LLM-004: Regime-change detection from weekly summaries

- **Overview**: As a modeler, I want the system to flag scheme/QB/coaching changes so that model priors adjust when the underlying team changes.
- **Value Proposition**: Prevents stale season-long assumptions from dominating predictions when context flips.

## Acceptance Criteria
- LLM tags weekly team summaries with `regime_change` boolean and category (e.g., QB change, OC tendency shift).
- Downstream pipeline widens uncertainty or shifts priors when flagged.
- Audit view shows before/after feature deltas for flagged teams.

## Technical Requirements
- Prompt LLM with rolling team reports (last 3 weeks).
- Simple rules to widen prediction intervals or adjust weights in stacker.
- Store flags in `data/gold/regime_flags.parquet`.

## Implementation Plan
- Generate weekly summaries per team.
- Design prompt and schema for flags.
- Wire into meta-model weight selection (see MOD-002).

## Definition of Done
- At least 10 historical known regime flips are detected in backtest.
- Downstream variance responds as expected in flagged weeks.

## Related Features
MOD-002, EVAL-002
