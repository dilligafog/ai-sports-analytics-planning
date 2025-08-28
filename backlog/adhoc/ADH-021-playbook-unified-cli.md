---
id: ADH-021
title: Playbook Unified Cli
epic: adhoc
status: accepted
priority: medium
effort: TBD
branch_name: adh-021-playbook-unified-cli
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# Step 3 — Unified CLI with Data Sources

**Feature:** Unified CLI with Data Sources  
**Value:** Having all data collection run through one CLI (`busta`) means we can manage odds, scores, props, PFR stats, and news consistently. This makes the pipeline predictable, reproducible, and easy to extend without patchwork scripts.

## Steps
1. **Context** – Right now, the code for sources (`odds_api`, `pfr_scraper`, `news_rss`, `kaggle_importer`) exists, but not everything is wired into the CLI cleanly. Running from the project root with `busta` should feel simple and consistent.  
2. **Implementation** –  
   - Update `cli.py` so each source has a `busta collect <source>` command.  
   - Ensure that each command writes raw data in the proper directory structure (`data/raw/<source>`).  
   - Confirm imports are project-root aware (no broken relative paths).  
   - Add logging so we can see counts of rows/events fetched after each run.  
3. **Validation** – From the project root, run:  
   ```bash
   busta collect odds
   busta collect scores
   busta collect pfr
   busta collect news
   ```  
   Each should create/update files in `data/raw/` and report summary stats.  
4. **Next Impact** – With all data flowing through one CLI, we’re ready to schedule recurring data pulls (Step 4) and start building training datasets consistently from gold features.
