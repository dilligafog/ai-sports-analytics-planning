# Story Staging Area

This directory serves as a staging area for new stories before they are processed and moved to the appropriate epic folders in the backlog.

## Directory Structure

```
staging/
├── README.md              # This file
├── new/                   # New story files waiting to be processed
├── templates/             # Quick-start templates for different story types
├── bulk/                  # Bulk import files (JSON, CSV, YAML)
└── processed/            # Archive of recently processed stories
```

## Workflow

### 1. Story Creation
- Place new story files in `staging/new/`
- Use templates from `staging/templates/` for consistency
- Follow naming convention: `TEMP-###-descriptive-title.md`

### 2. Processing
- Run `python scripts/ingest_stories.py` to process staged stories
- Stories are validated, assigned proper IDs, and moved to correct epic folders
- Backlog JSON files are automatically updated

### 3. Archive
- Processed stories are moved to `staging/processed/` for reference
- Original staging files are kept for audit trail

## Input Formats

### Method 1: Markdown Files
Use the standard story template format. Place in `staging/new/`.

### Method 2: Quick JSON
Create a simple JSON file for bulk story creation:
```json
{
  "stories": [
    {
      "title": "Story title",
      "epic": "core",
      "user_story": "As a user I want...",
      "acceptance_criteria": ["Criterion 1", "Criterion 2"],
      "priority": "medium",
      "estimate": "3sp"
    }
  ]
}
```

### Method 3: CSV Bulk Import
For large numbers of stories from external tools:
```csv
title,epic,priority,estimate,user_story,acceptance_criteria
"Story 1","core","high","2sp","As a user...","Can do X; Can do Y"
```

### Method 4: Interactive CLI
Use `python scripts/ingest_stories.py --interactive` for guided story creation.

## Auto-Processing Rules

Stories are automatically:
1. **ID Assignment**: Next available ID in the target epic
2. **File Naming**: Converted to proper kebab-case format
3. **Epic Placement**: Moved to correct backlog subfolder
4. **JSON Updates**: Added to PRIORITIZATION.json and COMPLETE_BACKLOG.json
5. **Validation**: Checked for required fields and formatting

## Quality Gates

Before processing, stories must have:
- ✅ Clear title
- ✅ Valid epic assignment
- ✅ User story format
- ✅ At least one acceptance criterion
- ✅ Reasonable estimate

## Templates Available

- `basic_story.md` - Standard user story
- `technical_story.md` - Infrastructure/technical work
- `spike_story.md` - Research and investigation
- `epic_story.md` - Large feature breakdown
- `bug_story.md` - Defect resolution
