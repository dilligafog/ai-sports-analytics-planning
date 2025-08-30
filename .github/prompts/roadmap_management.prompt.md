```prompt
# Roadmap Management Prompt

## Role
Manage the strategic roadmap for the AI Sports Analytics project, organizing stories into logical development sequences and planning iterations.

## Roadmap Components

### Themes
Large strategic initiatives that span multiple iterations:
- **Foundation**: Core infrastructure and data pipeline
- **Intelligence**: Machine learning and prediction models
- **Experience**: User interfaces and interaction design
- **Integration**: Third-party services and APIs
- **Performance**: Optimization and scalability
- **Growth**: Marketing and user acquisition

### Epics
Collections of related stories that deliver significant value:
- **Epic**: User Authentication System
  - Stories: AUTH-001, AUTH-002, AUTH-003
  - Timeline: 2-3 sprints
  - Value: Secure user access and personalization

### Iterations
Time-boxed development cycles (2-week sprints):
- **Sprint Goals**: Clear objective for the iteration
- **Story Selection**: Based on priority, dependencies, capacity
- **Milestone Alignment**: Progress toward larger goals

## Planning Horizons

### Current Sprint (Now)
- **Focus**: Stories in active development
- **Visibility**: High detail, daily tracking
- **Scope**: Fixed, no changes without replanning

### Next Sprint (Next 2 weeks)
- **Focus**: Stories ready for development
- **Visibility**: Detailed acceptance criteria
- **Scope**: Flexible, can be adjusted based on current sprint outcomes

### Current Quarter (3 months)
- **Focus**: Epics and major milestones
- **Visibility**: High-level story mapping
- **Scope**: Strategic direction, major features

### Next Quarter (3-6 months)
- **Focus**: Themes and strategic initiatives
- **Visibility**: Rough story estimates
- **Scope**: Vision alignment, major architectural decisions

## Roadmap Artifacts

### Story Map
```
User Journey: Betting Analysis Workflow
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ Discover    │ Analyze     │ Predict     │ Track       │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ AUTH-001    │ DATA-001    │ PRED-001    │ DASH-001    │
│ Register    │ Import Data │ Train Model │ View Results│
│             │             │             │             │
│ AUTH-002    │ DATA-002    │ PRED-002    │ DASH-002    │
│ Login       │ Clean Data  │ Predictions │ Performance │
│             │             │             │             │
│ UI-001      │ DATA-003    │ PRED-003    │ SOCIAL-001  │
│ Landing     │ Feature Eng │ Evaluation  │ Share Picks │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

### Release Planning
```markdown
## Release 1.0: MVP (End of Q1)
**Theme**: Foundation
**Goal**: Core prediction pipeline with basic UI

### Milestones
- [ ] Data pipeline functional (DATA-001, DATA-002)
- [ ] Basic prediction model (PRED-001, PRED-002)
- [ ] Simple web interface (UI-001, UI-002)
- [ ] User authentication (AUTH-001, AUTH-002)

## Release 1.1: Enhanced Experience (Mid Q2)
**Theme**: Intelligence + Experience
**Goal**: Improved predictions and user experience

### Milestones
- [ ] Advanced models (PRED-003, PRED-004)
- [ ] Rich dashboard (DASH-001, DASH-002)
- [ ] Social features (SOCIAL-001, SOCIAL-002)
```

## Roadmap Maintenance

### Weekly Review
1. **Story Progress**: Use `python scripts/update_story.py --list` to track ready stories
2. **Priority Analysis**: Run `python scripts/manage_priorities.py --list` for current structure
3. **Quality Validation**: Generate `python scripts/backlog_groomer.py` reports for health checks
4. **Stakeholder Updates**: Use script outputs to communicate progress and data-driven changes

### Monthly Planning
1. **Epic Progress**: Use script-generated priority analysis for epic completion assessment
2. **Strategic Alignment**: Run `python scripts/manage_priorities.py --auto-prioritize` for business logic scoring
3. **Capacity Planning**: Use grooming reports to adjust future sprint loads based on story complexity
4. **Dependency Management**: Use validation scripts to identify and resolve story dependencies

### Quarterly Strategy
1. **Theme Evolution**: Adjust strategic themes based on learning
2. **Market Feedback**: Incorporate user and market feedback
3. **Technical Evolution**: Adjust for technology and architectural changes
4. **Resource Planning**: Align roadmap with team growth and capabilities

## Roadmap Communication

### Stakeholder Views
- **Executive**: Themes, major milestones, business value
- **Product**: Epics, user value, market fit
- **Engineering**: Stories, technical dependencies, architecture
- **Users**: Features, capabilities, timeline

### Update Frequency
- **Daily**: Sprint progress, blockers
- **Weekly**: Sprint goals, story completion
- **Monthly**: Epic progress, release timeline
- **Quarterly**: Theme evolution, strategic direction

## Anti-Patterns
- ❌ Over-planning distant future (beyond one quarter)
- ❌ Ignoring implementation feedback for roadmap adjustments
- ❌ Rigid adherence to plans when circumstances change
- ❌ Planning without considering team capacity and velocity
- ❌ Roadmap that doesn't align with user and business value
```
