# ADH (Ad-Hoc) Story Workflow

## Overview

ADH stories are ad-hoc bug fixes, maintenance tasks, and quick improvements that bypass the formal backlog prioritization process. These stories are designed for rapid execution and don't require extensive planning or refinement.

## ADH Story Characteristics

- **Prefix**: All ADH stories start with `ADH-###` (e.g., ADH-001, ADH-002)
- **Type**: `ad-hoc` in story metadata
- **Priority**: `ad-hoc` (not prioritized against backlog stories)
- **Effort**: `ad-hoc` (no formal estimation)
- **Planning**: Minimal - just enough to understand the work

## Workflow

### 1. Direct to Active
- ADH stories bypass the `backlog/` directory entirely
- Created directly in `active/` when work begins
- No formal refinement or prioritization needed

### 2. Execution
- Work proceeds immediately without waiting for prioritization
- Focus on quick fixes and improvements
- Minimal documentation requirements

### 3. Completion
- Move from `active/` to `completed/` when work is done
- Eventually moves to `accepted/` like other stories
- Track completion for metrics but don't block other work

## When to Use ADH Stories

### ✅ Good for ADH:
- Bug fixes discovered during development
- Quick maintenance tasks (< 4 hours)
- Log cleanup and repository hygiene
- Simple configuration updates
- Immediate blockers for ongoing work
- Developer tools and productivity improvements

### ❌ Not suitable for ADH:
- New features requiring user research
- Complex architectural changes
- Stories requiring multiple dependencies
- Work that affects user-facing functionality significantly
- Changes requiring extensive testing or deployment coordination

## ADH Story Template

```markdown
---
id: ADH-###-Brief_Description
title: Brief Description of Work
type: ad-hoc
status: in-progress  
priority: ad-hoc
effort: ad-hoc
labels: [ad-hoc, maintenance] # or [ad-hoc, bugfix], etc.
created: YYYY-MM-DD
author: developer
dependencies: []
---

# Brief Description of Work

## Ad-hoc Story

**As a** developer  
**I want** to [describe the work]  
**So that** [describe the benefit]

## Description

Brief description of what needs to be done and why.

## Tasks

- [ ] Complete the work described in the story title
- [ ] Ensure all CI checks pass
- [ ] Update documentation if needed
- [ ] Test the change works as expected

## Acceptance Criteria

- [ ] Work is completed and functional
- [ ] No regression in existing functionality
- [ ] CI/CD pipeline passes
- [ ] Quick verification that change works as intended

## Notes

Any additional context or considerations.
```

## Tracking and Metrics

- ADH stories are tracked in `backlog/PRIORITIZATION.json` under the `adhoc_workflow` section
- Completion metrics help understand maintenance overhead
- ADH stories don't count against regular story velocity
- Review ADH story patterns monthly to identify systematic issues

## Integration with Regular Workflow

- ADH stories run parallel to regular story workflow
- Don't block regular story progression for ADH work
- Can interrupt regular stories for critical bugs only
- Regular stories take priority for planning and architectural decisions

## Examples of Recent ADH Stories

- **ADH-001**: Update Busta for Adhoc Stories - Tool improvements for handling ADH workflow
- **ADH-002**: Fix Inventory Sidebar - Quick UI bug fix
- **ADH-003**: Untrack Log Files - Repository cleanup

## Guidelines

1. **Keep them small** - If it takes more than 4 hours, consider making it a regular story
2. **Act fast** - Don't let ADH stories linger in active/ for days
3. **Document briefly** - Just enough to understand what was done and why
4. **Test quickly** - Ensure changes work but don't over-engineer the testing
5. **Clean up** - Move completed ADH stories to staging regularly
