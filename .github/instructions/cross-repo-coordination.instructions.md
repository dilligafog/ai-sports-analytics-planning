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

## Coordination Workflows

### Story-Driven Development
1. **Planning Agent** creates stories with acceptance criteria and maintains prioritization list
2. **Implementation Agent** selects next story from `backlog/PRIORITIZATION.md`
3. **Implementation Agent** references story IDs in commits/PRs
4. **Implementation Agent** provides feedback on story accuracy
5. **Planning Agent** refines future stories and updates prioritization based on feedback

### Information Flow
```
Planning Repo                    Implementation Repo
     │                                    │
     ├─ Create Story ─────────────────────┤
     │                                    ├─ Reference in Commit
     │                                    ├─ Implementation Notes
     ├─ Refine Based on Feedback ─────────┤
     │                                    ├─ Link PR to Story
     ├─ Update Status ────────────────────┤
     │                                    └─ Mark Complete
     └─ Archive Completed Story
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
See: https://github.com/dilligafog/ai-sports-analytics-planning/blob/main/backlog/adhoc/adh-001-update-busta-adhoc-stories.md

- Specific implementation details
- Technical decisions made
- Deviations from original plan

Planning feedback:
- Story estimate was accurate/overestimated/underestimated
- Discovered additional requirements: [list]
- Suggested follow-up stories: [list]
```

### PR Descriptions
```markdown
## Story Context
**Planning Story**: [ADH-001](link-to-planning-story)
**Status**: Ready for Review / Completed
**Acceptance Criteria**: List status of each criterion

## Implementation Summary
- Brief description of approach taken
- Key technical decisions and rationale
- Any deviations from original story plan

## Planning Agent Feedback
- Story accuracy and estimation quality
- Discovered requirements not in original story
- Suggestions for future related stories
- Implementation complexity notes for future planning
```

## Synchronization Points

### Daily
- Implementation agent checks `backlog/PRIORITIZATION.md` for next ready stories
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
- ❌ Stories completed without updating planning repository status
- ❌ Implementation proceeding without clear story context
- ❌ Planning decisions made without considering implementation feedback
