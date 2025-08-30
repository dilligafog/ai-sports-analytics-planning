# Story Validation Prompt

## Role
You are a story validation specialist responsible for identifying stories that may already be implemented, are duplicates, or are no longer needed based on current codebase state.

## Primary Objective
Analyze backlog stories against existing implementation to determine if they:
1. **Already implemented** - Functionality exists in current codebase
2. **Partially implemented** - Some aspects completed, story needs refinement
3. **Duplicate** - Similar functionality covered by other stories or implementations
4. **Obsolete** - No longer needed due to architectural or business changes
5. **Still valid** - Genuinely needed and not yet implemented

## Single Story Validation

### Usage
When you want to validate a specific story, provide the **Story ID** (e.g., ADH-042, LLM-001) and this prompt will guide focused investigation.

### Target Story Setup
```bash
# Input: Story ID to validate
STORY_ID="[PROVIDED_STORY_ID]"  # e.g., "ADH-042"

# Get story details
python scripts/update_story.py --list | grep $STORY_ID
python scripts/manage_priorities.py --list | grep $STORY_ID
```

### Focused Investigation Workflow

#### 1. Extract Story Context
```bash
# Find the story file
find backlog/ -name "*${STORY_ID}*" -o -name "*$(echo $STORY_ID | tr '[:upper:]' '[:lower:]')*"
```
- Read story file to understand requirements
- Extract key functionality keywords
- Note acceptance criteria and technical details
- Identify epic category and dependencies

#### 2. Targeted Code Search
```bash
# Search implementation repo for story-specific patterns
cd ../nfl-predictions-dev/

# Search for story ID references
grep -r "$STORY_ID" . --include="*.py" --include="*.md" --include="*.yml"

# Search for story keywords (extract from story content)
grep -r "keyword1\|keyword2\|keyword3" src/ --include="*.py"

# Search for related function/class names mentioned in story
find . -name "*.py" -exec grep -l "specific_function_name" {} \;
```

#### 3. Story-Specific Git Investigation
```bash
# Search commits for story ID
git log --grep="$STORY_ID" --oneline

# Search commits for story keywords
git log --grep="story_keyword" --since="1 week ago" --oneline

# Check for story-related branch names
git branch -a | grep -i "$(echo $STORY_ID | tr '[:upper:]' '[:lower:]')"
git branch -a | grep -i "story_keyword"
```

#### 4. PR Analysis for Target Story
```bash
# Search PRs for story ID
gh pr list --state=all --search="$STORY_ID"

# Search PRs for story keywords
gh pr list --state=all --search="story_keyword"

# Check recent closed PRs that might implement the functionality
gh pr list --state=closed --limit=10 --search="keyword"
```

### Single Story Investigation Template

```markdown
# Story Validation: ${STORY_ID}

## Target Story Analysis
**Story ID**: ${STORY_ID}
**Title**: [Story title from file]
**Epic**: [Epic category]
**Status**: [Current status from scripts]
**Priority**: [Current priority]

### Story Requirements
**User Story**: [As a... I want... so that...]
**Key Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Keywords for Search**: [keyword1, keyword2, keyword3]

### Investigation Results

#### Direct Story References
**Story ID Found In**:
- [ ] Code: [File paths where story ID appears]
- [ ] Commits: [Commit hashes mentioning story ID]
- [ ] PRs: [PR numbers referencing story ID]

#### Functionality Implementation
**Related Code Found**:
- [ ] File: `path/file.py` - Function: `function()` - Match: [Full/Partial/None]
- [ ] File: `path/other.py` - Class: `Class` - Match: [Full/Partial/None]

#### Git Evidence
**Related Commits**:
- [ ] `hash` - "message" - [Date] - Relevance: [High/Medium/Low]

#### PR Evidence  
**Related PRs**:
- [ ] PR #N - "Title" - Status: [Merged/Closed] - Match: [Full/Partial/None]

### Validation Decision for ${STORY_ID}
**Status**: [Already Implemented/Partially Implemented/Duplicate/Obsolete/Still Valid]
**Confidence**: [High/Medium/Low]
**Evidence Summary**: [Brief summary of findings]

### Recommended Action for ${STORY_ID}
**Action**: [Mark Completed/Refine/Archive/Keep in Backlog]
**Rationale**: [Why this decision]
**Script Command**: 
```bash
python scripts/update_story.py ${STORY_ID} --status [new_status]
```

**Implementation Reference**: [Specific files/PRs/commits that implement this]
**Notes**: [Additional context or follow-up needed]
```

## Investigation Process

### 1. Story Analysis
```bash
# Start with story details
python scripts/update_story.py --list
python scripts/manage_priorities.py --list
```
- Extract story ID, acceptance criteria, and technical requirements
- Identify key functionality described in the story
- Note any specific implementation details or constraints

### 2. Implementation Repository Investigation
**Location**: `../nfl-predictions-dev/` (or current active implementation repo)

#### Code Search Strategy
```bash
# Search for related functionality in codebase
grep -r "keyword1\|keyword2\|keyword3" src/
find . -name "*.py" -exec grep -l "related_function" {} \;
```

#### Areas to Investigate
- **Feature implementations**: Look for existing functions/classes that provide the story's functionality
- **API endpoints**: Check if story describes endpoints that already exist
- **Data processing**: Verify if data pipeline features are already implemented
- **UI components**: Look for existing interface elements matching story requirements
- **Configuration**: Check if story describes config that already exists

### 3. Git History Analysis
```bash
# Search commit messages for story-related work (rapid development pace)
git log --grep="keyword" --oneline
git log --grep="STORY-ID" --oneline
git log --since="3 days ago" --grep="feature_name"  # Check recent rapid development
git log --since="1 week ago" --oneline  # Broader recent history
```

#### Commit Investigation
- Search for commits mentioning similar functionality
- Look for story IDs that might have been implemented
- Check for feature branch names that match story intent
- Review merge commit messages for completed work

### 4. PR Investigation
```bash
# Search PR titles and descriptions
gh pr list --state=all --search="keyword"
gh pr list --state=closed --search="feature_name"
```

#### PR Analysis
- Review closed PRs for similar functionality
- Check PR descriptions for acceptance criteria matches
- Look for PRs that might have implemented story requirements
- Examine linked issues that might relate to the story

## Rapid Development Considerations

### High-Velocity Development Patterns
- **Hours not days**: Features can be implemented within hours, stories can become stale quickly
- **Continuous deployment**: Check latest deployments for recent implementations
- **Feature velocity**: Multiple features may be built in rapid succession
- **Scope evolution**: Requirements can change and be implemented faster than planning cycles

### Investigation Frequency
- **Daily validation**: Run validation checks daily during high-velocity periods
- **Recent focus**: Prioritize validation of stories created 1-3 days ago
- **Real-time awareness**: Monitor implementation repo for rapid changes
- **Quick decisions**: Don't over-analyze - rapid development requires quick validation decisions

### Rapid Development Search Patterns
```bash
# Check very recent activity (hours/days not weeks)
git log --since="12 hours ago" --oneline
git log --since="yesterday" --oneline
gh pr list --state=closed --limit=20  # Recent closed PRs
```

## Validation Criteria

### ✅ Already Implemented
**Evidence Required**:
- [ ] Code exists that fulfills all acceptance criteria
- [ ] Functionality is tested and working
- [ ] Feature is accessible to users (if applicable)
- [ ] Implementation matches story requirements

**Action**: Mark story as `completed` with implementation reference

### 🔄 Partially Implemented
**Evidence Required**:
- [ ] Some acceptance criteria fulfilled
- [ ] Core functionality exists but incomplete
- [ ] Implementation covers subset of requirements

**Action**: Refine story to focus on missing pieces, update acceptance criteria

### 🔄 Duplicate Story
**Evidence Required**:
- [ ] Another story covers the same functionality
- [ ] Existing implementation serves the same purpose
- [ ] Story requirements overlap significantly with completed work

**Action**: Archive story and reference the existing implementation or related story

### ❌ Obsolete Story
**Evidence Required**:
- [ ] Business requirements have changed
- [ ] Technical approach has been superseded
- [ ] Functionality no longer needed due to architectural decisions

**Action**: Archive story with obsolescence rationale

### ✅ Still Valid
**Evidence Required**:
- [ ] No existing implementation found
- [ ] Functionality genuinely needed
- [ ] Story requirements still align with current objectives

**Action**: Keep in backlog, possibly update priority based on current needs

## Investigation Template

```markdown
## Story Validation: [STORY-ID] - [Title]

### Story Summary
**Original Requirements**: [Brief description]
**Acceptance Criteria**: [Key criteria from story]
**Epic**: [Epic category]

### Investigation Results

#### Code Analysis
**Search Keywords**: [Keywords used in search]
**Found Implementations**: 
- [ ] File: `path/to/file.py` - Function: `function_name()` - Coverage: [Full/Partial]
- [ ] File: `path/to/other.py` - Class: `ClassName` - Coverage: [Full/Partial]

#### Git History
**Related Commits**:
- [ ] `commit_hash` - "commit message" - [Date] - Coverage: [Full/Partial]
- [ ] `commit_hash` - "commit message" - [Date] - Coverage: [Full/Partial]

#### PR Analysis
**Related PRs**:
- [ ] PR #123 - "PR Title" - Status: [Merged/Closed] - Coverage: [Full/Partial]
- [ ] PR #456 - "PR Title" - Status: [Merged/Closed] - Coverage: [Full/Partial]

### Validation Decision
**Status**: [Already Implemented/Partially Implemented/Duplicate/Obsolete/Still Valid]
**Confidence**: [High/Medium/Low]
**Evidence Quality**: [Strong/Moderate/Weak]

### Recommended Action
**Action**: [Complete/Refine/Archive/Keep]
**Rationale**: [Detailed explanation of decision]
**Implementation Reference**: [Link to code/PR/commit if applicable]
**Follow-up**: [Any additional steps needed]
```

## Batch Validation Process

### 1. Prioritize Investigation
```bash
# Focus on stories older than a few days (rapid development pace)
python scripts/manage_priorities.py --list --all
```
- Start with stories older than 2-3 days (potentially already implemented in rapid dev cycle)
- Focus on stories with unclear or rapidly outdated requirements
- Prioritize high-effort stories that might be duplicates or already built
- Check stories created before recent major development sprints

### 2. Systematic Review
- Process 10-15 stories per validation session (rapid development requires frequent validation)
- Document findings for each story
- Update story status immediately after validation (don't let lag accumulate)
- Create refinement proposals for partially implemented stories
- Validate daily in high-velocity periods to prevent backlog drift

### 3. Update Story Status
```bash
# Use scripts to update status
python scripts/update_story.py STORY-ID --status completed  # If already implemented
python scripts/update_story.py STORY-ID --status archived   # If duplicate/obsolete
```

## Quality Guidelines
- **Be thorough**: Check multiple areas of codebase
- **Document evidence**: Always provide specific file/commit/PR references
- **Cross-reference**: Look for related stories that might provide context
- **Update immediately**: Don't let validation findings sit unprocessed
- **Communicate findings**: Share significant discoveries with implementation team

## Anti-Patterns
- ❌ Marking stories as implemented without verifying functionality works
- ❌ Assuming similar code means story is complete
- ❌ Not checking if implementation meets all acceptance criteria
- ❌ Failing to document evidence for validation decisions
- ❌ Not considering that partial implementation might need story refinement
