# Story S11 — UI/CLI Surfacing & Source Configuration

**Last Updated:** 2025-08-24 13:59:19

## Overview
As a user, I want to manage social sources via config and run them from the CLI so I can iterate quickly without code edits.

## Value Proposition
Developer speed; reproducible runs.

## Acceptance Criteria
- `config/social_sources.yaml` supports: accounts, queries, language, lookback, limits, include_rt/replies, and per-provider options.
- CLI examples in README; dry-run flag prints planned calls without hitting APIs.
- Schema validation errors are friendly and actionable.

## Technical Requirements
- Files: `config/social_sources.yaml`, `README.md` updates.
- CLI: `busta pipeline collect social --provider {x|bluesky} --dry-run --since 90m`

## Implementation Plan
1. Add schema & validation for config (pydantic or voluptuous).
2. Implement `--dry-run` and `--since` flags.
3. Provide example config and sample commands in README.

## Definition of Done
- Example config committed; `busta pipeline collect social --dry-run` shows the plan without network calls.

## Related Features
Provider ingestion (S02–S05); compliance flags (S10).
