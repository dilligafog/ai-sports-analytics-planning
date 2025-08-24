# Story S03 — Twitter/X: Keyword & List Search

**Last Updated:** 2025-08-24 13:59:19

## Overview
As an analyst, I want keyword and list-based search on X so that we capture breaking news beyond the curated handles.

## Value Proposition
Broader coverage for emergent stories (injuries, trades, suspensions).

## Acceptance Criteria
- Config supports `x.search.queries` with boolean operators and required hashtags/mentions.
- Per-query limits and cooldowns; language filter enforced.
- Posts pass relevance filter (teams/players/league terms) before normalization.

## Technical Requirements
- Extend `social_x.py` with search client.
- Enforce cool-downs by query; `state/social_x_search.json` for per-query cursors.
- Integration with `relevance_filter.py` (S06).

## Implementation Plan
1. Add search iterator with paging & `since_time`/`since_id` as supported.
2. Integrate relevance filter prior to bronze write.
3. Tests: query parsing, rate-limit handling, and dedupe with S07.

## Definition of Done
- At least one query per division returns posts; noise rate <30% in manual sample review.

## Related Features
Relevance filter (S06); moderation; dedupe (S07).
