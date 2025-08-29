---
id: UI-001
epic: llm_backlog
status: draft
owner: ui-team
priority: medium
estimate: 3sp
dependencies: [LLM-001]
tags: [ui, landing]
market: moneyline
layer: Web
last_updated: 2025-08-24
emit_metadata:
  source_id: ui_cards
  layer: Web
  input_path: web_build/data/
  notes: Landing page with daily games & confidence
---

# UI-001: Landing page with daily games & confidence

- **Overview**: As a user, I want a dashboard of today’s games with confidence and edges so that I can quickly scan opportunities.
- **Value Proposition**: Speeds decision-making and highlights top value bets.

## Acceptance Criteria
- List games for selected date; show ATS/ML/Total confidence, market line, model line, and edge.
- Filters: market type, minimum edge, hide abstains.
- Responsive; accessible; basic keyboard nav.

## Technical Requirements
- Static site (HTML/CSS/JS) consuming a JSON endpoint from the pipeline outputs.
- Simple client-side sorting and filtering.
- Dark mode support.

## Implementation Plan
- Define output JSON contract from inference pipeline.
- Build static UI and wire filters.
- Add smoke tests with sample data.

## Definition of Done
- Renders with fixture JSON; Lighthouse performance ≥ 90.
- Cross-browser check on latest Chrome/Firefox/Edge.

## Related Features
UI-002, MOD-004
