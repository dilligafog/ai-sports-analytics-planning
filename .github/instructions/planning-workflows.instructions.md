---
applyTo: '**'
---

# Planning Repository - Agent Workflows

Purpose: Define exact responsibilities and safe procedures for the Planning Agent so it can manage stories, proposals, roadmaps and PRs without stepping on implementation work.

Primary responsibilities
- Review and update proposals (migrate into `proposals/` when accepted)
- Update roadmaps, stories and priorities
- Maintain the story prioritization list (`backlog/PRIORITIZATION.json`) for implementation agents
- Groom the backlog and prepare stories for implementation using the JSON-based structure
- Coordinate with the `busta story` workflow system for seamless implementation transitions
- Update story status from `completed` to `accepted` using `python scripts/update_story.py STORY-ID --status accepted` when they meet acceptance criteria
- Never modify files directly - all status management happens through JSON updates and automated workflows
- Manage PRs for the planning repository (author, review, merge as needed)

Story lifecycle actions (Planning Agent)
1. New proposals: create a file under `proposals/` using the proposal template. Assign an owner and priority.
2. When a proposal is approved: create or update related stories in `backlog/` and the `roadmaps/` mapping.
3. Backlog grooming: reorder and split/merge backlog items, add acceptance criteria and estimates. Update prioritization list as needed.
4. Story workflow integration: Implementation Agent uses `busta story start [STORY_ID]` to begin work, which automatically moves stories from backlog to active and creates proper git branches
5. Acceptance: when an implementation completes via `busta story close`, update the story status from `completed` to `accepted` using `python scripts/update_story.py STORY-ID --status accepted`. Update the story with outcome notes and references to implementation PRs and release notes.

Rules and constraints
- The Planning Agent must never modify story files in `backlog/` — all status management happens through the `update_story.py` script which updates PRIORITIZATION.json
- Story workflow integration: the `busta story start/close` commands handle automated story transitions and git operations
- Backlog refinement should focus on JSON-based prioritization and story content quality
- All planning changes must be committed and opened as PRs in the planning repository so they are auditable.
- Keep a clear changelog entry in story JSON metadata when updating status (date, author, outcome).
- Coordinate with automated workflow systems rather than manual file operations

PR management
- Create clear PR titles like `planning: update STORY-ID status to accepted (outcome)` or `planning: add proposal PROPOSAL-ID - <short title>`
- In PR body: include links to implementation PRs, outcomes, verification steps, and any follow-ups for the backlog

Coordination with Implementation Agent
- Implementation Agent uses `busta story start [STORY_ID]` to automatically select and begin work on prioritized stories
- Story start workflow automatically moves stories from backlog to active and creates feature branches
- Implementation Agent uses `busta story close` to complete stories with automated CI checks, commits, PR creation, and status updates
- When updating a story status to `accepted`, include a link to the implementation PR and a short note describing verification steps and any unresolved follow-ups.
- When new dependencies or scope change are discovered, create a proposal (in `proposals/`) and notify the Implementation Agent via the PR or by referencing the implementation PR in the proposal.

Operational notes
- Use descriptive commit messages and include story IDs (format: `ADH-###`) in commits and PRs.
- Keep proposals and stories small and testable. Split large items into smaller follow-ups.
