---
applyTo: '**'
---

# Planning Repository Instructions

## Purpose
This repository serves as the strategic planning hub for the AI Sports Analytics project. Focus on story creation, refinement, and roadmap management rather than technical implementation.

## Core Responsibilities
1. **Story Management** - Create, refine, and organize user stories across epic categories
2. **Proposal Management** - Review and process high-level feature proposals through approval workflow
3. **Roadmap Planning** - Organize stories into themes, epics, and quarterly iterations
4. **Implementation Planning** - Create detailed technical implementation guides
5. **Story Refinement** - Continuously improve story quality and acceptance criteria
6. **Analytics & Reporting** - Generate automated health, velocity, and priority reports
7. **Cross-Repository Coordination** - Sync with implementation repository via script-based workflows
8. **Stakeholder Communication** - Maintain clear progress visibility through reports and roadmaps

## Repository Structure
```
.
├── .github/          # GitHub workflows, templates, and agent instructions
├── backlog/          # Story inventory organized by epic
│   ├── adhoc/        # Ad-hoc fixes and maintenance stories
│   ├── core/         # Core platform functionality stories
│   ├── infra/        # Infrastructure and deployment stories
│   ├── ingestion/    # Data ingestion and pipeline stories
│   ├── llm/          # LLM integration and AI features
│   ├── modeling/     # Prediction model stories
│   ├── quality/      # Testing and quality assurance stories
│   ├── social_media/ # Social media integration stories
│   ├── ui/           # User interface and experience stories
│   └── *.json        # Priority and status management files
├── implementation_plans/ # Detailed technical implementation guides
├── proposals/        # High-level feature and architecture proposals
│   └── processed/    # Completed proposals by status
│       ├── accepted/ # Approved proposals ready for story creation
│       ├── declined/ # Rejected proposals with rationale
│       └── deferred/ # Proposals postponed for future consideration
├── refinements/      # Story refinement documentation by category
│   ├── api/          # API-related refinements
│   ├── infrastructure/ # Infrastructure refinements
│   ├── integration/  # Integration refinements
│   └── reporting/    # Reporting refinements
├── reports/          # Automated analytics and health reports
├── roadmaps/         # Strategic planning documents and quarterly roadmaps
├── scripts/          # Automation scripts for story and priority management
├── staging/          # Temporary area for story creation and processing
│   ├── processed/    # Stories that have been ingested into backlog
│   └── templates/    # Template files for story staging
└── templates/        # Master templates for stories and proposals
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
- **Documentation Hygiene**: Only create reports and summaries when explicitly requested

## Documentation Guidelines
- **Script outputs only**: Use script-generated reports for status and analytics
- **No unsolicited summaries**: Do not create summary documents unless specifically asked
- **Existing reports**: Reference automated reports in `/reports/` directory rather than creating new ones
- **Keep it lean**: Focus on actionable planning work rather than documentation overhead
- **Clean as you go**: Use existing structures and avoid creating redundant documentation

## Anti-Patterns to Avoid
- ❌ Technical implementation details in planning documents
- ❌ Stories without clear user value
- ❌ Over-planning distant future (beyond one quarter)
- ❌ Ignoring implementation feedback
- ❌ Planning in isolation from implementation realities
- ❌ Bypassing story workflow automation for manual operations
- ❌ Starting implementation without using `busta story start` workflow
- ❌ Creating summary reports or documentation unless explicitly requested
- ❌ Duplicating information that already exists in automated reports
- ❌ Adding documentation overhead that requires later cleanup
