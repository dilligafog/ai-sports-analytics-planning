---
id: ING-004
title: Playbook Data Sources
epic: ingestion
status: accepted
priority: medium
effort: TBD
branch_name: ing-004-playbook-data-sources
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# Step 2 — Data Sources Implementation

**Feature:** Data Ingestion from External Sources  
**Value:** Ingesting structured (odds, scores, PFR stats) and unstructured (news) data gives us the raw inputs for predictive models. Without reliable ingestion, no downstream modeling can occur.

## Steps
1. **Context** – We need to collect NFL-related data from multiple APIs and scrapers. Currently, nothing is wired to consistently fetch and store it.  
2. **Implementation** –  
   - Implement `odds_api` for odds, props, and scores.  
   - Implement `pfr_scraper` for historical stats.  
   - Implement `news_rss` for unstructured headlines.  
   - Implement `kaggle_importer` for historical packaged datasets.  
   - Store all outputs under `data/raw/<source>`.  
3. **Validation** – Run each collector manually and confirm files populate with non-empty results.  
4. **Next Impact** – With ingestion complete, we can unify these under one CLI (Step 3) and start building pipelines for feature engineering.
