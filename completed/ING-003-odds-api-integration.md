---
id: ING-003
epic: llm_backlog
status: completed
owner: team-data
priority: high
estimate: 2sp
dependencies: []
tags: [ingestion, odds]
market: moneyline
layer: Raw
last_updated: 2025-08-24
completed_date: 2025-08-24
emit_metadata:
  source_id: odds_api
  layer: Raw
  input_path: data/raw/odds/
  notes: Moneyline/spread/total feeds
---

# ING-003: Odds API integration (moneyline, spread, totals, props) ✅ COMPLETED

- **Overview**: As a modeler, I want market lines and implied probabilities so that our models can compare, calibrate, and generate actionable deltas.
- **Value Proposition**: Markets encode wisdom-of-crowds priors; comparing model vs market drives bet selection and risk controls.

## Acceptance Criteria ✅ ALL COMPLETE
- ✅ CLI `busta pipeline collect odds` saves odds data (modern CLI pattern)
- ✅ Support for multiple books; schema includes `event_id, book, market, side, price, timestamp`
- ✅ Derived fields: `implied_prob`, `vig_adjusted_prob` calculated in features layer
- ✅ Join keys created between `event_id` and team/game dimension table

## Technical Requirements ✅ ALL COMPLETE  
- ✅ Handle rate limits with backoff; 0.8s sleep between requests
- ✅ Create `data/silver/odds_api/odds/YYYY-MM-DD/data.parquet` with normalized columns
- ✅ Support historical pulls with date filtering

## Implementation Status ✅ PRODUCTION READY
- ✅ Provider client and auth implemented (`OddsApiClient`)
- ✅ Normalized schema with proper error handling
- ✅ Implied probability functions and vig removal (`moneyline_to_prob`, `normalize_two_way`)
- ✅ Multi-market support: h2h (moneyline), spreads, totals, props
- ✅ 9+ major sportsbooks integrated

## Definition of Done ✅ ALL COMPLETE
- ✅ End-to-end run produces odds for all games (tested: 272 events)
- ✅ Probability math and join logic working (tested with ML/ATS features)
- ✅ Multi-book support documented and working

## Production Commands
```bash
# Collect odds
busta pipeline collect odds --markets h2h --parquet
busta pipeline collect odds --markets spreads --parquet  
busta pipeline collect odds --markets totals --parquet

# Collect scores
busta pipeline collect scores --parquet

# Generate features with implied probabilities
busta features --market moneyline --processed-dir data/silver
busta features --market ats --processed-dir data/silver
busta features --market all --processed-dir data/silver
```

## Related Features
MOD-002, EVAL-002
