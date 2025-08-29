---
id: API-002
title: Status transition endpoints with validation
branch_name: api-002-status-transition-endpoints-validation
epic: api
status: draft
priority: high
estimate: "4sp"
dependencies: [API-001]
labels: [api, status, transitions, validation, workflow]
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

# API-002: Status transition endpoints with validation

## User Story
**As a** project manager or automation system  
**I want** validated status transition endpoints for stories  
**So that** story lifecycle changes follow proper workflow rules and maintain audit trails

## Value Proposition
Ensures story status changes follow business rules and provides audit trail for workflow compliance, preventing invalid state transitions and maintaining data integrity.

## Acceptance Criteria
- [ ] POST /api/v1/stories/{id}/transition - Change story status with validation
- [ ] Valid transition rules enforced (backlog → active → completed → accepted)
- [ ] Transition validation includes dependency checks across backlogs
- [ ] Status history automatically recorded for all transitions with backlog context
- [ ] Transition reasons and notes can be included in requests
- [ ] Bulk status transitions supported for multiple stories within/across backlogs
- [ ] Rollback capability for recent status changes
- [ ] Validation prevents invalid transitions (e.g., backlog → completed)
- [ ] Cross-backlog dependency validation (can't complete if dependencies in other backlogs not done)
- [ ] Notification system for status change events with backlog awareness

## Technical Notes
- Implement state machine pattern for status transitions
- Store transition history with timestamps and user information
- Include business rule validation before allowing transitions
- Consider implementing transition permissions based on user roles
- Support for conditional transitions based on story properties
- Error messages should clearly explain why transitions are invalid

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Comprehensive unit tests for all transition scenarios
- [ ] Integration tests with status history recording
- [ ] Business rule validation thoroughly tested
- [ ] API documentation includes transition flow diagrams
- [ ] Performance tests for bulk transition operations

## References
- [TOOL-001 Proposal](../../proposals/TOOL-001-dockerized-story-workflow-api.md)
- [Story Lifecycle Documentation](../../README.md)
- [Status History Schema from Proposal](../../proposals/TOOL-001-dockerized-story-workflow-api.md#database-schema)

---
**Story Lifecycle:**
- Created: 2025-08-28 by planning-agent
- Started: [date] by [implementer]  
- Completed: [date]
- Accepted: [date]