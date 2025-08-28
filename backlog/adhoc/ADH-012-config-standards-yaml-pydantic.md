---
id: ADH-012
title: Config Standards Yaml Pydantic
epic: adhoc
status: accepted
priority: medium
effort: TBD
branch_name: adh-012-config-standards-yaml-pydantic
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# Configuration Standards (YAML + Pydantic)

## Overview
**User Story**: As a developer, I want consistent config patterns so that new sources and models are easy to add.

**Value Proposition**: Consistency reduces defects and onboarding time for LLM pipeline development.

## Acceptance Criteria
- [x] All configs live under `config/` with pydantic validation
- [x] Secrets are never in YAML; environment variables or .env only  
- [x] CLI validates config and prints helpful error messages
- [x] Schema versioning for critical configs (news sources, teams)
- [x] Pre-commit hook to validate YAML

## Technical Requirements
- Use `pydantic-settings` for configuration management
- Provide `.env.example` template for secrets
- Schema versioning for critical configs (news sources, teams)
- Pre-commit hook to validate YAML
- CLI command `busta config doctor` to validate configurations

## Implementation Plan
1. **Define pydantic models** for all config schemas
2. **Add validators and CLI** `busta config doctor` command
3. **Document config locations** and provide examples
4. **Set up pre-commit hooks** for YAML validation
5. **Migrate existing configs** to new standards

## Definition of Done
- [x] All configs use pydantic validation
- [x] `busta config doctor` command validates all configs
- [x] Documentation updated with config patterns
- [x] Pre-commit hooks validate YAML on commit
- [x] `.env.example` file created with all required secrets
- [x] Existing configs migrated to new standards

## Related Features
- Foundational for all LLM ingestion and processing stories
- Enables consistent configuration across data pipeline
- Supports future news RSS and odds API integration
