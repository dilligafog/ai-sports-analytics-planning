---
id: UI-002
epic: llm_backlog
status: draft
owner: ui-team
priority: medium
estimate: 3sp
dependencies: [LLM-002, UI-001]
tags: [ui, game-detail]
market: moneyline
layer: Web
last_updated: 2025-08-24
emit_metadata:
  source_id: game_detail_ui
  layer: Web
  input_path: web_build/predictions/
  notes: Game detail page with rationale and signals
---

# UI-002: Game detail page with rationale and signals

- **Overview**: As a user, I want a per-game detail view so that I can see why a pick is recommended.
- **Value Proposition**: Transparency improves trust and lets power users dig in.

## Acceptance Criteria
- Show calibrated probabilities, edges vs market, top contributing features.
- Display LLM evidence quotes with links; show abstain reasons when applicable.
- Export view as PDF with timestamp and model version.

## Technical Requirements
- Client renders explanation JSON and evidence list.
- Print CSS for PDF; include watermark with model version.
- Error states for missing data.

## Implementation Plan
- Define JSON for detail view (EXP-001).
- Build components and routing.
- Add export-to-PDF button.

## Definition of Done
- Detail view matches sample; PDF export verified.
- Unit tests for rendering edge cases.

## Related Features
EXP-001, MOD-002, LLM-002
