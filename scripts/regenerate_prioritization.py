#!/usr/bin/env python3
"""
Regenerate backlog/PRIORITIZATION.md from current story files

Usage: python3 scripts/regenerate_prioritization.py
"""
import os
import re
import yaml
from pathlib import Path
import json
from datetime import datetime

def extract_story_metadata(filepath):
    """Extract metadata from a story file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Make filepath relative to repository root
    if filepath.startswith(os.getcwd()):
        rel_filepath = filepath[len(os.getcwd()):].lstrip('/')
    else:
        rel_filepath = filepath
    
    story_data = {
        'filepath': rel_filepath,
        'id': None,
        'title': None,
        'priority': None,
        'estimate': None,
        'dependencies': [],
        'status': None,
        'owner': None,
        'tags': [],
        'epic': None,
        'layer': None,
        'has_yaml': False
    }
    
    # Try to extract YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1])
                story_data.update({
                    'id': metadata.get('id'),
                    'priority': metadata.get('priority'),
                    'estimate': metadata.get('estimate'),
                    'dependencies': metadata.get('dependencies', []),
                    'status': metadata.get('status'),
                    'owner': metadata.get('owner'),
                    'tags': metadata.get('tags', []),
                    'epic': metadata.get('epic'),
                    'layer': metadata.get('layer'),
                    'has_yaml': True
                })
                content_after_yaml = parts[2]
            except Exception as e:
                print(f"Failed to parse YAML in {filepath}: {e}")
                content_after_yaml = content
        else:
            content_after_yaml = content
    else:
        content_after_yaml = content
    
    # Extract title from first heading
    title_match = re.search(r'^#\s+(.+)$', content_after_yaml, re.MULTILINE)
    if title_match:
        story_data['title'] = title_match.group(1).strip()
    
    # If no ID from YAML, try to extract from title or filename
    if not story_data['id']:
        if story_data['title']:
            id_match = re.search(r'(S\d+|[A-Z]+-\d+|[A-Z_]+)', story_data['title'])
            if id_match:
                story_data['id'] = id_match.group(1)
        
        if not story_data['id']:
            filename = os.path.basename(filepath)
            story_data['id'] = filename.replace('.md', '').replace('_', '-').upper()
    
    return story_data

def categorize_priority(story):
    """Convert priority text to numerical value for sorting"""
    priority_map = {
        'high': 1,
        'medium': 2,
        'low': 3,
        None: 4
    }
    return priority_map.get(story['priority'], 4)

def has_blocking_dependencies(story, all_stories):
    """Check if story has dependencies that are not completed"""
    if not story['dependencies']:
        return False
    return len(story['dependencies']) > 0

def format_estimate(estimate):
    return estimate if estimate else "Not specified"

def format_dependencies(deps):
    if not deps:
        return "None"
    return ", ".join(deps)

def format_owner(owner):
    return owner if owner else "TBD"

def main():
    """Main function to regenerate prioritization list"""
    base_dir = os.getcwd()
    backlog_dir = os.path.join(base_dir, 'backlog')
    
    if not os.path.exists(backlog_dir):
        print("Error: backlog directory not found. Run from repository root.")
        return
    
    # Find all story files
    story_files = []
    for root, dirs, files in os.walk(backlog_dir):
        for file in files:
            if file.endswith('.md') and file not in ['README.md', 'index.md', '_template.md', 'PRIORITIZATION.md']:
                story_files.append(os.path.join(root, file))
    
    # Parse all stories
    stories = []
    for filepath in story_files:
        try:
            story = extract_story_metadata(filepath)
            stories.append(story)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    # Sort stories by priority and dependencies
    stories.sort(key=lambda s: (
        has_blocking_dependencies(s, stories),
        categorize_priority(s),
        s['id'] or 'ZZZ'
    ))
    
    # Group stories
    no_deps_high = [s for s in stories if not s['dependencies'] and s['priority'] == 'high']
    no_deps_medium = [s for s in stories if not s['dependencies'] and s['priority'] == 'medium']
    no_deps_low = [s for s in stories if not s['dependencies'] and s['priority'] == 'low']
    no_deps_unspecified = [s for s in stories if not s['dependencies'] and not s['priority']]
    has_deps = [s for s in stories if s['dependencies']]
    
    # Generate prioritization file content
    output = f"""# Story Prioritization List

**Purpose**: Prioritized task list for coding agents to select next work items  
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}  
**Total Stories**: {len(stories)}  

## Quick Start for Implementation Agents

1. **Pick the first available story** from the "Ready to Start" section below
2. **Verify dependencies** are completed before beginning work
3. **Reference the story ID** in all commits and PRs (format: `feat(STORY-ID): description`)
4. **Update this planning repo** when work begins and completes
5. **Report outcomes** including lessons learned and follow-up needs

## Story Selection Criteria

Stories are prioritized by:
- **🚫 No blocking dependencies** (ready to start immediately)
- **🔥 High business impact** (pick accuracy, user confidence)
- **⚡ Foundation components** (unblock future work)
- **📊 Clear scope** (well-defined acceptance criteria)

---

## Ready to Start (No Dependencies)

"""

    # Add sections for each priority level
    if no_deps_high:
        output += "### 🔥 High Priority - Start These First\n\n"
        for i, story in enumerate(no_deps_high, 1):
            output += f"""**{i}. {story['id'] or 'NO-ID'}** - {story['title'] or 'No title'}
- **File**: `{story['filepath']}`
- **Owner**: {format_owner(story['owner'])}
- **Estimate**: {format_estimate(story['estimate'])}
- **Epic**: {story['epic'] or 'Not specified'}
- **Tags**: {', '.join(story['tags']) if story['tags'] else 'None'}

"""

    if no_deps_medium:
        output += "### 📋 Medium Priority - Next in Queue\n\n"
        for i, story in enumerate(no_deps_medium, len(no_deps_high) + 1):
            output += f"""**{i}. {story['id'] or 'NO-ID'}** - {story['title'] or 'No title'}
- **File**: `{story['filepath']}`
- **Owner**: {format_owner(story['owner'])}
- **Estimate**: {format_estimate(story['estimate'])}
- **Epic**: {story['epic'] or 'Not specified'}

"""

    if no_deps_low:
        output += "### 📝 Low Priority - Future Work\n\n"
        for i, story in enumerate(no_deps_low, len(no_deps_high) + len(no_deps_medium) + 1):
            output += f"""**{i}. {story['id'] or 'NO-ID'}** - {story['title'] or 'No title'}
- **File**: `{story['filepath']}`
- **Owner**: {format_owner(story['owner'])}
- **Estimate**: {format_estimate(story['estimate'])}

"""

    if no_deps_unspecified:
        output += "### ❓ Priority Needs Review\n\n"
        start_num = len(no_deps_high) + len(no_deps_medium) + len(no_deps_low) + 1
        for i, story in enumerate(no_deps_unspecified, start_num):
            output += f"""**{i}. {story['id'] or 'NO-ID'}** - {story['title'] or 'No title'}
- **File**: `{story['filepath']}`
- **Owner**: {format_owner(story['owner'])}
- **Note**: Priority needs to be assigned

"""

    # Add dependency section
    if has_deps:
        output += """---

## Blocked by Dependencies

These stories require other work to be completed first:

"""
        for story in has_deps:
            output += f"""**{story['id'] or 'NO-ID'}** - {story['title'] or 'No title'} ({story['priority'] or 'priority TBD'})
- **Dependencies**: {format_dependencies(story['dependencies'])}
- **File**: `{story['filepath']}`

"""

    # Add footer
    output += f"""---

## Strategic Context

### Current Focus Areas
1. **Pick Accuracy** - Model improvements and data quality ({len([s for s in stories if 'models' in s['filepath'] or 'modeling' in s['filepath']])} stories)
2. **LLM Pipeline** - News ingestion and feature extraction ({len([s for s in stories if 'llm' in s['filepath']])} stories)  
3. **Infrastructure** - Platform reliability and automation ({len([s for s in stories if 'infrastructure' in s['filepath'] or 'infra' in s['filepath']])} stories)
4. **Social Media** - Twitter/X and Bluesky integration ({len([s for s in stories if 'social_media' in s['filepath']])} stories)

### Implementation Notes
- **Story Format**: Some stories use YAML frontmatter, others use simple markdown
- **Cross-Repo Links**: Reference implementation repo in commits: `github.com/dilligafog/ai-sports-analytics`
- **Estimates**: Stories with estimates use story points (sp) or days (d)
- **Status Tracking**: Update story status in planning repo when work progresses

### Automation
This file is auto-generated from story metadata. To regenerate:
```bash
python3 scripts/regenerate_prioritization.py
```

**Last Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    # Write the file
    output_path = os.path.join(backlog_dir, 'PRIORITIZATION.md')
    with open(output_path, 'w') as f:
        f.write(output)
    
    print(f"✅ Generated {output_path}")
    print(f"📊 Total stories: {len(stories)}")
    print(f"🚀 Ready to start: {len(no_deps_high)} high + {len(no_deps_medium)} medium + {len(no_deps_low)} low priority")
    print(f"🚫 Blocked by dependencies: {len(has_deps)} stories")

if __name__ == '__main__':
    main()