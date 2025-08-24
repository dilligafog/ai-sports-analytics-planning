---
id: INF-004
epic: llm_backlog
status: draft
owner: infra-team
priority: high
estimate: 2sp
dependencies: []
tags: [secrets, security]
market: null
layer: Infra
last_updated: 2025-08-24
emit_metadata:
  source_id: secrets_management
  layer: Infra
  input_path: null
  notes: Guidelines for key rotation
---

# INF-004: Secrets management & key rotation

- **Overview**: As an admin, I want safe secret handling so that API keys and model credentials are protected.
- **Value Proposition**: Reduces risk of key leaks and simplifies rotation.

## Acceptance Criteria
- All secret values come from env vars; `.env.example` documents names.
- Rotation guide in `docs/secrets.md`; rotation tested in CI via injected ephemeral keys.
- No secrets in logs or persisted prompts.

## Technical Requirements
- Use dotenv in local dev; GitHub Actions secrets in CI.
- Redaction middleware for logs and LLM audit files.
- Pre-commit scan for accidental secrets.

## Implementation Plan
- Implement secrets loader and redaction.
- Add CI checks and docs.
- Run rotation drill and document steps.

## Definition of Done
- Secret scans clean; audit logs show redacted tokens.
- Rotation executed successfully in test.

## Related Features
ING-003, LLM-002
