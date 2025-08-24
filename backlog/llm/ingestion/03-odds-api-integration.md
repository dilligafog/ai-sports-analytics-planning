---
id: ING-003
epic: llm_backlog
status: draft
owner: team-data
priority: high
estimate: 2sp
dependencies: []
tags: [ingestion, odds]
market: moneyline
layer: Raw
last_updated: 2025-08-24
emit_metadata:
  source_id: odds_api
  layer: Raw
  input_path: data/raw/odds/
  notes: Moneyline/spread/total feeds
---

# ING-003: Odds API integration (moneyline, spread, totals, props)

- **Overview**: As a modeler, I want market lines and implied probabilities so that our models can compare, calibrate, and generate actionable deltas.
- **Value Proposition**: Markets encode wisdom-of-crowds priors; comparing model vs market drives bet selection and risk controls.

## Acceptance Criteria
- CLI `python -m src.cli collect odds` saves `data/bronze/odds_raw.parquet`.
- Support for multiple books; schema includes `event_id, book, market, side, price, timestamp`.
- Derived fields: `implied_prob`, `vig_adjusted_prob` stored in silver layer.
- Join keys created between `event_id` and team/game dimension table.

## Technical Requirements
- Handle rate limits with backoff; cache identical requests for 60s.
- Create `data/silver/odds.parquet` with normalized columns.
- Support historical pulls where provider allows; otherwise snapshot current.

## Implementation Plan
- Implement provider client and auth.
- Transform to normalized schema and write tests.
- Add implied probability functions and vig removal per market.

## Definition of Done
- End-to-end run produces odds for all games scheduled next 7 days.
- Unit tests for prob math and join logic pass.
- Docs include supported books and markets.

## Related Features
MOD-002, EVAL-002
