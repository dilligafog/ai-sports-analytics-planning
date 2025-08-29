---
id: ADH-001
title: Update Busta CLI for Adhoc Story Workflow Integration
epic: adhoc
status: accepted
priority: urgent
effort: "2sp"
branch_name: adh-001-update-busta-adhoc-stories
labels:
- adhoc
- workflow
- cli
- implementation
created: 2025-08-26
completed: 2025-08-26
accepted_date: 2025-08-27
author: Neo Starlord of Thunder
owner: Neo Starlord of Thunder
dependencies: []
---

# ADH-001: Update Busta CLI for Adhoc Story Workflow Integration

## Problem Statement
The Busta CLI on the implementation side needed updates to support the new standardized story workflow with YAML frontmatter, branch naming conventions, and integration with the planning repository's JSON tracking system.

## Solution Approach
Updated the implementation repository's CLI tooling to:
- Read story metadata from YAML frontmatter (including `branch_name` field)
- Support standardized story ID formats (EPIC-###)
- Integrate with planning repository story lifecycle
- Handle ADH (ad-hoc) story workflow patterns

## Acceptance Criteria
- [x] Busta CLI reads `branch_name` from story YAML frontmatter
- [x] Story workflow supports EPIC-### ID format
- [x] ADH story lifecycle integrated with implementation workflow
- [x] CLI tools compatible with planning repository JSON structure
- [x] Branch creation follows standardized naming from story files

## Implementation Details
**Completed**: August 26, 2025

### Changes Made:
1. **Story Metadata Integration**: Updated CLI to parse YAML frontmatter from planning repository
2. **Branch Naming**: Implemented automatic branch creation using `branch_name` field from stories
3. **Workflow Synchronization**: Added support for updating story status back to planning repository
4. **ADH Pattern Support**: Special handling for urgent ad-hoc stories with immediate workflow
5. **Cross-Repository Coordination**: CLI now references planning repository stories consistently

### Technical Implementation:
- Modified story parsing to read standardized YAML frontmatter
- Added branch name validation and automatic Git branch creation
- Implemented story status synchronization between repositories
- Added ADH workflow shortcuts for urgent fixes
- Enhanced CLI help and documentation for new workflow

## ADH Justification
This was an urgent implementation-side fix needed to support the newly standardized story management system from the planning repository. Without this update, the implementation workflow would be incompatible with the new planning structure.

## Cross-Repository Impact
- **Planning Repository**: Stories now properly reference implementation branches
- **Implementation Repository**: CLI seamlessly integrates with planning story lifecycle
- **Workflow**: Unified development process across both repositories

---
**ADH Workflow:**
- Created: 2025-08-26 - Implementation CLI incompatible with new story format
- Started: 2025-08-26 - Immediate CLI updates needed for workflow continuity
- Completed: 2025-08-26 - CLI updated and workflow integration working
- Accepted: 2025-08-27 - Planning repository acknowledges successful implementation
