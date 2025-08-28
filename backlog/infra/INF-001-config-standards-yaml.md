---
id: INF-001
epic: llm_backlog
status: draft
owner: infra-team
priority: medium
estimate: 2sp
dependencies: []
tags: [config, yaml, pydantic]
market: null
layer: Infra
last_updated: 2025-08-24
emit_metadata:
  source_id: config_standards
  layer: Infra
  input_path: config/
  notes: YAML + pydantic standards
---

# INF-001: Configuration standards (YAML + pydantic)

- **Overview**: As a developer, I want consistent config patterns so that new sources and models are easy to add.
- **Value Proposition**: Consistency reduces defects and onboarding time.

## Acceptance Criteria
- All configs live under `config/` with pydantic validation.
- Secrets are never in YAML; environment variables or .env only.
- CLI validates config and prints helpful error messages.

## Technical Requirements
- Use `pydantic-settings`; provide `.env.example`.
- Schema versioning for critical configs (news sources, teams).
- Pre-commit hook to validate YAML.

## Implementation Plan
- Define pydantic models.
- Add validators and CLI `config doctor`.
- Document config locations and examples.

## Definition of Done
- `config doctor` passes on clean repo; fails with clear errors on bad files.
- Docs updated; sample configs included.

## Related Features
ING-001, LLM-003
