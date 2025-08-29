# Reports & Analytics 📊

Automated reporting and metrics for AI Sports Analytics planning repository.

## Report Types

### 📈 **Velocity Reports** (`velocity/`)
- Sprint completion rates
- Story point throughput
- Epic progress tracking
- Team capacity analysis

### 🎯 **Priority Analytics** (`priority/`)
- Priority distribution analysis
- Backlog health metrics
- Stale story detection
- Epic balance reports

### 🔄 **Workflow Metrics** (`workflow/`)
- Story lifecycle timing
- Bottleneck identification
- Processing efficiency
- Automation performance

### 📋 **Backlog Health** (`backlog/`)
- Story completeness scoring
- Dependency mapping
- Risk assessment
- Technical debt tracking

## Automated Generation

Reports are automatically generated via:
- **Daily**: Workflow metrics and priority snapshots
- **Weekly**: Velocity and backlog health analysis  
- **Monthly**: Strategic overview and trend analysis
- **On-demand**: Custom reports via CLI tools

## GitHub Integration

- **README Badges**: Live metrics displayed in repository
- **GitHub Pages**: Dashboard hosting for stakeholder access
- **Actions**: Automated report generation on schedule
- **Releases**: Milestone reports attached to releases

## Usage

```bash
# Generate all reports
python scripts/generate_reports.py

# Specific report types
python scripts/generate_reports.py --type velocity
python scripts/generate_reports.py --type priority --output html

# Dashboard generation
python scripts/generate_dashboard.py --deploy-pages
```
