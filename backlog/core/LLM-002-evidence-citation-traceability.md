---
id: LLM-002
epic: llm_backlog
status: backlog
owner: team-llm
priority: high
estimate: 2sp
dependencies: [LLM-001]
tags: [llm, traceability, evidence]
market: null
layer: Silver
last_updated: 2025-08-29
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
- [ ] **Evidence Requirements**: Every signal includes at least one `evidence` item with exact quote and URL.
- [ ] **Traceability**: A `trace_id` is stored to link prompt → output → downstream model row.
- [ ] **Audit CLI**: CLI `python -m src.cli audit llm-signal --trace-id <id>` reproduces the prompt/response payloads from logs.
- [ ] **PII Redaction**: Sensitive information automatically redacted from stored logs.
- [ ] **Performance**: Audit queries return results in < 2 seconds.

## Technical Requirements
- [ ] Persist prompts/responses with redacted keys in `data/logs/llm_audit/`.
- [ ] Hash of cleaned article text + schema version as `trace_id`.
- [ ] Audit command reads logs and prints compact JSON.
- [ ] Automatic log rotation after 30 days.
- [ ] GDPR-compliant data handling.

## Implementation Plan
1. **Week 1**: Add middleware to log inputs/outputs with redaction
2. **Week 2**: Create audit CLI and minimal viewer
3. **Week 3**: Document privacy considerations and retention policies

## Definition of Done
- [ ] Random audit of 20 samples reconstructs evidence correctly.
- [ ] PII redaction verified when applicable.
- [ ] All team members can use audit CLI successfully.
- [ ] Documentation covers privacy and compliance requirements.

## Related Features
LLM-001, EXP-001
