---
id: PUBLIC_BETTING_DATA_INTEGRATION
epic: ingestion
status: draft
owner: TBD
priority: medium
estimate: 5
dependencies: []
tags: [betting, trends]
market: null
layer: Bronze
last_updated: 2025-08-24
emit_metadata:
  source_id: public_betting
  layer: Bronze
  input_path: null
  notes: null
---

# User Story: Public Betting Data Integration

## Overview
**As a** betting analyst  
**I want** public betting data integrated into our prediction system  
**So that** I can identify value opportunities where our predictions differ from public sentiment

## Value Proposition
Understanding public betting patterns enables contrarian strategies and reveals market inefficiencies. Integrating public betting percentages and line movement data helps identify value bets where public sentiment may be driving non-optimal lines.

## Acceptance Criteria
- System collects public betting percentages, money distribution, and line movement data
- Data is collected from multiple sportsbooks for comprehensive coverage
- Historical data is available for analysis of public betting patterns
- Data is processed into a standardized format for feature engineering
- UI displays public betting information alongside predictions
- LLM can reference public betting trends in generating narratives

## Technical Requirements
- Implement data collection from public betting data sources
- Create schema for betting trend data storage
- Develop line movement analysis capabilities
- Integrate public betting data into UI visualizations
- Expose public betting context to LLM components

## Implementation Plan
1. Research and select reliable public betting data sources
2. Implement data collection and storage
3. Create analysis tools for line movement and betting trends
4. Integrate with UI for visualization
5. Enhance LLM prompts to include public betting context

## Definition of Done
- Public betting data is collected, processed, and available in the system
- UI displays public betting percentages and line movement
- Value bet identification considers divergence from public sentiment
- LLM generates narratives that reference relevant public betting trends

## Related Features
- Data Source Integration Framework (dependency)
- UI Visualization Components (will be enhanced)
- AI-Generated Sales Pitch (will be enhanced)
