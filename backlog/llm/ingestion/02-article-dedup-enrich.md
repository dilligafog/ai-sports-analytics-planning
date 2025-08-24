---
id: ING-002
epic: llm_backlog
status: draft
owner: team-data
priority: high
estimate: 3sp
dependencies: [ING-001]
tags: [ingestion, dedup, enrichment]
market: null
layer: Bronze
last_updated: 2025-08-24
emit_metadata:
  source_id: dedup_enrich
  layer: Bronze
  input_path: data/bronze/news/
  notes: Deduplication, canonicalization, language detection
---

# ING-002: Article deduplication & enrichment pipeline

- **Overview**: As a platform engineer, I want to deduplicate and enrich articles so that downstream LLMs receive a clean, consolidated text per story.
- **Value Proposition**: Reduces LLM cost and noise by collapsing near-duplicates and attaching high-value metadata (teams, players).

## Acceptance Criteria
- Near-duplicate clustering based on URL canonicalization + title similarity > 0.9 or content cosine similarity > 0.92.
- Resolved record includes `cluster_id`, chosen `canonical_url`, and merged `evidence_urls`.
- NER tags for NFL teams and players attached to each record; team tags mapped to `game_id` when possible.
- `data/silver/news_clean.parquet` produced with <1% duplicates on spot check.

## Technical Requirements
- Use MinHash or cosine sim over sentence embeddings for clustering.
- Entity recognition with a sports-tuned dictionary + fuzzy match (Levenshtein/Jaro-Winkler).
- Map team names/aliases to team codes; try to infer `game_id` using date/opponent heuristics.

## Implementation Plan
- Implement canonical URL + strip UTM parameters.
- Build embedding pipeline and clusterer (faiss or sklearn).
- NER + dictionary augment; persist entity spans.
- Unit tests with synthetic near-dup sets.

## Definition of Done
- Precision/recall on duplicate test set ≥ 0.95/0.90.
- NER spot-check accuracy > 90% on 100-sample audit.
- Docs include rules for team/opponent/game mapping.

## Related Features
ING-001, LLM-001
