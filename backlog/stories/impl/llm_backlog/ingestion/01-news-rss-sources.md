---
id: ING-001
epic: llm_backlog
status: draft
owner: team-data
priority: high
estimate: 2sp
dependencies: []
tags: [ingestion, rss]
market: null
layer: Raw
last_updated: 2025-08-24
emit_metadata:
  source_id: rss_feeds
  layer: Raw
  input_path: data/raw/news_rss/
  notes: RSS sources list and normalization
---

# ING-001: Expand and standardize News RSS sources

- **Overview**: As a data engineer, I want dozens of curated NFL news RSS sources categorized for modeling relevance so that we can systematically ingest high-signal news.
- **Value Proposition**: More and better sources increase coverage of starter status, coach intent, and injuries that drive preseason and regular-season edges.

## Acceptance Criteria
- At least 50 unique RSS/Atom feeds configured across categories: Team beats, National outlets, Injury reports, Weather, and Fantasy/Depth Chart.
- Config lives in a single YAML file under `config/news_sources.yml` with fields: `id`, `name`, `url`, `category`, `priority`, `team_scope` (nullable), `active` (bool).
- Collector logs per-source fetch status, HTTP code, and item counts.
- Duplicate items across feeds are deduped by canonical URL + title hash.
- Daily run via CLI command `python -m src.cli collect news` populates `data/bronze/news_raw.parquet`.

## Technical Requirements
- Implement requests with conditional GET (ETag/Last-Modified).
- Normalize to schema: `source_id, fetched_at, published_at, title, url, author, summary, content_html, content_text, team_tags`.
- Use readability/boilerpipe-style extraction for `content_text`.
- Add basic HTML sanitizer and strip tracking query params for canonical URL.

## Implementation Plan
- Define YAML schema and validation (pydantic).
- Write `sources/news_rss.py` to read YAML and fetch feeds with backoff.
- Implement HTML → text extractor with fallback.
- Persist raw items to bronze; add dedup logic into silver layer.
- Add unit tests with 3–5 mocked feeds.

## Definition of Done
- YAML validated in CI; sample run produces >500 items across last 48h.
- Parquet schema documented in `docs/schemas/news_raw.md`.
- Logs include per-source metrics and error reasons.
- README updated with run instructions.

## Related Features
ING-002, LLM-001, LLM-003
