---
# Story template for docs/stories
id: STORY-ID
epic: epic-name
status: draft # draft | in-progress | blocked | done
owner: team-or-person
priority: medium # low | medium | high
estimate: null # e.g. 2d, 3sp, or null
dependencies: []
tags: []
market: null # moneyline | ats | ou | null
layer: null # Raw | Bronze | Silver | Gold | Predictions | Results | Analysis | Reports | Dashboard
last_updated: 2025-08-24
emit_metadata:
  source_id: null
  layer: null
  input_path: null
  notes: null
---

# Title: Short descriptive title

Summary
- One-paragraph summary of the story and goal.

Acceptance criteria
- Clear, testable bullets that define done.

Done checklist
- [ ] Implementation completed
- [ ] Tests/validation added
- [ ] Documentation updated

How to run / validate (CLI-first)
Use `busta` commands where applicable. Provide minimal example commands.

```bash
# Example: run feature generation for moneyline
busta features --market moneyline

# Example: run pipeline step
busta pipeline data normalize-bronze
```

Design / Implementation notes
- Short notes about approach, data shapes, edge cases.

Machine-readable fields (for automation)
- `emit_metadata` block above should be filled for sources and inputs.

Related issues / PRs
- Link to relevant issue or PR

Recommended reviewer(s)
- @handle or team name

Edge cases
- Enumerate 2-4 likely edge cases (missing data, rate limits, name collisions)
