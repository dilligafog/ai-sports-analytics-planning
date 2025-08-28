---
id: LLM-014
title: Llm Feature Extraction From News
epic: core
status: accepted
priority: medium
effort: TBD
branch_name: llm-014-llm-feature-extraction-from-news
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# LLM Feature Extraction from News

## Overview
# LLM Feature Extraction from News - ✅ COMPLETED

## Overview
**User Story**: As a data scientist, I want LLMs to extract structured signals from NFL news (injury impacts, coach changes, etc.) so that my models can incorporate high-value textual information.

**Value Proposition**: Structured signals from unstructured text allows models to capture timing and magnitude of lineup changes that traditional stats miss.

## Acceptance Criteria
- [x] ✅ Pydantic schemas for structured signal extraction (injury, personnel, confidence)
- [x] ✅ LLM integration with OpenAI API using gpt-3.5-turbo for cost efficiency
- [x] ✅ Batch processing with 50% cost optimization vs real-time processing
- [x] ✅ Conservative signal thresholds to avoid false positives
- [x] ✅ CLI integration: `busta features llm extract` and batch operations

## Results Achieved
- **Complete LLM pipeline** with real API integration (no mocks)
- **Cost-efficient processing** at ~$0.03 per run using gpt-3.5-turbo
- **Production-safe error handling** with no fallback data generation
- **Pydantic validation** ensuring signal quality and structure
- **Batch optimization** reducing API costs by 50% for large datasets

## Definition of Done
- [x] ✅ LLM can extract structured signals from NFL news articles
- [x] ✅ Signal confidence scoring implemented
- [x] ✅ Cost-efficient batch processing available
- [x] ✅ CLI integration complete with model parameter support
- [x] ✅ Production deployment ready (no mock fallbacks)

## Technical Requirements
- System prompt enforcing JSON-only + abstention patterns
- Pydantic schema with validator to drop/flag out-of-range values
- Caching by (`cluster_id`, `schema_version`) for efficiency
- Integration with OpenAI/Anthropic APIs with proper error handling
- Batch processing capabilities for multiple articles

## Implementation Plan
1. **Define pydantic schema** and JSON validator for LLM outputs
2. **Implement LLM extraction** in `packages/features/src/features/llm_features.py`
3. **Create batch processing** for multiple articles
4. **Add caching layer** for repeated extractions
5. **Integrate with CLI** via `busta features --llm-extract`

## Definition of Done
- [ ] LLM extraction producing valid JSON signals
- [ ] Schema validation catching invalid outputs
- [ ] Caching reducing redundant API calls
- [ ] Gold layer populated with structured signals
- [ ] Evidence citations linking back to source articles
- [ ] CLI integration working with existing pipeline

## Related Features
- Depends on News RSS Sources Integration
- Depends on Article Deduplication pipeline
- Feeds into model training evaluation
- Supports AI-generated sales pitch
