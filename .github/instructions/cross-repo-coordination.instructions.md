---
applyTo: '**'
---

# Cross-Repository Coordination Instructions

## Repository Roles

### Implementation Repository
**Location**: https://github.com/dilligafog/ai-sports-analytics  
**Focus**: Technical implementation, code, testing, deployment  
**Agent Type**: Implementation specialist

### Planning Repository  
**Location**: https://github.com/dilligafog/ai-sports-analytics-planning  
**Focus**: Strategic planning, story management, roadmap evolution  
**Agent Type**: Planning specialist

## Busta Story Workflow Commands

The Implementation Agent uses these automated workflow commands:

### `busta story start [STORY_ID]`
Automated story startup with full repository coordination:
- `busta story start` or `busta story start NEXT` - Start highest priority story
- `busta story start UI-001` - Start specific story by ID
- `busta story start adhoc "Fix Bug"` - Start ad-hoc story (auto-assigned ADH-### ID)

**Automation includes:**
- Syncs planning repository to get latest priorities
- Creates feature branch (e.g., `feature/UI-001`)
- Moves story from backlog to active folder
- Creates story context templates for commit and PR messages
- Commits and pushes planning changes

### `busta story close`
Automated story completion with full quality assurance:
- Validates story templates are updated with actual work
- Runs comprehensive CI checks (format, lint, test)
- Commits all changes using prepared templates
- Pushes feature branch and creates pull request
- Moves story to completed folder in planning repository
- Cleans up story context and temporary files

### `busta story next [--detail]`
Preview next priority story without starting:
- Shows story ID, title, estimate, and acceptance criteria
- Use `--detail` flag for full story information
- Helps with planning and story selection

### Story Context System
The workflow creates templates in `.story-context/` that must be customized:
- `commit-template.md` - Pre-filled commit message template
- `pr-template.md` - Pre-filled pull request description
- `story-notes.md` - Development notes and decisions

**Important:** Templates are auto-generated but must be updated with actual implementation details before closing.

## Coordination Workflows

### Story-Driven Development
1. **Planning Agent** creates stories with acceptance criteria and maintains prioritization list
2. **Implementation Agent** uses `busta story start [STORY_ID]` to select and begin work on next priority story
3. **Story Start Automation** automatically moves story from backlog to active, creates feature branch, and sets up story context
4. **Implementation Agent** references story IDs in commits/PRs during development
5. **Implementation Agent** uses `busta story close` to complete story with automated CI checks, commits, PR creation
6. **Story Close Automation** moves completed story to planning repo with metadata and cleanup
7. **Planning Agent** refines future stories and updates prioritization based on feedback

### Information Flow
```
Planning Repo                          Implementation Repo
     │                                        │
     ├─ Create Story ─────────────────────────┤
     │                                        ├─ busta story start [ID]
     │                                        │   ├─ Auto move backlog→active
     │                                        │   ├─ Create feature branch  
     │                                        │   └─ Setup story context
     │                                        ├─ Development & Commits
     ├─ Auto story move ──────────────────────┤   (reference story ID)
     │                                        ├─ busta story close
     │                                        │   ├─ CI checks & validation
     │                                        │   ├─ Auto commit & push
     │                                        │   └─ Create PR
     ├─ Auto completed status ────────────────┤
     ├─ Refine Based on Feedback ─────────────┤
     │                                        └─ Continue development
     └─ Archive Accepted Story
```

### Communication Patterns

#### Story Creation (Planning → Implementation)
- Planning agent creates story with clear acceptance criteria
- Implementation agent reviews story before starting work
- Any questions or clarifications handled in story comments

#### Implementation Progress (Implementation → Planning)
- Commit messages reference story IDs: `feat(ADH-001): implement OAuth flow`
- PR descriptions link to planning stories
- Implementation discoveries noted for planning refinement

#### Story Completion (Both)
- Implementation agent marks technical completion
- Planning agent moves story to completed with outcome notes
- Lessons learned captured for future story estimation

## Reference Formats

### Commit Messages
```
<type>(story-id): <description>

Implements story ADH-001 from planning repository.
Story workflow: Started with `busta story start ADH-001`
See: https://github.com/dilligafog/ai-sports-analytics-planning/blob/main/backlog/adhoc/adh-001-update-busta-adhoc-stories.md

Implementation details:
- Specific implementation details
- Technical decisions made
- Deviations from original plan

Planning feedback:
- Story estimate was accurate/overestimated/underestimated
- Discovered additional requirements: [list]
- Suggested follow-up stories: [list]

Story completion: Use `busta story close` to finalize
```

### PR Descriptions
```markdown
## Story Context
**Planning Story**: [ADH-001](link-to-planning-story)
**Story Workflow**: Started with `busta story start ADH-001`, completed with `busta story close`
**Status**: Ready for Review / Completed
**Acceptance Criteria**: List status of each criterion

## Implementation Summary
- Brief description of approach taken
- Key technical decisions and rationale
- Any deviations from original story plan

## Story Workflow Notes
- Templates were updated in `.story-context/` before closing
- CI checks passed (format, lint, test)
- Planning repository synchronized automatically

## Planning Agent Feedback
- Story accuracy and estimation quality
- Discovered requirements not in original story
- Suggestions for future related stories
- Implementation complexity notes for future planning
```

## Synchronization Points

### Daily
- Implementation agent uses `busta story start` to automatically select next priority story
- Story workflow automatically handles backlog→active transitions and branch creation
- Planning agent monitors implementation progress and updates story status
- Quick status updates on active stories

### Weekly  
- Review completed stories and capture lessons learned
- Adjust story estimates based on implementation feedback
- Regenerate prioritization list if significant backlog changes
- Plan next iteration based on velocity and capacity

### Monthly
- Roadmap adjustments based on implementation discoveries
- Epic progress review and replanning if needed
- Cross-repository dependency resolution

## Quality Assurance

### Story Quality Gates
- [ ] Clear user value proposition
- [ ] Testable acceptance criteria
- [ ] Realistic size estimation
- [ ] Minimal external dependencies
- [ ] Implementation feasibility confirmed

### Coordination Quality Gates
- [ ] Story IDs consistently referenced in implementation
- [ ] Implementation feedback incorporated into planning
- [ ] Status synchronization between repositories
- [ ] Lessons learned captured for future planning
- [ ] Cross-repository links maintained and functional

## Anti-Patterns
- ❌ Implementation agent creating stories without planning agent input
- ❌ Planning agent making technical decisions without implementation input
- ❌ Bypassing `busta story` workflow for manual git operations
- ❌ Closing stories with `busta story close` without updating `.story-context/` templates
- ❌ Starting work without using `busta story start` for proper tracking
- ❌ Implementation proceeding without clear story context
- ❌ Planning decisions made without considering implementation feedback
