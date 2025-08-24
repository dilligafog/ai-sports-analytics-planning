# Story S07 — De-duplication & Cross-Post Collapsing

**Last Updated:** 2025-08-24 13:59:19

## Overview
As a data engineer, I want to detect duplicates and cross-posts across RSS, X, and Bluesky so that downstream views don’t double-count stories.

## Value Proposition
Cleaner analytics; saner UI; avoids skewed engagement metrics.

## Acceptance Criteria
- Exact duplicates by provider id removed; near-dupes collapsed via URL canonicalization + text similarity.
- Cross-post grouping: link posts that share the same canonical URL or ≥0.9 similarity.
- `story_group_id` assigned and persisted for grouped items.

## Technical Requirements
- Files: `packages/data_pipeline/src/nfl_data_pipeline/transform/dedupe.py`
- Use MinHash or cosine similarity (tf-idf) on normalized text.
- URL canonicalizer (UTM stripping, t.co expansion).

## Implementation Plan
1. Implement URL canonicalization utilities with tests.
2. Implement text cleaning + similarity scoring; tune threshold.
3. Persist `story_group_id` and verify stable grouping across runs.

## Definition of Done
- In a mixed sample, duplicate rate reduced by ≥80% vs. raw; tests cover common near-dupe cases.

## Related Features
Social schema (S01); feed health (S09); UI surfacing.
