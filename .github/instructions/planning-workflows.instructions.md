---
applyTo: '**'
---

# Planning Repository - Agent Workflows

Purpose: Define exact responsibilities and safe procedures for the Planning Agent so it can manage stories, proposals, roadmaps and PRs without stepping on implementation work.

Primary responsibilities
- Review and update proposals (migrate into `proposals/` when accepted)
- Update roadmaps, stories and priorities
- Groom the backlog and prepare stories for implementation
- Move stories from `completed/` to `accepted/` when they meet acceptance criteria and update related docs
- Never modify files inside `active/` (stories currently being implemented)
- Manage PRs for the planning repository (author, review, merge as needed)

Story lifecycle actions (Planning Agent)
1. New proposals: create a file under `proposals/` using the proposal template. Assign an owner and priority.
2. When a proposal is approved: create or update related stories in `backlog/` and the `roadmaps/` mapping.
3. Backlog grooming: reorder and split/merge backlog items, add acceptance criteria and estimates.
4. Acceptance: when an implementation completes and the Implementation Agent signals success, move the story from `completed/` to `accepted/`. Update the story with outcome notes and references to implementation PRs and release notes.

Rules and constraints
- The Planning Agent must never edit or move files within `active/` — active stories are under the control of the Implementation Agent while work is in progress.
- All planning changes must be committed and opened as PRs in the planning repository so they are auditable.
- Keep a clear changelog entry in story frontmatter when moving a story between folders (status, date, author).

PR management
- Create clear PR titles like `planning: move STORY-ID to accepted (outcome)` or `planning: add proposal PROPOSAL-ID - <short title>`
- In PR body: include links to implementation PRs, outcomes, verification steps, and any follow-ups for the backlog

Coordination with Implementation Agent
- When moving a story to `accepted/`, include a link to the implementation PR and a short note describing verification steps and any unresolved follow-ups.
- When new dependencies or scope change are discovered, create a proposal (in `proposals/`) and notify the Implementation Agent via the PR or by referencing the implementation PR in the proposal.

Operational notes
- Use descriptive commit messages and include story IDs (format: `CATEGORY-###`) in commits and PRs.
- Keep proposals and stories small and testable. Split large items into smaller follow-ups.
