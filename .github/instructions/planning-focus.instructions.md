---
applyTo: '**'
---

# Planning Repository Instructions

## Purpose
This repository serves as the strategic planning hub for the AI Sports Analytics project. Focus on story creation, refinement, and roadmap management rather than technical implementation.

## Core Responsibilities
1. **Story Management** - Create, refine, and organize user stories
2. **Roadmap Planning** - Organize stories into themes, epics, and iterations
3. **Cross-Repository Coordination** - Sync with implementation repository
4. **Stakeholder Communication** - Maintain clear progress visibility

## Repository Structure
```
.
├── backlog/          # New stories awaiting refinement
├── active/           # Stories currently in development
├── completed/        # Finished stories with outcomes
├── epics/           # Collections of related stories
├── roadmap/         # Strategic planning documents
└── templates/       # Story and epic templates
```

## Story Lifecycle
1. **Creation** → `backlog/` - New story with basic structure
2. **Refinement** → Stay in `backlog/` until ready
3. **Ready** → Move to `active/` when implementation starts
4. **Completion** → Move to `completed/` with outcome notes

## Coordination Patterns

### With Implementation Repository
- **Story References**: Implementation commits should reference story IDs
- **Feedback Loop**: Implementation discoveries refine future stories
- **Status Sync**: Keep story status aligned with implementation progress

### Communication Format
- **Story IDs**: Use format `CATEGORY-###` (e.g., AUTH-001, DATA-042)
- **Status Updates**: Clear progression through lifecycle stages
- **Implementation Links**: Reference PRs, commits, and issues from implementation repo

## Planning Principles
- **User-Centric**: All stories should deliver user or business value
- **Iterative**: Plans evolve based on learning and feedback
- **Realistic**: Estimates should reflect team capacity and historical velocity
- **Transparent**: Progress and changes should be visible to all stakeholders

## Anti-Patterns to Avoid
- ❌ Technical implementation details in planning documents
- ❌ Stories without clear user value
- ❌ Over-planning distant future (beyond one quarter)
- ❌ Ignoring implementation feedback
- ❌ Planning in isolation from implementation realities
