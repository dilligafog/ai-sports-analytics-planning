# Story Refinement Prompt

## Role
Help refine existing stories based on implementation feedback, changing requirements, or new discoveries.

## Refinement Triggers
1. **Implementation Feedback** - Developer discovers issues or improvements
2. **Scope Creep** - Story becomes larger than originally estimated
3. **Dependency Changes** - Related stories change, affecting this one
4. **Technical Discoveries** - Implementation reveals new requirements
5. **User Feedback** - End users request modifications

## Refinement Process

### 1. Analyze Current State
- Review original story and acceptance criteria
- Check implementation progress by reviewing PRs and commits
- Check for existing code that may provide the same functionality
- Identify what's changed since story creation

### 2. Determine Refinement Type
- **Split**: Story too large, break into smaller pieces
- **Merge**: Related stories should be combined
- **Update**: Acceptance criteria need modification
- **Reprioritize**: Story priority has changed
- **Archive**: Story no longer needed

### 3. Update Story Structure
- Revise user story statement if needed
- Update acceptance criteria based on learnings
- Adjust technical notes and dependencies
- Update estimates based on implementation feedback

### 4. Communicate Changes
- Note refinement rationale in story comments
- Update roadmap if priority or estimates changed
- Notify implementation agent of significant changes

## Refinement Templates

### Split Story Template
```markdown
## Refinement: Split Story

**Original Story**: [Link to original]
**Reason for Split**: [Why story became too large]

### New Story 1: [Title]
[Focused user story and acceptance criteria]

### New Story 2: [Title]
[Focused user story and acceptance criteria]

**Dependencies**: Story 1 → Story 2
**Updated Estimates**: Original 8pts → Story 1: 3pts, Story 2: 5pts
```

### Update Criteria Template
```markdown
## Refinement: Updated Acceptance Criteria

**Change Reason**: [Implementation feedback/user request/technical discovery]

### Removed Criteria
- ~~[Old criterion that's no longer relevant]~~

### Added Criteria
- [New criterion based on discoveries]
- [Additional criterion for edge case handling]

### Modified Criteria
- **Old**: [Previous criterion]
- **New**: [Updated criterion with clarification]
```

## Quality Checks
- [ ] Refined story still delivers user value
- [ ] Acceptance criteria remain testable
- [ ] Dependencies are clearly documented
- [ ] Estimates reflect current understanding
- [ ] Roadmap impact is considered

## Documentation
- Always document the refinement rationale
- Link to related implementation PRs or issues
- Update story status and timeline if needed
- Preserve history of changes for future reference
