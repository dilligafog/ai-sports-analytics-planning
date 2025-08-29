---
applyTo: '**'
---

# Planning Repository - Agent Workflows

Purpose: Define exact responsibilities and safe procedures for the Planning Agent so it can manage stories, proposals, roadmaps and PRs without stepping on implementation work.

Primary responsibilities
- Review and update proposals (migrate into `proposals/` when accepted)
- Update roadmaps, stories and priorities
- Maintain the story prioritization list (`backlog/PRIORITIZATION.md`) for implementation agents
- Groom the backlog and prepare stories for implementation
- Update story status from `completed` to `accepted` using `python scripts/update_story.py STORY-ID --status accepted` when they meet acceptance criteria
- Never modify files - all status management happens through JSON updates
- Manage PRs for the planning repository (author, review, merge as needed)

Story lifecycle actions (Planning Agent)
1. New proposals: create a file under `proposals/` using the proposal template. Assign an owner and priority.
2. When a proposal is approved: create or update related stories in `backlog/` and the `roadmaps/` mapping.
3. Backlog grooming: reorder and split/merge backlog items, add acceptance criteria and estimates. Update prioritization list as needed.
4. Acceptance: when an implementation completes and the Implementation Agent signals success, update the story status from `completed` to `accepted` using `python scripts/update_story.py STORY-ID --status accepted`. Update the story with outcome notes and references to implementation PRs and release notes.

Rules and constraints
- The Planning Agent must never modify story files in `backlog/` — all status management happens through the `update_story.py` script which updates PRIORITIZATION.json
- All planning changes must be committed and opened as PRs in the planning repository so they are auditable.
- Keep a clear changelog entry in story JSON metadata when updating status (date, author, outcome).

PR management
- Create clear PR titles like `planning: update STORY-ID status to accepted (outcome)` or `planning: add proposal PROPOSAL-ID - <short title>`
- In PR body: include links to implementation PRs, outcomes, verification steps, and any follow-ups for the backlog

Coordination with Implementation Agent
- When updating a story status to `accepted`, include a link to the implementation PR and a short note describing verification steps and any unresolved follow-ups.
- When new dependencies or scope change are discovered, create a proposal (in `proposals/`) and notify the Implementation Agent via the PR or by referencing the implementation PR in the proposal.

Operational notes
- Use descriptive commit messages and include story IDs (format: `ADH-###`) in commits and PRs.
- Keep proposals and stories small and testable. Split large items into smaller follow-ups.
