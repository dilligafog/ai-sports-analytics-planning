---
id: ADH-011
title: Code Style Inventory
epic: adhoc
status: accepted
priority: medium
effort: TBD
branch_name: adh-011-code-style-inventory
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# Code Style and Logging Inventory

This document tracks the status of code formatting and logging implementation across the codebase.
Last updated: August 21, 2025

## Style Guide
- New Format: Uses `from __future__ import annotations` and follows the new style guide
- Logging: Uses the centralized logging configuration via `logging_config.py`

## Packages Status

### packages/models/

| File | New Format | Logging | Notes |
|------|------------|---------|--------|
| src/models/cli.py | ✅ | ❌ | |
| src/models/training.py | ✅ | ❌ | |
| src/models/metrics.py | ❌ | ❌ | |
| src/models/brier.py | ❌ | ❌ | |
| src/models/roi.py | ❌ | ❌ | |

### packages/data_pipeline/

| File | New Format | Logging | Notes |
|------|------------|---------|--------|
| src/nfl_data_pipeline/cli.py | ❌ | ✅ | Main entry point |
| src/nfl_data_pipeline/config.py | ❌ | ✅ | Configuration handling |
| src/nfl_data_pipeline/logging_config.py | ❌ | ✅ | Core logging setup |
| src/nfl_data_pipeline/stages/normalize.py | ❌ | ❌ | |
| src/nfl_data_pipeline/stages/integrate.py | ❌ | ❌ | |
| src/nfl_data_pipeline/stages/features.py | ❌ | ❌ | |
| src/nfl_data_pipeline/sources/feed_health.py | ❌ | ✅ | |
| src/nfl_data_pipeline/sources/kaggle_importer.py | ❌ | ✅ | |

### packages/features/

| File | New Format | Logging | Notes |
|------|------------|---------|--------|
| src/features/cli.py | ✅ | ✅ | CLI interface for feature generation |
| src/features/metrics.py | N/A | N/A | File does not exist yet |

## Action Items

1. Update all model-related files to use logging
2. Update data pipeline stages to use both new format and logging
3. Update feature engineering package to use both new format and logging
4. Ensure all new files follow both standards

## How to Update

1. Add to top of file:
   ```python
   from __future__ import annotations
   ```

2. Replace print statements with logging:
   ```python
   from ..logging_config import setup_logging, get_component_logger
   logger = get_component_logger(__name__)
   
   # Use logger instead of print
   logger.info("Processing started")
   logger.debug("Detailed info for debugging")
   logger.warning("Warning message")
   logger.error("Error message")
   ```

## Notes
- All new files should include both the new format annotation and proper logging
- When updating existing files, both changes should be made together
- Test coverage should be maintained when making these changes
