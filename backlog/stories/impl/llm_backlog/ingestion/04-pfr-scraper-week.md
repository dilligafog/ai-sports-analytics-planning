---
id: ING-004
epic: llm_backlog
status: draft
owner: team-data
priority: medium
estimate: 2sp
dependencies: []
tags: [ingestion, pfr]
market: null
layer: Bronze
last_updated: 2025-08-24
emit_metadata:
  source_id: pfr_scraper
  layer: Bronze
  input_path: data/raw/pfr/
  notes: Weekly schedule and team stats
---

# ING-004: PFR weekly schedule & team stats scraper

- **Overview**: As a data scientist, I want structured schedule and recent team performance so that models can leverage form and matchup context.
- **Value Proposition**: Provides ground truth schedule and simple rolling stats without vendor lock-in.

## Acceptance Criteria
- `python -m src.cli collect pfr-week` writes `data/bronze/pfr_week_raw.parquet`.
- Transform step computes last-5 rolling efficiency stats for offense/defense.
- Keys: `game_id, week, season, home_team, away_team, kickoff_et`.

## Technical Requirements
- Respect robots.txt and polite delay.
- Cache pages to disk; parse with lxml/BeautifulSoup.
- Unit tests for 2 sample weeks.

## Implementation Plan
- Scrape schedule and stats tables; build parsers.
- Derive features; write to silver/gold tables.
- Link to odds and LLM signals via `game_id`.

## Definition of Done
- Schemas documented; joins validated on 100% of upcoming games.
- CI task scrapes a small sample during tests.

## Related Features
MOD-001, MOD-002, LLM-001
