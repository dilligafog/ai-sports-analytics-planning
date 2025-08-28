---
id: INF-009
title: ADH Story File Storage System
branch_name: inf-009-adhoc-story-file-storage
epic: infrastructure
status: backlog
priority: high
estimate: "1sp"
dependencies: []
labels: [adhoc, workflow, infrastructure, process-improvement]
created: 2025-08-27
author: Strategic Nexus Prime
owner: Neo Starlord of Thunder
market: null
layer: null
last_updated: 2025-08-27
emit_metadata:
  source_id: null
  layer: null
  input_path: null
  notes: "Critical for ADH workflow consistency and branch naming"
---

# INF-009: ADH Story File Storage System

## User Story
**As a** development team  
**I want** persistent file storage for ADH stories  
**So that** branch naming is consistent and story references are trackable throughout the workflow

## Value Proposition
- **Consistent branch naming**: ADH stories get same `STORY-ID-descriptive-name` format as regular stories
- **Trackable references**: All story lifecycle events can reference a persistent file
- **Workflow uniformity**: ADH and regular stories follow identical file-based processes
- **Audit trail**: Complete history of ADH decisions and implementations
- **Complete JSON tracking**: All stories (including ADH) tracked in unified PRIORITIZATION.json system

## Acceptance Criteria
- [ ] Create `adhoc/` directory structure for ADH story files
- [ ] ADH stories get persistent `.md` files with standard YAML frontmatter including `branch_name` field
- [ ] ADH file naming follows pattern: `ADH-###-descriptive-name.md`
- [ ] Branch naming for ADH work follows: `ADH-###-descriptive-name` (from YAML `branch_name` field)
- [ ] ADH workflow updated to create file before starting implementation
- [ ] ADH files move through same lifecycle: `adhoc/` → `active/` → `completed/` → `accepted/`
- [ ] All ADH stories included in PRIORITIZATION.json with proper status tracking
- [ ] Neo Starlord of Thunder can update ADH story status via `scripts/update_story.py`
- [ ] ADH stories visible in `--list` and `--list --all` outputs
- [ ] Update ADH_WORKFLOW.md documentation with new JSON-integrated process

## Technical Notes
- ADH files should have minimal required content (just enough for branch naming and tracking)
- Fast creation process - don't slow down urgent ADH work
- Use template: `templates/adhoc_story_template.md` (already created with `branch_name` field)
- **JSON Integration**: ADH stories automatically included in PRIORITIZATION.json via `generate_complete_backlog.py`
- Status updates via: `python scripts/update_story.py ADH-### --status active`
- Branch creation: Use `branch_name` field from story YAML frontmatter

## Current ADH Workflow Issues
1. **No persistent files** → Inconsistent branch naming
2. **Lost context** → Hard to reference ADH work later  
3. **Tracking gaps** → ADH stories not in file-based systems
4. **Branch naming chaos** → No standard for ADH branches

## Proposed ADH Directory Structure
```
adhoc/
├── README.md                           # ADH workflow documentation
├── ADH-001-update-busta-adhoc.md     # Example existing ADH (retroactive)
├── ADH-002-fix-inventory-sidebar.md   # Example existing ADH (retroactive)
└── ADH-###-new-urgent-fix.md          # Future ADH stories

templates/                              # ✅ COMPLETED
├── adhoc_story_template.md            # ✅ Quick ADH story template with branch_name
└── standardized_story_template.md     # ✅ Full story template

scripts/                               # ✅ COMPLETED
├── update_story.py                    # ✅ Update any story status (including ADH)
└── generate_complete_backlog.py       # ✅ Auto-include ADH stories in JSON

backlog/
└── PRIORITIZATION.json                # ✅ COMPLETED - All stories tracked with status
```

## New ADH Workflow (JSON-Integrated)
1. **Create ADH file**: Copy `templates/adhoc_story_template.md` → `adhoc/ADH-###-description.md`
2. **Update YAML**: Set `branch_name`, `title`, and `id` fields
3. **Update JSON**: `python scripts/update_story.py ADH-### --status active`
4. **Create branch**: `git checkout -b {branch_name}` (from YAML)
5. **Implement fix**: Standard development process
6. **Mark complete**: `python scripts/update_story.py ADH-### --status completed`
7. **Move to accepted**: Strategic Nexus Prime processes completion

## Definition of Done
- [ ] ADH directory structure created
- [ ] ADH template created for fast story creation (✅ COMPLETED - `templates/adhoc_story_template.md`)
- [ ] Documentation updated (ADH_WORKFLOW.md)
- [ ] Complete PRIORITIZATION.json integration (✅ COMPLETED - all 46+ stories tracked)
- [ ] Status update tooling (✅ COMPLETED - `scripts/update_story.py`)
- [ ] ADH stories appear in story listing tools (✅ COMPLETED - `--list` and `--list --all`)
- [ ] Test ADH workflow with new file-based process
- [ ] Existing ADH stories migrated to new structure (retroactive files)
- [ ] Generate backlog script includes ADH stories (✅ COMPLETED - `scripts/generate_complete_backlog.py`)

## Implementation Status Updates
**2025-08-27**: Core JSON infrastructure completed by Strategic Nexus Prime:
- ✅ Complete backlog JSON system with 46 stories
- ✅ Story update tooling (`scripts/update_story.py`)
- ✅ ADH template with `branch_name` field
- ✅ Automatic backlog generation script
- 🔄 **Remaining**: ADH directory structure and workflow documentation

## References
- Related to current ADH workflow gap identified in story standardization
- Supports consistent branch naming across all story types
- Enables complete audit trail for all development work

---
**Story Lifecycle:**
- Created: 2025-08-27 by Strategic Nexus Prime
- Updated: 2025-08-27 by Strategic Nexus Prime (JSON infrastructure completed)
- Strategic Priority: High (blocks workflow standardization)  
- Implementation: Reduced to 1sp (core infrastructure already built)
- Status: ~70% complete (JSON system built, need ADH directory and docs)
