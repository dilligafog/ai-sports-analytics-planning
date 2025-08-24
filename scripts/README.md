# Scripts Directory

Automation scripts for maintaining the planning repository.

## Available Scripts

### `regenerate_prioritization.py`

**Purpose**: Automatically generate the `backlog/PRIORITIZATION.md` file from current story metadata.

**Usage**:
```bash
# From repository root
python3 scripts/regenerate_prioritization.py
```

**What it does**:
- Scans all story files in `backlog/` subdirectories
- Extracts metadata (priority, dependencies, estimates, etc.)
- Sorts stories by priority and dependency status
- Generates a comprehensive prioritization list for implementation agents

**When to run**:
- After adding new stories to the backlog
- After changing story priorities or dependencies  
- Weekly during backlog grooming
- Before major planning reviews

**Output**:
- Updates `backlog/PRIORITIZATION.md` with current story status
- Shows summary of ready vs blocked stories
- Maintains automation timestamp

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