# Scripts Directory

Automation scripts for maintaining the planning repository.

## Available Scripts

### `update_story.py`

**Purpose**: Direct JSON-based story workflow management for the prioritization system.

**Usage**:
```bash
# List ready stories for implementation
python scripts/update_story.py --list

# See all stories with status overview  
python scripts/update_story.py --all

# Update story status
python scripts/update_story.py STORY-ID --status active
python scripts/update_story.py STORY-ID --status completed
```

**What it does**:
- Provides CLI interface to story status management
- Shows ready-to-start stories for Neo Starlord of Thunder
- Updates story status in PRIORITIZATION.json
- Maintains epic and dependency tracking

### `generate_complete_backlog.py`

**Purpose**: Generate comprehensive JSON backlog from all story files.

**Usage**:
```bash
# Regenerate complete backlog JSON from current story files
python scripts/generate_complete_backlog.py
```

**What it does**:
- Scans all story files across epic folders
- Extracts YAML frontmatter and metadata
- Updates PRIORITIZATION.json with complete story tracking
- Maintains dependencies, epic categorization, and file paths

**When to run**:
- After adding new stories to backlog folders
- After major backlog restructuring
- Weekly backlog synchronization

### `migrate_backlog_structure.py`

**Purpose**: One-time migration tool for folder structure reorganization.

**Status**: ✅ **Completed** - Successfully migrated stories to clean epic-based folders

**What it accomplished**:
- Moved 24 LLM stories to functional folders (core, ingestion, modeling, quality, explain, infra)
- Updated all file paths in PRIORITIZATION.json
- Cleaned up old nested folder structure

## Script Development Guidelines

- **Keep scripts simple**: Focus on single, clear purposes
- **Use standard libraries**: Avoid external dependencies where possible
- **Include error handling**: Gracefully handle missing files or invalid data
- **Log meaningful output**: Help users understand what happened
- **Follow naming conventions**: Use snake_case and descriptive names

## Adding New Scripts

1. Create the script in this directory
2. Make it executable: `chmod +x script_name.py`
3. Add usage documentation to this README
4. Test thoroughly with various repository states
5. Consider integration with CI/CD if appropriate

## Related Documentation

- [Planning Workflows](../.github/instructions/planning-workflows.instructions.md)
- [Cross-Repository Coordination](../.github/instructions/cross-repo-coordination.instructions.md)
- [Backlog Organization](../backlog/README.md)