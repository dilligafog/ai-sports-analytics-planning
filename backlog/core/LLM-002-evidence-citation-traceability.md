---
id: LLM-002
epic: llm_backlog
status: draft
owner: team-llm
priority: high
estimate: 3sp
dependencies: [LLM-001]
tags: [llm, traceability, evidence]
market: null
layer: Silver
last_updated: 2025-08-24
emit_metadata:
  source_id: llm_outputs
  layer: Silver
  input_path: data/silver/llm_signals/
  notes: Store citations and provenance metadata
---

# LLM-002: Evidence citation & traceability for LLM outputs

- **Overview**: As a reviewer, I want each LLM-derived feature to include exact quotes and source URLs so that decisions are auditable.
- **Value Proposition**: Prevents over-trust in LLMs and enables quick human audits.

## Acceptance Criteria
- Every signal includes at least one `evidence` item with exact quote and URL.
- A `trace_id` is stored to link prompt → output → downstream model row.
- CLI `python -m src.cli audit llm-signal --trace-id <id>` reproduces the prompt/response payloads from logs.

## Technical Requirements
- Persist prompts/responses with redacted keys in `data/logs/llm_audit/`.
- Hash of cleaned article text + schema version as `trace_id`.
- Audit command reads logs and prints compact JSON.

## Implementation Plan
- Add middleware to log inputs/outputs.
- Create audit CLI and minimal viewer.
- Document privacy considerations and retention window.

## Definition of Done
- Random audit of 20 samples reconstructs evidence correctly.
- PII redaction verified when applicable.

## Related Features
LLM-001, EXP-001
