---
id: ING-005
epic: llm_backlog
status: draft
owner: team-data
priority: medium
estimate: 2sp
dependencies: [ING-001, ING-002]
tags: [ingestion, quality, filtering]
market: null
layer: Bronze
last_updated: 2025-08-24
emit_metadata:
  source_id: content_quality
  layer: Bronze
  input_path: data/bronze/news/
  notes: Content quality scoring before LLM processing
---

# ING-005: Content quality scoring and filtering

- **Overview**: As a data engineer, I want to filter low-quality content before LLM processing so that we don't waste API costs on noise.
- **Value Proposition**: Reduces LLM costs by 30-50% while improving signal quality by filtering spam, duplicates, and irrelevant content.

## Acceptance Criteria
- Quality scoring algorithm that considers: content length, NFL relevance, source credibility, and freshness
- Configurable quality thresholds per content category (breaking news vs analysis)
- Quality scores stored in `data/bronze/news_quality.parquet` with explanations
- <5% false negative rate on manual audit of filtered content
- Integration with LLM pipeline to skip low-quality articles

## Technical Requirements
- Lightweight ML model or heuristic scoring (no LLM required)
- Features: NFL entity density, readability score, source ranking, publication type
- Real-time scoring during ingestion pipeline
- Quality distribution monitoring and alerting
- Bypass mechanism for manual override of filtering decisions

## Implementation Plan
1. **Analyze current content quality** distribution and define quality metrics
2. **Build quality scoring model** using content features and source metadata
3. **Implement filtering logic** in ingestion pipeline with configurable thresholds
4. **Add quality monitoring** dashboard and alerting for distribution shifts
5. **Create manual override** interface for editorial review

## Definition of Done
- [ ] Quality scores correlate with manual assessment (r>0.8)
- [ ] 30%+ reduction in articles sent to LLM without signal loss
- [ ] Quality distribution monitoring alerts on anomalies
- [ ] Manual audit shows <5% false negative rate
- [ ] Integration with LLM pipeline respects quality filters

## Related Features
ING-001, ING-002, LLM-001, QLT-001
