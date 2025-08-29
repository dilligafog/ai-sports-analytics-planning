---
id: UI-006
title: Ui Architecture Quickstart
epic: ui
status: accepted
priority: medium
effort: TBD
branch_name: ui-006-ui-architecture-quickstart
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# Getting Started with the New UI Architecture

This guide will help you quickly get started with the new template-based approach we've implemented and provide information about the future separate UI repository architecture.

## Immediate Improvement: Template-Based Building

We've already implemented a template-based system that separates HTML/CSS/JS from Python code.

### Try It Out Now

```bash
# Navigate to the nfl-predictions repo
cd /home/bustabook/nfl-predictions

# Migrate from HTML-in-Python to templates (if not already done)
busta migrate-to-templates

# Build with the template-based approach
busta build-web --template-based

# Deploy as usual
busta deploy-web
```

### What Changed?

1. **Templates are in `/templates/`**:
   - `landing.html` - Main landing page with Jinja2 template syntax
   - `dashboard.html` - Performance dashboard template
   - `assets/styles.css` - CSS extracted from Python
   - `assets/main.js` - JavaScript extracted and enhanced

2. **Template-Based Builder**:
   A new `TemplateWebBuilder` class in `packages/models/src/models/template_web_builder.py` 
   that renders templates with data instead of embedding HTML in Python.

3. **Same Output**:
   The output structure is identical, so deployment is unchanged.

## Long-Term Solution: Separate UI Repository

For better frontend development, we recommend gradually moving to a separate UI repository.

### Getting Started with the UI Repository

```bash
# Navigate to the UI repo
cd /home/bustabook/nfl-predictions-ui

# Initialize with modern tools
npm init -y
npm install vite react react-dom

# Create basic structure
mkdir -p src/{components,pages,assets/{css,js}}

# Create basic configuration
touch vite.config.js
```

### Example React Component

We've created an example React component in `/docs/examples/GameCard.jsx` that shows how the UI 
would be structured in the separate repository.

### Data Exchange

The key to making this work is a well-defined data contract:

1. **Main Repository**:
   - Generates JSON files with all required data
   - Places them in predictable locations

2. **UI Repository**:
   - Fetches JSON files at runtime
   - Renders UI components with the data

### Transition Plan

1. **Phase 1: Use Templates** (Now - 2 weeks)
   - Immediately switch to template-based building
   - Improve templates and separate concerns

2. **Phase 2: Hybrid Approach** (2 weeks - 1 month)
   - Set up basic UI repository structure
   - Define data contract between repos
   - Start building React/Vue components

3. **Phase 3: Full Transition** (1-2 months)
   - Complete UI in separate repo
   - Main repo just generates data
   - Independent deployment pipeline

## Benefits

- **Immediate Improvements** with templates
- **Better Frontend Development** experience
- **Cleaner Separation** of concerns
- **Modern UI Capabilities** (interactive features)
- **Specialized Tools** for each part of the system

## Getting Help

For more details, see:
- `/docs/UI_ARCHITECTURE_PROPOSAL.md` - Full technical proposal
- `/docs/UI_BUILD_PROCESS_ANALYSIS.md` - Analysis of the current system
- `/packages/models/src/models/template_web_builder.py` - Template-based builder implementation
