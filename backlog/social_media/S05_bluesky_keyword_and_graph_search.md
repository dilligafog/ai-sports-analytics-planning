# Story S05 — Bluesky: Keyword/Graph Search

**Last Updated:** 2025-08-24 13:59:19

## Overview
As an analyst, I want keyword/hashtag search and simple graph expansion (followers of curated handles) on Bluesky to catch breaking items.

## Value Proposition
Captures emergent accounts and stories; improves recall.

## Acceptance Criteria
- Configurable `bluesky.search.queries` & optional “followees of” expansion.
- Relevance filter applied pre-persist; per-query rate-limit respected.
- Prevent uncontrolled growth of expanded handle set.

## Technical Requirements
- Extend `social_bluesky.py` with search and basic graph lookup.
- State tracking for expanded handles to avoid unbounded growth.
- Integration with relevance filter (S06).

## Implementation Plan
1. Implement search iterator; add simple “expand once” cache with TTL.
2. Integrate with S06 filter & S09 health logging.
3. Tests for graph expansion boundaries and state persistence.

## Definition of Done
- At least one query returns relevant posts across 2+ days; no explosion in handle count.

## Related Features
Relevance filter (S06); dedupe (S07); health (S09).
