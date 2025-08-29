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
1. **Creation** → `backlog/` subdirectory - New story with basic structure
2. **Refinement** → Status remains in JSON until ready
3. **Ready** → Implementation Agent uses `busta story start [STORY_ID]` to begin work
4. **Active** → Story automatically moved to active folder, feature branch created
5. **Development** → Implementation work with story ID references in commits
6. **Completion** → Implementation Agent uses `busta story close` for automated finish
7. **Accepted** → Planning Agent reviews and marks as accepted with outcome notes

## Coordination Patterns

### With Implementation Repository
- **Story Workflow Integration**: Implementation uses `busta story start/close` for automated coordination
- **Automated Synchronization**: Story status and branch management handled automatically
- **Story References**: Implementation commits reference story IDs via workflow templates
- **Feedback Loop**: Implementation discoveries refine future stories through automated context
- **Status Sync**: Story lifecycle tracked automatically across repositories

### Communication Format
- **Story IDs**: Use format `ADH-###` (e.g., ADH-001, ADH-042)
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
- ❌ Bypassing story workflow automation for manual operations
- ❌ Starting implementation without using `busta story start` workflow
