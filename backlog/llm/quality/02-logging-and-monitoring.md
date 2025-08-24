---
id: QLT-002
epic: llm_backlog
status: draft
owner: qa-team
priority: medium
estimate: 2sp
dependencies: []
tags: [logging, monitoring]
market: null
layer: Infra
last_updated: 2025-08-24
emit_metadata:
  source_id: logging_monitoring
  layer: Infra
  input_path: logs/
  notes: Structured logging & lightweight monitoring
---

# QLT-002: Structured logging & lightweight monitoring

- **Overview**: As an operator, I want structured logs and simple dashboards so that I can spot failures and slowdowns.
- **Value Proposition**: Cuts time-to-detect and time-to-fix for pipeline issues.

## Acceptance Criteria
- All jobs emit structured logs (JSON) including timing, counts, and error summaries.
- Basic dashboard (e.g., local Streamlit or simple HTML) shows last runs and KPIs.
- Alerts for repeated failures or missing new data for >6h.

## Technical Requirements
- Python `logging` with JSON formatter; logrotate/size caps.
- Small status page reading from `data/logs/` artifacts.
- Optional webhook/email for alerts (configurable).

## Implementation Plan
- Add logging utilities and context IDs.
- Create status page and simple alert hooks.
- Document ops playbook for common errors.

## Definition of Done
- Status page reflects latest run; alert fires on simulated failure.
- Logs searchable and compact.

## Related Features
INF-002, ING-*, LLM-*
