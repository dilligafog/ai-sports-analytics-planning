# Story S06 — Relevance Filter & Entity Linking for Social

**Last Updated:** 2025-08-24 13:59:19

## Overview
As a feature engineer, I want to filter and enrich social posts with detected teams/players so that only NFL-relevant content flows downstream.

## Value Proposition
Cuts noise; enables per-team feeds and model features (injury/lineup mentions).

## Acceptance Criteria
- Dictionary-driven matcher for team names, nicknames, tickers, player aliases.
- Optional simple NER (spaCy or rule-based) for player names; confidence score per post.
- Posts tagged with `teams[]`, `players[]`; off-topic posts dropped if below threshold.
- Unit tests cover ambiguous names (e.g., “Giants”), emojis, and hashtags.

## Technical Requirements
- Files: `packages/data_pipeline/src/nfl_data_pipeline/transform/relevance_filter.py`
- Config: `config/entities.yaml` (teams, aliases, stopwords).
- Optional dependency on spaCy small English model if enabled.

## Implementation Plan
1. Build token-normalized matcher; add emoji & hashtag normalization.
2. Add thresholding and confidence scoring.
3. Write tests with tricky nicknames and ambiguous city names.

## Definition of Done
- Precision ≥0.8 on a hand-labeled sample of 200 posts (document sample & results in repo).

## Related Features
Sentiment; dedupe; search stories (S03, S05).
