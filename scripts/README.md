# Scripts Directory

Automation scripts for maintaining the planning repository.

## 📋 Current Workflow

Stories are managed through JSON-based status updates. Files stay in their original `backlog/` subdirectories and status changes happen through `PRIORITIZATION.json` updates. **No file moving is required.**

## Prerequisites

Install required dependencies:
```bash
pip install -r scripts/requirements.txt
```

## ✅ Active Scripts

### `ingest_stories.py`

**Purpose**: Process new stories from staging area into the main backlog with proper ID assignment, validation, and epic placement.

**Usage**:
```bash
# Process all staged stories (markdown and JSON)
python scripts/ingest_stories.py

# Interactive story creation
python scripts/ingest_stories.py --interactive

# Create story from template
python scripts/ingest_stories.py --template basic --title "New Feature" --epic core
python scripts/ingest_stories.py --template technical --title "Database Migration" --epic infra
python scripts/ingest_stories.py --template spike --title "Research GraphQL" --epic core

# Process specific file types only
python scripts/ingest_stories.py --markdown-only
python scripts/ingest_stories.py --json-only

# Dry run to see what would be processed
python scripts/ingest_stories.py --dry-run
```

**Features**:
- Automatic story ID generation based on epic
- Validation of required fields and epic mappings
- Git branch name generation
- Markdown frontmatter parsing
- JSON bulk import support
- Story archiving to processed/ directory
- Integration with PRIORITIZATION.json

### `manage_priorities.py`

**Purpose**: Comprehensive priority management and backlog automation for strategic story refinement.

**Usage**:
```bash
# View current priority structure
python scripts/manage_priorities.py --list

# View all stories including unprocessed (priority 99)
python scripts/manage_priorities.py --list --all

# Set specific story priority
python scripts/manage_priorities.py --set LLM-001 --priority 5

# Insert new stories at top priorities, shift others down
python scripts/manage_priorities.py --insert RSS-001,RSS-002,RSS-003 --at 1 --shift

# Shift priority range down (dry run first)
python scripts/manage_priorities.py --shift-from 5 --positions 2 --dry-run
python scripts/manage_priorities.py --shift-from 5 --positions 2

# Auto-prioritize ready stories using business logic
python scripts/manage_priorities.py --auto-prioritize --max-priority 10

# Interactive mode for complex reordering
python scripts/manage_priorities.py --interactive
```

**What it does**:
- **Priority Visualization**: Shows current priority structure with status indicators
- **Batch Reordering**: Insert multiple stories and automatically shift existing priorities
- **Range Shifting**: Move entire priority ranges up or down
- **Auto-Prioritization**: Intelligent scoring of ready stories based on epic, dependencies, and business value
- **Interactive Mode**: Full-featured CLI for complex priority management
- **Dry Run Support**: Preview changes before applying them

**Business Logic Scoring**:
- **Core LLM**: Highest priority (score +10)
- **Modeling**: High priority (score +8)  
- **Ingestion**: Medium-high priority (score +7)
- **UI**: Medium priority (score +6)
- **Quality**: Medium-low priority (score +5)
- **Infrastructure**: Low priority (score +4)
- **Adhoc**: Lowest priority (score +1)
- **No Dependencies**: Easier to implement (+2 bonus)
- **Assigned Owner**: Ready for work (+1 bonus)

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

### `backlog_groomer.py`

**Purpose**: Comprehensive backlog grooming utility for systematic story refinement and validation.

**Usage**:
```bash
# Generate grooming report for top 20 stories
python scripts/backlog_groomer.py

# Run from repository root (recommended)
python backlog_groomer.py
```

**What it does**:
- **Story Validation**: Validates story ID formats and suggests corrections
- **Epic Standardization**: Ensures consistent epic naming across stories
- **Duplicate Detection**: Identifies and reports duplicate story entries
- **Priority Analysis**: Analyzes top-priority stories needing grooming
- **Report Generation**: Creates comprehensive grooming reports with actionable insights

**Features**:
- Automatic story ID validation with format suggestions (LLM-###, INF-###, etc.)
- Epic name standardization (infra → infrastructure, data_sources → ingestion)
- Duplicate story detection and reporting
- Top 20 priority story analysis
- Markdown report generation for grooming sessions

**When to run**:
- Before major grooming sessions to identify issues
- After bulk story imports to validate data quality
- Weekly backlog health checks
- When preparing stories for implementation handoff

**Output**: Generates `backlog_grooming_report.md` with detailed findings and recommendations.

**Current approach**: Status management happens through JSON updates in `PRIORITIZATION.json`. Story files remain in their original `backlog/` subdirectories.

## Script Development Guidelines

- **Keep scripts simple**: Focus on single, clear purposes
- **Use JSON-based updates**: Modify status through PRIORITIZATION.json, not file movement
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