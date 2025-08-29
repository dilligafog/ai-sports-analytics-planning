# AI Sports Analytics - Strategic Planning

**Main Implementation Repo**: [ai-sports-analytics](https://github.com/dilligafog/ai-sports-analytics)

## Purpose

This repository manages strategic planning, story development, and roadmap evolution for the AI Sports Analytics project. It works in partnership with the main implementation repository through automated synchronization and specialized AI agents.

## Repository Structure

### ✅ **Accepted** (`accepted/`)
Formally accepted stories that have been completed, verified, and meet all acceptance criteria. These stories serve as reference materials and provide complete implementation history.

### 📋 **Active Stories** (`active/`)
Current iteration stories being actively developed. Stories move here from backlog when development begins. Also contains ADH (ad-hoc) stories for bug fixes and maintenance.

### 🗃️ **Backlog** (`backlog/`)
Prioritized future work organized by theme:
- **Foundation**: Core infrastructure and data pipeline
- **Features**: ML models, LLM integration, social media
- **Operations**: Monitoring, deployment, performance
- **User Experience**: UI, documentation, APIs

### ✅ **Completed** (`completed/`)
Staging area for recently completed stories. Stories accumulate here before being moved to accepted/ in batches. Maintains traceability between planning and execution.

### 🚀 **ADH Workflow** ([`ADH_WORKFLOW.md`](./ADH_WORKFLOW.md))
Ad-hoc bug fixing and maintenance workflow. ADH stories bypass formal backlog prioritization for rapid execution of small fixes and improvements.

### 🗺️ **Roadmaps** (`roadmaps/`)
High-level strategic plans and release planning:
- Quarterly objectives
- Technology evolution
- Dependency mapping
- Resource allocation

## Agent Collaboration

### Planning Agent (This Repo)
- **Strategic thinking**: Roadmap planning and story generation
- **Backlog management**: Prioritization and dependency tracking  
- **Story refinement**: Updates based on implementation learnings
- **Pattern recognition**: Identifies recurring themes and opportunities

### Implementation Agent (Main Repo)
- **Tactical execution**: Code, tests, CI/CD
- **Technical decisions**: Architecture and implementation choices
- **Quality assurance**: Testing and performance validation
- **Delivery**: Feature completion and deployment

## Synchronization

Automated workflows watch the main repository for:
- **Commits**: Update story progress and completion status
- **PRs**: Refine story details based on actual implementation
- **Issues**: Generate new stories from discovered technical debt
- **Releases**: Archive completed stories and plan next iteration

## Current Status

**Last Updated**: 2025-01-27  
**Active Stories**: 1 (migration summary)  
**Backlog Stories**: 54+ (organized by theme)  
**Completed Stories**: 0  
**Accepted Stories**: 19 (migrated from implementation repo)  

**Next Actions**:
1. Migrate existing stories from main repo
2. Set up GitHub Actions for repo synchronization
3. Initialize story agent prompts
4. Establish workflow with implementation repo

Import branch
--------------

When migrating stories from the implementation repo, use the `feature/import-stories-from-impl` branch. Place incoming stories into `backlog/` and open a PR for the planning agent to review and assign.

## Usage

### For Planning Agent
Use prompts in `.github/prompts/` to:
- Refine stories based on implementation feedback
- Generate new stories from patterns
- Update roadmaps and priorities
- Maintain backlog health

### For Implementation Agent
Refer to this repo for:
- Current story context and acceptance criteria
- Strategic direction and priorities
- Implementation guidance and constraints

## Repository Links

- **Implementation**: https://github.com/dilligafog/ai-sports-analytics
- **Issues**: Use main repo for technical issues, this repo for planning discussions
- **Projects**: GitHub Projects boards for iteration planning
