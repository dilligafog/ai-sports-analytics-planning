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

**Purpose**: Comprehensive priority management and backlog automation for strategic story refinement. Focuses on active stories by excluding completed ones from main views.

**Usage**:
```bash
# View current priority structure (excludes completed stories)
python scripts/manage_priorities.py --list

# View all stories including completed ones
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
- **Priority Visualization**: Shows current priority structure with status indicators (excludes completed stories by default)
- **Batch Reordering**: Insert multiple stories and automatically shift existing priorities
- **Range Shifting**: Move entire priority ranges up or down
- **Auto-Prioritization**: Intelligent scoring of ready stories based on epic, dependencies, and business value
- **Interactive Mode**: Full-featured CLI for complex priority management
- **Dry Run Support**: Preview changes before applying them
- **Completed Story Handling**: Completed/accepted stories are hidden by default but accessible with --all flag

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

**Purpose**: Comprehensive backlog grooming utility for systematic story refinement and validation. Focuses on active stories by excluding completed ones from grooming reports.

**Usage**:
```bash
# Generate grooming report for top 20 active stories
python scripts/backlog_groomer.py

# Run from repository root (recommended)
python backlog_groomer.py
```

**What it does**:
- **Story Validation**: Validates story ID formats and suggests corrections for active stories only
- **Epic Standardization**: Ensures consistent epic naming across active stories
- **Duplicate Detection**: Identifies and reports duplicate story entries among active stories
- **Priority Analysis**: Analyzes top-priority active stories needing grooming
- **Report Generation**: Creates comprehensive grooming reports with actionable insights
- **Completed Story Exclusion**: Completed and accepted stories are excluded from all grooming activities

**Features**:
- Automatic story ID validation with format suggestions (LLM-###, INF-###, etc.)
- Epic name standardization (infra → infrastructure, data_sources → ingestion)
- Duplicate story detection and reporting (active stories only)
- Top 20 priority active story analysis
- Markdown report generation for grooming sessions
- Clear indication of excluded completed stories in reports

**When to run**:
- Before major grooming sessions to identify issues in active stories
- After bulk story imports to validate data quality of new stories
- Weekly backlog health checks for active work
- When preparing active stories for implementation handoff

**Output**: Generates `backlog_grooming_report.md` with detailed findings and recommendations for active stories only.

**Current approach**: Status management happens through JSON updates in `PRIORITIZATION.json`. Story files remain in their original `backlog/` subdirectories.

### `assign_priorities.py`

**Purpose**: Assigns strategic priorities to all backlog stories based on epic importance, business value, dependencies, and implementation readiness.

**Usage**:
```bash
# Assign priorities to all stories
python scripts/assign_priorities.py
```

**What it does**:
- Analyzes epic importance and business value
- Considers dependencies and implementation readiness
- Generates prioritization markdown and updates JSON files
- Provides priority distribution analysis by epic

### `cleanup_data.py`

**Purpose**: Cleans up data quality issues, standardizes formats, and improves consistency of the story backlog data.

**Usage**:
```bash
# Perform data cleanup
python scripts/cleanup_data.py

# Generate cleanup report without making changes
python scripts/cleanup_data.py --report

# Show what would be cleaned without applying changes
python scripts/cleanup_data.py --dry-run
```

**What it does**:
- Standardizes epic names and estimate values
- Assigns default owners for epics
- Cleans up titles and adds missing labels
- Generates cleanup reports with improvement summaries

### `fix_prioritization_format.py`

**Purpose**: Placeholder script for fixing prioritization format issues (currently empty).

### `generate_performance_analytics.py`

**Purpose**: Generates advanced performance insights including team velocity trends, epic performance comparisons, resource allocation optimization, burndown projections, and risk probability modeling.

**Usage**:
```bash
# Generate comprehensive performance analytics
python scripts/generate_performance_analytics.py --type comprehensive

# Generate specific analytics type
python scripts/generate_performance_analytics.py --type velocity
python scripts/generate_performance_analytics.py --type resource
python scripts/generate_performance_analytics.py --type risk
python scripts/generate_performance_analytics.py --type burndown

# Specify output file
python scripts/generate_performance_analytics.py --output custom_report.json
```

**What it does**:
- Analyzes team velocity trends and patterns
- Compares epic performance and resource allocation
- Generates burndown projections and risk assessments
- Saves reports to the reports directory

### `generate_real_dashboard.py`

**Purpose**: Generates a professional dashboard using ONLY real project data, no synthetic data or fake metrics.

**Usage**:
```bash
# Generate real data dashboard
python scripts/generate_real_dashboard.py
```

**What it does**:
- Analyzes actual project stories and metadata
- Creates dashboard with real status counts and epic breakdowns
- Tracks actual completion rates and priorities
- Generates dashboard files in the reports directory

### `generate_reports.py`

**Purpose**: Comprehensive reporting engine that generates metrics, analytics, and dashboards for story management, velocity tracking, and strategic planning insights.

**Usage**:
```bash
# Generate all reports in JSON format
python scripts/generate_reports.py

# Generate specific report type
python scripts/generate_reports.py --type velocity
python scripts/generate_reports.py --type health
python scripts/generate_reports.py --type priority
python scripts/generate_reports.py --type workflow

# Generate reports in markdown format
python scripts/generate_reports.py --format markdown

# Generate dashboard data only
python scripts/generate_reports.py --dashboard

# Specify output directory
python scripts/generate_reports.py --output /path/to/output
```

**What it does**:
- Generates velocity and throughput metrics
- Creates backlog health reports
- Analyzes priority distributions
- Tracks workflow metrics and dashboard data
- Supports both JSON and markdown output formats

### `rename_story_files.py`

**Purpose**: Renames existing story files to use branch_name-based naming convention and updates file path references.

**Usage**:
```bash
# Rename story files to branch_name.md format
python scripts/rename_story_files.py
```

**What it does**:
- Scans all story files in the backlog directory
- Extracts branch_name from YAML frontmatter
- Renames files to match their branch_name
- Updates file_path references in PRIORITIZATION.json
- Automatically regenerates COMPLETE_BACKLOG.json

### `test_reporting_system.py`

**Purpose**: Tests and validates the AI Sports Analytics reporting system, running comprehensive tests on data integrity, report generation, and dashboard functionality.

**Usage**:
```bash
# Run comprehensive tests
python scripts/test_reporting_system.py

# Save test results to file
python scripts/test_reporting_system.py --save-results

# Exit with error code if tests fail
python scripts/test_reporting_system.py --exit-on-failure
```

**What it does**:
- Validates required data files exist and are valid
- Tests report generation functionality
- Checks dashboard data integrity
- Generates test result summaries
- Supports saving results to JSON files

### `update_prioritization_paths.py`

**Purpose**: Updates PRIORITIZATION.json file paths to match renamed files by syncing with COMPLETE_BACKLOG.json.

**Usage**:
```bash
# Update file paths in PRIORITIZATION.json
python scripts/update_prioritization_paths.py
```

**What it does**:
- Loads both PRIORITIZATION.json and COMPLETE_BACKLOG.json
- Creates mapping from story ID to correct file path
- Updates file paths in PRIORITIZATION.json
- Reports number of paths updated

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