# Story Backlog

**Purpose**: Prioritized future work organized by strategic themes  
**Scope**: Formal stories requiring planning and refinement

**Last Updated**: 2025-08-26

## For Implementation Agents

**🚀 START HERE**: See [`PRIORITIZATION.md`](./PRIORITIZATION.md) for the ordered list of stories ready to implement.

The prioritization list provides:
- Stories ordered by priority and dependencies
- Clear indication of what's ready to start immediately  
- Cross-references to story files and metadata
- Implementation guidelines and coordination notes

## Story Types

### 📋 Formal Stories (This Backlog)
Stories requiring planning, refinement, and prioritization:
- User-facing features
- Architectural changes  
- Complex integrations
- Stories with dependencies

### 🚀 ADH Stories (Bypass Backlog)
Ad-hoc bug fixes and maintenance tasks that go directly to `active/`:
- Quick bug fixes (< 4 hours)
- Repository maintenance
- Tool improvements
- See [`../ADH_WORKFLOW.md`](../ADH_WORKFLOW.md) for details

## Organization
Stories are organized by functional area and priority, migrated from implementation repository and reorganized into planning-focused themes:

### Themed Directories
- `llm/` - LLM pipeline and feature stories (~30 stories across ingestion, modeling, evaluation, UI)
- `social_media/` - Twitter/X and Bluesky integration (12 stories)
- `models/` - ML model enhancements and prediction accuracy (8 stories)
- `infrastructure/` - Platform and operational improvements (3 stories)
- `ui/` - User interface and experience improvements (1 story)

## Priority Levels
Prioritization focuses on pick accuracy and user confidence per stakeholder direction:

- **P0**: Critical dependencies blocking other work
- **P1**: High-impact features for pick accuracy and user confidence
- **P2**: Medium-impact features for platform stability  
- **P3**: Nice-to-have features for future consideration

## Strategic Themes
1. **Pick Accuracy**: Model improvements, advanced statistics, data integration
2. **User Confidence**: Explanations, transparency, educational content
3. **Platform Reliability**: Infrastructure, automation, monitoring

**Current Backlog Count**: 54+ stories organized by theme and priority

## For Planning Agents

Organize and maintain stories using the themed directory structure below. The prioritization list is auto-generated from story metadata and should be regenerated when significant changes are made to the backlog.
