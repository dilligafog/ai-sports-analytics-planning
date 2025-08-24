---
id: INF-002
epic: llm_backlog
status: active
owner: infra-team
priority: high
estimate: 1sp
dependencies: []
tags: [cli, busta]
market: null
layer: Infra
last_updated: 2025-08-24
emit_metadata:
  source_id: busta_integration
  layer: Infra
  input_path: bin/busta
  notes: CLI-first enforcement
---

# INF-002: Task runner integration (busta/CLI from repo root)

- **Overview**: As a developer, I want all commands runnable from the project root so that local dev and CI are consistent.
- **Value Proposition**: Eliminates path confusion and speeds iteration.

## Acceptance Criteria
- Single entrypoint script runs collection, training, inference, and report generation.
- Works from repo root; relative paths handled correctly.
- CI job executes smoke pipeline without path errors.

## Technical Requirements
- Implement `busta` or `make`-like task runner with Python entrypoint.
- Centralize paths via `Settings` class.
- Add integration tests that spawn subprocess from root.

## Implementation Plan
- Refactor CLI to use root-relative paths.
- Add tasks for each pipeline stage.
- Write CI job that runs end-to-end sample.

## Definition of Done
- `busta run sample` completes locally and in CI.
- No hardcoded subdir assumptions remain.

## Related Features
ING-*, MOD-*, UI-*
