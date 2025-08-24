# Proposal: COORD-001 - Enhanced Cross-Repository Story Status Tracking

## Summary
Enhance the current story status tracking system to provide better visibility and coordination between the planning and implementation repositories while maintaining the preferred folder-based organization structure.

## Motivation
Based on stakeholder feedback: "I really like the folder structure of organizing the files though, it gives me a quick view without needing to open files. If we need improvements or adjustments, suggest them."

The current story status exists in markdown frontmatter, but we can improve the visual clarity and cross-repository synchronization while preserving the folder-based organization that provides quick status visibility.

## Proposed Changes

### Enhanced Status Visualization
- **Story Status Badges**: Add visual status indicators in story READMEs for each themed directory
- **Progress Dashboards**: Create summary views showing story counts by status within each theme
- **Cross-Repository Links**: Strengthen links between planning stories and implementation PRs/commits

### Improved Workflow Integration  
- **Automated Status Updates**: GitHub Actions workflow to update story status based on implementation repository events
- **Milestone Tracking**: Visual progress tracking for roadmap milestones across themed directories
- **Stakeholder Dashboards**: High-level views for quick status assessment without opening individual files

### Maintain Folder Organization Benefits
- **Directory-Level Status**: Quick visual assessment by folder structure (active/, completed/, etc.)
- **Theme-Based Grouping**: Enhanced with status summaries within each themed directory
- **Minimal File Changes**: Preserve current story markdown structure with metadata enhancements

## Acceptance Criteria
- [ ] Story status visible at directory level without opening individual files
- [ ] Cross-repository coordination maintains automatic status synchronization
- [ ] Implementation PR references automatically update planning story status
- [ ] Roadmap milestone progress visible in themed directory dashboards
- [ ] Stakeholder can assess progress with 30-second glance at folder structure

## Suggested Stories
- COORD-001: Implement status badge system for themed directories
- COORD-002: Create cross-repository status synchronization workflow
- COORD-003: Build milestone progress dashboards for roadmaps
- COORD-004: Enhance story-to-PR linking automation

## Impact
- Areas affected: GitHub Actions workflows, story templates, directory READMEs
- Benefits: Improved visibility while preserving preferred folder organization
- Stakeholder value: Faster status assessment, better coordination, maintained simplicity

## Notes
This proposal respects the stakeholder's preference for folder-based organization while addressing the need for improved cross-repository coordination mentioned in the .github/instructions. The goal is to enhance, not replace, the current structure.