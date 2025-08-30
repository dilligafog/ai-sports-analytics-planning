---
id: RPT-001
title: Epic analytics and cross-story reporting
branch_name: rpt-001-epic-analytics-cross-story-reporting
epic: reporting
status: draft
priority: medium
estimate: "5sp"
dependencies: [API-001, INF-013]
labels: [reporting, analytics, epics, dashboards]
created: 2025-08-28
author: planning-agent
owner: implementation-team
market: null
layer: null
last_updated: 2025-08-28
emit_metadata:
  source_id: null
  layer: null
  input_path: null
  notes: null
---

# RPT-001: Epic analytics and cross-story reporting

## User Story
**As a** planning agent or stakeholder  
**I want** comprehensive analytics and reporting across epics and stories  
**So that** I can track progress, identify bottlenecks, and make informed strategic planning decisions

## Value Proposition
Provides strategic insights into story portfolio health, epic progress, and cross-cutting patterns that support data-driven planning and resource allocation decisions.

## Acceptance Criteria
- [ ] GET /api/v1/reports/epic-summary - Stories by epic and status with counts across backlogs
- [ ] Epic completion percentages and progress tracking with backlog segmentation
- [ ] Story distribution analysis across priorities, estimates, and backlogs
- [ ] Cross-epic and cross-backlog dependency analysis and impact assessment
- [ ] Timeline analysis showing epic velocity and completion trends by backlog
- [ ] Resource allocation reporting by epic, team, and backlog
- [ ] Story aging analysis (time in each status) with backlog context
- [ ] Epic health scoring based on completion rate and cross-backlog dependencies
- [ ] Comparative epic performance metrics across different backlogs
- [ ] Customizable date ranges for all analytics with backlog filtering
- [ ] JSON export for simple GitHub Pages dashboard consumption
- [ ] Static dashboard data generation for minimal UI dependencies

## Technical Notes
- Leverage SQLite analytical functions and window functions for complex queries across backlogs
- Implement caching for expensive analytical queries with backlog-aware cache keys
- Create views for frequently accessed metrics with backlog segmentation
- Support real-time analytics with WebSocket updates including cross-backlog events
- Generate static JSON files for simple GitHub Pages dashboard consumption
- Minimize UI dependencies by focusing on data export rather than complex visualizations
- Include data visualization recommendations in API responses
- Consider pre-computed metrics for common dashboard views

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Analytics endpoints return results within 2 seconds
- [ ] Unit tests cover all analytical calculations
- [ ] Data accuracy verified against manual calculations
- [ ] API documentation includes example responses and interpretations
- [ ] Performance tests with large story datasets

## References
- [TOOL-001 Proposal](../../proposals/TOOL-001-dockerized-story-workflow-api.md)
- [Reporting Endpoints from Proposal](../../proposals/TOOL-001-dockerized-story-workflow-api.md#reporting--analytics)
- [Epic Strategy Documentation](../../roadmaps/README.md)

---
**Story Lifecycle:**
- Created: 2025-08-28 by planning-agent
- Started: [date] by [implementer]  
- Completed: [date]
- Accepted: [date]