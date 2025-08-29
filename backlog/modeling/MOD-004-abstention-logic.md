---
id: MOD-004
epic: llm_backlog
status: draft
owner: modeling-team
priority: medium
estimate: 3sp
dependencies: [MOD-003]
tags: [modeling, abstention]
market: null
layer: Gold
last_updated: 2025-08-24
emit_metadata:
  source_id: abstention_logic
  layer: Gold
  input_path: models/abstention/
  notes: Abstention and do-not-bet rules
---

# MOD-004: Abstention and do-not-bet logic

- **Overview**: As a bettor, I want the system to pass on low-information or contradictory games so that we avoid negative-EV spots.
- **Value Proposition**: Fewer forced bets, higher realized edge.

## Acceptance Criteria
- Rules: abstain when LLM signals conflict or regime change flagged + high uncertainty.
- Minimum edge thresholds configurable per market (e.g., ≥ 2.5% over market).
- UI shows reason for abstention.

## Technical Requirements
- Edge computation vs vig-adjusted market probs.
- Uncertainty from model variance and LLM signal confidence.
- Expose `abstain_reason` in output API.

## Implementation Plan
- Define rules and thresholds; implement evaluator.
- Integrate into pick selection and UI display.
- Add tests for abstention scenarios.

## Definition of Done
- Backtest shows improved Sharpe and lower drawdowns.
- UI surfaces clear abstain reasons.

## Related Features
LLM-004, UI-002
