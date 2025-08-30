---
applyTo: '**'
---

# Planning Repository - Agent Workflows

Purpose: Define exact responsibilities and safe procedures for the Planning Agent so it can manage stories, proposals, roadmaps and PRs without stepping on implementation work.

## Primary Responsibilities

- Review and update proposals (migrate into `proposals/` when accepted)
- Manage story lifecycle through script-based automation
- Maintain strategic prioritization using `manage_priorities.py`
- Perform systematic backlog grooming using `backlog_groomer.py`
- Coordinate with the `busta story` workflow system in the implementation repository for seamless transitions
- Process new stories through `ingest_stories.py` with proper validation and epic assignment
- Never modify story files directly - all management happens through JSON-based scripts
- Manage PRs for the planning repository (author, review, merge as needed)

## Script-Based Story Management

All story operations must use the provided scripts to ensure data consistency and workflow integration:

- **Story Ingestion**: `python scripts/ingest_stories.py` for processing new stories from staging
- **Priority Management**: `python scripts/manage_priorities.py` for strategic story ordering
- **Status Updates**: `python scripts/update_story.py` for workflow state transitions
- **Backlog Health**: `python scripts/backlog_groomer.py` for validation and grooming reports
- **Bulk Operations**: `python scripts/generate_complete_backlog.py` for full synchronization

## Story Lifecycle Actions (Planning Agent)

### 1. New Story Creation
```bash
# Interactive story creation with template selection
python scripts/ingest_stories.py --interactive

# Create specific story types
python scripts/ingest_stories.py --template basic --title "Feature Name" --epic core
python scripts/ingest_stories.py --template technical --title "Tech Task" --epic infra
python scripts/ingest_stories.py --template spike --title "Research Task" --epic core

# Process staged markdown/JSON files
python scripts/ingest_stories.py --dry-run  # Preview first
python scripts/ingest_stories.py            # Process all staged
```

### 2. Strategic Prioritization
```bash
# View current priority structure
python scripts/manage_priorities.py --list

# Set strategic priorities for implementation readiness
python scripts/manage_priorities.py --set STORY-ID --priority 5

# Insert high-priority stories and shift others
python scripts/manage_priorities.py --insert LLM-001,LLM-002 --at 1 --shift

# Auto-prioritize ready stories using business logic
python scripts/manage_priorities.py --auto-prioritize --max-priority 10

# Interactive mode for complex reordering sessions
python scripts/manage_priorities.py --interactive
```

### 3. Backlog Grooming
```bash
# Generate comprehensive grooming report
python scripts/backlog_groomer.py

# Review findings in generated report
cat backlog_grooming_report.md
```

### 4. Status Management
```bash
# List ready stories for implementation handoff
python scripts/update_story.py --list

# Update story status during workflow transitions
python scripts/update_story.py STORY-ID --status active     # When busta story start
python scripts/update_story.py STORY-ID --status completed  # When busta story close
python scripts/update_story.py STORY-ID --status accepted   # After verification
```

### 5. Bulk Synchronization
```bash
# Regenerate complete backlog after major changes
python scripts/generate_complete_backlog.py
```

## Rules and Constraints

### Script-First Operations
- **Never modify story files directly** - all operations must use the provided scripts
- **Always use dry-run flags** when available to preview changes before applying
- **Status management** happens exclusively through `update_story.py` and `PRIORITIZATION.json`
- **Story ingestion** uses templates and validation through `ingest_stories.py`
- **Priority changes** use strategic scoring and batch operations through `manage_priorities.py`

### Workflow Integration
- **Story transitions**: Coordinate with `busta story start/close` commands in implementation repository
- **Backlog grooming**: Use `backlog_groomer.py` to identify validation issues and refinement needs
- **Priority alignment**: Use business logic scoring to ensure strategic story ordering
- **Data consistency**: Run `generate_complete_backlog.py` after major structural changes

### Quality Gates
- All planning changes must be committed and opened as PRs for audit trail
- Story validation and epic standardization through grooming reports
- Priority conflicts resolved through interactive management sessions
- Template customization required - no stub stories accepted for implementation

### Coordination Protocol
- Use script outputs and reports to communicate story readiness
- Include grooming reports in planning PRs for transparency
- Reference priority changes and business justification in commit messages
- Maintain clear changelog entries in story JSON metadata

## PR Management

### Planning Repository PRs
```bash
# Before creating PR - run validation
python scripts/backlog_groomer.py

# Create PR with script-generated context
git add .
git commit -m "planning: STORY-ID priority update (business justification)"
```

**PR Title Patterns**:
- `planning: update STORY-ID status to accepted (outcome summary)`
- `planning: prioritize LLM epic stories for Q3 implementation`
- `planning: ingest new stories from proposal PROPOSAL-ID`
- `planning: backlog grooming - resolve validation issues`

**PR Body Requirements**:
- Include grooming report excerpts for validation changes
- Reference implementation PRs for status updates
- Document priority changes with business justification
- Link to related proposals or roadmap updates

### Cross-Repository Implementation Coordination

**Planning Repository (this repo)**:
```bash
# Planning Agent: Prepare stories for implementation
python scripts/update_story.py --list          # Show ready stories
python scripts/manage_priorities.py --list     # Show priority order
```

**Implementation Repository (`nfl-predictions-dev`)**:
```bash
# Implementation Agent: Query and start work
busta story start [STORY_ID]    # Auto-discovers from planning repo priorities
# ... implementation work happens ...
busta story close               # Completes with CI checks and PR creation
```

**Handoff Protocol**:
1. **Planning Agent**: Stories marked ready in `ai-sports-analytics-planning`
2. **Implementation Agent**: Discovers stories via `busta story start` in `nfl-predictions-dev`
3. **Auto-sync**: Implementation tools read from planning repo's `PRIORITIZATION.json`
4. **Status updates**: Implementation completion triggers updates back to planning repo
5. **Planning Agent**: Verify and accept with `python scripts/update_story.py STORY-ID --status accepted`

**Scope Changes**:
- Create proposal in `proposals/` for new dependencies discovered during implementation
- Reference implementation repository PR in proposal for context
- Use `manage_priorities.py` to adjust affected story priorities in planning repo
- Cross-repository coordination through planning PR comments or implementation PR references

## Operational Notes

### Daily Operations
```bash
# Morning planning routine
python scripts/update_story.py --list          # Check ready stories
python scripts/manage_priorities.py --list     # Review current priorities

# Weekly grooming session
python scripts/backlog_groomer.py              # Generate health report
python scripts/manage_priorities.py --auto-prioritize --max-priority 15

# After bulk changes
python scripts/generate_complete_backlog.py    # Synchronize data
```

### Script Integration Patterns
- **Preview before apply**: Always use `--dry-run` flags when available
- **Batch operations**: Use `manage_priorities.py --interactive` for complex reordering
- **Validation first**: Run `backlog_groomer.py` before major changes
- **Template enforcement**: Use `ingest_stories.py --template` for consistent story structure
- **Business logic**: Let `--auto-prioritize` handle epic-based scoring

### Commit Message Standards
- Include story IDs in format: `ADH-###`, `LLM-###`, `INF-###`
- Reference script operations: `planning: auto-prioritize core epic stories`
- Include business context: `planning: prioritize LLM stories for Q3 delivery`
- Cross-reference: `planning: accept STORY-ID (implements feature X in PR #123)`

### Error Recovery
- Use `generate_complete_backlog.py` to rebuild from source files
- Check `backlog_grooming_report.md` for validation issues
- Use `manage_priorities.py --list --all` to see unprocessed stories
- Validate epic mappings through grooming reports before major operations
