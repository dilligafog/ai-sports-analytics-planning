# Implementation Plans

## Purpose

This folder contains detailed implementation plans for complex user stories that require architectural design, technical specifications, or multi-phase execution strategies before development begins.

## When to Create Implementation Plans

Create implementation plans for stories that have:

- **High complexity** (8+ story points)
- **Architectural implications** (new systems, major refactors)
- **Multiple integration points** (cross-system dependencies)
- **Unclear technical approach** (research or experimentation needed)
- **Multi-phase delivery** (can be broken into smaller deliverables)

## Plan Structure

Each implementation plan should follow this structure:

```markdown
# [STORY-ID] Implementation Plan - [Story Title]

## Overview
- **Story Reference**: Link to backlog story
- **Epic**: Which epic this belongs to
- **Estimated Effort**: Total story points
- **Timeline**: Expected delivery phases

## Technical Approach
- **Architecture**: High-level system design
- **Technology Stack**: Tools, frameworks, libraries
- **Integration Points**: External systems and APIs
- **Data Flow**: How data moves through the system

## Implementation Phases
### Phase 1: [Foundation/Setup]
- Deliverables
- Story points: X
- Dependencies

### Phase 2: [Core Features]  
- Deliverables
- Story points: Y
- Dependencies

### Phase 3: [Integration/Polish]
- Deliverables  
- Story points: Z
- Dependencies

## Technical Decisions
- **Decision 1**: Rationale and alternatives considered
- **Decision 2**: Trade-offs and implications

## Risks and Mitigation
- **Risk**: Impact and likelihood
- **Mitigation**: Prevention and contingency plans

## Success Criteria
- **Functional**: What the system should do
- **Non-functional**: Performance, reliability, usability requirements
- **Testing**: How success will be validated

## Follow-up Work
- Stories that should be created after implementation
- Technical debt or improvements to consider
```

## Workflow Integration

### Planning Agent Responsibilities
1. **Create Plans**: For complex stories before they enter `ready_to_start`
2. **Refine Plans**: Based on implementation feedback and discoveries
3. **Track Progress**: Monitor phase completion and update estimates
4. **Archive Plans**: Move completed plans to reference documentation

### Implementation Agent Interaction
1. **Review Plans**: Before starting work on complex stories
2. **Provide Feedback**: On feasibility, effort estimates, and approach
3. **Update Progress**: Report phase completion and discoveries
4. **Suggest Refinements**: Based on implementation experience

## File Naming Convention

```
[STORY-ID]-implementation-plan.md
```

Examples:
- `DATA_SOURCE_INTEGRATION_FRAMEWORK-implementation-plan.md`
- `LLM-001-implementation-plan.md`
- `UI-003-implementation-plan.md`

## Relationship to Other Folders

### vs. `backlog/`
- **Backlog**: User stories with acceptance criteria
- **Implementation Plans**: Technical approach and execution strategy

### vs. `proposals/`
- **Proposals**: New feature ideas and business requirements
- **Implementation Plans**: How to build accepted features

### vs. `active/`
- **Active**: Stories currently being implemented
- **Implementation Plans**: Blueprint for how to implement them

### vs. `accepted/`
- **Accepted**: Completed and verified stories
- **Implementation Plans**: Can be archived as reference documentation

## Best Practices

### For Complex Stories
- Create implementation plan before moving story to `ready_to_start`
- Break large stories into phases of 3-5 story points each
- Identify critical path dependencies early

### For Cross-System Features
- Map all integration points and data flows
- Plan for testing at each integration boundary
- Consider rollback and migration strategies

### For Research-Heavy Work
- Include spike stories for proof-of-concept work
- Document alternative approaches considered
- Plan for potential pivots based on research outcomes

### For Infrastructure Changes
- Consider impact on existing features
- Plan for gradual rollout and feature flags
- Include monitoring and observability from day one

## Archive Strategy

When a story is completed:
1. **Update Plan**: Add actual effort and lessons learned
2. **Archive**: Move to `accepted/` with story completion
3. **Extract Patterns**: Use learnings to improve future planning
4. **Reference**: Keep as example for similar future work

## Quality Gates

Before implementation begins:
- [ ] Technical approach is clearly defined
- [ ] Dependencies are identified and ready
- [ ] Success criteria are measurable
- [ ] Risks have mitigation strategies
- [ ] Story can be broken into reviewable phases

## Examples

See these reference implementation plans:
- [Example coming soon - first complex story]

---

*This folder supports the story-driven development workflow by ensuring complex technical work is properly planned before implementation begins.*
