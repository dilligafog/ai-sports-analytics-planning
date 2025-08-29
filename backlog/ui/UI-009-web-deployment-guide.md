---
id: UI-009
title: Web Deployment Guide
epic: ui
status: accepted
priority: medium
effort: TBD
branch_name: ui-009-web-deployment-guide
labels:
- accepted
created: '2025-08-27'
accepted_date: '2025-08-27'
author: migration
dependencies: []
---

# Web Deployment Guide

This guide explains how to deploy the NFL Predictions web interface using GitHub Pages with a separate repository approach.

## Overview

The web deployment system uses a two-repository approach:
1. **Main Repository** (`ai-sports-analytics`): Contains the core application, data pipeline, and models
2. **UI Repository** (`nfl-predictions-ui`): Contains only the static web assets for GitHub Pages

This separation keeps the main repository focused on functionality while the UI repository serves as a clean, deployable package.

## Template-Based Build System

The web interface now uses a template-based build system with Jinja2, separating HTML/CSS/JS from Python code for better maintainability:

- **Templates**: Located in `/templates/` directory
- **Assets**: CSS/JS files in `/templates/assets/`
- **Builder**: `TemplateWebBuilder` class renders templates with data

## Quick Start

### 1. Build Web Package
```bash
# Activate environment and build web assets
cd /home/bustabook/nfl-predictions
portal  # or source .venv/bin/activate
busta build-web
```

This creates a `web_build/` directory with:
- `index.html` - Main landing page with navigation
- `credibility.html` - Performance dashboard
- `methodology.html` - Model explanations  
- `predictions/` - Current week predictions
- `weeks/` - Weekly performance reports
- `assets/` - CSS, JS, and other static assets
- `data/` - JSON data files for dashboards
- `.nojekyll` - GitHub Pages configuration
- `README.md` - Documentation for the web package

### 2. Deploy to GitHub Pages
```bash
# Deploy to your UI repository
busta deploy-web git@github.com:your-username/nfl-predictions-ui.git

# Or with custom options
busta deploy-web git@github.com:your-username/nfl-predictions-ui.git \
  --repo-dir ../custom-ui-dir \
  --message "Deploy week 1 predictions and performance dashboard"
```

### 3. Configure GitHub Pages
1. Go to your UI repository on GitHub
2. Navigate to **Settings > Pages**
3. Set source to **Deploy from a branch**
4. Select **main** branch and **/ (root)** folder
5. Save the settings

Your site will be available at `https://your-username.github.io/nfl-predictions-ui/`

## Architecture

### Template-Based System

The web build process now uses templates with Jinja2:

1. **Templates Directory Structure**
   ```
   templates/
   ├── landing.html           # Landing page template
   ├── dashboard.html         # Dashboard template
   ├── predictions.html       # Predictions template (when implemented)
   └── assets/
       ├── styles.css         # Separate CSS files
       ├── main.js            # Main JavaScript
       └── dashboard.js       # Dashboard-specific JS
   ```

2. **Template Build Process**
   - Templates are rendered with context data from predictions
   - Static assets are copied to the output directory
   - Data files are included for client-side JavaScript

3. **Dry Run Option**
   ```bash
   busta deploy-web --dry-run
   ```
   Preview what would be deployed without making actual changes

### Current Web Components

The system consolidates several disconnected web components:

1. **Dashboard System** (`data/dashboard/season_2025/`)
   - Performance tracking dashboard with metrics
   - Weekly analysis pages
   - Interactive charts and visualizations

2. **Prediction Pages** 
   - `week1_predictions.html` (root directory)
   - `apps/predictions-ui/predictions.html`
   - Static prediction displays

3. **Methodology Documentation**
   - Model explanations and feature descriptions
   - Credibility and transparency information

### Unified Structure

The build process creates a unified, web-friendly structure:

```
web_build/
├── index.html              # Main navigation page
├── credibility.html        # Performance dashboard  
├── methodology.html        # Model explanations
├── predictions/            # Current predictions
│   ├── predictions.html
│   └── week1_predictions.html
├── weeks/                  # Weekly performance reports
├── assets/                 # CSS, JS, images
│   ├── dashboard.css
│   └── performance.js
├── data/                   # JSON data for charts
├── .nojekyll              # GitHub Pages config
└── README.md              # Documentation
```

## Build Process Details

### WebBuilder Class

The `WebBuilder` class in `packages/models/src/models/web_builder.py` handles:

- **File Discovery**: Automatically finds web assets across the repository
- **Structure Unification**: Creates a consistent, web-friendly directory layout
- **Index Generation**: Creates a main navigation page if none exists
- **Asset Optimization**: Copies and organizes CSS, JS, and data files
- **Deployment Preparation**: Adds GitHub Pages configuration files

### Key Features

- **Automatic Asset Discovery**: Finds web files regardless of their current location
- **Unified Navigation**: Creates a main index page linking all components
- **GitHub Pages Ready**: Includes `.nojekyll` and proper structure
- **Build Metadata**: Tracks build information and source repository
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Deployment Process Details

### WebDeployer Class

The `WebDeployer` class in `scripts/deploy_web.py` handles:

- **Repository Management**: Clones or updates the UI repository
- **Content Synchronization**: Replaces UI repository contents with new web package
- **Git Operations**: Commits and pushes changes automatically
- **Error Handling**: Validates package and handles deployment failures

### Deployment Workflow

1. **Validation**: Ensures web package exists and has required files
2. **Repository Preparation**: Clones UI repo or pulls latest changes
3. **Content Replacement**: Removes old content, copies new web package
4. **Git Operations**: Commits changes and pushes to GitHub
5. **GitHub Pages Update**: GitHub automatically updates the live site

## Customization

### Custom Build Options

```bash
# Build to custom directory
busta build-web --output-dir custom_web_build

# Deploy with custom settings
busta deploy-web git@github.com:user/repo.git \
  --repo-dir ../custom-ui-location \
  --message "Custom deployment message"
```

### Extending the Build Process

To add new web components:

1. **Add Source Detection**: Update `WebBuilder._copy_*_files()` methods
2. **Update Structure**: Modify directory creation in `_clean_and_create_directories()`
3. **Enhance Navigation**: Update `_generate_index_html()` for new sections
4. **Test Integration**: Ensure new components work with existing assets

### Custom Styling and Assets

The build process automatically includes:
- CSS files from dashboard assets
- JavaScript files for interactive features
- JSON data files for charts and metrics
- Any additional assets in the dashboard structure

## Troubleshooting

### Common Issues

**Build Fails - Configuration Error**
```bash
# Ensure you're in the correct environment
cd /home/bustabook/nfl-predictions
portal
busta build-web
```

**Deploy Fails - Repository Access**
```bash
# Check SSH key setup for GitHub
ssh -T git@github.com

# Use HTTPS if SSH fails
busta deploy-web https://github.com/user/nfl-predictions-ui.git
```

**Missing Web Components**
```bash
# Ensure dashboard has been generated
busta generate-dashboard --season 2025

# Check for prediction files
ls week1_predictions.html
ls apps/predictions-ui/predictions.html
```

### Logging and Debugging

All operations use structured logging:
```bash
# Check build logs
tail -f logs/models.log

# Enable debug logging
export LOG_LEVEL=DEBUG
busta build-web
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Deploy Web Interface
on:
  push:
    branches: [main]
    paths: ['data/dashboard/**', 'week*_predictions.html', 'apps/predictions-ui/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m venv .venv
        source .venv/bin/activate
        pip install -e packages/data_pipeline -e packages/models
    - name: Build and deploy
      env:
        DEPLOY_KEY: ${{ secrets.UI_REPO_DEPLOY_KEY }}
      run: |
        source .venv/bin/activate
        busta build-web
        busta deploy-web git@github.com:user/nfl-predictions-ui.git
```

## Best Practices

### Regular Updates
- Build and deploy after each dashboard generation
- Update when new predictions are available
- Refresh after model performance analysis

### Repository Management
- Keep UI repository clean (only web assets)
- Use descriptive commit messages
- Tag releases for major updates

### Performance Optimization
- Minimize large data files in the web package
- Use efficient JSON formats for chart data
- Optimize images and assets before building

## Security Considerations

- Never include API keys or sensitive data in web package
- Use environment variables for configuration
- Validate all inputs and file paths
- Keep deployment credentials secure

## Future Enhancements

### Planned Features
- Automated daily builds and deployments
- CDN integration for better performance
- Progressive web app (PWA) capabilities
- Advanced interactive visualizations

### Monitoring
- Build success/failure notifications
- Deployment status tracking
- Web performance monitoring
- User analytics integration
