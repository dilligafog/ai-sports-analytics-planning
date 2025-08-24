---
id: EXP-001
epic: llm_backlog
status: draft
owner: explainability-team
priority: medium
estimate: 2sp
dependencies: [LLM-002]
tags: [explainability, ui]
market: null
layer: Predictions
last_updated: 2025-08-24
emit_metadata:
  source_id: explanations
  layer: Predictions
  input_path: web_build/predictions/
  notes: Grounded explanation cards for picks
---

# EXP-001: Grounded explanation cards for picks

- **Overview**: As an end user, I want concise explanations tied to data so that I trust the recommended picks.
- **Value Proposition**: Converts numbers into understandable narratives without hallucinations.

## Acceptance Criteria
- Explanations limited to 3 bullets + 1 risk; all claims supported by feature values or evidence quotes.
- Strict grounding: tool may only reference fields passed in the payload, with evidence URLs whitelisted from our dataset.
- Temperature=0; JSON schema enforced for the explanation payload.

## Technical Requirements
- Prompt template that lists allowed fields; refusal when unknown.
- Render to UI card with links to evidence.
- Unit tests comparing generated text vs allowed inputs.

## Implementation Plan
- Define explanation schema and prompt.
- Implement `llm_explain.pick_card()`.
- Wire to UI detail page and export to PDF.

## Definition of Done
- No hallucinations in 50-sample audit.
- Average word count under 90 words; all links functional.

## Related Features
UI-002, LLM-002
