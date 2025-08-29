---
id: RPT-005
title: Simple GitHub Pages dashboard template
branch_name: rpt-005-simple-github-pages-dashboard-template
epic: reporting
status: draft
priority: medium
estimate: "3sp"
dependencies: [RPT-001]
labels: [reporting, github-pages, dashboard, simple-ui]
created: 2025-08-29
author: planning-agent
owner: implementation-team
market: null
layer: null
last_updated: 2025-08-29
emit_metadata:
  source_id: null
  layer: null
  input_path: null
  notes: null
---

# RPT-005: Simple GitHub Pages dashboard template

## User Story
**As a** stakeholder across multiple projects  
**I want** a simple GitHub Pages dashboard that consumes exported JSON data  
**So that** I can view project status and progress without requiring live API access or complex infrastructure

## Value Proposition
Provides essential project visibility through a basic GitHub Pages template that consumes static JSON files exported from plan_pipe, enabling public dashboard access without exposing the plan_pipe API to the internet.

## Acceptance Criteria
- [ ] Simple HTML template with minimal JavaScript for basic interactivity
- [ ] Displays essential project metrics (story counts, epic progress, velocity trends)
- [ ] Consumes static JSON data files exported by plan_pipe (no live API calls)
- [ ] Template can be easily customized per project with basic configuration
- [ ] No complex build process or framework dependencies
- [ ] Responsive design works on desktop and mobile
- [ ] GitHub Pages compatible with automatic deployment
- [ ] JSON data files can be committed to repository and served statically
- [ ] Clear documentation for JSON export workflow and dashboard deployment
- [ ] Basic styling that works across different project themes
- [ ] Support for multiple projects within single dashboard instance
- [ ] Graceful handling of missing or outdated JSON data

## Technical Notes
- Use vanilla HTML/CSS/JavaScript to avoid build dependencies
- Fetch JSON data from static files exported by plan_pipe (committed to repository)
- Implement basic charts using lightweight libraries (Chart.js or similar)
- Template should be easily forkable and customizable
- Focus on essential metrics rather than comprehensive analytics
- Ensure fast loading and minimal resource requirements
- No live API calls - all data comes from pre-generated JSON files
- Include fallback handling for missing or stale data

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Template tested with sample project data
- [ ] Documentation includes setup and customization guide
- [ ] GitHub Pages deployment verified
- [ ] Template works without JavaScript for basic content
- [ ] Performance optimized for fast loading

## References
- [TOOL-001 Proposal](../../proposals/TOOL-001-dockerized-story-workflow-api.md)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Simple Dashboard Requirements from Proposal](../../proposals/TOOL-001-dockerized-story-workflow-api.md#key-features)

---
**Story Lifecycle:**
- Created: 2025-08-29 by planning-agent
- Started: [date] by [implementer]  
- Completed: [date]
- Accepted: [date]
